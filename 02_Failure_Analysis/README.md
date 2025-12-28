# Failure Analysis

**Module 02: Edge Cases, Failure Modes, and Adversarial Robustness for Autonomous Vehicles**

---

## Overview

Understanding and mitigating perception failures is critical for autonomous vehicle safety. This module provides comprehensive analysis of real-world autonomous vehicle incidents, edge case detection methodologies, out-of-distribution (OOD) detection techniques, and adversarial attack defense strategies. Through systematic failure analysis, students learn to identify, categorize, and address the limitations of AI-based perception systems.

### Module Objectives

Upon completing this module, you will:

1. **Analyze Real-World Failures**: Investigate documented autonomous vehicle incidents and extract root causes
2. **Identify Edge Cases**: Recognize corner cases and long-tail scenarios that challenge perception systems
3. **Implement OOD Detection**: Apply out-of-distribution detection methods to identify novel scenarios
4. **Understand Adversarial Attacks**: Analyze physical and digital attacks on perception systems
5. **Develop Defense Mechanisms**: Implement adversarial training and detection strategies
6. **Apply SOTIF Framework**: Use ISO 21448 methodology to systematically identify unsafe scenarios
7. **Quantify Failure Modes**: Categorize and measure perception failure frequencies and impacts

---

## Why Failure Analysis Matters

### Critical Challenges in Autonomous Vehicle Safety

**1. Real-World Incident Analysis**
- **Uber ATG Tempe (2018)**: Fatal pedestrian collision due to perception system failure and safety driver inattention
- **Tesla Autopilot incidents**: Multiple crashes involving perception limitations with stationary objects
- **Waymo emergency braking**: False positive detections causing unnecessary stops
- Each incident reveals systemic vulnerabilities requiring analysis and mitigation

**2. The Long-Tail Problem**
- Training datasets are dominated by common scenarios (highway driving, clear weather)
- Rare scenarios are underrepresented but disproportionately dangerous
- Examples: overturned vehicles, animals on road, objects falling from trucks
- Statistical rarity makes these scenarios difficult to collect and validate
- "99% accuracy" is insufficient when the 1% includes critical failures

**3. Distribution Shift and Domain Gap**
- Models trained on specific datasets (e.g., sunny California) fail in novel environments
- Geographic shift: Different road markings, vehicle types, driving behaviors
- Temporal shift: Seasonal changes, construction zones, new infrastructure
- Sensor degradation: Dirt accumulation, hardware aging, calibration drift
- OOD detection is essential for safe operation outside training distribution

**4. Adversarial Vulnerability**
- **Physical adversarial examples**: Patches on stop signs causing misclassification
- **Sensor spoofing**: LiDAR jamming, GPS spoofing, camera dazzling
- **Data poisoning**: Compromised training data leading to backdoor vulnerabilities
- **Model extraction**: Reverse-engineering proprietary models for targeted attacks
- Intersection of ISO 26262 (functional safety) and ISO/SAE 21434 (cybersecurity)

**5. Corner Case Identification**
- Systematic enumeration is impossible - infinite possible scenarios
- Edge cases discovered through:
  - Simulation-based testing (Monte Carlo, adversarial generation)
  - Field operational tests with disengagement analysis
  - Crowdsourced incident reporting
  - Synthetic scenario generation
- SOTIF requires proactive identification of unknown unsafe scenarios

**6. Safety vs. Availability Trade-off**
- Overly conservative systems: Frequent false alarms reduce user trust
- Overly permissive systems: Missed detections create safety hazards
- Minimum Risk Condition (MRC) strategies: When to stop, slow down, or request takeover
- ISO 26262 ASIL decomposition addresses this trade-off systematically

---

## Module Structure

### 📓 Notebooks

1. **[07_AV_Failure_Case_Studies.ipynb](notebooks/07_AV_Failure_Case_Studies.ipynb)**
   - Uber ATG Tempe incident: Pedestrian detection failure analysis
   - Tesla Autopilot crashes: Camera-based perception limitations
   - Waymo disengagements: Categorization and root cause analysis
   - Cruise GM incident: Complex urban interaction failures
   - Lessons learned and systemic improvements
   - NTSB investigation reports and safety recommendations

2. **[08_OOD_Detection.ipynb](notebooks/08_OOD_Detection.ipynb)**
   - Out-of-distribution detection fundamentals
   - Statistical methods: Mahalanobis distance, KNN-based detection
   - Deep learning approaches: Maximum softmax probability, ODIN, energy-based models
   - Bayesian uncertainty: Epistemic vs. aleatoric uncertainty
   - Ensemble disagreement and Monte Carlo Dropout
   - Benchmark datasets: KITTI-C (corruption), nuScenes-OOD

3. **[09_Corner_Cases_and_Edge_Cases.ipynb](notebooks/09_Corner_Cases_and_Edge_Cases.ipynb)**
   - Definition and taxonomy of edge cases
   - Long-tail scenario identification methodologies
   - Rare object classes: Emergency vehicles, construction equipment, animals
   - Unusual weather: Heavy rain, dense fog, snow accumulation
   - Infrastructure anomalies: Missing lane markings, roadwork, detours
   - Scenario generation for systematic edge case testing
   - PEGASUS methodology for scenario-based validation

