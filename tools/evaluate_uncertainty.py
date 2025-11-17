"""
Evaluate Uncertainty Estimation Quality for 3D Object Detection

Metrics:
- Calibration: Expected Calibration Error (ECE)
- Correlation: Uncertainty vs Error correlation
- AUROC: Area under ROC curve for error detection
- Retention curves: Performance vs uncertainty threshold
"""

import argparse
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
from sklearn.metrics import roc_auc_score, roc_curve
from scipy.stats import spearmanr, pearsonr


def parse_config():
    parser = argparse.ArgumentParser(description='Evaluate Uncertainty Estimation')
    parser.add_argument('--result_file', type=str, required=True,
                        help='path to uncertainty results pickle file')
    parser.add_argument('--gt_path', type=str, required=True,
                        help='path to ground truth labels')
    parser.add_argument('--output_dir', type=str, default='../output/uncertainty_eval',
                        help='output directory for evaluation results')
    parser.add_argument('--iou_threshold', type=float, default=0.7,
                        help='IoU threshold for TP/FP classification')
    parser.add_argument('--num_bins', type=int, default=10,
                        help='number of bins for calibration')

    return parser.parse_args()


def load_ground_truth(gt_path, frame_ids):
    """Load ground truth labels for given frame IDs"""
    from pcdet.datasets.kitti.kitti_object_eval_python import kitti_common

    gt_annos = []

    for frame_id in frame_ids:
        # KITTI format: frame_id is like '000001.txt'
        if isinstance(frame_id, str):
            if frame_id.endswith('.bin'):
                frame_id = frame_id.replace('.bin', '')
            label_file = os.path.join(gt_path, f'{frame_id}.txt')
        else:
            label_file = os.path.join(gt_path, f'{frame_id:06d}.txt')

        if os.path.exists(label_file):
            anno = kitti_common.get_label_anno(label_file)
            gt_annos.append(anno)
        else:
            # Empty annotation
            gt_annos.append({
                'name': np.array([]),
                'truncated': np.array([]),
                'occluded': np.array([]),
                'alpha': np.array([]),
                'bbox': np.zeros((0, 4)),
                'dimensions': np.zeros((0, 3)),
                'location': np.zeros((0, 3)),
                'rotation_y': np.array([])
            })

    return gt_annos


def compute_iou_3d(boxes1, boxes2):
    """Compute 3D IoU between two sets of boxes"""
    from pcdet.ops.iou3d_nms.iou3d_nms_utils import boxes_iou3d_gpu
    import torch

    if len(boxes1) == 0 or len(boxes2) == 0:
        return np.zeros((len(boxes1), len(boxes2)))

    boxes1_tensor = torch.from_numpy(boxes1).cuda()
    boxes2_tensor = torch.from_numpy(boxes2).cuda()

    ious = boxes_iou3d_gpu(boxes1_tensor, boxes2_tensor)

    return ious.cpu().numpy()


def match_predictions_to_gt(pred_boxes, pred_scores, gt_boxes, iou_threshold=0.7):
    """
    Match predictions to ground truth using IoU

    Returns:
        tp_mask: boolean array indicating true positives
        ious: IoU values for each prediction
    """
    if len(pred_boxes) == 0:
        return np.array([]), np.array([])

    if len(gt_boxes) == 0:
        return np.zeros(len(pred_boxes), dtype=bool), np.zeros(len(pred_boxes))

    # Compute IoU
    ious = compute_iou_3d(pred_boxes, gt_boxes)

    # For each prediction, find best matching GT
    max_ious = np.max(ious, axis=1)

    # True positive if IoU >= threshold
    tp_mask = max_ious >= iou_threshold

    return tp_mask, max_ious


