"""
Monte Carlo Dropout Uncertainty Estimation for 3D Object Detection
Performs multiple stochastic forward passes and computes uncertainty metrics
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
    parser = argparse.ArgumentParser(description='Monte Carlo Dropout Uncertainty Estimation')
    parser.add_argument('--cfg_file', type=str, required=True,
                        help='specify the config for training')
    parser.add_argument('--ckpt', type=str, required=True,
                        help='checkpoint to start from')
    parser.add_argument('--data_path', type=str, required=True,
                        help='path to KITTI format dataset')
    parser.add_argument('--batch_size', type=int, default=1,
                        help='batch size for inference')
    parser.add_argument('--num_samples', type=int, default=30,
                        help='number of MC dropout samples')
    parser.add_argument('--output_dir', type=str, default='../output/mc_dropout_uncertainty',
                        help='output directory for results')
    parser.add_argument('--split', type=str, default='val',
                        choices=['train', 'val', 'test'],
                        help='dataset split to use')
    parser.add_argument('--workers', type=int, default=4,
                        help='number of workers for dataloader')
    parser.add_argument('--save_predictions', action='store_true',
                        help='save predictions with uncertainty')

    args = parser.parse_args()

    cfg_from_yaml_file(args.cfg_file, cfg)
    cfg.TAG = Path(args.cfg_file).stem
    cfg.EXP_GROUP_PATH = '/'.join(args.cfg_file.split('/')[1:-1])

    return args, cfg


def enable_mc_dropout(model):
    """Enable MC Dropout for all dropout layers"""
    for module in model.modules():
        if module.__class__.__name__.startswith('MonteCarloDropout'):
            module.train()  # Keep dropout active
        elif isinstance(module, (torch.nn.Dropout, torch.nn.Dropout2d, torch.nn.Dropout3d)):
            module.train()  # Keep dropout active
    return model


def mc_dropout_inference(model, dataloader, num_samples=30, device='cuda'):
    """
    Perform MC Dropout inference

    Args:
        model: trained model
        dataloader: data loader
        num_samples: number of stochastic forward passes
        device: device to run on

    Returns:
        results: list of dictionaries containing predictions and uncertainties
    """
    model.eval()  # Set to eval mode first
    enable_mc_dropout(model)  # Then enable dropout layers

    results = []

    with torch.no_grad():
        for i, batch_dict in enumerate(tqdm(dataloader, desc='MC Dropout Inference')):
            load_data_to_gpu(batch_dict)

            # Storage for multiple forward passes
            all_boxes = []
            all_scores = []
            all_labels = []

            # Perform multiple stochastic forward passes
            for sample_idx in range(num_samples):
                pred_dicts, _ = model(batch_dict)

                # Extract predictions for first item in batch
                pred_dict = pred_dicts[0]

                if pred_dict['pred_boxes'].shape[0] > 0:
                    all_boxes.append(pred_dict['pred_boxes'].cpu().numpy())
                    all_scores.append(pred_dict['pred_scores'].cpu().numpy())
                    all_labels.append(pred_dict['pred_labels'].cpu().numpy())

            # Compute uncertainty metrics
            if len(all_boxes) > 0:
                uncertainty_dict = compute_uncertainty_metrics(
                    all_boxes, all_scores, all_labels, num_samples
                )
            else:
                uncertainty_dict = {
                    'boxes': np.array([]),
                    'scores': np.array([]),
                    'labels': np.array([]),
                    'score_variance': np.array([]),
                    'score_std': np.array([]),
                    'box_variance': np.array([]),
                    'epistemic_uncertainty': np.array([]),
                    'predictive_entropy': np.array([])
                }

            # Add frame_id for tracking
            uncertainty_dict['frame_id'] = batch_dict['frame_id'][0]
            results.append(uncertainty_dict)

    return results


def compute_uncertainty_metrics(all_boxes, all_scores, all_labels, num_samples):
    """
    Compute uncertainty metrics from multiple forward passes

    Metrics:
    - Score variance: variance of confidence scores
    - Score std: standard deviation of scores
    - Box variance: variance in box locations
    - Epistemic uncertainty: knowledge uncertainty
    - Predictive entropy: prediction uncertainty
    """

    # Match detections across forward passes using Hungarian matching
    matched_detections = match_detections_across_samples(all_boxes, all_scores, all_labels)

    # Compute mean predictions
    mean_boxes = []
    mean_scores = []
    mean_labels = []
    score_variances = []
    score_stds = []
    box_variances = []
    epistemic_uncertainties = []
    predictive_entropies = []

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

        # Score uncertainty
        score_var = np.var(scores)
        score_std = np.std(scores)

        # Box position uncertainty (variance in x, y, z)
        box_var = np.mean(np.var(boxes[:, :3], axis=0))

        # Epistemic uncertainty (knowledge uncertainty)
        # Measured by variance of predictions
        epistemic = score_var

        # Predictive entropy
        # H(p) = -sum(p * log(p))
        score_prob = scores / (scores.sum() + 1e-10)
        pred_entropy = -np.sum(score_prob * np.log(score_prob + 1e-10))

        mean_boxes.append(mean_box)
        mean_scores.append(mean_score)
        mean_labels.append(mean_label)
        score_variances.append(score_var)
        score_stds.append(score_std)
        box_variances.append(box_var)
        epistemic_uncertainties.append(epistemic)
        predictive_entropies.append(pred_entropy)

    return {
        'boxes': np.array(mean_boxes) if len(mean_boxes) > 0 else np.array([]),
        'scores': np.array(mean_scores) if len(mean_scores) > 0 else np.array([]),
        'labels': np.array(mean_labels) if len(mean_labels) > 0 else np.array([]),
        'score_variance': np.array(score_variances) if len(score_variances) > 0 else np.array([]),
        'score_std': np.array(score_stds) if len(score_stds) > 0 else np.array([]),
        'box_variance': np.array(box_variances) if len(box_variances) > 0 else np.array([]),
        'epistemic_uncertainty': np.array(epistemic_uncertainties) if len(epistemic_uncertainties) > 0 else np.array([]),
        'predictive_entropy': np.array(predictive_entropies) if len(predictive_entropies) > 0 else np.array([])
    }


def match_detections_across_samples(all_boxes, all_scores, all_labels, iou_threshold=0.5):
    """
    Match detections across multiple MC samples using IoU-based matching

    Returns:
        List of detection groups, each containing boxes, scores, labels from different samples
    """
    from pcdet.ops.iou3d_nms.iou3d_nms_utils import boxes_iou3d_gpu

    if len(all_boxes) == 0:
        return []

    # Start with first sample as reference
    detection_groups = []
    for box_idx in range(len(all_boxes[0])):
        detection_groups.append({
            'boxes': [all_boxes[0][box_idx]],
            'scores': [all_scores[0][box_idx]],
            'labels': [all_labels[0][box_idx]]
        })

    # Match detections from subsequent samples
    for sample_idx in range(1, len(all_boxes)):
        boxes_sample = all_boxes[sample_idx]
        scores_sample = all_scores[sample_idx]
        labels_sample = all_labels[sample_idx]

        if len(boxes_sample) == 0:
            continue

        # Compute IoU between current groups and new sample
        matched_indices = set()

        for group in detection_groups:
            if len(group['boxes']) == 0:
                continue

            # Use most recent box in group as reference
            ref_box = torch.from_numpy(np.array([group['boxes'][-1]])).cuda()
            sample_boxes = torch.from_numpy(boxes_sample).cuda()

            # Compute IoU
            ious = boxes_iou3d_gpu(ref_box, sample_boxes)
            max_iou, max_idx = torch.max(ious[0], dim=0)

            if max_iou > iou_threshold and max_idx.item() not in matched_indices:
                # Match found
                group['boxes'].append(boxes_sample[max_idx.item()])
                group['scores'].append(scores_sample[max_idx.item()])
                group['labels'].append(labels_sample[max_idx.item()])
                matched_indices.add(max_idx.item())

        # Add unmatched detections as new groups
        for box_idx in range(len(boxes_sample)):
            if box_idx not in matched_indices:
                detection_groups.append({
                    'boxes': [boxes_sample[box_idx]],
                    'scores': [scores_sample[box_idx]],
                    'labels': [labels_sample[box_idx]]
                })

    return detection_groups


def save_results(results, output_dir, args):
    """Save uncertainty estimation results"""
    os.makedirs(output_dir, exist_ok=True)

    # Save as pickle
    result_file = os.path.join(output_dir, 'mc_dropout_results.pkl')
    with open(result_file, 'wb') as f:
        pickle.dump(results, f)

    print(f'\nResults saved to {result_file}')

    # Save summary statistics
    summary_file = os.path.join(output_dir, 'uncertainty_summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f'MC Dropout Uncertainty Estimation Summary\n')
        f.write(f'=' * 50 + '\n\n')
        f.write(f'Config: {args.cfg_file}\n')
        f.write(f'Checkpoint: {args.ckpt}\n')
        f.write(f'Number of MC samples: {args.num_samples}\n')
        f.write(f'Dataset split: {args.split}\n')
        f.write(f'Number of frames: {len(results)}\n\n')

        # Aggregate statistics
        all_score_vars = []
        all_score_stds = []
        all_box_vars = []
        all_epistemic = []
        all_entropies = []
        total_detections = 0

        for res in results:
            if len(res['scores']) > 0:
                total_detections += len(res['scores'])
                all_score_vars.extend(res['score_variance'].tolist())
                all_score_stds.extend(res['score_std'].tolist())
                all_box_vars.extend(res['box_variance'].tolist())
                all_epistemic.extend(res['epistemic_uncertainty'].tolist())
                all_entropies.extend(res['predictive_entropy'].tolist())

        f.write(f'Total detections: {total_detections}\n\n')

        if len(all_score_vars) > 0:
            f.write(f'Score Variance:\n')
            f.write(f'  Mean: {np.mean(all_score_vars):.6f}\n')
            f.write(f'  Std:  {np.std(all_score_vars):.6f}\n')
            f.write(f'  Min:  {np.min(all_score_vars):.6f}\n')
            f.write(f'  Max:  {np.max(all_score_vars):.6f}\n\n')

            f.write(f'Score Std:\n')
            f.write(f'  Mean: {np.mean(all_score_stds):.6f}\n')
            f.write(f'  Std:  {np.std(all_score_stds):.6f}\n')
            f.write(f'  Min:  {np.min(all_score_stds):.6f}\n')
            f.write(f'  Max:  {np.max(all_score_stds):.6f}\n\n')

            f.write(f'Box Variance (position):\n')
            f.write(f'  Mean: {np.mean(all_box_vars):.6f}\n')
            f.write(f'  Std:  {np.std(all_box_vars):.6f}\n')
            f.write(f'  Min:  {np.min(all_box_vars):.6f}\n')
            f.write(f'  Max:  {np.max(all_box_vars):.6f}\n\n')

            f.write(f'Epistemic Uncertainty:\n')
            f.write(f'  Mean: {np.mean(all_epistemic):.6f}\n')
            f.write(f'  Std:  {np.std(all_epistemic):.6f}\n')
            f.write(f'  Min:  {np.min(all_epistemic):.6f}\n')
            f.write(f'  Max:  {np.max(all_epistemic):.6f}\n\n')

            f.write(f'Predictive Entropy:\n')
            f.write(f'  Mean: {np.mean(all_entropies):.6f}\n')
            f.write(f'  Std:  {np.std(all_entropies):.6f}\n')
            f.write(f'  Min:  {np.min(all_entropies):.6f}\n')
            f.write(f'  Max:  {np.max(all_entropies):.6f}\n')

    print(f'Summary saved to {summary_file}')


def main():
    args, cfg = parse_config()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Setup logger
    log_file = os.path.join(output_dir, 'log_mc_dropout.txt')
    logger = common_utils.create_logger(log_file, rank=0)
    logger.info('=' * 50)
    logger.info('Monte Carlo Dropout Uncertainty Estimation')
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

    # Build model
    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=test_set)
    model.load_params_from_file(filename=args.ckpt, logger=logger, to_cpu=False)
    model.cuda()

    logger.info(f'Model loaded from {args.ckpt}')
    logger.info(f'Number of MC samples: {args.num_samples}')

    # Run MC Dropout inference
    results = mc_dropout_inference(
        model=model,
        dataloader=test_loader,
        num_samples=args.num_samples,
        device='cuda'
    )

    # Save results
    save_results(results, output_dir, args)

    logger.info('MC Dropout uncertainty estimation completed!')


if __name__ == '__main__':
    main()
