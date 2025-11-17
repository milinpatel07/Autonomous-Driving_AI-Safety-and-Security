#!/bin/bash

# Example: How to use the uncertainty estimation scripts
# This is a simple example showing typical usage

echo "=========================================="
echo "Uncertainty Estimation Example"
echo "=========================================="
echo ""
echo "This example shows how to run uncertainty estimation on your CARLA KITTI dataset"
echo ""

# ============================================
# Step 1: Setup paths
# ============================================

echo "Step 1: Setup paths"
echo "-------------------"

# Update these paths to match your setup
CONFIG_FILE="cfgs/kitti_models/pv_rcnn_car.yaml"
DATA_PATH="../data/kitti"
CHECKPOINT="../output/pv_rcnn_car/default/ckpt/checkpoint_epoch_80.pth"
CHECKPOINT_DIR="../output/pv_rcnn_car_ensemble/"  # For ensemble (optional)

echo "Config:     $CONFIG_FILE"
echo "Data:       $DATA_PATH"
echo "Checkpoint: $CHECKPOINT"
echo ""

# ============================================
# Step 2: Check if checkpoint exists
# ============================================

echo "Step 2: Check checkpoint"
echo "------------------------"

if [ ! -f "$CHECKPOINT" ]; then
    echo "WARNING: Checkpoint not found at: $CHECKPOINT"
    echo ""
    echo "Please train a model first using:"
    echo "  python train.py --cfg_file $CONFIG_FILE --batch_size 2 --epochs 80"
    echo ""
    echo "Or update the CHECKPOINT variable above to point to your trained model."
    exit 1
else
    echo "Checkpoint found: $CHECKPOINT"
fi
echo ""

# ============================================
# Step 3: Run MC Dropout Uncertainty
# ============================================

echo "Step 3: Run MC Dropout Uncertainty Estimation"
echo "----------------------------------------------"
echo ""
echo "Running Monte Carlo Dropout with 30 stochastic forward passes..."
echo "This will take some time (approximately 30x normal inference time)"
echo ""

python mc_dropout_uncertainty.py \
    --cfg_file "$CONFIG_FILE" \
    --ckpt "$CHECKPOINT" \
    --data_path "$DATA_PATH" \
    --num_samples 30 \
    --split val \
    --batch_size 1 \
    --workers 4 \
    --output_dir ../output/mc_dropout_uncertainty \
    --save_predictions

if [ $? -eq 0 ]; then
    echo ""
    echo "MC Dropout completed successfully!"
    echo "Results saved to: ../output/mc_dropout_uncertainty/"
else
    echo ""
    echo "ERROR: MC Dropout failed!"
    exit 1
fi
echo ""

# ============================================
# Step 4: Evaluate Uncertainty
# ============================================

echo "Step 4: Evaluate Uncertainty Estimation"
echo "----------------------------------------"
echo ""
echo "Computing calibration metrics, AUROC, and correlation..."
echo ""

python evaluate_uncertainty.py \
    --result_file ../output/mc_dropout_uncertainty/mc_dropout_results.pkl \
    --gt_path "$DATA_PATH/training/label_2" \
    --output_dir ../output/uncertainty_evaluation/mc_dropout \
    --iou_threshold 0.7 \
    --num_bins 10

if [ $? -eq 0 ]; then
    echo ""
    echo "Evaluation completed successfully!"
    echo "Results saved to: ../output/uncertainty_evaluation/mc_dropout/"
else
    echo ""
    echo "ERROR: Evaluation failed!"
    exit 1
fi
echo ""

# ============================================
# Step 5: View Results
# ============================================

echo "Step 5: View Results"
echo "--------------------"
echo ""
echo "Uncertainty estimation summary:"
cat ../output/mc_dropout_uncertainty/uncertainty_summary.txt
echo ""
echo ""
echo "Evaluation summary:"
cat ../output/uncertainty_evaluation/mc_dropout/evaluation_summary.txt
echo ""
echo ""

# ============================================
# Optional: Run Ensemble (if you have multiple models)
# ============================================

echo "Optional: Ensemble Uncertainty"
echo "-------------------------------"
echo ""

if [ -d "$CHECKPOINT_DIR" ] && [ "$(ls -A $CHECKPOINT_DIR/*.pth 2>/dev/null)" ]; then
    echo "Found checkpoints in $CHECKPOINT_DIR"
    echo "Running ensemble uncertainty estimation..."
    echo ""

    python ensemble_uncertainty.py \
        --cfg_file "$CONFIG_FILE" \
        --ckpt_dir "$CHECKPOINT_DIR" \
        --data_path "$DATA_PATH" \
        --split val \
        --batch_size 1 \
        --workers 4 \
        --output_dir ../output/ensemble_uncertainty \
        --iou_threshold 0.5

    if [ $? -eq 0 ]; then
        echo ""
        echo "Ensemble completed successfully!"

        # Evaluate ensemble
        python evaluate_uncertainty.py \
            --result_file ../output/ensemble_uncertainty/ensemble_results.pkl \
            --gt_path "$DATA_PATH/training/label_2" \
            --output_dir ../output/uncertainty_evaluation/ensemble \
            --iou_threshold 0.7 \
            --num_bins 10
    fi
else
    echo "No ensemble checkpoints found in $CHECKPOINT_DIR"
    echo ""
    echo "To use ensemble uncertainty, train multiple models with different seeds:"
    echo "  python train.py --cfg_file $CONFIG_FILE --extra_tag seed_42"
    echo "  python train.py --cfg_file $CONFIG_FILE --extra_tag seed_123"
    echo "  python train.py --cfg_file $CONFIG_FILE --extra_tag seed_456"
fi
echo ""

# ============================================
# Summary
# ============================================

echo "=========================================="
echo "Done!"
echo "=========================================="
echo ""
echo "Output directories:"
echo "  MC Dropout results:    ../output/mc_dropout_uncertainty/"
echo "  Evaluation results:    ../output/uncertainty_evaluation/mc_dropout/"
echo ""
echo "Key files to check:"
echo "  - uncertainty_summary.txt         (statistical summary)"
echo "  - evaluation_summary.txt          (calibration metrics)"
echo "  - calibration_curve.png           (calibration plot)"
echo "  - retention_curve.png             (uncertainty vs accuracy)"
echo "  - uncertainty_vs_error.png        (scatter plot)"
echo ""
echo "For more options, see: ./run_uncertainty_estimation.sh --help"
echo ""
