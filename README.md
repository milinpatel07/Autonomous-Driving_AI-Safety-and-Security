# Autonomous Driving: AI Safety and Security

A comprehensive educational resource on building safe autonomous vehicles.

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security)

---

## About This Repository

This repository provides a structured learning path for understanding autonomous vehicle safety and security. It covers perception systems, failure modes, international safety standards, and practical implementation techniques.

**What you'll learn:**
- Perception systems (cameras, LiDAR, radar, sensor fusion)
- AI-based object detection and tracking
- Failure analysis and edge cases
- Safety standards (ISO 26262, ISO 21448, ISO/SAE 21434)
- AI safety (uncertainty quantification, model calibration)
- Regulatory frameworks and certification
- Real-world deployment challenges

**Who this is for:**
- Graduate students in autonomous systems, robotics, or AI safety
- Engineers working on ADAS/AD systems
- Researchers in computer vision and safety-critical AI
- Anyone preparing for automotive safety roles

---

## Repository Structure

**25 Jupyter notebooks across 8 modules:**

```
Autonomous-Driving_AI-Safety-and-Security/
├── 01_Perception_Systems/     # 7 notebooks - Sensors, detection, fusion
├── 02_Failure_Analysis/       # 4 notebooks - Failures, OOD, adversarial
├── 03_Functional_Safety/      # ISO 26262 fundamentals
├── 04_SOTIF/                  # ISO 21448 fundamentals
├── 05_Cybersecurity/          # ISO/SAE 21434 fundamentals
├── 06_AI_Safety/              # 5 notebooks - Uncertainty, calibration
├── 07_Regulation_Legal/       # Regulatory frameworks (expanding)
├── 08_Advanced_Topics/        # 6 notebooks - Deployment, integration
├── templates/                 # HARA, SOTIF, TARA analysis templates
├── docs/                      # Reference documentation
└── requirements.txt           # Python dependencies
```

---

## Module Overview

### Module 01: Perception Systems (7 notebooks)
How do autonomous vehicles see and understand the world?
- SAE automation levels (J3016) and system architecture
- Sensor technologies (camera, LiDAR, radar)
- AI-based object detection (YOLO, R-CNN, DETR)
- Sensor fusion strategies
- 3D point cloud processing
- Industry datasets (KITTI, nuScenes, Waymo)

[Start here](01_Perception_Systems/)

### Module 02: Failure Analysis (4 notebooks)
What can go wrong and why do perception systems fail?
- Real-world AV incidents (Uber ATG, Tesla Autopilot)
- Out-of-distribution (OOD) detection
- Corner cases and edge cases
- Adversarial attacks on perception

[Learn more](02_Failure_Analysis/)

### Module 03: Functional Safety - ISO 26262
How do we systematically ensure safety?
- ISO 26262 fundamentals and structure
- V-Model development lifecycle
- ASIL classification (A/B/C/D)
- Hazard Analysis and Risk Assessment (HARA)

[Learn more](03_Functional_Safety/)

### Module 04: SOTIF - ISO 21448
How do we handle performance limitations and unknown scenarios?
- Safety of the Intended Functionality
- Known/unknown safe/unsafe scenarios (4-quadrant model)
- Triggering conditions and validation strategies

[Learn more](04_SOTIF/)

### Module 05: Cybersecurity - ISO/SAE 21434
How do we protect against malicious actors?
- Automotive cybersecurity threat landscape
- Threat Analysis and Risk Assessment (TARA)
- Sensor spoofing and V2X attacks
- Safety-security integration

[Learn more](05_Cybersecurity/)

### Module 06: AI Safety (5 notebooks)
How do we make AI systems we can trust?
- Uncertainty types (aleatoric vs epistemic)
- Uncertainty quantification (MC Dropout, Deep Ensembles)
- Model calibration (Temperature Scaling, ECE)
- Safety validation and testing
- AI safety standards (ISO/PAS 8800)

[Learn more](06_AI_Safety/)

### Module 07: Regulation and Legal Framework
How do regulations govern autonomous vehicle deployment?
- International regulatory frameworks (UNECE WP.29)
- Regional regulations (EU, US, China)
- Certification and type approval
- Liability frameworks

