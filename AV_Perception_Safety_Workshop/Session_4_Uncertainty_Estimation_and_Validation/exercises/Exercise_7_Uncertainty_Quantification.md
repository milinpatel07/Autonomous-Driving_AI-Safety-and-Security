# Exercise 7: Uncertainty Quantification for AV Perception

**Session 4: Uncertainty Estimation and Validation**
**Duration:** 60 minutes
**Difficulty:** Advanced

## Objectives

By the end of this exercise, you will:
- Implement MC Dropout for a real object detection model (YOLOv8)
- Compare MC Dropout with Deep Ensembles
- Analyze uncertainty on out-of-distribution examples
- Design uncertainty-aware decision logic for AVs
- Connect uncertainty quantification to ISO 21448 (SOTIF)

---

## Prerequisites

- Completed Sessions 1-3 of the workshop
- Familiarity with PyTorch and object detection
- Understanding of Notebooks 15-16 from Session 4

---

## Part 1: Implement MC Dropout for YOLOv8 (20 min)

### Task 1.1: Setup

Download a pre-trained YOLOv8 model and prepare test data:

```python
# Install dependencies
!pip install ultralytics torch torchvision

from ultralytics import YOLO
import torch
import numpy as np
import matplotlib.pyplot as plt

# Load pre-trained YOLOv8
model = YOLO('yolov8n.pt')  # Nano model for speed

# Get sample images
# Use COCO val dataset or your own AV dataset
```

### Task 1.2: Add Dropout to YOLOv8

**Challenge:** YOLOv8 doesn't have dropout by default. You need to add it!

**Options:**
1. **Add dropout layers** to the model architecture
2. **Use DropBlock** (better for conv nets)
3. **Implement approximate dropout** using other stochastic regularization

**Your task:**
- Modify the YOLOv8 backbone to include dropout layers
- OR implement a wrapper that applies stochastic forward passes
- Verify dropout is active during inference

```python
class MCDropoutWrapper:
    """
    Wrapper to enable MC Dropout for YOLOv8.

    TODO: Implement this class!
    """

    def __init__(self, model, dropout_rate=0.2, n_samples=30):
        # Your code here
        pass

    def predict_with_uncertainty(self, image):
        """
        Run multiple forward passes with dropout.

        Returns:
            detections: List of detections
            uncertainty: Uncertainty estimates for each detection
        """
        # Your code here
        pass
```

### Task 1.3: Visualize Uncertainty

Create visualizations showing:
- Bounding boxes with uncertainty as color/thickness
- Scatter plot: confidence vs epistemic uncertainty
- Examples where uncertainty is HIGH (these are interesting!)

**Expected output:**
- Image with color-coded boxes (green=certain, red=uncertain)
- Quantitative uncertainty metrics per detection

---

## Part 2: Build Deep Ensemble (15 min)

### Task 2.1: Train Ensemble Members

You have two options:

**Option A (Fast):** Download multiple pre-trained YOLOv8 variants
```python
models = [
    YOLO('yolov8n.pt'),   # Nano
    YOLO('yolov8s.pt'),   # Small
    YOLO('yolov8m.pt'),   # Medium
]
```

**Option B (Better):** Fine-tune same model with different seeds
```python
# Fine-tune on subset of data with different initializations
for seed in [42, 123, 456, 789, 101]:
    model = YOLO('yolov8n.pt')
    # Fine-tune with this seed...
```

### Task 2.2: Ensemble Predictions

Implement ensemble inference:

```python
class YOLOEnsemble:
    """
    Deep Ensemble for YOLOv8.

    TODO: Implement this class!
    """

    def __init__(self, models):
        self.models = models

    def predict_with_uncertainty(self, image, iou_threshold=0.5):
        """
        Get ensemble predictions with uncertainty.

        Challenge: How do you match detections across models?
        - Different models might predict different numbers of boxes
        - Need to associate corresponding detections (use IoU)

        Returns:
            detections: Consensus detections
            uncertainty: Per-detection uncertainty
        """
        # Your code here
        pass
```

**Key challenge:** Matching detections across models!
- Use IoU (Intersection over Union) to match boxes
- Compute variance of matched predictions
- Handle cases where models disagree on object existence

---

## Part 3: Out-of-Distribution Analysis (15 min)

