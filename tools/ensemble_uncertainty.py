"""
Ensemble-based Uncertainty Estimation for 3D Object Detection
Uses multiple independently trained models to estimate uncertainty
"""

import argparse
import glob
import os
import pickle
import numpy as np
import torch
from pathlib import Path
from tqdm import tqdm

from pcdet.config import cfg, cfg_from_yaml_file
from pcdet.datasets import DatasetTemplate
from pcdet.models import build_network, load_data_to_gpu
from pcdet.utils import common_utils


def parse_config():
    parser = argparse.ArgumentParser(description='Ensemble Uncertainty Estimation')
    parser.add_argument('--cfg_file', type=str, required=True,
                        help='specify the config for evaluation')
    parser.add_argument('--ckpt_dir', type=str, required=True,
                        help='directory containing model checkpoints')
    parser.add_argument('--data_path', type=str, required=True,
                        help='path to KITTI format dataset')
    parser.add_argument('--batch_size', type=int, default=1,
                        help='batch size for inference')
    parser.add_argument('--output_dir', type=str, default='../output/ensemble_uncertainty',
                        help='output directory for results')
    parser.add_argument('--split', type=str, default='val',
                        choices=['train', 'val', 'test'],
                        help='dataset split to use')
    parser.add_argument('--workers', type=int, default=4,
                        help='number of workers for dataloader')
    parser.add_argument('--iou_threshold', type=float, default=0.5,
                        help='IoU threshold for matching detections')

    args = parser.parse_args()

    cfg_from_yaml_file(args.cfg_file, cfg)
    cfg.TAG = Path(args.cfg_file).stem
    cfg.EXP_GROUP_PATH = '/'.join(args.cfg_file.split('/')[1:-1])

    return args, cfg


def load_models(ckpt_dir, cfg, test_set, logger):
    """Load all model checkpoints from directory"""
    # Find all checkpoint files
    ckpt_files = glob.glob(os.path.join(ckpt_dir, '*.pth'))

    if len(ckpt_files) == 0:
        raise ValueError(f'No checkpoint files found in {ckpt_dir}')

    logger.info(f'Found {len(ckpt_files)} checkpoint files')

    models = []
    for ckpt_file in ckpt_files:
        model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=test_set)
        model.load_params_from_file(filename=ckpt_file, logger=logger, to_cpu=False)
        model.cuda()
        model.eval()
        models.append(model)
        logger.info(f'  Loaded: {os.path.basename(ckpt_file)}')

    return models


def ensemble_inference(models, dataloader, device='cuda'):
    """
    Perform ensemble inference with multiple models

    Args:
        models: list of trained models
        dataloader: data loader
        device: device to run on

    Returns:
        results: list of dictionaries containing predictions and uncertainties
    """
    results = []

    with torch.no_grad():
        for i, batch_dict in enumerate(tqdm(dataloader, desc='Ensemble Inference')):
            load_data_to_gpu(batch_dict)

            # Storage for predictions from all models
            all_boxes = []
            all_scores = []
            all_labels = []

            # Get predictions from each model
            for model in models:
                pred_dicts, _ = model(batch_dict)
                pred_dict = pred_dicts[0]

                if pred_dict['pred_boxes'].shape[0] > 0:
                    all_boxes.append(pred_dict['pred_boxes'].cpu().numpy())
                    all_scores.append(pred_dict['pred_scores'].cpu().numpy())
                    all_labels.append(pred_dict['pred_labels'].cpu().numpy())

            # Compute uncertainty metrics
            if len(all_boxes) > 0:
                uncertainty_dict = compute_ensemble_uncertainty(
                    all_boxes, all_scores, all_labels, len(models)
                )
            else:
                uncertainty_dict = {
                    'boxes': np.array([]),
                    'scores': np.array([]),
                    'labels': np.array([]),
                    'score_variance': np.array([]),
                    'score_std': np.array([]),
                    'box_variance': np.array([]),
                    'model_disagreement': np.array([]),
                    'epistemic_uncertainty': np.array([]),
                    'predictive_entropy': np.array([]),
                    'detection_frequency': np.array([])
                }

            # Add frame_id for tracking
            uncertainty_dict['frame_id'] = batch_dict['frame_id'][0]
            results.append(uncertainty_dict)

    return results