def compute_expected_calibration_error(confidences, accuracies, num_bins=10):
    """
    Compute Expected Calibration Error (ECE)

    ECE = sum_i (|bin_i| / N) * |acc_i - conf_i|

    Args:
        confidences: prediction confidences
        accuracies: binary accuracy (1 for TP, 0 for FP)
        num_bins: number of bins

    Returns:
        ece: expected calibration error
        bin_stats: statistics per bin
    """
    if len(confidences) == 0:
        return 0.0, []

    # Create bins
    bin_boundaries = np.linspace(0, 1, num_bins + 1)
    bin_stats = []

    ece = 0.0
    total_samples = len(confidences)

    for i in range(num_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]

        # Find samples in this bin
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        bin_size = np.sum(in_bin)

        if bin_size > 0:
            bin_confidence = np.mean(confidences[in_bin])
            bin_accuracy = np.mean(accuracies[in_bin])
            bin_error = np.abs(bin_accuracy - bin_confidence)

            ece += (bin_size / total_samples) * bin_error

            bin_stats.append({
                'bin_lower': bin_lower,
                'bin_upper': bin_upper,
                'bin_size': bin_size,
                'bin_confidence': bin_confidence,
                'bin_accuracy': bin_accuracy,
                'bin_error': bin_error
            })
        else:
            bin_stats.append({
                'bin_lower': bin_lower,
                'bin_upper': bin_upper,
                'bin_size': 0,
                'bin_confidence': 0.0,
                'bin_accuracy': 0.0,
                'bin_error': 0.0
            })

    return ece, bin_stats


def compute_uncertainty_error_correlation(uncertainties, errors):
    """
    Compute correlation between uncertainty and error

    Higher correlation means better uncertainty estimation
    """
    if len(uncertainties) == 0 or len(errors) == 0:
        return 0.0, 0.0

    # Spearman correlation (rank-based)
    spearman_corr, spearman_p = spearmanr(uncertainties, errors)

    # Pearson correlation (linear)
    pearson_corr, pearson_p = pearsonr(uncertainties, errors)

    return spearman_corr, pearson_corr


def compute_auroc_for_error_detection(uncertainties, is_correct):
    """
    Compute AUROC for detecting errors using uncertainty

    High uncertainty should correspond to errors (FP)
    Low uncertainty should correspond to correct predictions (TP)
    """
    if len(uncertainties) == 0:
        return 0.5

    # Invert is_correct to get is_error
    is_error = ~is_correct

    if np.all(is_error) or np.all(~is_error):
        # All same label, AUROC undefined
        return 0.5

    auroc = roc_auc_score(is_error, uncertainties)

    return auroc


def compute_retention_curves(scores, uncertainties, is_correct, num_thresholds=20):
    """
    Compute retention curves: accuracy vs fraction retained

    By removing high-uncertainty predictions, accuracy should increase
    """
    # Sort by uncertainty (low to high)
    sorted_indices = np.argsort(uncertainties)

    fractions_retained = np.linspace(0.1, 1.0, num_thresholds)
    accuracies = []
    avg_scores = []

    for fraction in fractions_retained:
        num_to_keep = int(len(sorted_indices) * fraction)
        if num_to_keep == 0:
            continue

        kept_indices = sorted_indices[:num_to_keep]

        accuracy = np.mean(is_correct[kept_indices])
        avg_score = np.mean(scores[kept_indices])

        accuracies.append(accuracy)
        avg_scores.append(avg_score)

    return fractions_retained[:len(accuracies)], accuracies, avg_scores


