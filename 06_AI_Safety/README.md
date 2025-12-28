# Module 06: AI Safety

How do we make AI systems we can trust?

AI-based perception introduces new safety challenges. This module covers uncertainty quantification, model calibration, and trustworthiness for ML systems in autonomous vehicles.

---

## What's in This Module

**5 notebooks covering:**
- Uncertainty types (aleatoric vs epistemic)
- Uncertainty quantification methods
- Model calibration
- Safety validation and testing
- AI safety standards

---

## Notebooks

### 1. Uncertainty Types in Deep Learning
**[15_Uncertainty_Types_in_Deep_Learning.ipynb](notebooks/15_Uncertainty_Types_in_Deep_Learning.ipynb)**

Understanding uncertainty:
- Aleatoric uncertainty: Irreducible data noise
- Epistemic uncertainty: Model uncertainty from limited training data
- Why both matter for safety
- Sources of uncertainty in AV perception
- Uncertainty visualization

### 2. MC Dropout and Ensembles
**[16_MC_Dropout_and_Ensembles.ipynb](notebooks/16_MC_Dropout_and_Ensembles.ipynb)**

Practical uncertainty quantification:
- Monte Carlo Dropout: Bayesian approximation
- Deep Ensembles: Multiple models for uncertainty
- Snapshot Ensembles: Efficient ensembling
- Prediction variance as uncertainty estimate
- Accuracy vs latency trade-offs

### 3. Calibration and Reliability
**[17_Calibration_and_Reliability.ipynb](notebooks/17_Calibration_and_Reliability.ipynb)**

Making confidence scores trustworthy:
- Expected Calibration Error (ECE)
- Reliability diagrams
- Temperature scaling: Simple calibration fix
- Isotonic regression and Platt scaling
- Why calibration matters for safety decisions

### 4. Safety Validation and Testing
**[18_Safety_Validation_and_Testing.ipynb](notebooks/18_Safety_Validation_and_Testing.ipynb)**

Uncertainty-aware validation:
- Corner case discovery via uncertainty sampling
- Active learning for efficient data collection
- Metamorphic testing for AI systems
- Coverage metrics for neural networks
- SOTIF validation with uncertainty quantification

### 5. AI Safety Standards
**[05_ai_safety_standards.ipynb](notebooks/05_ai_safety_standards.ipynb)**

Regulatory framework:
- ISO/PAS 8800: Safety and Artificial Intelligence
- ISO/IEC TR 5469: AI management system
- Trustworthiness pillars: Robustness, explainability, transparency
- Data quality requirements
- Model lifecycle management
- Integration with ISO 26262 and ISO 21448

---

## Why This Matters

**AI systems have unique safety challenges:**
- Neural networks are overconfident - predict high confidence even when wrong
- Black box problem - hard to explain decisions to regulators
- Dataset bias - models fail on underrepresented scenarios
- Distribution shift - performance degrades outside training data
- Need systematic approach to quantify and manage these risks

**Key insights:**
- Aleatoric uncertainty: "The data is noisy" (irreducible)
- Epistemic uncertainty: "The model is uncertain" (reducible with more data)
- Calibration: Making confidence scores actually mean something
- OOD detection: Knowing when to say "I don't know"

---

## Prerequisites

**Required:**
- Deep learning fundamentals (CNNs, backpropagation)
- Probability and Bayesian statistics basics
- Perception systems (Module 01)
- ISO 26262 and SOTIF (Modules 03, 04)

**Software:**
- Python 3.8+
- PyTorch or TensorFlow with Probability extensions
- NumPy, scikit-learn, Matplotlib
- Optional: netcal (calibration library)

---

## Tools Used

- **TensorFlow Probability / Pyro** - Bayesian deep learning
- **netcal** - Neural network calibration
- **Captum** - Model interpretability for PyTorch
- **SHAP** - SHapley Additive exPlanations
- **Adversarial Robustness Toolbox (ART)** - Attack/defense implementations

---

## Learning Path

**Beginner:**
1. Uncertainty types (15) - Understand the fundamentals
2. MC Dropout and Ensembles (16) - Practical methods
3. Calibration (17) - Make predictions trustworthy

**Intermediate:**
4. Safety validation (18) - Uncertainty-aware testing
5. AI safety standards (05) - Regulatory compliance

---

## Relevant Standards

- **ISO/PAS 8800** - Safety and Artificial Intelligence
- **ISO/IEC TR 5469** - AI functional safety
- **ISO 26262** - AI integration considerations
- **ISO 21448 (SOTIF)** - Performance limitations for AI
- **EU AI Act** - High-risk AI systems (AVs included)

---

## After This Module

Continue to:
- **Module 08 (Advanced Topics)** - Runtime monitoring, explainability, deployment
- **Module 02 (Failure Analysis)** - OOD detection as practical application
- **Module 04 (SOTIF)** - Apply uncertainty for unknown scenario detection

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
