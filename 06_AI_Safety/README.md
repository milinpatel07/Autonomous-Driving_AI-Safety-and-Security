# AI Safety

**Module 06: Uncertainty Quantification and Trustworthiness for Machine Learning in Autonomous Vehicles**

---

## Overview

AI safety addresses the unique challenges of deploying machine learning systems in safety-critical autonomous vehicles. Unlike traditional software with deterministic behavior, deep learning models exhibit non-deterministic predictions, dataset dependencies, and uncertainty that must be quantified and managed. This module provides comprehensive coverage of uncertainty quantification, out-of-distribution detection, model calibration, adversarial robustness, and emerging AI safety standards.

### Module Objectives

Upon completing this module, you will:

1. **Understand Uncertainty Types**: Distinguish between aleatoric (data) and epistemic (model) uncertainty
2. **Quantify Uncertainty**: Implement Bayesian deep learning, Monte Carlo Dropout, and ensemble methods
3. **Calibrate Models**: Apply temperature scaling and isotonic regression for reliable confidence estimates
4. **Detect OOD Inputs**: Identify out-of-distribution scenarios that violate training assumptions
5. **Validate AI Systems**: Apply uncertainty-aware testing and corner case discovery
6. **Apply AI Safety Standards**: Implement ISO/PAS 8800 and ISO/IEC TR 5469 requirements
7. **Ensure Explainability**: Develop interpretable models and post-hoc explanation methods
8. **Integrate with Safety Standards**: Connect AI safety to ISO 26262, ISO 21448, and ISO/SAE 21434

---

## Why AI Safety Matters

### Critical Challenges in AI for Safety-Critical Systems

**1. The Black Box Problem**
- Deep neural networks have millions to billions of parameters
- Decision-making process is opaque - difficult to explain why a prediction was made
- Regulators and safety assessors require explainability for certification
- Conflict: Most accurate models (transformers, large ensembles) are least interpretable
- ISO/PAS 8800 requires transparency and explainability for AI systems
- XAI (Explainable AI) methods: LIME, SHAP, Grad-CAM, attention visualization

**2. Aleatoric vs. Epistemic Uncertainty**
- **Aleatoric uncertainty**: Irreducible noise in data (sensor noise, measurement errors)
  - Example: Blurry image due to motion - cannot reduce through more training
  - Can be modeled but not eliminated
- **Epistemic uncertainty**: Model uncertainty due to limited training data
  - Example: Never seen snow during training - high uncertainty in snowy conditions
  - Can be reduced with more diverse training data
  - Critical for OOD detection: High epistemic uncertainty → do not trust prediction
- Safety-critical systems need both types quantified

**3. Overconfidence and Calibration**
- **Standard neural networks are overconfident**: Predict 99.9% confidence even on wrong answers
- **Calibration gap**: Predicted probability does not match actual accuracy
  - Model says "95% confident" but only correct 70% of the time
- **Expected Calibration Error (ECE)**: Measures calibration quality
- **Temperature scaling**: Post-processing to improve calibration
- SOTIF requires calibrated uncertainty for runtime decision-making

**4. Dataset Bias and Distribution Shift**
- **Training bias**: Dataset not representative of deployment environment
  - Geographic bias: Trained on California data, deployed in Germany
  - Temporal bias: Trained on 2018 data, deployed in 2024 (new vehicle types)
  - Demographic bias: Pedestrian detection fails on underrepresented groups
- **Covariate shift**: Input distribution changes (P(X) changes but P(Y|X) stable)
- **Concept drift**: Relationship between inputs and outputs changes over time
- Continuous monitoring and retraining required (ISO/PAS 8800)

**5. Adversarial Vulnerability**
- **Digital attacks**: FGSM, PGD create imperceptible perturbations that fool models
- **Physical attacks**: Adversarial patches on stop signs, road surfaces
- **Model extraction**: Querying deployed model to steal intellectual property
- **Backdoor attacks**: Training data poisoning creates hidden triggers
- Adversarial training improves robustness but reduces nominal accuracy
- Certified defenses provide provable robustness guarantees (limited to small perturbations)

