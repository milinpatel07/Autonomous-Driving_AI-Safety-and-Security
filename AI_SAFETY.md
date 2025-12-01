<!--
Copyright (c) 2025 Milin Patel
Hochschule Kempten - University of Applied Sciences

Autonomous Driving: AI Safety and Security Workshop
This project is licensed under the MIT License.
-->

# AI Safety for Autonomous Vehicles

**Uncertainty Quantification, Trustworthiness, and Safe AI/ML Systems**

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**References:** ISO/IEC TR 5469:2024, ISO/IEC 23894:2023, NIST AI RMF

---

> **📖 Quick Start:** For workshop overview and getting started, see [README.md](README.md)
>
> **Purpose:** This document provides detailed technical reference for AI/ML safety in autonomous systems. It complements the main README with in-depth guidance on uncertainty quantification, data quality, robustness, explainability, and integration with traditional safety standards.

---

## Table of Contents

1. [Introduction](#introduction)
2. [AI Safety Principles](#ai-safety-principles)
3. [Uncertainty Quantification](#uncertainty-quantification)
4. [Data Quality and Bias](#data-quality-and-bias)
5. [Model Trustworthiness](#model-trustworthiness)
6. [Runtime Monitoring](#runtime-monitoring)
7. [Explainability and Interpretability](#explainability-and-interpretability)
8. [Continuous Learning and Model Updates](#continuous-learning-and-model-updates)
9. [Integration with Safety Standards](#integration-with-safety-standards)
10. [Practical Implementation](#practical-implementation)
11. [References](#references)

---

## Introduction

Artificial Intelligence and Machine Learning systems in autonomous vehicles present unique safety challenges beyond traditional functional safety. Neural networks are:
- **Non-deterministic:** Small input changes can cause large output changes
- **Opaque:** "Black box" decision-making processes
- **Data-dependent:** Performance depends critically on training data quality and representativeness
- **Vulnerable:** Susceptible to adversarial attacks and out-of-distribution inputs

This document provides comprehensive guidance on developing **safe AI/ML systems** for autonomous driving, integrating:
- **ISO/IEC TR 5469:2024** - Functional safety and AI systems
- **ISO/IEC 23894:2023** - AI risk management
- **ISO/IEC 42001:2023** - AI management system
- **NIST AI Risk Management Framework** (AI RMF)

---

## AI Safety Principles

### 1. Data Quality

**Principle:** AI systems are only as good as their training data

**Requirements:**
- **Representativeness:** Training data covers operational design domain (ODD)
- **Diversity:** Includes rare events, edge cases, corner cases
- **Labeling Accuracy:** Ground truth annotations are correct and consistent
- **Bias Assessment:** Dataset does not over-represent or under-represent subgroups
- **Documentation:** Data provenance, collection methodology, known limitations

**Example - Pedestrian Detection Dataset Requirements:**

| Attribute | Requirement | Validation Method |
|-----------|-------------|-------------------|
| **Sample Size** | >100,000 pedestrian instances | Count unique pedestrians |
| **Diversity (Age)** | Children: 15%, Adults: 70%, Elderly: 15% | Demographic annotation |
| **Diversity (Clothing)** | All seasons, colors, reflective materials | Attribute tagging |
| **Occlusion** | 20% partial occlusion, 5% heavy occlusion | Visibility metric |
| **Lighting** | Day: 50%, Night: 30%, Dawn/Dusk: 20% | Timestamp analysis |
| **Weather** | Clear: 60%, Rain: 25%, Fog: 10%, Snow: 5% | Metadata review |
| **Pose** | Standing: 40%, Walking: 50%, Running: 5%, Other: 5% | Action labels |
| **Annotation Quality** | Inter-annotator agreement >95% (IoU) | Multi-annotator validation |

**Data Collection Strategy:**
1. **Naturalistic driving data:** Real-world fleet deployment
2. **Targeted collection:** Deliberate capture of rare scenarios
3. **Synthetic data:** Simulation-generated images for rare events
4. **Data augmentation:** Transformations to increase diversity (rotation, brightness, noise)

### 2. Robustness

**Principle:** AI systems should maintain performance under distribution shift and perturbations

**Types of Robustness:**

#### 2.1 Natural Robustness
- **Weather variation:** Rain, fog, snow, sun glare
- **Sensor degradation:** Dirty lenses, calibration drift
- **Time of day:** Day, night, twilight
- **Geographic variation:** Different road designs, signage, driver behavior

**Testing:** Hold-out test sets from different geographic regions, weather conditions

#### 2.2 Adversarial Robustness
- **Digital attacks:** Pixel-level perturbations (FGSM, PGD, C&W)
- **Physical attacks:** Adversarial patches on stop signs, stickers on lanes

**Defenses:**
- Adversarial training (train on adversarial examples)
- Certified robustness (provable bounds on perturbation tolerance)
- Input preprocessing (JPEG compression, bit depth reduction)

#### 2.3 Out-of-Distribution (OOD) Detection
- **Distribution shift:** Test data differs from training distribution
- **Novelty detection:** Encounter objects/scenarios not in training data

**OOD Detection Methods:**

| Method | Approach | Computational Cost | Accuracy |
|--------|----------|-------------------|----------|
| **Confidence Thresholding** | Reject if max softmax <τ | Very Low | Moderate |
| **Mahalanobis Distance** | Measure distance in feature space | Low | High |
| **Energy-Based Detection** | Use energy score from logits | Very Low | High |
| **Deep Ensembles** | Measure disagreement between models | High | Very High |
| **MC Dropout** | Stochastic forward passes | Medium | High |
| **OpenMax** | Open-set recognition with EVT | Low | Moderate |

**Implementation Example (Energy-Based OOD):**

```python
def energy_score(logits, T=1.0):
    """
    Energy-based OOD detection (Liu et al. 2020)
    Lower energy = more in-distribution
    """
    return -T * torch.logsumexp(logits / T, dim=1)

def is_ood(logits, threshold=-10.0):
    E = energy_score(logits)
    return E > threshold  # High energy = OOD
```

### 3. Uncertainty Awareness

**Principle:** AI systems should quantify and communicate uncertainty in predictions

**Uncertainty Types:**

#### Aleatoric Uncertainty (Data Uncertainty)
- **Definition:** Irreducible uncertainty from noisy observations
- **Sources:** Sensor noise, occlusions, ambiguous situations
- **Estimation:** Learn variance in neural network output

**Example:** Object is partially occluded by tree → inherent ambiguity in exact position

#### Epistemic Uncertainty (Model Uncertainty)
- **Definition:** Reducible uncertainty from lack of knowledge
- **Sources:** Insufficient training data, model capacity limitations
- **Estimation:** Bayesian inference, ensembles, dropout

**Example:** Model has never seen a horse-drawn carriage → high epistemic uncertainty

**Mathematical Formulation:**

For a classification task:

```
Total Uncertainty = Aleatoric Uncertainty + Epistemic Uncertainty

H[y|x] = E_p(w|D) [H[y|x,w]] + H[E_p(w|D)[y|x,w]]
  ↑              ↑                    ↑
Total        Aleatoric           Epistemic
```

Where:
- `y`: output class
- `x`: input data
- `w`: model weights
- `D`: training dataset
- `H[·]`: entropy (measure of uncertainty)

### 4. Fail-Safe Mechanisms

**Principle:** AI systems should degrade gracefully when confidence is low

**Graceful Degradation Strategies:**

| Scenario | Detection | Response |
|----------|-----------|----------|
| **Low Confidence Detection** | Object confidence <50% | Conservative assumption: treat as obstacle, slow down |
| **OOD Input** | Energy score >threshold | Alert safety driver, request takeover |
| **Sensor Failure** | No valid sensor data | Transition to Minimal Risk Condition (MRC) |
| **High Uncertainty** | Epistemic uncertainty >τ | Reduce speed, increase following distance |
| **Contradictory Sensors** | Camera says "clear", LiDAR says "obstacle" | Trust more reliable sensor (LiDAR for presence) |

**Minimal Risk Condition (MRC):**
- Bring vehicle to complete stop
- Activate hazard lights
- Move to shoulder if possible
- Alert occupants and remote operator

---

## Uncertainty Quantification

### Methods for Uncertainty Estimation

#### 1. Bayesian Neural Networks (BNNs)

**Concept:** Treat network weights as probability distributions, not point estimates

**Advantages:**
- Principled Bayesian framework
- Natural uncertainty quantification

**Disadvantages:**
- Computationally expensive
- Difficult to train (approximate inference required)

**Implementation:**
- Variational inference (mean-field approximation)
- Markov Chain Monte Carlo (MCMC) sampling

#### 2. Monte Carlo Dropout (MC Dropout)

**Concept:** Apply dropout at test time, run multiple stochastic forward passes

**Algorithm:**
```python
def mc_dropout_predict(model, x, n_samples=30):
    """
    MC Dropout uncertainty estimation

    Args:
        model: Neural network with dropout layers
        x: Input data
        n_samples: Number of stochastic forward passes

    Returns:
        mean_prediction: Average prediction
        uncertainty: Standard deviation (epistemic)
    """
    model.train()  # Enable dropout at test time

    predictions = []
    for _ in range(n_samples):
        with torch.no_grad():
            pred = torch.softmax(model(x), dim=1)
            predictions.append(pred)

    predictions = torch.stack(predictions)  # [n_samples, batch, classes]

    mean_prediction = predictions.mean(dim=0)
    uncertainty = predictions.std(dim=0)

    return mean_prediction, uncertainty
```

**Advantages:**
- Easy to implement (minimal code changes)
- Moderate computational cost (parallelizable)

**Disadvantages:**
- Only estimates epistemic uncertainty
- Requires careful dropout rate tuning

**Recommended for:** Real-time AV perception systems

#### 3. Deep Ensembles

**Concept:** Train multiple neural networks independently, aggregate predictions

**Algorithm:**
```python
class DeepEnsemble:
    def __init__(self, models):
        """
        models: List of independently trained neural networks
        """
        self.models = models

    def predict(self, x):
        """
        Ensemble prediction with uncertainty
        """
        predictions = []
        for model in self.models:
            with torch.no_grad():
                pred = torch.softmax(model(x), dim=1)
                predictions.append(pred)

        predictions = torch.stack(predictions)  # [n_models, batch, classes]

        mean_prediction = predictions.mean(dim=0)
        epistemic_uncertainty = predictions.std(dim=0)

        return mean_prediction, epistemic_uncertainty
```

**Advantages:**
- State-of-the-art uncertainty estimation
- Captures model diversity
- No architectural changes needed

**Disadvantages:**
- High computational cost (training and inference)
- Memory overhead (multiple models)

**Recommended for:** High-integrity perception (ASIL C/D)

#### 4. Evidential Deep Learning

**Concept:** Predict parameters of a higher-order distribution (e.g., Dirichlet) over class probabilities

**Advantages:**
- Single forward pass (efficient)
- Directly estimates uncertainty without sampling

**Disadvantages:**
- Requires custom loss functions
- Less mature than MC Dropout and Ensembles

**Reference:** Sensoy et al. (2018) - "Evidential Deep Learning to Quantify Classification Uncertainty"

### Calibration

**Calibration:** Alignment between predicted confidence and actual accuracy

**Well-Calibrated Model:** If model predicts 80% confidence, it should be correct 80% of the time

**Reliability Diagram:** Visualize calibration

```
Accuracy
   ↑
1.0│     ╱ Perfect calibration
   │    ╱
   │   ╱  ○ ○
   │  ╱ ○     ○
   │ ╱○         ○ (Actual model)
0.5│╱
   │
   └────────────────────────> Confidence
    0.5                 1.0
```

**Expected Calibration Error (ECE):**

```
ECE = Σ (|confidence - accuracy|) × (samples in bin) / (total samples)
```

**Post-hoc Calibration Methods:**

1. **Temperature Scaling**
   - Divide logits by scalar temperature T before softmax
   - Optimize T on validation set to minimize NLL
   - Single parameter, preserves accuracy, improves calibration

2. **Platt Scaling**
   - Fit logistic regression on top of classifier outputs
   - More flexible than temperature scaling

3. **Isotonic Regression**
   - Non-parametric calibration method
   - Fits monotonic function

**Implementation (Temperature Scaling):**

```python
class TemperatureScaling(nn.Module):
    def __init__(self):
        super().__init__()
        self.temperature = nn.Parameter(torch.ones(1) * 1.5)

    def forward(self, logits):
        return logits / self.temperature

def calibrate(model, val_loader):
    """
    Calibrate model using temperature scaling
    """
    temp_model = TemperatureScaling()
    optimizer = torch.optim.LBFGS([temp_model.temperature], lr=0.01)

    def closure():
        optimizer.zero_grad()
        loss = 0
        for x, y in val_loader:
            logits = model(x)
            scaled_logits = temp_model(logits)
            loss += F.cross_entropy(scaled_logits, y)
        loss.backward()
        return loss

    optimizer.step(closure)

    return temp_model.temperature.item()
```

---

## Data Quality and Bias

### Dataset Bias Assessment

**Types of Bias:**

1. **Selection Bias:** Training data not representative of deployment
   - Example: Trained on California highways, deployed in Boston urban

2. **Label Bias:** Annotators systematically mislabel certain subgroups
   - Example: Annotators miss pedestrians in dark clothing at night

3. **Measurement Bias:** Sensors have different accuracy for subgroups
   - Example: Radar cross-section varies with vehicle size

4. **Temporal Bias:** World changes over time, training data becomes stale
   - Example: New vehicle models, updated road signs

**Bias Mitigation Strategies:**

1. **Diverse Data Collection:** Explicitly target underrepresented scenarios
2. **Re-sampling:** Oversample minority classes during training
3. **Domain Adaptation:** Fine-tune models on target deployment region
4. **Fairness Constraints:** Enforce similar performance across subgroups
5. **Continuous Monitoring:** Track performance metrics by demographic/scenario

### Data Augmentation for Robustness

**Geometric Augmentations:**
- Rotation (±5°)
- Scaling (0.9×-1.1×)
- Translation (±10% of image)
- Flipping (horizontal only for symmetric objects)

**Photometric Augmentations:**
- Brightness adjustment (±20%)
- Contrast adjustment (0.8×-1.2×)
- Saturation adjustment (0.8×-1.2×)
- Hue shift (±10°)

**Advanced Augmentations:**
- Cutout / Random Erasing (simulate occlusions)
- MixUp (blend two images)
- AutoAugment (learned augmentation policies)

**Weather Simulation:**
- Rain rendering (droplets, wet road)
- Fog simulation (depth-based attenuation)
- Snow overlay (falling snow, accumulated snow)

---

## Model Trustworthiness

### Trustworthiness Attributes (ISO/IEC TR 5469)

1. **Accuracy:** Correct predictions on representative data
2. **Robustness:** Resilience to input perturbations and distribution shift
3. **Reliability:** Consistent performance over time and conditions
4. **Explainability:** Ability to explain predictions
5. **Transparency:** Documented model architecture, training process
6. **Privacy:** Protection of sensitive data
7. **Fairness:** Equitable performance across subgroups
8. **Accountability:** Clear assignment of responsibility

### Model Documentation (Model Cards)

**Model Card Contents:**
- **Model Details:** Architecture, training data, hyperparameters
- **Intended Use:** ODD, recommended operating conditions
- **Performance:** Accuracy, precision, recall on test sets
- **Limitations:** Known failure modes, OOD scenarios
- **Trade-offs:** Speed vs. accuracy, robustness vs. performance
- **Ethical Considerations:** Bias assessment, fairness analysis

**Example Model Card (Pedestrian Detection):**

```markdown
# Model Card: Pedestrian Detection YOLOv8

## Model Details
- Architecture: YOLOv8-large
- Parameters: 43.7M
- Training Data: Custom dataset, 150K pedestrian instances
- Training Duration: 72 hours on 8× NVIDIA A100

## Intended Use
- Application: Autonomous vehicle perception
- ODD: Urban and highway, 0-130 km/h, day/night
- Not intended for: Off-road, unpaved roads

## Performance
- Precision: 96.2% @ IoU 0.5
- Recall: 98.5% @ IoU 0.5
- Inference Time: 18ms (55 FPS) on NVIDIA Drive AGX

## Limitations
- Reduced recall in heavy rain (<90%)
- Struggles with heavily occluded pedestrians (>70% occluded)
- False positives on pedestrian-shaped shadows

## Fairness
- Children detection: 97.8% recall (vs. 98.5% adult)
- Dark clothing: 97.1% recall (vs. 98.9% light clothing)
```

---

## Runtime Monitoring

### Anomaly Detection

**Purpose:** Detect inputs or behaviors that indicate potential safety issues

**Monitoring Dimensions:**

1. **Input Monitoring**
   - Sensor health (self-test, diagnostics)
   - Input distribution shift (detect OOD)
   - Adversarial input detection

2. **Output Monitoring**
   - Prediction confidence (reject low-confidence outputs)
   - Output plausibility (range checks, physics constraints)
   - Temporal consistency (smooth trajectories)

3. **Cross-Modal Consistency**
   - Camera vs. LiDAR agreement
   - Radar velocity vs. optical flow

**Example: Temporal Consistency Check**

```python
class TemporalConsistencyMonitor:
    def __init__(self, max_delta_position=2.0, max_delta_velocity=5.0):
        """
        Monitor object tracks for sudden jumps (potential errors)

        Args:
            max_delta_position: Max position change (m) between frames
            max_delta_velocity: Max velocity change (m/s) between frames
        """
        self.max_delta_position = max_delta_position
        self.max_delta_velocity = max_delta_velocity
        self.prev_objects = {}

    def check(self, current_objects, dt=0.1):
        """
        Check if object tracks are temporally consistent

        Returns:
            List of anomalous object IDs
        """
        anomalies = []

        for obj_id, obj in current_objects.items():
            if obj_id in self.prev_objects:
                prev = self.prev_objects[obj_id]

                # Check position jump
                delta_pos = np.linalg.norm(obj.position - prev.position)
                if delta_pos > self.max_delta_position:
                    anomalies.append((obj_id, 'position_jump', delta_pos))

                # Check velocity jump
                delta_vel = np.linalg.norm(obj.velocity - prev.velocity)
                if delta_vel > self.max_delta_velocity:
                    anomalies.append((obj_id, 'velocity_jump', delta_vel))

        self.prev_objects = current_objects.copy()

        return anomalies
```

### Safety Performance Indicators (SPI)

**Real-time Metrics:**

| Metric | Threshold | Action if Violated |
|--------|-----------|-------------------|
| **Detection Recall** | >95% (on validation buffer) | Alert safety driver |
| **False Positive Rate** | <0.1 per km | Log for offline analysis |
| **OOD Detection Rate** | <1% of frames | Acceptable, but monitor trend |
| **Average Confidence** | >80% | If drops below, reduce speed |
| **Sensor Disagreement** | <5% of detections | Investigate sensor calibration |

---

## Explainability and Interpretability

### Explainability Methods for Perception

**Goal:** Understand which input features drive predictions

#### 1. Gradient-Based Methods

**Grad-CAM (Gradient-weighted Class Activation Mapping):**
- Visualizes which regions of image influenced prediction
- Backpropagates gradient to convolutional layer, creates heatmap

**Implementation Sketch:**
```python
def grad_cam(model, image, target_class):
    """
    Compute Grad-CAM heatmap
    """
    # Forward pass
    features, output = model(image, return_features=True)

    # Backward pass
    model.zero_grad()
    output[target_class].backward()

    # Grad-CAM computation
    gradients = model.get_gradients()  # dY/dF
    weights = gradients.mean(dim=[2, 3], keepdim=True)  # Global average pooling
    cam = (weights * features).sum(dim=1, keepdim=True)  # Weighted sum
    cam = F.relu(cam)  # ReLU (only positive influences)

    return cam
```

**Output:** Heatmap showing which pixels contributed to prediction

#### 2. Attention Mechanisms

**Self-Attention (Transformers):**
- Attention weights show which input tokens model "attended to"
- Useful for multi-modal fusion (camera + LiDAR)

#### 3. Counterfactual Explanations

**Concept:** What minimal change to input would change prediction?

**Example:** "If traffic light was green instead of red, car would proceed"

### Interpretability for Safety

**Use Cases:**
1. **Failure Analysis:** Understand why model failed in incident
2. **Validation:** Verify model uses correct features (not shortcuts)
3. **Trust Building:** Explain decisions to regulators, users

**Caution:** Explanations can be misleading (rationalization ≠ ground truth reasoning)

---

## Continuous Learning and Model Updates

### Model Update Strategies

**Challenge:** Real-world distribution changes over time (new vehicle models, road infrastructure updates, weather patterns)

**Approaches:**

#### 1. Periodic Retraining
- Schedule: Quarterly or annually
- Trigger: Accumulated data from fleet
- Process: Retrain from scratch or fine-tune

#### 2. Continual Learning
- Online learning with new data
- Mitigate catastrophic forgetting (old knowledge lost)
- Techniques: Elastic Weight Consolidation (EWC), rehearsal buffers

#### 3. Active Learning
- Identify most informative samples for labeling
- Strategies: Uncertainty sampling, diversity sampling
- Reduces labeling cost

### Over-the-Air (OTA) Model Updates

**Safety Considerations:**

1. **Validation Before Deployment:**
   - New model tested on comprehensive test suite
   - Performance non-degradation guarantee
   - Shadow mode: run new model in parallel, compare outputs

2. **Gradual Rollout:**
   - Deploy to small percentage of fleet initially (e.g., 1%)
   - Monitor performance metrics
   - Expand rollout if metrics acceptable

3. **Rollback Capability:**
   - If new model underperforms, revert to previous version
   - A/B partition for firmware redundancy

4. **Traceability:**
   - Log which model version was active during any incident
   - Version control for models, data, training code

---

## Integration with Safety Standards

### ISO 26262 Integration

**ML-specific Considerations for ISO 26262:**

1. **Non-Determinism:**
   - Traditional software: output deterministic given input
   - Neural networks: stochastic training, sensitive to initialization
   - **Mitigation:** Diverse models (ensembles), uncertainty quantification

2. **Requirements Coverage:**
   - Traditional: test cases cover requirements
   - ML: test cases cannot cover entire input space
   - **Mitigation:** Scenario-based testing, statistical evidence

3. **Verification Challenges:**
   - Cannot formally prove correctness of neural networks
   - **Mitigation:** Extensive testing, certified robustness bounds

**ISO 26262 Adaptations:**
- Safety mechanisms: OOD detection, uncertainty thresholding
- Diversity: Camera + LiDAR, multiple neural architectures
- Runtime monitoring: Input/output plausibility checks

### ISO 21448 (SOTIF) Integration

**ML Performance Limitations:**
- Neural networks have inherent error rate (not 100% accurate)
- Triggering conditions: rare scenarios, distribution shift

**SOTIF Process for ML:**

1. **Identify Known Limitations:**
   - Test model on diverse scenarios
   - Document failure modes (e.g., "fails on heavily occluded pedestrians")

2. **Discover Unknown Limitations:**
   - Adversarial testing, corner case generation
   - Field data analysis (disengagements, near-misses)

3. **Mitigate Limitations:**
   - Multi-sensor fusion
   - Conservative assumptions when uncertain
   - Human oversight in safety driver mode

4. **Validation:**
   - Extensive testing: millions of km
   - Statistical confidence in residual risk

---

## Practical Implementation

### End-to-End AI Safety Pipeline

**Phase 1: Data & Training**
```
Data Collection → Data Quality → Bias Assessment
       ↓              ↓              ↓
   Labeling    → Validation   → Diverse Sampling
       ↓              ↓              ↓
  Training    → Regularization → Uncertainty Est.
```

**Phase 2: Validation**
```
Test Suite → Scenario Coverage → Adversarial Testing
     ↓              ↓                  ↓
  OOD Test → Calibration → Robustness Metrics
     ↓              ↓                  ↓
 Safety Case → Documentation → Approval
```

**Phase 3: Deployment**
```
Shadow Mode → Gradual Rollout → Monitoring
     ↓              ↓              ↓
 Validation → Performance → Anomaly Detection
     ↓              ↓              ↓
Full Deploy → OTA Updates → Continuous Learning
```

### Checklist for Safe AI in AVs

- [ ] **Data:** Representative, diverse, bias-assessed, documented
- [ ] **Training:** Regularization, data augmentation, uncertainty estimation
- [ ] **Validation:** >99% recall on safety-critical classes, tested on edge cases
- [ ] **Calibration:** ECE <5%, reliability diagram shows good calibration
- [ ] **OOD Detection:** Implemented and tested, false positive rate <1%
- [ ] **Uncertainty:** Quantified (MC Dropout or Ensemble), thresholds defined
- [ ] **Robustness:** Adversarial training, tested on physical perturbations
- [ ] **Monitoring:** Runtime anomaly detection, safety performance indicators
- [ ] **Explainability:** Failure analysis tools (Grad-CAM, attention visualization)
- [ ] **Documentation:** Model cards, safety case, traceability
- [ ] **Fallback:** Graceful degradation, Minimal Risk Condition defined
- [ ] **Updates:** OTA mechanism, validation pipeline, rollback capability

---

## References

### Standards and Guidelines

- **ISO/IEC TR 5469:2024** - Artificial intelligence — Functional safety and AI systems
- **ISO/IEC 23894:2023** - Information technology — AI — Guidance on risk management
- **ISO/IEC 42001:2023** - AI management system
- **NIST AI Risk Management Framework** (AI RMF 1.0, January 2023)
- **EU AI Act** (Regulation on Artificial Intelligence, 2024)

### Academic Papers

#### Uncertainty Quantification
- Gal & Ghahramani (2016): "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"
- Kendall & Gal (2017): "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
- Lakshminarayanan et al. (2017): "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"

#### Calibration
- Guo et al. (2017): "On Calibration of Modern Neural Networks"
- Kuleshov et al. (2018): "Accurate Uncertainties for Deep Learning Using Calibrated Regression"

#### OOD Detection
- Hendrycks & Gimpel (2017): "A Baseline for Detecting Misclassified and Out-of-Distribution Examples"
- Liu et al. (2020): "Energy-based Out-of-distribution Detection"
- Liang et al. (2018): "Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks"

#### Adversarial Robustness
- Goodfellow et al. (2015): "Explaining and Harnessing Adversarial Examples" (FGSM)
- Madry et al. (2018): "Towards Deep Learning Models Resistant to Adversarial Attacks" (PGD)
- Eykholt et al. (2018): "Robust Physical-World Attacks on Deep Learning Visual Classification" (Physical adversarial)

#### Explainability
- Selvaraju et al. (2017): "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"
- Lundberg & Lee (2017): "A Unified Approach to Interpreting Model Predictions" (SHAP)

### Books

- **"Bayesian Deep Learning"** by Andrew Gordon Wilson (in progress)
- **"Probabilistic Machine Learning: Advanced Topics"** by Kevin Murphy (2023)
- **"Trustworthy Machine Learning"** by Kush R. Varshney (2022)
- **"Artificial Intelligence Safety and Security"** by Roman V. Yampolskiy (2018)

### Tools and Libraries

- **Uncertainty Toolbox:** Python library for uncertainty quantification metrics
- **Evidential Deep Learning:** TensorFlow implementation
- **Captum:** PyTorch library for model interpretability
- **Alibi:** Python library for explainability and confidence estimation

---

**Document Version:** 1.0
**Last Updated:** 2025-01-18
**Author:** Milin Patel
**License:** MIT

---

*This document is part of the comprehensive Autonomous Driving: AI, Safety, and Security Workshop. For functional safety, see [SAFETY.md](SAFETY.md). For cybersecurity, see [SECURITY.md](SECURITY.md).*