4. **[10_Adversarial_Attacks_on_Perception.ipynb](notebooks/10_Adversarial_Attacks_on_Perception.ipynb)**
   - Digital adversarial attacks: FGSM, PGD, C&W optimization
   - Physical adversarial attacks: Patches, 3D objects, projected patterns
   - Sensor-specific attacks: Camera (adversarial patterns), LiDAR (spoofing), Radar (jamming)
   - Attack detection mechanisms: Input validation, statistical anomaly detection
   - Adversarial training and certified defenses
   - ISO/SAE 21434 cybersecurity risk assessment integration

---

## Prerequisites

### Knowledge
- Understanding of autonomous vehicle perception (Module 01)
- Machine learning and deep learning fundamentals
- Basic probability and statistics
- Familiarity with PyTorch or TensorFlow

### Software
- Python 3.8+
- PyTorch 1.12+ or TensorFlow 2.8+
- Libraries: NumPy, scikit-learn, Matplotlib, OpenCV
- Adversarial Robustness Toolbox (ART)
- Optional: CARLA Simulator for scenario testing

---

## Failure Analysis Tools and Frameworks

- **Adversarial Robustness Toolbox (ART)**: IBM's library for adversarial attacks and defenses
- **Foolbox**: Adversarial attack framework for PyTorch and TensorFlow
- **CleverHans**: TensorFlow-based adversarial examples library
- **CARLA Scenario Runner**: Corner case scenario generation
- **nuScenes-devkit**: Dataset analysis and failure case extraction

---

## Learning Path

### Beginner Path
1. Start with **07_AV_Failure_Case_Studies** to understand real-world failures
2. Proceed to **09_Corner_Cases_and_Edge_Cases** for systematic identification
3. Learn **08_OOD_Detection** for runtime anomaly detection

### Advanced Path
4. Master **10_Adversarial_Attacks_on_Perception** for security-aware design

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Analyze NTSB report and create fault tree for Uber ATG incident
2. **Exercise 2**: Implement Mahalanobis distance-based OOD detector
3. **Exercise 3**: Generate synthetic corner cases using CARLA Scenario Runner
4. **Exercise 4**: Create physical adversarial patch for stop sign misclassification
5. **Exercise 5**: Develop adversarial training pipeline and measure robustness improvement

---

## Code Examples

Located in `code/`:
- `failure_taxonomy.py`: Categorization framework for perception failures
- `ood_detector.py`: Out-of-distribution detection implementations
- `adversarial_attack.py`: FGSM, PGD attack generation
- `robustness_evaluation.py`: Model robustness benchmarking
- `scenario_generator.py`: Edge case scenario synthesis

---

## Industry Standards and References

### Standards
- **ISO 26262**: Functional Safety - Failure Mode and Effects Analysis (FMEA)
- **ISO 21448 (SOTIF)**: Known/unknown unsafe scenarios, triggering conditions
- **ISO/SAE 21434**: Cybersecurity Engineering - Threat Analysis and Risk Assessment (TARA)
- **ISO/PAS 8800**: Safety and Artificial Intelligence - Robustness requirements
- **UL 4600**: Standard for Safety for the Evaluation of Autonomous Products

### Key Papers
- Hendrycks & Dietterich (2019): "Benchmarking Neural Network Robustness to Common Corruptions and Perturbations"
- Eykholt et al. (2018): "Robust Physical-World Attacks on Deep Learning Visual Classification"
- Breitenstein et al. (2020): "Corner Cases for Visual Perception in Automated Driving"
- Boloor et al. (2020): "Attacking Vision-Based Perception in End-to-End Autonomous Driving Models"
- Kang et al. (2020): "Testing Deep Neural Networks for Safety-Critical Systems"

### Resources
- [NTSB Investigation Reports](https://www.ntsb.gov/)
- [California DMV Disengagement Reports](https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/disengagement-reports/)
- [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- [RobustBench Leaderboard](https://robustbench.github.io/)

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Analyze real-world autonomous vehicle incidents and extract root causes
✓ Identify and categorize edge cases and corner scenarios
✓ Implement out-of-distribution detection methods
✓ Generate adversarial examples for perception systems
✓ Develop adversarial defenses and robustness improvements
✓ Apply SOTIF methodology for unknown unsafe scenario identification
✓ Conduct Failure Mode and Effects Analysis (FMEA) for perception
✓ Integrate safety (ISO 26262) and security (ISO/SAE 21434) considerations

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding what can fail

### Related Modules
- **Module 03**: Functional Safety - FMEA and hazard analysis
- **Module 04**: SOTIF - Systematic scenario identification
- **Module 05**: Cybersecurity - Adversarial attacks as security threats

### Follow-up Modules
- **Module 06**: AI Safety - Uncertainty quantification for failure detection
- **Module 07**: Validation & Verification - Testing edge cases and adversarial robustness
- **Module 08**: Advanced Topics - Runtime monitoring and MRC strategies

---

## Next Steps

After completing this module:
- **Module 04**: SOTIF - Apply systematic methodology for unknown unsafe scenario identification
- **Module 06**: AI Safety - Implement uncertainty-aware detection for OOD scenarios
- **Module 05**: Cybersecurity - Expand adversarial attack analysis to full threat model

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
