# Autonomous Driving: AI Safety and Security

**Comprehensive Educational Resource on Perception Systems, Functional Safety, and Cybersecurity for Autonomous Vehicles**

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**Version:** 2.0.0
**Focus:** Autonomous Systems, AI Safety, Functional Safety Standards, Cybersecurity

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Google Colab](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-ASIL%20D-red.svg)](https://www.iso.org/standard/68383.html)
[![ISO 21448](https://img.shields.io/badge/ISO%2021448-SOTIF-orange.svg)](https://www.iso.org/standard/77490.html)
[![ISO/SAE 21434](https://img.shields.io/badge/ISO%2FSAE%2021434-Cybersecurity-blue.svg)](https://www.iso.org/standard/70918.html)

---

## 📖 Overview

This repository provides a comprehensive educational resource on **autonomous vehicle perception systems, functional safety engineering, Safety of the Intended Functionality (SOTIF), automotive cybersecurity, and AI safety**. The content integrates international standards (ISO 26262, ISO 21448, ISO/SAE 21434, ISO 8800) with practical implementations using PyTorch, Open3D, and industry-standard datasets.

**NEW in v2.0:** Comprehensive LiDAR technology module covering sensor fundamentals, point cloud processing, and 3D annotation methodologies for autonomous vehicle perception data preparation.

### Target Audience

- **Graduate Students**: Autonomous systems, robotics, AI safety, computer vision
- **Automotive Engineers**: Perception system development, ADAS/AD integration
- **Safety Engineers**: ISO 26262, ISO 21448 (SOTIF) certification and validation
- **Cybersecurity Professionals**: Automotive security (ISO/SAE 21434) implementation
- **Researchers**: AI safety, uncertainty quantification, verification & validation
- **Machine Learning Engineers**: Deep learning for safety-critical applications

### Prerequisites

- **Programming**: Python (intermediate), familiarity with NumPy, PyTorch
- **Mathematics**: Linear algebra, probability theory, statistics
- **Machine Learning**: Deep learning fundamentals, computer vision
- **Domain Knowledge**: Basic understanding of automotive systems (recommended)

---

## 🎯 Learning Objectives

Upon completing this educational resource, you will be able to:

### Technical Competencies

1. **Perception Systems**
   - Implement AI-based perception algorithms (object detection, segmentation, tracking)
   - Design and evaluate sensor fusion architectures (camera, LiDAR, radar)
   - Process and annotate 3D point cloud data
   - Work with autonomous driving datasets (KITTI, nuScenes, Waymo)

2. **LiDAR Technology** (NEW in v2.0)
   - Understand LiDAR sensor physics and scanning mechanisms
   - Process point cloud data structures and coordinate transformations
   - Execute 3D annotation methodologies (cuboids, segmentation, tracking)
   - Handle annotation challenges (occlusions, low-density regions, temporal consistency)
   - Implement quality assurance processes for annotation

3. **AI Safety**
   - Apply uncertainty quantification techniques (Bayesian DL, MC Dropout, Ensembles)
   - Implement out-of-distribution detection methods
   - Evaluate adversarial robustness and develop defenses
   - Perform model calibration and reliability assessment

### Safety Engineering

4. **ISO 26262 (Functional Safety)**
   - Conduct Hazard Analysis and Risk Assessment (HARA)
   - Perform ASIL decomposition and allocation
   - Develop safety goals and functional safety concepts
   - Create safety cases for perception systems

5. **ISO 21448 (SOTIF - Safety of the Intended Functionality)**
   - Identify performance limitations and triggering conditions
   - Analyze known/unknown safe/unsafe scenarios
   - Design validation strategies for AI-based functions
   - Implement field monitoring and continuous learning

6. **ISO 8800 / ISO/IEC TR 5469 (AI Safety)**
   - Apply trustworthiness principles (robustness, explainability, transparency)
   - Assess data quality and dataset bias
   - Implement runtime monitoring and anomaly detection
   - Manage model lifecycle and updates

### Cybersecurity

7. **ISO/SAE 21434 (Automotive Cybersecurity)**
   - Conduct Threat Analysis and Risk Assessment (TARA)
   - Identify and mitigate attack vectors (sensor spoofing, V2X manipulation)
   - Implement secure development lifecycle practices
   - Perform cybersecurity validation and penetration testing

---

## 📚 Repository Structure

The repository is organized into **10 comprehensive modules**, each containing Jupyter notebooks, code implementations, exercises, and resources.

```
Autonomous-Driving_AI-Safety-and-Security/
│
├── README.md                                    # Main documentation (this file)
├── LICENSE                                      # MIT License
├── requirements.txt                             # Python dependencies
├── V2_REORGANIZATION_PLAN.md                    # v2 migration documentation
│
├── docs/                                        # Comprehensive documentation
│   ├── SAFETY.md                                # ISO 26262 & ISO 21448 reference
│   ├── SECURITY.md                              # ISO/SAE 21434 reference
│   ├── AI_SAFETY.md                             # AI/ML safety guidelines
│   └── STANDARDS_OVERVIEW.md                    # Standards integration guide
│
├── 01_Perception_Systems/                       # AI-based perception fundamentals
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_sae_automation_levels.ipynb       # SAE J3016 levels 0-5
│   │   ├── 02_sensor_technologies.ipynb         # Camera, LiDAR, Radar comparison
│   │   ├── 03_object_detection.ipynb            # YOLO, R-CNN, modern architectures
│   │   ├── 04_sensor_fusion.ipynb               # Early, late, deep fusion
│   │   └── 05_pedestrian_detection.ipynb        # Safety-critical case study
│   ├── code/                                    # Reusable implementations
│   └── exercises/                               # Hands-on assignments
│
├── 02_Failure_Analysis/                         # Edge cases and failure modes
│   ├── README.md
│   ├── notebooks/
│   │   ├── 07_AV_Failure_Case_Studies.ipynb     # Real-world incidents analysis
│   │   ├── 08_OOD_Detection.ipynb               # Out-of-distribution detection
│   │   ├── 09_Corner_Cases_and_Edge_Cases.ipynb # Long-tail scenarios
│   │   └── 10_Adversarial_Attacks_on_Perception.ipynb
│   ├── code/
│   └── exercises/
│
├── 03_Functional_Safety/                        # ISO 26262 implementation
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_iso_26262_fundamentals.ipynb      # V-Model, ASIL, safety lifecycle
│   │   ├── 02_hazard_analysis_risk_assessment.ipynb  # HARA methodology
│   │   ├── 03_asil_decomposition.ipynb          # Safety requirements allocation
│   │   └── 04_safety_case_development.ipynb     # Argumentation and evidence
│   ├── templates/
│   │   ├── HARA_Template.md                     # Hazard Analysis template
│   │   └── Safety_Case_Template.md
│   └── exercises/
│
├── 04_SOTIF/                                    # ISO 21448 Safety of Intended Functionality
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_sotif_fundamentals.ipynb          # Known/unknown safe/unsafe
│   │   ├── 02_triggering_conditions.ipynb       # Performance limitations
│   │   ├── 03_scenario_based_validation.ipynb   # Testing strategies
│   │   └── 04_field_monitoring.ipynb            # Continuous validation
│   ├── templates/
│   └── exercises/
│
├── 05_Cybersecurity/                            # ISO/SAE 21434 implementation
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_automotive_cybersecurity.ipynb    # Threat landscape
│   │   ├── 02_threat_analysis_risk_assessment.ipynb  # TARA methodology
│   │   ├── 03_attack_vectors.ipynb              # Sensor spoofing, V2X attacks
│   │   └── 04_secure_development.ipynb          # SDL practices
│   ├── templates/
│   │   └── TARA_Template.md
│   └── exercises/
│
├── 06_AI_Safety/                                # Uncertainty and trustworthiness
│   ├── README.md
│   ├── notebooks/
│   │   ├── 15_Uncertainty_Types_in_Deep_Learning.ipynb
│   │   ├── 16_MC_Dropout_and_Ensembles.ipynb    # Uncertainty quantification
│   │   ├── 17_Calibration_and_Reliability.ipynb # Temperature scaling, ECE
│   │   ├── 18_Safety_Validation_and_Testing.ipynb
│   │   └── 05_ai_safety_standards.ipynb         # ISO 8800, ISO/IEC TR 5469
│   ├── code/
│   └── exercises/
│
├── 07_Validation_Verification/                  # Testing and validation
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_testing_strategies.ipynb          # SIL, HIL, VIL, DIL
│   │   ├── 02_scenario_generation.ipynb         # Concrete, logical, functional
│   │   ├── 03_simulation_based_testing.ipynb    # CARLA, SUMO
│   │   └── 04_field_testing.ipynb               # FOT, statistical evidence
│   └── exercises/
│
├── 08_Advanced_Topics/                          # Integration and deployment
│   ├── README.md
│   ├── notebooks/
│   │   ├── 19_V2X_Communication.ipynb           # C-V2X, DSRC, security
│   │   ├── 20_Explainability_XAI.ipynb          # LIME, SHAP, Grad-CAM
│   │   ├── 21_Standards_Integration.ipynb       # Multi-standard compliance
│   │   ├── 22_Industry_Deployment.ipynb         # Economic, regulatory barriers
│   │   ├── 23_ODD_Runtime_Monitoring.ipynb      # ISO 34503, MRC
│   │   └── 24_Standards_Gaps.ipynb              # Research frontier
│   └── exercises/
│
├── 09_LiDAR_Technology/                         # ⭐ NEW IN V2.0 ⭐
│   ├── README.md                                # Comprehensive LiDAR guide
│   ├── notebooks/
│   │   ├── 01_lidar_sensor_fundamentals.ipynb   # ToF, phase-shift, scanning mechanisms
│   │   ├── 02_point_cloud_processing.ipynb      # Data structures, filtering, ground removal
│   │   ├── 03_3d_annotation_fundamentals.ipynb  # Cuboids, segmentation, instance labeling
│   │   ├── 04_annotation_challenges.ipynb       # Occlusions, temporal consistency
│   │   ├── 05_multimodal_annotation.ipynb       # LiDAR-Camera fusion
│   │   ├── 06_annotation_quality_assurance.ipynb # QA metrics, validation pipelines
│   │   ├── 07_annotation_tools_workflows.ipynb  # Professional platforms, AI-assisted
│   │   └── 08_lidar_safety_considerations.ipynb # Failure modes, weather impacts
│   ├── code/
│   │   ├── point_cloud_utils.py                 # Processing utilities
│   │   ├── annotation_utils.py                  # 3D bounding box operations
│   │   ├── visualization.py                     # Open3D visualization
│   │   └── quality_metrics.py                   # IoU, precision, recall
│   ├── exercises/
│   └── resources/
│
├── 10_Datasets_Benchmarks/                      # AV datasets and evaluation
│   ├── README.md
│   ├── notebooks/
│   │   ├── 01_dataset_overview.ipynb            # KITTI, nuScenes, Waymo comparison
│   │   ├── 02_dataset_analysis.ipynb            # Statistical analysis, bias assessment
│   │   ├── 03_benchmark_metrics.ipynb           # AP, mAP, IoU evaluation
│   │   └── 04_custom_dataset_creation.ipynb     # Data collection best practices
│   └── exercises/
│
├── case_studies/                                # Real-world incident analysis
│   ├── README.md
│   ├── uber_atg_2018.md                         # Fatal crash analysis
│   ├── tesla_autopilot.md                       # Camera-based limitations
│   └── waymo_scenarios.md                       # Corner case handling
│
├── exercises/                                   # Comprehensive exercise sets
│   ├── functional_safety/
│   ├── cybersecurity/
│   └── ai_safety/
│
└── datasets/                                    # Sample data and loaders
    ├── README.md
    └── sample_data/
```

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

**Zero installation required - run notebooks directly in your browser**

1. Navigate to any module folder (e.g., `01_Perception_Systems/notebooks/`)
2. Click on a notebook file
3. Click the "Open in Colab" badge at the top
4. Dependencies install automatically when you run the first cell

**Recommended Learning Path:**
```
01_Perception_Systems → 09_LiDAR_Technology → 02_Failure_Analysis →
03_Functional_Safety → 04_SOTIF → 05_Cybersecurity → 06_AI_Safety →
07_Validation_Verification → 08_Advanced_Topics
```

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

# Navigate to any module and open notebooks
```

**System Requirements:**
- Python 3.8+ (tested on 3.8, 3.9, 3.10, 3.11)
- 8GB RAM minimum (16GB recommended for large datasets)
- GPU optional but recommended (CUDA 11.3+)
- 15GB disk space for datasets

### Option 3: Browse on GitHub

View all notebooks directly on GitHub with rendered outputs and visualizations.

---

## 🛠️ Technologies and Frameworks

### Deep Learning
- **PyTorch** (2.0+): Neural network training and inference
- **Ultralytics YOLOv8**: Real-time object detection
- **Torchvision**: Pre-trained models and transforms
- **MMDetection**: Unified detection framework

### Computer Vision and 3D
- **OpenCV** (4.5+): Image processing
- **Open3D**: 3D point cloud processing and visualization
- **Kornia**: Differentiable computer vision

### Uncertainty and Probabilistic ML
- **TensorFlow Probability**: Bayesian layers
- **PyTorch Distributions**: Probability distributions
- **Uncertainty Toolbox**: Calibration metrics

### Data Science
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Matplotlib / Seaborn**: Visualization
- **Plotly**: Interactive 3D plots

### Autonomous Driving Datasets
- **KITTI DevKit**: Object detection, tracking, depth
- **nuScenes DevKit**: Multi-modal full sensor suite
- **Waymo Open Dataset**: Large-scale diverse scenarios

---

## 🌟 What's NEW in v2.0

### Major Enhancements

1. **Comprehensive LiDAR Module (Module 09)** ⭐
   - 8 detailed notebooks covering sensor fundamentals to annotation QA
   - Addresses 10 critical LiDAR annotation challenges:
     - 10× time complexity vs 2D annotation
     - Pattern recognition in 1M+ points/second data
     - Physics and domain knowledge requirements
     - Occlusion handling (partial, complete, self-occlusion)
     - 9+ label types (cuboids, segmentation, tracking, attributes)
     - Weather challenges (rain ghost points, fog attenuation)
     - Multi-modal fusion (LiDAR-Camera alignment)
     - 4D annotation tools and AI-assisted workflows
     - Safety-critical precision (5-10 cm error tolerance)
   - Practical implementations with Open3D
   - Professional annotation workflow guidance

2. **Reorganized Structure**
   - Topic-based modules (vs. session-based)
   - Clearer navigation and prerequisites
   - Consistent module organization
   - Enhanced cross-referencing

3. **Enhanced Documentation**
   - Removed workshop terminology
   - Academic rigor and proper citations
   - Comprehensive standards integration guide
   - Industry case studies

4. **Improved Code Quality**
   - Type hints and docstrings
   - Modular, reusable implementations
   - Better visualization utilities
   - Unit tests for core functions

---

## 📊 Standards Coverage

This resource provides practical implementation guidance for:

### ISO 26262 (Functional Safety)
**Scope:** Electrical/electronic systems in road vehicles
**Current Version:** ISO 26262:2018 (Second edition)
**Coverage:**
- V-Model development process
- ASIL (A, B, C, D) classification and decomposition
- Safety goals and functional safety concepts
- Hardware-software interface considerations for AI accelerators
- Verification and validation for ML components

**Key Notebooks:** Module 03 (Functional Safety)

### ISO 21448 (SOTIF - Safety of the Intended Functionality)
**Published:** June 2022
**Complements:** ISO 26262 (addresses performance limitations)
**Coverage:**
- Known safe/unsafe, unknown safe/unsafe scenarios
- Triggering conditions identification
- Performance limitations analysis
- Verification and validation strategies
- Field monitoring and continuous learning

**Key Notebooks:** Module 04 (SOTIF)

### ISO/SAE 21434 (Automotive Cybersecurity)
**Published:** August 2021
**Developed by:** ISO and SAE jointly
**Coverage:**
- Threat Analysis and Risk Assessment (TARA)
- Cybersecurity goals and CAL levels
- Attack vector identification and mitigation
- Secure development lifecycle
- Cybersecurity validation and penetration testing

**Key Notebooks:** Module 05 (Cybersecurity)

### ISO 8800 / ISO/IEC TR 5469 (AI Safety)
**Status:** ISO/IEC TR 5469:2024 published, ISO 8800 in development
**Coverage:**
- Trustworthiness characteristics (robustness, explainability)
- Data quality and bias assessment
- Uncertainty quantification
- Runtime monitoring
- Model lifecycle management

**Key Notebooks:** Module 06 (AI Safety)

---

## 💡 LiDAR Annotation: Key Facts (Module 09)

### Why LiDAR Annotation is Critical

1. **10× Time Investment**: LiDAR annotation requires 10× more time than 2D images due to full 3D parameterization (x, y, z, l, w, h, θ)

2. **Massive Data Volume**: High-end sensors capture up to **1 million points per second**, creating processing challenges

3. **Expert Pattern Recognition**: Raw point clouds appear as noise; annotators require significant training to recognize patterns

4. **Physics Knowledge**: Annotators require real-world understanding of vehicle dimensions, road rules, environmental context

5. **Occlusion Complexity**: Handling partial/complete occlusions is the hardest challenge - predicting hidden object boundaries

6. **9+ Label Types**: 3D cuboids, semantic segmentation, lanes, drivable areas, ROIs, tracking IDs, attributes, relationships

7. **Environmental Noise**: Rain creates ghost points, fog reduces range 200m→50m, requiring filtering expertise

8. **Sensor Fusion**: LiDAR-Camera fusion annotation requires handling additional complexity, including precise calibration and 2D-3D alignment

9. **Advanced Tools**: Professional platforms feature 4D playback, AI-assisted labeling, auto-complete, active learning

10. **Safety-Critical Precision**: **5-10 cm error** can affect vehicle safety decisions; IoU must exceed 95%

**Comprehensive coverage in Module 09**

---

## 📖 Learning Paths

### Path 1: Perception Engineer
**Goal:** Master AI-based perception systems

1. Module 01: Perception Systems
2. Module 09: LiDAR Technology ⭐
3. Module 10: Datasets & Benchmarks
4. Module 02: Failure Analysis
5. Module 06: AI Safety

### Path 2: Safety Engineer
**Goal:** ISO 26262 and SOTIF certification

1. Module 03: Functional Safety
2. Module 04: SOTIF
3. Module 07: Validation & Verification
4. Module 02: Failure Analysis
5. Module 08: Advanced Topics (Standards Integration)

### Path 3: Cybersecurity Specialist
**Goal:** ISO/SAE 21434 implementation

1. Module 05: Cybersecurity
2. Module 08: Advanced Topics (V2X Security)
3. Module 02: Failure Analysis (Adversarial Attacks)
4. Module 07: Validation & Verification

### Path 4: Research Scientist
**Goal:** AI safety and uncertainty quantification

1. Module 06: AI Safety
2. Module 02: Failure Analysis
3. Module 07: Validation & Verification
4. Module 08: Advanced Topics (XAI, ODD)

### Path 5: Complete Autonomous Systems
**Goal:** End-to-end AV development

All modules in sequence: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10

---

## 🎓 Academic Use

This resource has been used in:
- Graduate courses on autonomous systems
- Professional training programs
- Research projects and publications
- Industry certification preparation

### Citation

If you use this resource in your research, teaching, or industrial work, please cite:

```bibtex
@misc{patel2025av_safety_security,
  author = {Patel, Milin},
  title = {Autonomous Driving: AI Safety and Security},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  version = {2.0.0},
  howpublished = {\url{https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}},
  note = {Comprehensive educational resource on perception systems, functional safety (ISO 26262), SOTIF (ISO 21448), cybersecurity (ISO/SAE 21434), AI safety, and LiDAR technology}
}
```

---

## 🤝 Contributing

Contributions are welcome! Areas for contribution:

- Additional notebooks on emerging topics
- Case studies and real-world examples
- Code optimizations and bug fixes
- Documentation improvements
- Translations to other languages
- Dataset loaders and utilities

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📧 Contact

**Milin Patel**
Hochschule Kempten - University of Applied Sciences
Focus: Autonomous Systems, AI Safety, Functional Safety Standards

- GitHub: [@milinpatel07](https://github.com/milinpatel07)
- Issues: [GitHub Issues](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues)

For questions, please open a GitHub issue with appropriate label.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ISO and SAE** for developing comprehensive safety and security standards
- **KITTI, nuScenes, Waymo** for providing open autonomous driving datasets
- **Open-source community** for tools and frameworks
- **Hochschule Kempten** for supporting this educational initiative
- **Industry partners** for case study contributions and feedback

---

## 📈 Version History

**v2.0.0** (2025-12-04)
- ⭐ NEW: Comprehensive LiDAR technology module (Module 09)
- Reorganized from session-based to topic-based structure
- Enhanced documentation with academic rigor
- Improved code quality and reusability
- Added comprehensive case studies
- Expanded standards integration guidance

**v1.0.0** (2025-01-18)
- Initial release with 5 sessions, 24 notebooks
- Coverage: Perception, Failure Analysis, Standards, Uncertainty, Integration
- ISO 26262, ISO 21448, ISO/SAE 21434 implementation
- 11 exercises with templates

---

## 🔗 Quick Links

- [Module 01: Perception Systems](01_Perception_Systems/)
- [Module 09: LiDAR Technology](09_LiDAR_Technology/) ⭐ NEW
- [Module 03: Functional Safety](03_Functional_Safety/)
- [Module 04: SOTIF](04_SOTIF/)
- [Module 05: Cybersecurity](05_Cybersecurity/)
- [Module 06: AI Safety](06_AI_Safety/)
- [Documentation](docs/)
- [Case Studies](case_studies/)

---

**Getting Started: [Module 01, Notebook 01: SAE Automation Levels](01_Perception_Systems/notebooks/01_sae_automation_levels.ipynb)**

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