def compute_ensemble_uncertainty(all_boxes, all_scores, all_labels, num_models):
    """
    Compute ensemble uncertainty metrics

    Metrics:
    - Score variance: variance of confidence scores across models
    - Score std: standard deviation of scores
    - Box variance: variance in box locations
    - Model disagreement: how much models disagree
    - Epistemic uncertainty: knowledge uncertainty from model variance
    - Predictive entropy: prediction uncertainty
    - Detection frequency: how many models detected this object
    """
    from pcdet.ops.iou3d_nms.iou3d_nms_utils import boxes_iou3d_gpu

    # Match detections across models
    matched_detections = match_detections_across_models(all_boxes, all_scores, all_labels)

    # Compute metrics for each matched detection
    mean_boxes = []
    mean_scores = []
    mean_labels = []
    score_variances = []
    score_stds = []
    box_variances = []
    model_disagreements = []
    epistemic_uncertainties = []
    predictive_entropies = []
    detection_frequencies = []

    for det_group in matched_detections:
        if len(det_group['boxes']) == 0:
            continue

        boxes = np.array(det_group['boxes'])
        scores = np.array(det_group['scores'])
        labels = np.array(det_group['labels'])

        # Mean predictions
        mean_box = np.mean(boxes, axis=0)
        mean_score = np.mean(scores)
        mean_label = int(np.median(labels))

        # Detection frequency (how many models detected this)
        detection_freq = len(scores) / num_models

        # Score uncertainty
        score_var = np.var(scores)
        score_std = np.std(scores)

        # Box position uncertainty
        box_var = np.mean(np.var(boxes[:, :3], axis=0))

        # Model disagreement (variance across models)
        model_disagreement = score_var + box_var

        # Epistemic uncertainty (knowledge uncertainty)
        epistemic = score_var

        # Predictive entropy
        score_prob = scores / (scores.sum() + 1e-10)
        pred_entropy = -np.sum(score_prob * np.log(score_prob + 1e-10))

        mean_boxes.append(mean_box)
        mean_scores.append(mean_score)
        mean_labels.append(mean_label)
        score_variances.append(score_var)
        score_stds.append(score_std)
        box_variances.append(box_var)
        model_disagreements.append(model_disagreement)
        epistemic_uncertainties.append(epistemic)
        predictive_entropies.append(pred_entropy)
        detection_frequencies.append(detection_freq)

    return {
        'boxes': np.array(mean_boxes) if len(mean_boxes) > 0 else np.array([]),
        'scores': np.array(mean_scores) if len(mean_scores) > 0 else np.array([]),
        'labels': np.array(mean_labels) if len(mean_labels) > 0 else np.array([]),
        'score_variance': np.array(score_variances) if len(score_variances) > 0 else np.array([]),
        'score_std': np.array(score_stds) if len(score_stds) > 0 else np.array([]),
        'box_variance': np.array(box_variances) if len(box_variances) > 0 else np.array([]),
        'model_disagreement': np.array(model_disagreements) if len(model_disagreements) > 0 else np.array([]),
        'epistemic_uncertainty': np.array(epistemic_uncertainties) if len(epistemic_uncertainties) > 0 else np.array([]),
        'predictive_entropy': np.array(predictive_entropies) if len(predictive_entropies) > 0 else np.array([]),
        'detection_frequency': np.array(detection_frequencies) if len(detection_frequencies) > 0 else np.array([])
    }


def match_detections_across_models(all_boxes, all_scores, all_labels, iou_threshold=0.5):
    """Match detections across multiple models using IoU"""
    from pcdet.ops.iou3d_nms.iou3d_nms_utils import boxes_iou3d_gpu

    if len(all_boxes) == 0:
        return []

    # Start with first model as reference
    detection_groups = []
    for box_idx in range(len(all_boxes[0])):
        detection_groups.append({
            'boxes': [all_boxes[0][box_idx]],
            'scores': [all_scores[0][box_idx]],
            'labels': [all_labels[0][box_idx]]
        })

    # Match detections from subsequent models
    for model_idx in range(1, len(all_boxes)):
        boxes_model = all_boxes[model_idx]
        scores_model = all_scores[model_idx]
        labels_model = all_labels[model_idx]

        if len(boxes_model) == 0:
            continue

        matched_indices = set()

        for group in detection_groups:
            if len(group['boxes']) == 0:
                continue

            # Use mean box as reference
            ref_box = torch.from_numpy(np.array([np.mean(group['boxes'], axis=0)])).cuda()
            model_boxes = torch.from_numpy(boxes_model).cuda()

            # Compute IoU
            ious = boxes_iou3d_gpu(ref_box, model_boxes)
            max_iou, max_idx = torch.max(ious[0], dim=0)

            if max_iou > iou_threshold and max_idx.item() not in matched_indices:
                group['boxes'].append(boxes_model[max_idx.item()])
                group['scores'].append(scores_model[max_idx.item()])
                group['labels'].append(labels_model[max_idx.item()])
                matched_indices.add(max_idx.item())

        # Add unmatched detections as new groups
        for box_idx in range(len(boxes_model)):
            if box_idx not in matched_indices:
                detection_groups.append({
                    'boxes': [boxes_model[box_idx]],
                    'scores': [scores_model[box_idx]],
                    'labels': [labels_model[box_idx]]
                })

    return detection_groups