**6. Runtime Monitoring Requirements**
- **ISO 21448 (SOTIF)**: Requires continuous validation and field monitoring
- **ISO 34503**: Runtime ODD compliance monitoring
- **Runtime checks**:
  - Input validation: Is sensor data within expected range?
  - Uncertainty thresholding: Is model confidence above safety threshold?
  - OOD detection: Is this scenario novel/outside training distribution?
  - Temporal consistency: Do predictions align across consecutive frames?
- **Minimum Risk Condition (MRC)**: Trigger safe state when monitoring detects anomaly

---

## Module Structure

### 📓 Notebooks

1. **[15_Uncertainty_Types_in_Deep_Learning.ipynb](notebooks/15_Uncertainty_Types_in_Deep_Learning.ipynb)**
   - Aleatoric uncertainty: Data noise and measurement errors
   - Epistemic uncertainty: Model uncertainty from limited data
   - Heteroscedastic aleatoric uncertainty: Input-dependent noise
   - Sources of uncertainty in autonomous driving perception
   - Uncertainty decomposition and analysis
   - Visualization of uncertainty maps

2. **[16_MC_Dropout_and_Ensembles.ipynb](notebooks/16_MC_Dropout_and_Ensembles.ipynb)**
   - Monte Carlo Dropout: Bayesian approximation via dropout at test time
   - Deep Ensembles: Training multiple models with different initializations
   - Snapshot Ensembles: Cyclic learning rates for efficient ensembling
   - Uncertainty estimation via prediction variance
   - Computational trade-offs: Accuracy vs. latency
   - Implementation on KITTI object detection

3. **[17_Calibration_and_Reliability.ipynb](notebooks/17_Calibration_and_Reliability.ipynb)**
   - Expected Calibration Error (ECE) and Maximum Calibration Error (MCE)
   - Reliability diagrams: Visualizing calibration quality
   - Temperature scaling: Single-parameter post-processing
   - Isotonic regression: Non-parametric calibration
   - Platt scaling for binary classifiers
   - Calibration for multi-class detection and segmentation
   - Safety implications of miscalibration

4. **[18_Safety_Validation_and_Testing.ipynb](notebooks/18_Safety_Validation_and_Testing.ipynb)**
   - Uncertainty-aware testing strategies
   - Corner case discovery via uncertainty sampling
   - Active learning for efficient data labeling
   - Metamorphic testing for AI systems
   - Coverage metrics for neural networks (neuron coverage, DeepXplore)
   - Statistical testing and hypothesis validation
   - SOTIF validation with uncertainty quantification

5. **[05_ai_safety_standards.ipynb](notebooks/05_ai_safety_standards.ipynb)**
   - ISO/PAS 8800: Road Vehicles - Safety and Artificial Intelligence
   - ISO/IEC TR 5469: AI management system
   - Trustworthiness pillars: Robustness, explainability, transparency, fairness
   - Data quality requirements and dataset documentation
   - Model lifecycle management: Training, validation, deployment, monitoring
   - Integration with ISO 26262 and ISO 21448
   - EU AI Act considerations for autonomous vehicles

---

## Prerequisites

### Knowledge
- Deep learning fundamentals (CNNs, backpropagation, optimization)
- Probability theory and Bayesian statistics
- Understanding of perception systems (Module 01)
- Familiarity with ISO 26262 and SOTIF (Modules 03, 04)

### Software
- Python 3.8+
- PyTorch 1.12+ or TensorFlow 2.8+ with Probability extensions
- Libraries: NumPy, scikit-learn, Matplotlib, netcal (calibration)
- Optional: Captum (explainability), ART (adversarial robustness)

---

## AI Safety Tools and Frameworks

- **TensorFlow Probability / Pyro**: Bayesian deep learning frameworks
- **netcal**: Neural network calibration library
- **Captum**: Model interpretability for PyTorch
- **SHAP**: SHapley Additive exPlanations
- **Alibi**: Black-box model explanations and adversarial detection
- **Adversarial Robustness Toolbox (ART)**: Attack and defense implementations

---

## Learning Path

### Beginner Path
1. Start with **15_Uncertainty_Types_in_Deep_Learning** to understand fundamentals
2. Proceed to **16_MC_Dropout_and_Ensembles** for practical uncertainty quantification
3. Learn **17_Calibration_and_Reliability** for trustworthy predictions

