#!/bin/bash

# Uncertainty Estimation Pipeline for 3D Object Detection
# This script runs both MC Dropout and Ensemble uncertainty estimation

set -e  # Exit on error

# ============================================================
# Configuration
# ============================================================

# Paths
CFG_FILE="cfgs/kitti_models/pv_rcnn_car.yaml"
DATA_PATH="../data/kitti"
CHECKPOINT=""  # Path to single checkpoint for MC Dropout
CHECKPOINT_DIR=""  # Directory with multiple checkpoints for Ensemble
GT_LABEL_PATH="../data/kitti/training/label_2"

# MC Dropout parameters
NUM_MC_SAMPLES=30  # Number of stochastic forward passes

# Data split
SPLIT="val"  # train, val, or test

# Output directories
MC_OUTPUT_DIR="../output/mc_dropout_uncertainty"
ENSEMBLE_OUTPUT_DIR="../output/ensemble_uncertainty"
EVAL_OUTPUT_DIR="../output/uncertainty_evaluation"

# Other parameters
BATCH_SIZE=1
NUM_WORKERS=4
IOU_THRESHOLD=0.7

# ============================================================
# Parse command line arguments
# ============================================================

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --cfg_file CFG          Config file (default: cfgs/kitti_models/pv_rcnn_car.yaml)"
    echo "  --data_path PATH        Path to KITTI dataset (default: ../data/kitti)"
    echo "  --ckpt CHECKPOINT       Single checkpoint for MC Dropout"
    echo "  --ckpt_dir DIR          Directory with checkpoints for Ensemble"
    echo "  --split SPLIT           Dataset split: train/val/test (default: val)"
    echo "  --num_mc_samples N      Number of MC samples (default: 30)"
    echo "  --mc_only               Run only MC Dropout"
    echo "  --ensemble_only         Run only Ensemble"
    echo "  --eval_only             Run only evaluation (requires prior results)"
    echo "  --help                  Show this help message"
    echo ""
    echo "Examples:"
    echo "  # MC Dropout only"
    echo "  $0 --ckpt ../output/model.pth --mc_only"
    echo ""
    echo "  # Ensemble only"
    echo "  $0 --ckpt_dir ../output/checkpoints/ --ensemble_only"
    echo ""
    echo "  # Both methods"
    echo "  $0 --ckpt ../output/model.pth --ckpt_dir ../output/checkpoints/"
}

RUN_MC=true
RUN_ENSEMBLE=true
RUN_EVAL=true
EVAL_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --cfg_file)
            CFG_FILE="$2"
            shift 2
            ;;
        --data_path)
            DATA_PATH="$2"
            shift 2
            ;;
        --ckpt)
            CHECKPOINT="$2"
            shift 2
            ;;
        --ckpt_dir)
            CHECKPOINT_DIR="$2"
            shift 2
            ;;
        --split)
            SPLIT="$2"
            shift 2
            ;;
        --num_mc_samples)
            NUM_MC_SAMPLES="$2"
            shift 2
            ;;
        --mc_only)
            RUN_ENSEMBLE=false
            shift
            ;;
        --ensemble_only)
            RUN_MC=false
            shift
            ;;
        --eval_only)
            EVAL_ONLY=true
            RUN_MC=false
            RUN_ENSEMBLE=false
            shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# ============================================================
# Validation
# ============================================================

if [ "$EVAL_ONLY" = false ]; then
    if [ "$RUN_MC" = true ] && [ -z "$CHECKPOINT" ]; then
        echo "Error: --ckpt required for MC Dropout"
        exit 1
    fi

    if [ "$RUN_ENSEMBLE" = true ] && [ -z "$CHECKPOINT_DIR" ]; then
        echo "Error: --ckpt_dir required for Ensemble"
        exit 1
    fi

    if [ ! -f "$CFG_FILE" ]; then
        echo "Error: Config file not found: $CFG_FILE"
        exit 1
    fi

    if [ ! -d "$DATA_PATH" ]; then
        echo "Error: Data path not found: $DATA_PATH"
        exit 1
    fi
fi

# ============================================================
# Print configuration
# ============================================================