def save_results(results, output_dir, args, num_models):
    """Save ensemble uncertainty results"""
    os.makedirs(output_dir, exist_ok=True)

    # Save as pickle
    result_file = os.path.join(output_dir, 'ensemble_results.pkl')
    with open(result_file, 'wb') as f:
        pickle.dump(results, f)

    print(f'\nResults saved to {result_file}')

    # Save summary statistics
    summary_file = os.path.join(output_dir, 'uncertainty_summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f'Ensemble Uncertainty Estimation Summary\n')
        f.write(f'=' * 50 + '\n\n')
        f.write(f'Config: {args.cfg_file}\n')
        f.write(f'Checkpoint directory: {args.ckpt_dir}\n')
        f.write(f'Number of models: {num_models}\n')
        f.write(f'Dataset split: {args.split}\n')
        f.write(f'Number of frames: {len(results)}\n\n')

        # Aggregate statistics
        all_score_vars = []
        all_score_stds = []
        all_box_vars = []
        all_disagreements = []
        all_epistemic = []
        all_entropies = []
        all_det_freqs = []
        total_detections = 0

        for res in results:
            if len(res['scores']) > 0:
                total_detections += len(res['scores'])
                all_score_vars.extend(res['score_variance'].tolist())
                all_score_stds.extend(res['score_std'].tolist())
                all_box_vars.extend(res['box_variance'].tolist())
                all_disagreements.extend(res['model_disagreement'].tolist())
                all_epistemic.extend(res['epistemic_uncertainty'].tolist())
                all_entropies.extend(res['predictive_entropy'].tolist())
                all_det_freqs.extend(res['detection_frequency'].tolist())

        f.write(f'Total detections: {total_detections}\n\n')

        if len(all_score_vars) > 0:
            f.write(f'Score Variance:\n')
            f.write(f'  Mean: {np.mean(all_score_vars):.6f}\n')
            f.write(f'  Std:  {np.std(all_score_vars):.6f}\n')
            f.write(f'  Min:  {np.min(all_score_vars):.6f}\n')
            f.write(f'  Max:  {np.max(all_score_vars):.6f}\n\n')

            f.write(f'Box Variance (position):\n')
            f.write(f'  Mean: {np.mean(all_box_vars):.6f}\n')
            f.write(f'  Std:  {np.std(all_box_vars):.6f}\n\n')

            f.write(f'Model Disagreement:\n')
            f.write(f'  Mean: {np.mean(all_disagreements):.6f}\n')
            f.write(f'  Std:  {np.std(all_disagreements):.6f}\n\n')

            f.write(f'Epistemic Uncertainty:\n')
            f.write(f'  Mean: {np.mean(all_epistemic):.6f}\n')
            f.write(f'  Std:  {np.std(all_epistemic):.6f}\n\n')

            f.write(f'Detection Frequency:\n')
            f.write(f'  Mean: {np.mean(all_det_freqs):.3f}\n')
            f.write(f'  Min:  {np.min(all_det_freqs):.3f}\n')
            f.write(f'  Max:  {np.max(all_det_freqs):.3f}\n')

    print(f'Summary saved to {summary_file}')


def main():
    args, cfg = parse_config()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Setup logger
    log_file = os.path.join(output_dir, 'log_ensemble.txt')
    logger = common_utils.create_logger(log_file, rank=0)
    logger.info('=' * 50)
    logger.info('Ensemble Uncertainty Estimation')
    logger.info('=' * 50)

    # Build dataset
    from pcdet.datasets import build_dataloader
    test_set, test_loader, sampler = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        class_names=cfg.CLASS_NAMES,
        batch_size=args.batch_size,
        dist=False,
        workers=args.workers,
        logger=logger,
        training=False,
        root_path=Path(args.data_path),
        merge_all_iters_to_one_epoch=False
    )

    logger.info(f'Dataset: {len(test_set)} samples')

    # Load ensemble models
    models = load_models(args.ckpt_dir, cfg, test_set, logger)

    # Run ensemble inference
    results = ensemble_inference(
        models=models,
        dataloader=test_loader,
        device='cuda'
    )

    # Save results
    save_results(results, output_dir, args, len(models))

    logger.info('Ensemble uncertainty estimation completed!')


if __name__ == '__main__':
    main()