### Intermediate Path
4. Study **18_Safety_Validation_and_Testing** for uncertainty-aware validation
5. Understand **05_ai_safety_standards** for regulatory compliance

### Advanced Path
- Integrate with Module 02 (Failure Analysis) for adversarial robustness
- Combine with Module 04 (SOTIF) for unknown unsafe scenario detection
- Apply Module 07 (Validation & Verification) for comprehensive AI testing

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Implement MC Dropout for pedestrian detection uncertainty
2. **Exercise 2**: Train deep ensemble and compare uncertainty with single model
3. **Exercise 3**: Calibrate object detection model and measure ECE improvement
4. **Exercise 4**: Build OOD detector using epistemic uncertainty threshold
5. **Exercise 5**: Develop runtime monitoring system with uncertainty-based MRC trigger

---

## Code Examples

Located in `code/`:
- `mc_dropout.py`: Monte Carlo Dropout implementation
- `deep_ensemble.py`: Training and inference for ensembles
- `calibration.py`: Temperature scaling and ECE computation
- `ood_detection.py`: Out-of-distribution detection methods
- `explainability.py`: LIME, SHAP, Grad-CAM implementations

---

## Industry Standards and References

### Standards
- **ISO/PAS 8800**: Road Vehicles - Safety and Artificial Intelligence
- **ISO/IEC TR 5469**: Artificial Intelligence - Functional Safety and AI Systems
- **ISO 26262**: Functional Safety - AI integration considerations
- **ISO 21448 (SOTIF)**: Performance limitations for AI-based functions
- **UL 4600**: Safety for Autonomous Products - AI validation
- **EU AI Act**: High-risk AI systems (autonomous vehicles included)
- **IEEE P700x**: Standards for ethically aligned design

### Key Papers
- Gal & Ghahramani (2016): "Dropout as a Bayesian Approximation: Representing Model Uncertainty"
- Lakshminarayanan et al. (2017): "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
- Guo et al. (2017): "On Calibration of Modern Neural Networks"
- Hendrycks & Gimpel (2017): "A Baseline for Detecting Misclassified and Out-of-Distribution Examples"
- Amodei et al. (2016): "Concrete Problems in AI Safety"
- Koopman & Wagner (2018): "Toward a Framework for Highly Automated Vehicle Safety Validation"

### Resources
- [ISO/PAS 8800](https://www.iso.org/standard/83303.html)
- [EU AI Act](https://artificialintelligenceact.eu/)
- [Partnership on AI](https://partnershiponai.org/)
- [Center for AI Safety](https://www.safe.ai/)
- [Trustworthy AI Guidelines (EU)](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai)

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Distinguish between aleatoric and epistemic uncertainty
✓ Implement Monte Carlo Dropout and deep ensembles
✓ Calibrate neural networks using temperature scaling
✓ Measure calibration quality with ECE and reliability diagrams
✓ Detect out-of-distribution inputs using uncertainty
✓ Apply uncertainty-aware validation strategies
✓ Understand ISO/PAS 8800 and ISO/IEC TR 5469 requirements
✓ Integrate AI safety with ISO 26262 and SOTIF
✓ Develop runtime monitoring with uncertainty thresholds

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding AI-based perception
- **Module 03**: Functional Safety - ISO 26262 foundation
- **Module 04**: SOTIF - Performance limitations and validation

### Related Modules
- **Module 02**: Failure Analysis - OOD detection and adversarial robustness
- **Module 05**: Cybersecurity - Adversarial attacks as security threats
- **Module 07**: Validation & Verification - Uncertainty-aware testing

### Follow-up Modules
- **Module 08**: Advanced Topics - Runtime monitoring and MRC
- **Module 09**: LiDAR Technology - Uncertainty for 3D perception
- **Module 10**: Datasets & Benchmarks - Dataset bias and quality

---

## Next Steps

After completing this module:
- **Module 07**: Validation & Verification - Apply uncertainty-aware testing
- **Module 08**: Advanced Topics - Runtime ODD monitoring and explainability
- **Module 10**: Datasets & Benchmarks - Understand dataset bias implications

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