### Task 3.1: Create OOD Dataset

Collect or generate OOD images:

**Examples of OOD for AV perception:**
- Unusual weather (heavy snow, sandstorm)
- Rare objects (animals, construction equipment)
- Adversarial perturbations
- Corrupted images (blur, noise, occlusion)

**Datasets you can use:**
- COCO-C (COCO with corruptions)
- ImageNet-C corruptions applied to COCO
- Your own synthetic corruptions

```python
def create_ood_dataset():
    """
    Create OOD examples.

    TODO: Implement corruptions!
    """
    # Ideas:
    # 1. Gaussian noise
    # 2. Motion blur
    # 3. Weather simulation (fog, rain)
    # 4. Occlusion (random boxes)
    # 5. Brightness/contrast changes
    pass
```

### Task 3.2: Analyze Uncertainty on OOD

**Hypothesis:** Uncertainty should be HIGHER on OOD examples.

Test this:
```python
# Run both MC Dropout and Ensemble on:
# 1. In-distribution data (normal COCO images)
# 2. OOD data (corrupted images)

# Compare:
# - Mean epistemic uncertainty
# - Detection confidence
# - Number of detections
# - Uncertainty distributions
```

**Questions to answer:**
1. Is epistemic uncertainty higher on OOD data? By how much?
2. Does MC Dropout or Ensemble better detect OOD?
3. Can you set a threshold to flag OOD scenarios?
4. What false positive/negative rate do you get?

---

## Part 4: Uncertainty-Aware Decision Logic (10 min)

### Task 4.1: Design Decision Rules

Implement uncertainty-aware logic for AV decisions:

```python
class UncertaintyAwareAV:
    """
    AV decision module using uncertainty.

    TODO: Implement decision logic!
    """

    def __init__(self,
                 confidence_threshold=0.8,
                 epistemic_threshold=0.15,
                 safety_margin=1.5):
        self.confidence_threshold = confidence_threshold
        self.epistemic_threshold = epistemic_threshold
        self.safety_margin = safety_margin

    def make_decision(self, detections, uncertainties):
        """
        Make driving decision based on detections and uncertainty.

        Decision zones:
        1. NORMAL: High confidence, low uncertainty → normal operation
        2. CAUTION: Moderate uncertainty → slow down, increase margins
        3. FALLBACK: High uncertainty → activate fallback, request takeover
        4. STOP: Very high uncertainty → minimal risk condition

        Args:
            detections: List of object detections
            uncertainties: Uncertainty for each detection

        Returns:
            action: One of ['NORMAL', 'CAUTION', 'FALLBACK', 'STOP']
            reason: Explanation for decision
        """
        # Your code here
        # Consider:
        # - Pedestrians (high safety priority)
        # - Distance to objects
        # - Epistemic vs aleatoric uncertainty
        # - Multiple uncertain objects
        pass
```

### Task 4.2: Test Decision Logic

Create test scenarios and verify your logic:

```python
# Test cases:
# 1. Clear day, confident pedestrian detection → NORMAL
# 2. Rain, moderate uncertainty → CAUTION
# 3. Unknown object, high epistemic uncertainty → FALLBACK
# 4. Complete sensor failure → STOP

# For each case:
# - Simulate the scenario
# - Run decision logic
# - Verify correct action
```

---

## Part 5: Connect to SOTIF (ISO 21448) (10 min)

### Task 5.1: SOTIF Scenario Classification

Map your uncertainty findings to SOTIF framework:

**Create a table:**

| Scenario | Uncertainty | SOTIF Classification | Mitigation |
|----------|-------------|---------------------|------------|
| Clear day, normal traffic | Low | Known Safe | Normal operation |
| Rain, pedestrian crossing | Medium | Known Unsafe (manageable) | Reduce speed, increase safety margin |
| Heavy fog, low visibility | High aleatoric | Known Unsafe (limits) | Activate fallback system |
| Unknown object type | High epistemic | Unknown Unsafe | Stop/Minimal risk condition |

**Your task:**
1. Add 5-10 real scenarios from your testing
2. Classify each using SOTIF categories
3. Define mitigation strategy based on uncertainty

### Task 5.2: Define ODD Boundaries

Use uncertainty to define Operational Design Domain:

```python
class ODDValidator:
    """
    Validate if current scenario is within ODD using uncertainty.

    TODO: Implement this!
    """

    def __init__(self):
        # Define ODD boundaries
        self.max_epistemic_uncertainty = 0.25
        self.max_ood_probability = 0.15
        self.min_detection_confidence = 0.70

    def is_within_odd(self, detections, uncertainties, conditions):
        """
        Check if current scenario is within ODD.

        Returns:
            within_odd: Boolean
            limiting_factor: What constraint is violated (if any)
            confidence: How close to ODD boundary (0-1)
        """
        # Your code here
        pass
```

**Deliverable:** Document showing:
- ODD definition with uncertainty-based boundaries
- How uncertainty monitoring enforces ODD
- Fallback strategy when leaving ODD

---

## Submission Requirements

### Code Deliverables

1. **`mc_dropout_yolo.py`**: MC Dropout implementation
2. **`ensemble_yolo.py`**: Deep Ensemble implementation
3. **`ood_analysis.ipynb`**: Jupyter notebook with OOD analysis
4. **`decision_logic.py`**: Uncertainty-aware decision module
5. **`odd_validator.py`**: ODD validation using uncertainty

### Report (2-3 pages)

Include:

1. **Implementation Summary:**
   - How you added dropout to YOLOv8
   - Ensemble training/inference strategy
   - Challenges faced and solutions

2. **Quantitative Results:**
   - MC Dropout vs Ensemble comparison table
   - OOD detection performance (ROC curve, threshold analysis)
   - Computational costs (inference time, memory)

3. **Uncertainty Analysis:**
   - Example images with high/low uncertainty
   - Uncertainty distributions (in-dist vs OOD)
   - Correlation between uncertainty and detection errors

4. **SOTIF Integration:**
   - SOTIF scenario classification table
   - ODD definition with uncertainty boundaries
   - Fallback strategy explanation

5. **Safety Argument:**
   - How uncertainty quantification improves safety
   - Limitations and residual risks
   - Recommendations for production deployment

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Implementation** | 30 | MC Dropout and Ensemble correctly implemented |
| **OOD Detection** | 20 | Effective OOD detection using uncertainty |
| **Decision Logic** | 20 | Well-designed uncertainty-aware decisions |
| **SOTIF Integration** | 15 | Clear connection to ISO 21448 |
| **Analysis Quality** | 10 | Thorough experimentation and insights |
| **Code Quality** | 5 | Clean, documented, reproducible |
| **Total** | 100 | |

---

## Bonus Challenges (Optional)

### Bonus 1: Bayesian YOLOv8 (+10 points)
- Implement true Bayesian inference (variational or MCMC)
- Compare with MC Dropout

### Bonus 2: Real-time Uncertainty (+10 points)
- Optimize for real-time inference (<100ms)
- Trade-off analysis: speed vs uncertainty quality

### Bonus 3: Temporal Uncertainty (+10 points)
- Track uncertainty over video sequences
- Detect uncertainty trends (increasing = leaving ODD)

### Bonus 4: Multi-Sensor Fusion (+15 points)
- Combine uncertainty from camera + LiDAR
- Does fusion reduce uncertainty?

---

## Resources

### Papers
- Gal & Ghahramani (2016): "Dropout as a Bayesian Approximation"
- Kendall & Gal (2017): "What Uncertainties Do We Need in Bayesian Deep Learning?"
- Lakshminarayanan et al. (2017): "Simple and Scalable Predictive Uncertainty Estimation"
- Miller et al. (2019): "Evaluating Model Robustness and Uncertainty for AV"

### Code Examples
- Uncertainty Toolbox: https://github.com/uncertainty-toolbox/uncertainty-toolbox
- YOLOv8 docs: https://docs.ultralytics.com/

### Standards
- ISO 21448 (SOTIF): Safety of the Intended Functionality
- ISO 26262 Part 8: Validation

---

## Tips for Success

1. **Start Simple:** Get basic MC Dropout working before optimizing
2. **Visualize Early:** Plot uncertainty distributions frequently
3. **Sanity Checks:** Uncertainty should be higher on difficult examples
4. **Test Edge Cases:** Focus on scenarios where model struggles
5. **Think Safety:** Always ask "How does this improve safety?"

Good luck! Remember: **Uncertainty estimation is not just academic - it's essential for safe AVs!**
