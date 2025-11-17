# Uncertainty Estimation for 3D Object Detection

This repository includes comprehensive uncertainty estimation methods for 3D object detection on KITTI-format datasets (including CARLA-generated data).

## Overview

Two main uncertainty estimation methods are implemented:

1. **Monte Carlo (MC) Dropout** - Uses stochastic forward passes with dropout enabled
2. **Ensemble Learning** - Combines predictions from multiple independently trained models

Both methods provide uncertainty metrics and are evaluated using calibration and correlation metrics.

## Features

- **MC Dropout Uncertainty**: Performs multiple stochastic forward passes (default: 30 samples)
- **Ensemble Uncertainty**: Aggregates predictions from multiple models
- **Comprehensive Metrics**:
  - Score variance and standard deviation
  - Box position variance
  - Epistemic uncertainty (knowledge uncertainty)
  - Predictive entropy
  - Model disagreement (ensemble only)
  - Detection frequency (ensemble only)

- **Evaluation Metrics**:
  - Expected Calibration Error (ECE)
  - AUROC for error detection
  - Uncertainty-error correlation (Spearman & Pearson)
  - Retention curves
  - Calibration plots

## Requirements

The code uses the existing OpenPCDet framework with the following key dependencies:

```bash
# Already installed in OpenPCDet
- PyTorch
- CUDA
- pcdet (OpenPCDet package)
- numpy
- matplotlib
- scikit-learn
- scipy
```

## Quick Start

### 1. Prepare Your Dataset

Ensure your CARLA-generated KITTI format dataset is organized as:

```
data/kitti/
├── ImageSets/
│   ├── train.txt
│   ├── val.txt
│   └── test.txt
├── training/
│   ├── velodyne/    # .bin point cloud files
│   ├── label_2/     # .txt label files (KITTI format)
│   ├── calib/       # .txt calibration files
│   └── image_2/     # .png images (optional)
└── testing/
    └── ...
```

### 2. Train Your Model(s)

**For MC Dropout**: Train a single model with dropout enabled (already configured in `pv_rcnn_car.yaml`)

```bash
cd tools
python train.py --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
                --batch_size 2 \
                --epochs 80
```

**For Ensemble**: Train multiple models with different random seeds

```bash
# Model 1
python train.py --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
                --batch_size 2 \
                --extra_tag seed_42 \
                --set OPTIMIZATION.RANDOM_SEED 42

# Model 2
python train.py --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
                --batch_size 2 \
                --extra_tag seed_123 \
                --set OPTIMIZATION.RANDOM_SEED 123

# Model 3 (recommended: 3-5 models)
python train.py --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
                --batch_size 2 \
                --extra_tag seed_456 \
                --set OPTIMIZATION.RANDOM_SEED 456
```

### 3. Run Uncertainty Estimation

#### Option A: Use the All-in-One Script (Recommended)

```bash
cd tools

# Run both MC Dropout and Ensemble
./run_uncertainty_estimation.sh \
    --ckpt ../output/pv_rcnn_car/default/ckpt/checkpoint_epoch_80.pth \
    --ckpt_dir ../output/pv_rcnn_car_ensemble/

# Run only MC Dropout
./run_uncertainty_estimation.sh \
    --ckpt ../output/pv_rcnn_car/default/ckpt/checkpoint_epoch_80.pth \
    --mc_only

# Run only Ensemble
./run_uncertainty_estimation.sh \
    --ckpt_dir ../output/pv_rcnn_car_ensemble/ \
    --ensemble_only
```

#### Option B: Run Individual Scripts

**MC Dropout**:
```bash
python mc_dropout_uncertainty.py \
    --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
    --ckpt ../output/pv_rcnn_car/default/ckpt/checkpoint_epoch_80.pth \
    --data_path ../data/kitti \
    --num_samples 30 \
    --split val \
    --output_dir ../output/mc_dropout_uncertainty
```

**Ensemble**:
```bash
python ensemble_uncertainty.py \
    --cfg_file cfgs/kitti_models/pv_rcnn_car.yaml \
    --ckpt_dir ../output/pv_rcnn_car_ensemble/ \
    --data_path ../data/kitti \
    --split val \
    --output_dir ../output/ensemble_uncertainty
```

**Evaluation**:
```bash
python evaluate_uncertainty.py \
    --result_file ../output/mc_dropout_uncertainty/mc_dropout_results.pkl \
    --gt_path ../data/kitti/training/label_2 \
    --output_dir ../output/uncertainty_evaluation/mc_dropout \
    --iou_threshold 0.7
```

## Output Files

### MC Dropout Output
```
output/mc_dropout_uncertainty/
├── mc_dropout_results.pkl      # Predictions with uncertainty metrics
├── uncertainty_summary.txt     # Statistical summary
└── log_mc_dropout.txt         # Execution log
```

### Ensemble Output
```
output/ensemble_uncertainty/
├── ensemble_results.pkl        # Predictions with uncertainty metrics
├── uncertainty_summary.txt     # Statistical summary
└── log_ensemble.txt           # Execution log
```

### Evaluation Output
```
output/uncertainty_evaluation/
├── mc_dropout/
│   ├── uncertainty_metrics.pkl        # Detailed metrics
│   ├── evaluation_summary.txt         # Summary report
│   ├── calibration_curve.png          # Calibration plot
│   ├── retention_curve.png            # Retention analysis
│   └── uncertainty_vs_error.png       # Scatter plot
└── ensemble/
    └── ... (same structure)
```

## Understanding the Results

### Uncertainty Metrics