[Learn more](07_Regulation_Legal/)

### Module 08: Advanced Topics (6 notebooks)
How do we deploy safe systems in the real world?
- V2X communication security
- Explainability (LIME, SHAP, Grad-CAM)
- Multi-standard integration
- Runtime monitoring and ODD
- Industry deployment challenges
- Standards gaps and open problems

[Learn more](08_Advanced_Topics/)

---

## Quick Start

### Option 1: Google Colab (Recommended)
1. Navigate to any module folder
2. Click on a notebook
3. Click the "Open in Colab" badge
4. Run the cells - dependencies install automatically

**Start with:** [01_sae_automation_levels.ipynb](01_Perception_Systems/notebooks/01_sae_automation_levels.ipynb)

### Option 2: Local Installation
```bash
git clone https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git
cd Autonomous-Driving_AI-Safety-and-Security

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
jupyter lab
```

---

## Learning Paths

**Complete Path (Recommended):**
```
01 Perception → 02 Failures → 03 ISO 26262 → 04 SOTIF → 05 Cybersecurity → 06 AI Safety → 07 Regulation → 08 Advanced
```

**Perception Focus:**
```
01 Perception → 02 Failure Analysis → 06 AI Safety
```

**Safety Standards Focus:**
```
03 Functional Safety → 04 SOTIF → 05 Cybersecurity → 07 Regulation → 08 Advanced Topics
```

**Security Focus:**
```
05 Cybersecurity → 02 Failure Analysis (Adversarial) → 08 Advanced Topics (V2X)
```

---

## Standards Covered

| Standard | Topic | Module |
|----------|-------|--------|
| **ISO 26262** | Functional Safety | Module 03 |
| **ISO 21448** | Safety of Intended Functionality (SOTIF) | Module 04 |
| **ISO/SAE 21434** | Cybersecurity Engineering | Module 05 |
| **ISO/PAS 8800** | Safety and Artificial Intelligence | Module 06 |
| **ISO/IEC TR 5469** | AI Functional Safety | Module 06 |
| **SAE J3016** | Automation Levels | Module 01 |
| **UNECE R155/R156/R157** | UN Regulations | Module 07 |

---

## Templates

The `/templates` folder contains analysis templates for practical application:

- **HARA_Template.md** - Hazard Analysis and Risk Assessment (ISO 26262)
- **SOTIF_Analysis_Template.md** - SOTIF Analysis (ISO 21448)
- **TARA_Template.md** - Threat Analysis and Risk Assessment (ISO/SAE 21434)

[View templates](templates/)

---

## Technologies Used

| Category | Tools |
|----------|-------|
| **Deep Learning** | PyTorch, TensorFlow, Ultralytics YOLOv8 |
| **Computer Vision** | OpenCV, Open3D, MMDetection |
| **Datasets** | KITTI, nuScenes, Waymo Open Dataset |
| **Uncertainty** | TensorFlow Probability, PyTorch Distributions |
| **Visualization** | Matplotlib, Seaborn, Plotly |

---

## Version History

**v3.1.0** (2025-01-22) - Structural improvements
- Added Module 07 (Regulation and Legal Framework)
- Consolidated templates into shared `/templates` folder
- Fixed all Colab badge links
- Cleaned up formatting across notebooks
- Improved learning path documentation

**v3.0.0** (2025-12-28) - Clean, honest, focused
- Removed empty modules
- Simplified structure to working notebooks
- All links verified

**v2.0.0** (2025-12-04) - Restructure
- Reorganized module structure

**v1.0.0** (2025-01-18) - Initial release

---

## Contributing

Contributions are welcome. Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

For major changes, please open an issue first to discuss.

---

## Contact

**Milin Patel**
Hochschule Kempten - University of Applied Sciences
GitHub: [@milinpatel07](https://github.com/milinpatel07)

Questions or suggestions? [Open an issue](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues)

---

## Citation

```bibtex
@misc{patel2025av_safety,
  author = {Patel, Milin},
  title = {Autonomous Driving: AI Safety and Security},
  year = {2025},
  publisher = {GitHub},
  version = {3.1.0},
  url = {https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}
}
```

---

**Copyright (c) 2025 Milin Patel. All Rights Reserved.**