def evaluate_uncertainty(results, gt_annos, iou_threshold=0.7, num_bins=10):
    """
    Main uncertainty evaluation function

    Returns:
        metrics: dictionary of evaluation metrics
    """
    all_confidences = []
    all_uncertainties = []
    all_is_correct = []
    all_ious = []
    all_errors = []

    for res, gt_anno in zip(results, gt_annos):
        if len(res['boxes']) == 0:
            continue

        pred_boxes = res['boxes']
        pred_scores = res['scores']

        # Convert GT to boxes (KITTI format: [x, y, z, l, w, h, ry])
        if len(gt_anno['name']) > 0:
            # Filter only 'Car' class
            car_mask = gt_anno['name'] == 'Car'
            if np.sum(car_mask) > 0:
                gt_boxes = np.concatenate([
                    gt_anno['location'][car_mask],
                    gt_anno['dimensions'][car_mask][:, [1, 2, 0]],  # h, w, l -> l, w, h
                    gt_anno['rotation_y'][car_mask].reshape(-1, 1)
                ], axis=1)
            else:
                gt_boxes = np.array([])
        else:
            gt_boxes = np.array([])

        # Match predictions to GT
        tp_mask, ious = match_predictions_to_gt(pred_boxes, pred_scores, gt_boxes, iou_threshold)

        # Use score variance as uncertainty
        if 'score_variance' in res and len(res['score_variance']) > 0:
            uncertainties = res['score_variance']
        elif 'score_std' in res and len(res['score_std']) > 0:
            uncertainties = res['score_std']
        else:
            uncertainties = 1.0 - pred_scores  # Fallback

        # Compute errors (1 - IoU for matched, 1.0 for unmatched)
        errors = 1.0 - ious

        all_confidences.extend(pred_scores.tolist())
        all_uncertainties.extend(uncertainties.tolist())
        all_is_correct.extend(tp_mask.tolist())
        all_ious.extend(ious.tolist())
        all_errors.extend(errors.tolist())

    # Convert to numpy arrays
    all_confidences = np.array(all_confidences)
    all_uncertainties = np.array(all_uncertainties)
    all_is_correct = np.array(all_is_correct)
    all_ious = np.array(all_ious)
    all_errors = np.array(all_errors)

    # Compute metrics
    metrics = {}

    # 1. Calibration (ECE)
    ece, bin_stats = compute_expected_calibration_error(all_confidences, all_is_correct, num_bins)
    metrics['ECE'] = ece
    metrics['bin_stats'] = bin_stats

    # 2. Uncertainty-Error Correlation
    spearman_corr, pearson_corr = compute_uncertainty_error_correlation(all_uncertainties, all_errors)
    metrics['spearman_correlation'] = spearman_corr
    metrics['pearson_correlation'] = pearson_corr

    # 3. AUROC for error detection
    auroc = compute_auroc_for_error_detection(all_uncertainties, all_is_correct)
    metrics['AUROC'] = auroc

    # 4. Retention curves
    fractions, accuracies, avg_scores = compute_retention_curves(
        all_confidences, all_uncertainties, all_is_correct
    )
    metrics['retention_fractions'] = fractions
    metrics['retention_accuracies'] = accuracies
    metrics['retention_scores'] = avg_scores

    # 5. Basic statistics
    metrics['total_predictions'] = len(all_confidences)
    metrics['true_positives'] = np.sum(all_is_correct)
    metrics['false_positives'] = np.sum(~all_is_correct)
    metrics['precision'] = np.mean(all_is_correct)
    metrics['avg_uncertainty'] = np.mean(all_uncertainties)
    metrics['avg_confidence'] = np.mean(all_confidences)

    return metrics, (all_confidences, all_uncertainties, all_is_correct, all_errors)