1. **Score Variance**: Variance of confidence scores across samples/models
   - Higher variance = higher uncertainty

2. **Score Std**: Standard deviation of scores
   - Easier to interpret than variance

3. **Box Variance**: Variance in predicted box positions (x, y, z)
   - Spatial uncertainty of detection

4. **Epistemic Uncertainty**: Knowledge uncertainty
   - Reducible with more training data

5. **Predictive Entropy**: Prediction uncertainty
   - Measures randomness in predictions

6. **Model Disagreement** (Ensemble only): How much models disagree
   - High disagreement = high uncertainty

7. **Detection Frequency** (Ensemble only): Fraction of models detecting object
   - Low frequency = uncertain detection

### Evaluation Metrics

1. **Expected Calibration Error (ECE)**: Range [0, 1]
   - Lower is better (0 = perfect calibration)
   - Measures if confidence matches actual accuracy

2. **AUROC**: Range [0.5, 1.0]
   - Higher is better (1.0 = perfect error detection)
   - Measures ability to detect errors using uncertainty

3. **Uncertainty-Error Correlation**: Range [-1, 1]
   - Higher is better (1 = perfect correlation)
   - High uncertainty should correlate with high error

4. **Retention Curves**:
   - Shows accuracy improvement when removing uncertain predictions
   - Good uncertainty: steep curve (removing uncertain improves accuracy)

## Example Results

After running the pipeline, you'll see results like:

```
MC Dropout Uncertainty Estimation Summary
==================================================

Config: cfgs/kitti_models/pv_rcnn_car.yaml
Number of MC samples: 30
Dataset split: val
Number of frames: 3769

Total detections: 15234

Score Variance:
  Mean: 0.003421
  Std:  0.004127
  Min:  0.000012
  Max:  0.098765

Epistemic Uncertainty:
  Mean: 0.003421
  Std:  0.004127
  Min:  0.000012
  Max:  0.098765
```

And evaluation results:

```
Uncertainty Estimation Evaluation
==================================================

Total Predictions: 15234
True Positives: 13897
False Positives: 1337
Precision: 0.9122

Expected Calibration Error (ECE): 0.0234
  (Lower is better, 0 = perfect calibration)

AUROC (Error Detection): 0.7845
  (Higher is better, 0.5 = random, 1.0 = perfect)

Uncertainty-Error Correlation:
  Spearman: 0.6123
  Pearson:  0.5834
  (Higher is better)
```

## Advanced Usage

### Custom Number of MC Samples

```bash
python mc_dropout_uncertainty.py \
    --num_samples 50  # More samples = better uncertainty estimate (but slower)
```

### Custom IoU Thresholds

```bash
# For evaluation
python evaluate_uncertainty.py \
    --iou_threshold 0.5  # Lower = more lenient TP classification
```

### Using Different Splits

```bash
# Test on training set
./run_uncertainty_estimation.sh \
    --ckpt model.pth \
    --split train

# Test on test set
./run_uncertainty_estimation.sh \
    --ckpt model.pth \
    --split test
```

## Configuration

The uncertainty estimation uses the same configuration as your training:

**Key settings in `pv_rcnn_car.yaml`**:

```yaml
DENSE_HEAD:
  DROPOUT_PROB: 0.3      # Dropout probability
  MC_DROPOUT: True       # Enable MC Dropout

ROI_HEAD:
  DP_RATIO: 0.3         # Dropout ratio
  MC_DROPOUT: True      # Enable MC Dropout
```

## Tips for Best Results

1. **MC Dropout**:
   - Use 20-50 samples (30 is a good balance)
   - Ensure dropout is enabled in config (`MC_DROPOUT: True`)
   - Higher dropout rate (0.3-0.5) gives more variance

2. **Ensemble**:
   - Train 3-5 models with different random seeds
   - Use same architecture and hyperparameters
   - Can also vary data augmentation

3. **Evaluation**:
   - Use IoU threshold consistent with your task (0.7 for Car detection)
   - More bins (15-20) for calibration with large datasets

4. **Performance**:
   - MC Dropout: ~30x slower than single forward pass
   - Ensemble: Scales linearly with number of models
   - Use batch_size=1 for consistent memory usage

## Troubleshooting

### Out of Memory
- Reduce `--num_samples` for MC Dropout
- Use `--batch_size 1`
- Process smaller subsets of data

### No Uncertainty (all zeros)
- Check that `MC_DROPOUT: True` in config
- Verify dropout layers are present in model
- Ensure model is in eval mode but dropout is active

### Poor Calibration (high ECE)
- Try temperature scaling (use `temp_scaling.py`)
- Retrain with better data augmentation
- Check for dataset shift between train/val

### Low AUROC
- Uncertainty may not be informative for your data
- Try different uncertainty metrics
- Increase number of MC samples or ensemble size

## Citation

If you use this uncertainty estimation code, please cite:

```bibtex
@misc{openpcdet_uncertainty2023,
  title={Uncertainty Estimation for 3D Object Detection},
  author={OpenPCDet Contributors},
  year={2023},
  howpublished={\url{https://github.com/open-mmlab/OpenPCDet}}
}
```

## References

- [Dropout as a Bayesian Approximation](https://arxiv.org/abs/1506.02142) (Gal & Ghahramani, 2016)
- [What Uncertainties Do We Need in Bayesian Deep Learning?](https://arxiv.org/abs/1703.04977) (Kendall & Gal, 2017)
- [Ensemble Distribution Distillation](https://arxiv.org/abs/1909.00219) (Malinin et al., 2019)

## Contact

For issues or questions about uncertainty estimation, please open an issue on GitHub.
