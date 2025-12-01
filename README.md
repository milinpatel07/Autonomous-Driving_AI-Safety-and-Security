<!--
Copyright (c) 2025 Milin Patel
Hochschule Kempten - University of Applied Sciences

Autonomous Driving: AI Safety and Security Workshop
Comprehensive educational materials covering AI-based perception, ISO 26262,
ISO 21448 (SOTIF), ISO/SAE 21434, and uncertainty quantification for autonomous vehicles.

This project is licensed under the MIT License.
See the LICENSE file in the root directory for full license text.
-->

# Autonomous Driving: AI, Safety, and Security Workshop

**Comprehensive Workshop on AI-based Perception, Functional Safety, and Cybersecurity in Autonomous Vehicles**

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Focus:** Autonomous Systems, AI Safety, Functional Safety Standards

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Workshop Status](https://img.shields.io/badge/Status-Complete%20%26%20Ready-brightgreen.svg)]()
[![All Sessions](https://img.shields.io/badge/Sessions-5%2F5%20Complete-success.svg)]()
[![Google Colab](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-ASIL%20D-red.svg)](https://www.iso.org/standard/68383.html)
[![ISO 21448](https://img.shields.io/badge/ISO%2021448-SOTIF-orange.svg)](https://www.iso.org/standard/77490.html)
[![ISO/SAE 21434](https://img.shields.io/badge/ISO%2FSAE%2021434-Cybersecurity-blue.svg)](https://www.iso.org/standard/70918.html)

> **Workshop Status**: All 5 sessions complete. All 24 Jupyter notebooks can be used in Google Colab or locally.

---

## 📖 Overview

This repository provides a comprehensive, academically rigorous workshop on **Autonomous Driving with emphasis on AI-based perception, functional safety, and cybersecurity**. The workshop integrates international standards (ISO 26262, ISO 21448 SOTIF, ISO/SAE 21434) with practical implementations of perception algorithms, uncertainty quantification, and safety validation techniques.

**Target Audience:**
- Graduate students in autonomous systems, robotics, and AI safety
- Engineers developing safety-critical autonomous driving systems
- Researchers in AI safety, uncertainty estimation, and verification & validation
- Safety engineers working with ISO 26262 and ISO 21448 (SOTIF) compliance
- Cybersecurity professionals addressing automotive security (ISO/SAE 21434)

**Prerequisites:**
- Python programming (intermediate level)
- Basic machine learning and computer vision knowledge
- Familiarity with deep learning frameworks (PyTorch)
- Understanding of probability and statistics (for uncertainty quantification)
- Basic knowledge of automotive systems (recommended)

---

## 🎯 Learning Objectives

Upon completion of this workshop, participants will be able to:

### Technical Competencies
1. **Perception Systems**: Implement and evaluate AI-based perception algorithms (object detection, segmentation, sensor fusion)
2. **Sensor Technologies**: Analyze trade-offs between camera, LiDAR, and radar sensors in various operational design domains (ODDs)
3. **Uncertainty Quantification**: Apply Bayesian deep learning, Monte Carlo Dropout, and ensemble methods for uncertainty estimation
4. **Dataset Handling**: Work with industry-standard datasets (KITTI, nuScenes, Waymo Open Dataset)

### Safety and Standards
5. **ISO 26262 (Functional Safety)**: Understand ASIL decomposition, safety goals, and functional safety concepts for autonomous systems
6. **ISO 21448 (SOTIF)**: Identify and mitigate performance limitations and triggering conditions in AI-based perception
7. **ISO 8800 (AI Safety)**: Apply safety principles for AI/ML systems in safety-related applications
8. **Failure Mode Analysis**: Conduct systematic analysis of edge cases, corner cases, and out-of-distribution scenarios

### Security
9. **ISO/SAE 21434 (Cybersecurity)**: Understand threat analysis and risk assessment (TARA) for autonomous vehicles
10. **Adversarial Robustness**: Evaluate perception systems against adversarial attacks and sensor spoofing

---

## 📚 Workshop Structure

### **Session 1: AI-based Perception Systems**

**Focus:** Sensor modalities, object detection, and datasets

| Notebook | Topic | Standards Referenced |
|----------|-------|---------------------|
| 01 | SAE J3016 Automation Levels & AV Architecture | SAE J3016 |
| 02 | Sensor Modalities: Camera, LiDAR, Radar | ISO 26262-5 (Hardware) |
| 03 | Object Detection: YOLOv8, Faster R-CNN | - |
| 04 | AV Datasets: KITTI, nuScenes, Waymo | - |
| 05 | Sensor Fusion: Early, Late, Deep Fusion | ISO 26262-6 (SW) |
| 06 | Pedestrian Detection Safety Case Study | ISO 26262-3 (Concept) |

**Key Concepts:**
- SAE J3016 automation levels (L0-L5) and associated safety requirements
- Sensor comparison: measurement principles, failure modes, environmental limitations
- Deep learning architectures for object detection (YOLO, R-CNN families)
- Benchmark datasets and evaluation metrics (AP, mAP, IoU)
- Multi-modal sensor fusion architectures
- Safety-critical perception system design

---

### **Session 2: Failure Modes and Edge Cases**

**Focus:** Understanding AI failures, out-of-distribution detection, and safety validation

| Notebook | Topic | Standards Referenced |
|----------|-------|---------------------|
| 07 | Real-world AV Failures: Case Studies | ISO 21448 (SOTIF) |
| 08 | Out-of-Distribution (OOD) Detection | ISO 21448, ISO 8800 |
| 09 | Corner Cases and Edge Cases | ISO 21448 (Triggering Conditions) |
| 10 | Adversarial Attacks on Perception | ISO/SAE 21434 |

**Key Concepts:**
- Analysis of real-world AV accidents (Uber ATG 2018, Tesla Autopilot incidents)
- Specification insufficiencies vs. performance limitations (ISO 21448 terminology)
- OOD detection methods: Mahalanobis distance, energy-based detection, OpenMax
- Long-tail distribution in driving scenarios and rare event simulation
- Adversarial examples: FGSM, PGD, physical attacks on traffic signs
- Sensor spoofing and jamming attacks

**Case Studies:**
1. **Uber ATG Fatal Crash (2018)**: Perception system failure, safety driver monitoring
2. **Tesla Autopilot Crashes**: Limitations of camera-based perception in high-contrast scenarios
3. **Waymo Corner Cases**: Handling construction zones, unusual pedestrian behavior
4. **nuScenes Weather Challenges**: Performance degradation in rain and night conditions

---

### **Session 3: Safety and Security Standards**

**Focus:** ISO 26262, ISO 21448 (SOTIF), ISO/SAE 21434, and ISO 8800

| Notebook | Topic | Standards |
|----------|-------|-----------|
| 11 | ISO 26262: Functional Safety for AVs | ISO 26262-1 to 12 |
| 12 | ISO 21448: Safety of the Intended Functionality (SOTIF) | ISO 21448:2022 |
| 13 | ISO 8800: AI Safety in Autonomous Systems | ISO/IEC TR 5469, PAS 8800 |
| 14 | ISO/SAE 21434: Automotive Cybersecurity | ISO/SAE 21434:2021 |

**Key Concepts:**

#### ISO 26262 (Functional Safety)
- V-Model development process for safety-critical systems
- ASIL (Automotive Safety Integrity Level) classification: QM, ASIL A-D
- Safety goals and functional safety concepts for perception systems
- Hardware-software interface (HSI) considerations for AI accelerators
- Verification and validation strategies for ML-based components

#### ISO 21448 (SOTIF - Safety of the Intended Functionality)
- Known safe, known unsafe, unknown safe, unknown unsafe scenarios
- Triggering conditions and performance limitations
- Verification and validation for insufficient specifications
- Integration with ISO 26262 (combined safety argumentation)
- SOTIF process: design, verification, validation, and field monitoring

#### ISO 8800 / ISO/IEC TR 5469 (AI Safety)
- Trustworthiness characteristics: robustness, explainability, transparency
- Data quality and dataset bias assessment
- Training, validation, test set management
- Model monitoring and retraining strategies
- Human-AI interaction safety

#### ISO/SAE 21434 (Cybersecurity)
- Threat analysis and risk assessment (TARA) methodology
- Cybersecurity goals and requirements
- Attack vectors: sensor spoofing, V2X manipulation, ECU exploitation
- Secure software updates (OTA) and cryptographic protection
- Cybersecurity validation and penetration testing

**Deliverables:**
- Hazard analysis and risk assessment (HARA) template for perception systems
- SOTIF insufficiency analysis worksheet
- TARA (Threat Analysis and Risk Assessment) example for V2X communication
- Traceability matrix: safety requirements to verification tests

---

### **Session 4: Uncertainty Estimation and Validation**

**Focus:** Bayesian deep learning, uncertainty quantification, and safety validation

| Notebook | Topic | Techniques |
|----------|-------|------------|
| 15 | Uncertainty in Deep Learning: Aleatoric vs. Epistemic | Bayesian DL |
| 16 | Monte Carlo Dropout for Uncertainty | MC Dropout, Ensembles |
| 17 | Calibration and Reliability Diagrams | Temperature Scaling, ECE |
| 18 | Safety Validation and Testing | Scenario-based Testing |

**Key Concepts:**

#### Uncertainty Types
- **Aleatoric Uncertainty**: Irreducible uncertainty from noisy data (sensor noise, occlusions)
- **Epistemic Uncertainty**: Reducible uncertainty from lack of training data (OOD scenarios)
- **Model Uncertainty**: Uncertainty in learned parameters (weight distributions)

#### Uncertainty Estimation Methods
- **Bayesian Neural Networks (BNNs)**: Full posterior distribution over weights
- **Monte Carlo Dropout**: Approximate Bayesian inference using dropout at test time
- **Deep Ensembles**: Multiple models trained independently for diversity
- **Evidential Deep Learning**: Directly estimate higher-order uncertainty
- **Conformal Prediction**: Distribution-free uncertainty quantification

#### Calibration
- **Reliability Diagrams**: Visualizing calibration quality
- **Expected Calibration Error (ECE)**: Quantitative calibration metric
- **Temperature Scaling**: Post-hoc calibration technique
- **Platt Scaling**: Logistic regression-based calibration

#### Safety Validation
- **Scenario-based Testing**: Concrete, functional, logical scenarios (Pegasus 6-layer model)
- **Simulation-based Validation**: High-fidelity physics simulation (CARLA, SUMO)
- **X-in-the-Loop Testing**: SIL, HIL, VIL, DIL validation strategies
- **Field Operational Tests (FOT)**: Statistical evidence from real-world deployment
- **Formal Verification**: Mathematical proofs for safety properties (limited applicability to DNNs)

---

### **Session 5: Advanced Topics**

**Focus:** V2X communication, explainability, deployment challenges, and standards gaps

| Notebook | Topic | Standards Referenced |
|----------|-------|---------------------|
| 19 | V2X Communication and Cooperative Perception | SAE J2735, IEEE 802.11p, ISO/SAE 21434 |
| 20 | Explainability (XAI) for Safety Certification | ISO/IEC TR 5469, EU AI Act |
| 21 | Standards Integration - Practical Workflow | ISO 26262 + 21448 + 21434 |
| 22 | Industry Deployment Challenges | Real-world case studies |
| 23 | ODD Definition and Runtime Monitoring | ISO 34503, SAE J3016 |
| 24 | Standards Gaps and Open Problems | Research frontier |

**Key Concepts:**
- V2V, V2I, V2P, V2N communication protocols and security
- C-V2X vs DSRC comparison and deployment status
- XAI methods: LIME, SHAP, GradCAM for regulatory compliance
- Multi-standard integration and conflict resolution
- Regulatory barriers and economic viability analysis
- ODD specification using ISO 34503 framework
- Minimal Risk Condition (MRC) and graceful degradation
- Current standards limitations and open research problems

---

## 🚀 Quick Start

### Option 1: Google Colab

**Using Google Colab:**

1. Browse to any session folder and click the Colab badge at the top of a notebook
2. Dependencies install automatically when first cell is executed
3. For complete learning path, follow Session 1 → 2 → 3 → 4 → 5

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git
cd Autonomous-Driving_AI-Safety-and-Security

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Lab
jupyter lab

# Navigate to AV_Perception_Safety_Workshop/Session_1_AI_Perception_Systems/notebooks/
# and open 01_Introduction_SAE_Levels.ipynb
```

**System Requirements:**
- Python 3.8+ (tested on 3.8, 3.9, 3.10, 3.11)
- 8GB RAM minimum (16GB recommended for large datasets)
- GPU optional but recommended for training (CUDA 11.3+)
- 10GB disk space for datasets and models

### Option 3: Browse on GitHub

View all notebooks directly on GitHub with rendered outputs:
- [Session 1: AI Perception Systems](AV_Perception_Safety_Workshop/Session_1_AI_Perception_Systems/)
- [Session 2: Failure Modes and Edge Cases](AV_Perception_Safety_Workshop/Session_2_Failure_Modes_and_Edge_Cases/)
- [Session 3: Safety and Security Standards](AV_Perception_Safety_Workshop/Session_3_Safety_and_Security_Standards/)
- [Session 4: Uncertainty Estimation and Validation](AV_Perception_Safety_Workshop/Session_4_Uncertainty_Estimation_and_Validation/)
- [Session 5: Advanced Topics](AV_Perception_Safety_Workshop/Session_5_Advanced_Topics/)

---

## 🛠️ Technologies and Frameworks

### Deep Learning
- **PyTorch** (2.0+): Neural network training and inference
- **Ultralytics YOLOv8**: Real-time object detection
- **Torchvision**: Pre-trained models and transforms
- **MMDetection**: Unified detection framework (Faster R-CNN, RetinaNet, etc.)

### Computer Vision and 3D
- **OpenCV** (4.5+): Image processing and classical CV
- **Open3D**: 3D point cloud processing and visualization
- **Kornia**: Differentiable computer vision library

### Uncertainty and Probabilistic ML
- **TensorFlow Probability**: Bayesian layers and distributions
- **PyTorch Distributions**: Probability distributions
- **Uncertainty Toolbox**: Calibration metrics and visualization

### Data Science
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib / Seaborn**: Static visualization
- **Plotly**: Interactive 3D plots

### Autonomous Driving Datasets
- **KITTI DevKit**: Object detection, tracking, depth estimation
- **nuScenes DevKit**: Multi-modal dataset with full sensor suite
- **Waymo Open Dataset**: Large-scale AV dataset with diverse scenarios

---

## 📂 Repository Structure

```
Autonomous-Driving_AI-Safety-and-Security/
├── README.md                                    # Main documentation (this file)
├── LICENSE                                      # MIT License
├── requirements.txt                             # Python dependencies
├── SAFETY.md                                    # ISO 26262 & ISO 21448 documentation
├── SECURITY.md                                  # ISO/SAE 21434 & cybersecurity guidelines
├── AI_SAFETY.md                                 # ISO 8800 & AI safety principles
│
├── AV_Perception_Safety_Workshop/
│   │
│   ├── Session_1_AI_Perception_Systems/
│   │   ├── notebooks/
│   │   │   ├── 01_Introduction_SAE_Levels.ipynb
│   │   │   ├── 02_Sensor_Modalities_Visualization.ipynb
│   │   │   ├── 03_Object_Detection_Demo.ipynb
│   │   │   ├── 04_Dataset_Exploration.ipynb
│   │   │   ├── 05_Sensor_Fusion_Basics.ipynb
│   │   │   └── 06_Pedestrian_Detection_Case_Study.ipynb
│   │   │
│   │   ├── scripts/
│   │   │   ├── object_detection.py              # YOLOv8, Faster R-CNN implementations
│   │   │   ├── sensor_visualization.py          # LiDAR, camera visualization
│   │   │   ├── dataset_loader.py                # KITTI, nuScenes loaders
│   │   │   └── utils.py                         # Helper functions
│   │   │
│   │   ├── exercises/
│   │   │   ├── Exercise_1_SAE_Levels.md
│   │   │   └── Exercise_3_Object_Detection.md
│   │   │
│   │   └── resources/
│   │       └── links.md                         # External resources
│   │
│   ├── Session_2_Failure_Modes_and_Edge_Cases/
│   │   ├── notebooks/
│   │   │   ├── 07_AV_Failure_Case_Studies.ipynb
│   │   │   ├── 08_OOD_Detection.ipynb
│   │   │   ├── 09_Corner_Cases.ipynb
│   │   │   └── 10_Adversarial_Attacks.ipynb
│   │   │
│   │   ├── scripts/
│   │   │   ├── ood_detection.py                 # OOD detection methods
│   │   │   ├── adversarial.py                   # FGSM, PGD attacks
│   │   │   └── failure_analysis.py              # Failure mode analysis tools
│   │   │
│   │   ├── exercises/
│   │   │   └── Exercise_4_Adversarial_Robustness.md
│   │   │
│   │   └── resources/
│   │       └── links.md
│   │
│   ├── Session_3_Safety_and_Security_Standards/
│   │   ├── notebooks/
│   │   │   ├── 11_ISO_26262_Functional_Safety.ipynb
│   │   │   ├── 12_ISO_21448_SOTIF.ipynb
│   │   │   ├── 13_ISO_8800_AI_Safety.ipynb
│   │   │   └── 14_ISO_SAE_21434_Cybersecurity.ipynb
│   │   │
│   │   ├── templates/
│   │   │   ├── HARA_Template.xlsx              # Hazard Analysis & Risk Assessment
│   │   │   ├── SOTIF_Analysis_Template.xlsx
│   │   │   └── TARA_Template.xlsx              # Threat Analysis & Risk Assessment
│   │   │
│   │   ├── exercises/
│   │   │   ├── Exercise_5_HARA.md
│   │   │   └── Exercise_6_TARA.md
│   │   │
│   │   └── resources/
│   │       └── links.md
│   │
│   ├── Session_4_Uncertainty_Estimation_and_Validation/
│   │   ├── notebooks/
│   │   │   ├── 15_Uncertainty_Types.ipynb
│   │   │   ├── 16_MC_Dropout_Ensembles.ipynb
│   │   │   ├── 17_Calibration.ipynb
│   │   │   └── 18_Safety_Validation.ipynb
│   │   │
│   │   ├── scripts/
│   │   │   ├── uncertainty.py                   # Uncertainty quantification methods
│   │   │   ├── calibration.py                   # Calibration metrics and plots
│   │   │   └── validation.py                    # Validation test suite
│   │   │
│   │   ├── exercises/
│   │   │   ├── Exercise_7_Uncertainty.md
│   │   │   └── Exercise_8_Validation.md
│   │   │
│   │   └── resources/
│   │       └── links.md
│   │
│   └── Session_5_Advanced_Topics/
│       ├── notebooks/
│       │   ├── 19_V2X_Communication.ipynb
│       │   ├── 20_Explainability_XAI.ipynb
│       │   ├── 21_Standards_Integration.ipynb
│       │   ├── 22_Industry_Deployment.ipynb
│       │   ├── 23_ODD_Runtime_Monitoring.ipynb
│       │   └── 24_Standards_Gaps.ipynb
│       │
│       ├── exercises/
│       │   ├── Exercise_9_V2X_Security.md
│       │   ├── Exercise_10_XAI_Certification.md
│       │   └── Exercise_11_Multi_Standard_Integration.md
│       │
│       └── resources/
│           └── links.md
```

---

## 📊 Standards Reference

### ISO 26262 (Functional Safety)

**Scope:** Electrical and electronic (E/E) systems in road vehicles
**Current Version:** ISO 26262:2018 (Second edition)
**Parts:** 12 parts covering management, concept, system, hardware, software, validation

**Key Concepts:**
- **ASIL (Automotive Safety Integrity Level)**: QM, A, B, C, D (highest)
- **V-Model**: Requirements → Design → Implementation → Testing
- **Safety Lifecycle**: Concept → Development → Production → Operation → Decommissioning
- **Functional Safety Concept**: High-level safety requirements derived from safety goals

**Application to AVs:**
- Perception systems typically require ASIL B or C
- Trajectory planning and vehicle control require ASIL D
- Redundancy and fail-operational designs for higher ASILs

**Resources:**
- [ISO 26262-1:2018](https://www.iso.org/standard/68383.html) - Vocabulary
- [ISO 26262-3:2018](https://www.iso.org/standard/72437.html) - Concept phase
- [ISO 26262-6:2018](https://www.iso.org/standard/68389.html) - Software development

---

### ISO 21448 (SOTIF - Safety of the Intended Functionality)

**Scope:** Absence of unreasonable risk due to performance limitations and misuse
**Published:** June 2022
**Complements:** ISO 26262 (addresses different types of hazards)

**Key Concepts:**
- **Known Safe**: Scenarios verified to be safe
- **Known Unsafe**: Identified hazardous scenarios requiring mitigation
- **Unknown Unsafe**: Potentially hazardous scenarios not yet identified (residual risk)
- **Triggering Conditions**: Environmental/system conditions causing performance limitations
- **Performance Limitations**: Functional insufficiencies in sensors, algorithms

**SOTIF Process:**
1. **Design**: Minimize performance limitations and triggering conditions
2. **Verification**: Test known unsafe scenarios
3. **Validation**: Discover unknown unsafe scenarios through extensive testing
4. **Field Monitoring**: Continuous learning from deployed fleet

**Application to AI/ML:**
- Critical for neural network-based perception (non-deterministic behavior)
- OOD detection and uncertainty estimation as SOTIF mitigation
- Scenario-based testing and simulation for validation

**Resources:**
- [ISO 21448:2022](https://www.iso.org/standard/77490.html) - Main standard
- [PAS 21448:2019](https://www.iso.org/standard/77490.html) - Preliminary version

---

### ISO/SAE 21434 (Automotive Cybersecurity)

**Scope:** Cybersecurity engineering for road vehicles
**Published:** August 2021
**Developed by:** ISO and SAE jointly

**Key Concepts:**
- **TARA (Threat Analysis and Risk Assessment)**: Systematic identification of threats
- **Cybersecurity Goals**: High-level objectives derived from threat analysis
- **CAL (Cybersecurity Assurance Level)**: Similar to ASIL for security (CAL 1-4)
- **Attack Vector**: Path or means by which attacker gains access
- **Attack Feasibility**: Likelihood of successful attack (specialist knowledge, time, equipment)

**Threat Categories for AVs:**
1. **Sensor Attacks**: LiDAR spoofing, camera blinding, GNSS jamming
2. **V2X Attacks**: Message injection, denial of service, Sybil attacks
3. **Backend Attacks**: Cloud infrastructure compromise, data exfiltration
4. **Physical Access**: OBD-II exploitation, ECU reprogramming

**Cybersecurity Lifecycle:**
- Concept phase: TARA, cybersecurity goals
- Development: Secure design, implementation, verification
- Production: Secure manufacturing, key management
- Operations: Incident response, security updates (OTA)
- Decommissioning: Secure data deletion

**Resources:**
- [ISO/SAE 21434:2021](https://www.iso.org/standard/70918.html) - Main standard
- [SAE J3061](https://www.sae.org/standards/content/j3061_201601/) - Predecessor guideline

---

### ISO 8800 and AI Safety Guidelines

**Note:** ISO 8800 is not yet a published standard. Current AI safety guidance comes from:

- **ISO/IEC TR 5469:2024** - Artificial intelligence — Functional safety and AI systems
- **PAS 8800** (proposed, not yet published)
- **ISO/IEC 23894:2023** - Information technology — AI — Guidance on risk management
- **ISO/IEC 42001:2023** - AI management system

**Key AI Safety Principles:**
1. **Data Quality**: Representative, diverse, labeled correctly, bias assessment
2. **Model Transparency**: Explainability, interpretability, documentation
3. **Robustness**: Performance under distribution shift, adversarial perturbations
4. **Uncertainty Awareness**: Quantify and communicate model uncertainty
5. **Human Oversight**: Human-in-the-loop, human-on-the-loop designs
6. **Continuous Monitoring**: Performance tracking, anomaly detection, retraining triggers
7. **Fail-Safe Mechanisms**: Graceful degradation, fallback systems

**Integration with ISO 26262 and ISO 21448:**
- Data quality → SOTIF insufficiency mitigation
- Uncertainty quantification → ISO 26262 diagnostic coverage
- Monitoring → ISO 21448 field validation

**Resources:**
- [ISO/IEC TR 5469:2024](https://www.iso.org/standard/81283.html)
- [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

## 🔗 External Resources

### Standards Organizations
- [ISO (International Organization for Standardization)](https://www.iso.org/)
- [SAE International](https://www.sae.org/)
- [NIST (National Institute of Standards and Technology)](https://www.nist.gov/)
- [UNECE WP.29](https://unece.org/transport/vehicle-regulations) - UN vehicle regulations

### Datasets
- [KITTI Vision Benchmark](http://www.cvlibs.net/datasets/kitti/) - Object detection, tracking, depth
- [nuScenes Dataset](https://www.nuscenes.org/) - 1000 scenes, full sensor suite, Boston & Singapore
- [Waymo Open Dataset](https://waymo.com/open/) - 1950 segments, diverse weather and lighting
- [BDD100K](https://bdd-data.berkeley.edu/) - 100K diverse driving videos
- [Argoverse 2](https://www.argoverse.org/) - HD maps, motion forecasting
- [CADC (Canadian Adverse Driving Conditions)](http://cadcd.uwaterloo.ca/) - Snowy driving

### Simulation Platforms
- [CARLA Simulator](https://carla.org/) - Open-source AV simulation
- [SUMO](https://eclipse.dev/sumo/) - Traffic simulation
- [Waymo Sim Agents Challenge](https://waymo.com/open/challenges/2024/sim-agents/) - Behavior simulation

### Academic Papers and Books

#### Perception
- Geiger et al. (2012): "Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite"
- Caesar et al. (2020): "nuScenes: A multimodal dataset for autonomous driving"
- Bochkovskiy et al. (2020): "YOLOv4: Optimal Speed and Accuracy of Object Detection"

#### Safety
- Koopman & Wagner (2016): "Challenges in Autonomous Vehicle Testing and Validation"
- Kalra & Paddock (2016): "Driving to Safety: How Many Miles of Driving Would It Take to Demonstrate Autonomous Vehicle Reliability?"
- Ulbrich et al. (2015): "Defining and Substantiating the Terms Scene, Situation, and Scenario for Automated Driving"

#### Uncertainty
- Gal & Ghahramani (2016): "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"
- Kendall & Gal (2017): "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
- Lakshminarayanan et al. (2017): "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"

#### Books
- **"Automated Driving: Safer and More Efficient Future Driving"** (Watzenig & Horn, 2016)
- **"Autonomous Driving: Technical, Legal and Social Aspects"** (Maurer et al., 2016)
- **"Safety of the Intended Functionality: Engineering the System"** (Burton et al., 2023)
- **"ISO 26262 - A Practical Guide"** (Schmittner et al., 2022)

### Online Courses and Tutorials
- [Coursera: Self-Driving Cars Specialization](https://www.coursera.org/specializations/self-driving-cars) (University of Toronto)
- [Udacity: Self-Driving Car Engineer Nanodegree](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd0013)
- [Apollo Open Platform](https://apollo.auto/) - Baidu's open AV platform with tutorials
- [Autoware](https://www.autoware.org/) - Open-source AV software stack

---

## 🧪 Exercises and Assignments

Each session includes hands-on exercises with progressive difficulty:

### Session 1 Exercises
1. **SAE Automation Levels Analysis**: Understanding SAE J3016 levels and their safety implications
3. **Object Detection Performance**: Evaluate detection models on benchmark datasets

### Session 2 Exercises
4. **Adversarial Robustness Testing**: Generate adversarial examples and evaluate defensive techniques

### Session 3 Exercises
5. **HARA (Hazard Analysis and Risk Assessment)**: Complete HARA for perception system using ISO 26262 methodology
6. **TARA (Threat Analysis and Risk Assessment)**: Conduct cybersecurity TARA using ISO/SAE 21434 framework

### Session 4 Exercises
7. **Uncertainty Quantification**: Implement and compare uncertainty estimation methods (MC Dropout, Ensembles)
8. **Validation Strategy Design**: Develop scenario-based testing and validation approaches

### Session 5 Exercises
9. **V2X Security Analysis**: Apply TARA methodology to V2X communication systems
10. **XAI for Certification**: Generate explainability evidence for AI perception models using XAI techniques
11. **Multi-Standard Integration**: Perform combined ISO 26262 + ISO 21448 + ISO/SAE 21434 analysis

---

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- Additional case studies and real-world examples
- New notebooks on emerging topics (transformers, NeRF, world models)
- Improved documentation and tutorials
- Bug fixes and code optimization
- Translation to other languages

Please open an issue or submit a pull request.

---

## 📝 Citation

If you use this workshop in your research, teaching, or industrial work, please cite:

```bibtex
@misc{patel2025av_safety_security_workshop,
  author = {Patel, Milin},
  title = {Autonomous Driving: AI, Safety, and Security Workshop},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}},
  note = {Comprehensive workshop on AI-based perception, ISO 26262, ISO 21448, and ISO/SAE 21434}
}
```

---

## 📧 Contact

**Milin Patel**
Hochschule Kempten
Focus: Autonomous Systems, AI Safety, Functional Safety

- GitHub: [@milinpatel07](https://github.com/milinpatel07)
- Issues: [GitHub Issues](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues)

For workshop-related questions, please open a GitHub issue with the appropriate label.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ISO and SAE** for developing comprehensive safety and security standards
- **KITTI, nuScenes, Waymo** for providing open autonomous driving datasets
- **Open-source community** for tools and frameworks (PyTorch, OpenCV, Open3D)
- **Hochschule Kempten** for supporting this educational initiative

---

## Version History

- **v1.0** (2025): Complete workshop curriculum
  - All 5 sessions with 24 comprehensive Jupyter notebooks
  - Coverage: AI Perception, Failure Analysis, Safety & Security Standards, Uncertainty Quantification, and Advanced Topics
  - 11 hands-on exercises with templates and solutions
  - Full integration of ISO 26262, ISO 21448 (SOTIF), and ISO/SAE 21434
  - V2X Communication, XAI for certification, ODD definition, and standards integration
  - Comprehensive resources and reference materials

---

**Getting Started:**

[Session 1, Notebook 1: SAE Automation Levels](AV_Perception_Safety_Workshop/Session_1_AI_Perception_Systems/notebooks/01_Introduction_SAE_Levels.ipynb)

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
