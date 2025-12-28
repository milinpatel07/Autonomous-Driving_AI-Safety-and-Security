# Module 02: Failure Analysis

What can go wrong and why do perception systems fail?

Understanding failures is critical for building safe autonomous vehicles. This module analyzes real-world incidents, edge cases, and adversarial attacks.

---

## What's in This Module

**4 notebooks covering:**
- Real-world autonomous vehicle incidents
- Out-of-distribution detection
- Corner cases and edge cases
- Adversarial attacks on perception systems

---

## Notebooks

### 1. AV Failure Case Studies
**[07_AV_Failure_Case_Studies.ipynb](notebooks/07_AV_Failure_Case_Studies.ipynb)**

Learn from real-world incidents:
- Uber ATG Tempe (2018): Pedestrian detection failure
- Tesla Autopilot crashes: Camera limitations
- Waymo disengagements: Root cause analysis
- NTSB investigation reports
- Lessons learned

### 2. Out-of-Distribution Detection
**[08_OOD_Detection.ipynb](notebooks/08_OOD_Detection.ipynb)**

Detect when your model sees something new:
- Statistical methods (Mahalanobis distance, KNN)
- Deep learning approaches (ODIN, energy-based models)
- Bayesian uncertainty (epistemic vs aleatoric)
- Ensemble disagreement and MC Dropout
- Benchmark datasets: KITTI-C, nuScenes-OOD

### 3. Corner Cases and Edge Cases
**[09_Corner_Cases_and_Edge_Cases.ipynb](notebooks/09_Corner_Cases_and_Edge_Cases.ipynb)**

The long-tail problem:
- Definition and taxonomy
- Rare objects: emergency vehicles, animals, construction equipment
- Unusual weather: fog, snow, heavy rain
- Infrastructure anomalies: missing lane markings, roadwork
- Scenario generation for testing
- PEGASUS methodology

### 4. Adversarial Attacks on Perception
**[10_Adversarial_Attacks_on_Perception.ipynb](notebooks/10_Adversarial_Attacks_on_Perception.ipynb)**

Security vulnerabilities:
- Digital attacks: FGSM, PGD, C&W
- Physical attacks: adversarial patches on stop signs
- Sensor-specific attacks: camera, LiDAR spoofing, radar jamming
- Attack detection mechanisms
- Adversarial training and certified defenses
- ISO/SAE 21434 cybersecurity integration

---

## Why This Matters

**Real-world challenges:**
- 99% accuracy isn't enough when the 1% includes critical failures
- Models fail on scenarios not in training data
- Adversaries can exploit perception systems
- Safety requires identifying and handling edge cases

**Key insights:**
- Training datasets miss rare but dangerous scenarios
- Geographic and temporal distribution shift causes failures
- Adversarial examples exist in the physical world
- OOD detection is essential for safe operation

---

## Prerequisites

**Required:**
- Understanding of perception systems (Module 01)
- Machine learning and deep learning fundamentals
- Basic probability and statistics
- PyTorch or TensorFlow experience

**Software:**
- Python 3.8+
- PyTorch or TensorFlow
- NumPy, scikit-learn, Matplotlib, OpenCV
- Adversarial Robustness Toolbox (ART)

---

## Tools Used

- **Adversarial Robustness Toolbox (ART)** - Attacks and defenses
- **Foolbox** - Adversarial attack framework
- **CARLA Scenario Runner** - Corner case generation
- **nuScenes-devkit** - Dataset analysis

---

## Learning Path

**Beginner:**
1. Start with case studies (07) to understand real failures
2. Learn edge case identification (09)
3. Implement OOD detection (08)

**Advanced:**
4. Master adversarial attacks and defenses (10)

---

## Relevant Standards

- **ISO 26262** - Failure Mode and Effects Analysis (FMEA)
- **ISO 21448 (SOTIF)** - Known/unknown unsafe scenarios
- **ISO/SAE 21434** - Threat Analysis and Risk Assessment (TARA)
- **ISO/PAS 8800** - AI robustness requirements

---

## After This Module

Continue to:
- **Module 04 (SOTIF)** - Systematic methodology for unknown unsafe scenarios
- **Module 06 (AI Safety)** - Uncertainty-aware detection for OOD scenarios
- **Module 05 (Cybersecurity)** - Expand adversarial attack analysis

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