echo "============================================================"
echo "Uncertainty Estimation Pipeline"
echo "============================================================"
echo ""
echo "Configuration:"
echo "  Config file:        $CFG_FILE"
echo "  Data path:          $DATA_PATH"
echo "  Split:              $SPLIT"
echo "  Checkpoint:         $CHECKPOINT"
echo "  Checkpoint dir:     $CHECKPOINT_DIR"
echo "  MC samples:         $NUM_MC_SAMPLES"
echo ""
echo "Methods to run:"
echo "  MC Dropout:         $RUN_MC"
echo "  Ensemble:           $RUN_ENSEMBLE"
echo "  Evaluation:         $RUN_EVAL"
echo ""

# ============================================================
# Run MC Dropout Uncertainty Estimation
# ============================================================

if [ "$RUN_MC" = true ]; then
    echo "============================================================"
    echo "Running MC Dropout Uncertainty Estimation"
    echo "============================================================"

    python mc_dropout_uncertainty.py \
        --cfg_file "$CFG_FILE" \
        --ckpt "$CHECKPOINT" \
        --data_path "$DATA_PATH" \
        --batch_size $BATCH_SIZE \
        --num_samples $NUM_MC_SAMPLES \
        --output_dir "$MC_OUTPUT_DIR" \
        --split "$SPLIT" \
        --workers $NUM_WORKERS \
        --save_predictions

    echo ""
    echo "MC Dropout completed! Results saved to: $MC_OUTPUT_DIR"
    echo ""
fi

# ============================================================
# Run Ensemble Uncertainty Estimation
# ============================================================

if [ "$RUN_ENSEMBLE" = true ]; then
    echo "============================================================"
    echo "Running Ensemble Uncertainty Estimation"
    echo "============================================================"

    python ensemble_uncertainty.py \
        --cfg_file "$CFG_FILE" \
        --ckpt_dir "$CHECKPOINT_DIR" \
        --data_path "$DATA_PATH" \
        --batch_size $BATCH_SIZE \
        --output_dir "$ENSEMBLE_OUTPUT_DIR" \
        --split "$SPLIT" \
        --workers $NUM_WORKERS \
        --iou_threshold 0.5

    echo ""
    echo "Ensemble completed! Results saved to: $ENSEMBLE_OUTPUT_DIR"
    echo ""
fi

# ============================================================
# Evaluate Uncertainty Estimation
# ============================================================

if [ "$RUN_EVAL" = true ]; then
    echo "============================================================"
    echo "Evaluating Uncertainty Estimation"
    echo "============================================================"

    # Evaluate MC Dropout results
    if [ -f "$MC_OUTPUT_DIR/mc_dropout_results.pkl" ] || [ "$EVAL_ONLY" = true ]; then
        echo "Evaluating MC Dropout results..."
        python evaluate_uncertainty.py \
            --result_file "$MC_OUTPUT_DIR/mc_dropout_results.pkl" \
            --gt_path "$GT_LABEL_PATH" \
            --output_dir "$EVAL_OUTPUT_DIR/mc_dropout" \
            --iou_threshold $IOU_THRESHOLD \
            --num_bins 10
        echo ""
    fi

    # Evaluate Ensemble results
    if [ -f "$ENSEMBLE_OUTPUT_DIR/ensemble_results.pkl" ] || [ "$EVAL_ONLY" = true ]; then
        echo "Evaluating Ensemble results..."
        python evaluate_uncertainty.py \
            --result_file "$ENSEMBLE_OUTPUT_DIR/ensemble_results.pkl" \
            --gt_path "$GT_LABEL_PATH" \
            --output_dir "$EVAL_OUTPUT_DIR/ensemble" \
            --iou_threshold $IOU_THRESHOLD \
            --num_bins 10
        echo ""
    fi
fi

# ============================================================
# Summary
# ============================================================

echo "============================================================"
echo "Uncertainty Estimation Pipeline Complete!"
echo "============================================================"
echo ""

if [ "$RUN_MC" = true ]; then
    echo "MC Dropout results:       $MC_OUTPUT_DIR"
    echo "MC Dropout evaluation:    $EVAL_OUTPUT_DIR/mc_dropout"
fi

if [ "$RUN_ENSEMBLE" = true ]; then
    echo "Ensemble results:         $ENSEMBLE_OUTPUT_DIR"
    echo "Ensemble evaluation:      $EVAL_OUTPUT_DIR/ensemble"
fi

echo ""
echo "Done!"