def plot_calibration_curve(bin_stats, output_path):
    """Plot calibration curve"""
    plt.figure(figsize=(8, 6))

    bin_confidences = [b['bin_confidence'] for b in bin_stats if b['bin_size'] > 0]
    bin_accuracies = [b['bin_accuracy'] for b in bin_stats if b['bin_size'] > 0]

    plt.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
    plt.plot(bin_confidences, bin_accuracies, 'o-', label='Model Calibration')

    plt.xlabel('Confidence')
    plt.ylabel('Accuracy')
    plt.title('Calibration Curve')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_retention_curve(fractions, accuracies, output_path):
    """Plot retention curve"""
    plt.figure(figsize=(8, 6))

    plt.plot(fractions, accuracies, 'o-')
    plt.xlabel('Fraction of Predictions Retained')
    plt.ylabel('Accuracy (Precision)')
    plt.title('Retention Curve: Accuracy vs Fraction Retained')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_uncertainty_vs_error(uncertainties, errors, output_path):
    """Plot uncertainty vs error scatter"""
    plt.figure(figsize=(8, 6))

    plt.scatter(uncertainties, errors, alpha=0.5, s=10)
    plt.xlabel('Uncertainty (Score Variance)')
    plt.ylabel('Error (1 - IoU)')
    plt.title('Uncertainty vs Error')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def save_evaluation_results(metrics, output_dir):
    """Save evaluation results"""
    os.makedirs(output_dir, exist_ok=True)

    # Save metrics as pickle
    metrics_file = os.path.join(output_dir, 'uncertainty_metrics.pkl')
    with open(metrics_file, 'wb') as f:
        pickle.dump(metrics, f)

    # Save summary text
    summary_file = os.path.join(output_dir, 'evaluation_summary.txt')
    with open(summary_file, 'w') as f:
        f.write('Uncertainty Estimation Evaluation\n')
        f.write('=' * 50 + '\n\n')

        f.write(f'Total Predictions: {metrics["total_predictions"]}\n')
        f.write(f'True Positives: {metrics["true_positives"]}\n')
        f.write(f'False Positives: {metrics["false_positives"]}\n')
        f.write(f'Precision: {metrics["precision"]:.4f}\n\n')

        f.write(f'Expected Calibration Error (ECE): {metrics["ECE"]:.4f}\n')
        f.write(f'  (Lower is better, 0 = perfect calibration)\n\n')

        f.write(f'AUROC (Error Detection): {metrics["AUROC"]:.4f}\n')
        f.write(f'  (Higher is better, 0.5 = random, 1.0 = perfect)\n\n')

        f.write(f'Uncertainty-Error Correlation:\n')
        f.write(f'  Spearman: {metrics["spearman_correlation"]:.4f}\n')
        f.write(f'  Pearson:  {metrics["pearson_correlation"]:.4f}\n')
        f.write(f'  (Higher is better, means uncertainty correlates with error)\n\n')

        f.write(f'Average Confidence: {metrics["avg_confidence"]:.4f}\n')
        f.write(f'Average Uncertainty: {metrics["avg_uncertainty"]:.6f}\n')

    print(f'\nEvaluation results saved to {output_dir}')
    print(f'  Metrics: {metrics_file}')
    print(f'  Summary: {summary_file}')


def main():
    args = parse_config()

    # Load uncertainty results
    print(f'Loading uncertainty results from {args.result_file}')
    with open(args.result_file, 'rb') as f:
        results = pickle.load(f)

    print(f'Loaded {len(results)} frames')

    # Extract frame IDs
    frame_ids = [res['frame_id'] for res in results]

    # Load ground truth
    print(f'Loading ground truth from {args.gt_path}')
    gt_annos = load_ground_truth(args.gt_path, frame_ids)

    # Evaluate uncertainty
    print('Evaluating uncertainty estimation...')
    metrics, data = evaluate_uncertainty(
        results, gt_annos, args.iou_threshold, args.num_bins
    )

    all_confidences, all_uncertainties, all_is_correct, all_errors = data

    # Save results
    save_evaluation_results(metrics, args.output_dir)

    # Generate plots
    print('Generating plots...')
    plot_calibration_curve(
        metrics['bin_stats'],
        os.path.join(args.output_dir, 'calibration_curve.png')
    )
    plot_retention_curve(
        metrics['retention_fractions'],
        metrics['retention_accuracies'],
        os.path.join(args.output_dir, 'retention_curve.png')
    )
    plot_uncertainty_vs_error(
        all_uncertainties,
        all_errors,
        os.path.join(args.output_dir, 'uncertainty_vs_error.png')
    )

    print('\nEvaluation complete!')
    print(f'ECE: {metrics["ECE"]:.4f}')
    print(f'AUROC: {metrics["AUROC"]:.4f}')
    print(f'Spearman Correlation: {metrics["spearman_correlation"]:.4f}')


if __name__ == '__main__':
    main()
