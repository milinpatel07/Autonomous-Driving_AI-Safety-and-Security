# Autonomous Driving: AI Safety and Security

A structured, hands-on learning resource covering perception systems, functional safety, cybersecurity, and AI safety for autonomous vehicles — aligned with ISO 26262, ISO 21448, ISO/SAE 21434, and ISO/PAS 8800.

**Author:** [Milin Patel](https://github.com/milinpatel07) · Hochschule Kempten — University of Applied Sciences

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/)

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Modules](#modules)
  - [01 — Perception Systems](#01--perception-systems)
  - [02 — Failure Analysis](#02--failure-analysis)
  - [03 — Functional Safety (ISO 26262)](#03--functional-safety-iso-26262)
  - [04 — SOTIF (ISO 21448)](#04--sotif-iso-21448)
  - [05 — Cybersecurity (ISO/SAE 21434)](#05--cybersecurity-isosae-21434)
  - [06 — AI Safety (ISO/PAS 8800)](#06--ai-safety-isopas-8800)
  - [07 — Integration and Deployment](#07--integration-and-deployment)
- [Templates](#templates)
- [Learning Paths](#learning-paths)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Option A: Google Colab (Recommended)](#option-a-google-colab-recommended)
  - [Option B: Local Installation](#option-b-local-installation)
- [Standards and Regulations Covered](#standards-and-regulations-covered)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## Overview

Autonomous vehicles depend on the safe and secure interaction of perception, decision-making, and control systems. This repository provides **33 Jupyter notebooks** and **3 professional templates** organized into 7 progressive modules that cover:

- **Perception** — How autonomous vehicles sense their environment (cameras, LiDAR, radar, sensor fusion)
- **Failure analysis** — Real-world incidents (Uber, Tesla, Cruise), adversarial attacks, and edge cases
- **Functional safety** — Systematic hazard analysis using ISO 26262 (HARA, FMEA, ASIL, V&V)
- **SOTIF** — Performance limitations and triggering conditions under ISO 21448
- **Cybersecurity** — Threat modeling and attack surface analysis per ISO/SAE 21434
- **AI safety** — Uncertainty quantification, calibration, and trustworthiness under ISO/PAS 8800
- **Integration** — V2X communication, explainability (XAI), regulations (UNECE R155/R156, EU AI Act)

Each notebook is self-contained, executable in Google Colab with a single click, and includes explanations, working code, visualizations, and exercises.

---

## Repository Structure

```
Autonomous-Driving_AI-Safety-and-Security/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
│
├── 01_Perception_Systems/
│   └── notebooks/
│       ├── 01_sae_automation_levels.ipynb
│       ├── 02_sensor_technologies.ipynb
│       ├── 03_object_detection.ipynb
│       ├── 04_sensor_fusion.ipynb
│       ├── 05_pedestrian_detection.ipynb
│       ├── 06_lidar_sensor_fundamentals.ipynb
│       └── 07_dataset_overview.ipynb
│
├── 02_Failure_Analysis/
│   └── notebooks/
│       ├── 01_av_failure_case_studies.ipynb
│       ├── 02_ood_detection.ipynb
│       ├── 03_corner_cases_edge_cases.ipynb
│       └── 04_adversarial_attacks.ipynb
│
├── 03_Functional_Safety/
│   └── notebooks/
│       ├── 01_iso_26262_fundamentals.ipynb
│       ├── 02_hara_methodology.ipynb
│       ├── 03_fmea_analysis.ipynb
│       └── 04_verification_validation.ipynb
│
├── 04_SOTIF/
│   └── notebooks/
│       ├── 01_sotif_fundamentals.ipynb
│       ├── 02_scenario_analysis.ipynb
│       ├── 03_ood_detection_sotif.ipynb
│       └── 04_simulation_sotif_validation.ipynb
│
├── 05_Cybersecurity/
│   └── notebooks/
│       ├── 01_automotive_cybersecurity.ipynb
│       ├── 02_tara_methodology.ipynb
│       └── 03_attack_surface_analysis.ipynb
│
├── 06_AI_Safety/
│   └── notebooks/
│       ├── 01_ai_safety_standards.ipynb
│       ├── 02_uncertainty_types.ipynb
│       ├── 03_mc_dropout_ensembles.ipynb
│       ├── 04_calibration_reliability.ipynb
│       └── 05_safety_validation_testing.ipynb
│
├── 07_Integration_Deployment/
│   └── notebooks/
│       ├── 01_v2x_communication.ipynb
│       ├── 02_explainability_xai.ipynb
│       ├── 03_standards_integration.ipynb
│       ├── 04_industry_deployment.ipynb
│       ├── 05_odd_runtime_monitoring.ipynb
│       ├── 06_standards_gaps.ipynb
│       └── 07_regulations_type_approval.ipynb
│
└── templates/
    ├── HARA_Template.md
    ├── TARA_Template.md
    └── SOTIF_Analysis_Template.md
```

---

## Modules

### 01 — Perception Systems

How autonomous vehicles perceive their surroundings through sensors and algorithms.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_sae_automation_levels` | SAE J3016 levels (L0–L5), ODD definition, system architecture | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/01_sae_automation_levels.ipynb) |
| 2 | `02_sensor_technologies` | Camera, LiDAR, and radar — capabilities, limitations, trade-offs | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/02_sensor_technologies.ipynb) |
| 3 | `03_object_detection` | YOLO, Faster R-CNN, DETR — architectures and evaluation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/03_object_detection.ipynb) |
| 4 | `04_sensor_fusion` | Early, late, and deep fusion strategies for multi-sensor systems | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/04_sensor_fusion.ipynb) |
| 5 | `05_pedestrian_detection` | Specialized detection for vulnerable road users | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/05_pedestrian_detection.ipynb) |
| 6 | `06_lidar_sensor_fundamentals` | 3D point cloud processing and LiDAR data pipelines | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/06_lidar_sensor_fundamentals.ipynb) |
| 7 | `07_dataset_overview` | KITTI, nuScenes, and Waymo Open Dataset — structure and usage | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/01_Perception_Systems/notebooks/07_dataset_overview.ipynb) |

---

### 02 — Failure Analysis

Learning from real-world failures and understanding robustness challenges.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_av_failure_case_studies` | Uber ATG (2018), Tesla Autopilot, Cruise incidents — root causes and lessons | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/02_Failure_Analysis/notebooks/01_av_failure_case_studies.ipynb) |
| 2 | `02_ood_detection` | Out-of-distribution detection — techniques and safety implications | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/02_Failure_Analysis/notebooks/02_ood_detection.ipynb) |
| 3 | `03_corner_cases_edge_cases` | Identifying and testing corner cases and edge cases | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/02_Failure_Analysis/notebooks/03_corner_cases_edge_cases.ipynb) |
| 4 | `04_adversarial_attacks` | Adversarial perturbations, physical attacks, and defenses | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/02_Failure_Analysis/notebooks/04_adversarial_attacks.ipynb) |

---

### 03 — Functional Safety (ISO 26262)

Systematic methods for identifying, classifying, and mitigating safety risks.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_iso_26262_fundamentals` | V-Model, safety lifecycle, ASIL determination | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/03_Functional_Safety/notebooks/01_iso_26262_fundamentals.ipynb) |
| 2 | `02_hara_methodology` | Hazard Analysis and Risk Assessment — worked examples | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/03_Functional_Safety/notebooks/02_hara_methodology.ipynb) |
| 3 | `03_fmea_analysis` | Failure Mode and Effects Analysis for AV components | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/03_Functional_Safety/notebooks/03_fmea_analysis.ipynb) |
| 4 | `04_verification_validation` | V&V strategies, test coverage, and compliance evidence | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/03_Functional_Safety/notebooks/04_verification_validation.ipynb) |

---

### 04 — SOTIF (ISO 21448)

Addressing performance limitations and insufficiencies of the intended functionality.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_sotif_fundamentals` | ISO 21448 principles, four scenario categories (S1–S4) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/04_SOTIF/notebooks/01_sotif_fundamentals.ipynb) |
| 2 | `02_scenario_analysis` | Triggering condition identification and scenario generation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/04_SOTIF/notebooks/02_scenario_analysis.ipynb) |
| 3 | `03_ood_detection_sotif` | Out-of-distribution detection applied to SOTIF validation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/04_SOTIF/notebooks/03_ood_detection_sotif.ipynb) |
| 4 | `04_simulation_sotif_validation` | Simulation-based testing and scenario coverage analysis | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/04_SOTIF/notebooks/04_simulation_sotif_validation.ipynb) |

---

### 05 — Cybersecurity (ISO/SAE 21434)

Protecting autonomous vehicles against cyber threats across the development lifecycle.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_automotive_cybersecurity` | ISO/SAE 21434 framework, cybersecurity management systems | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/05_Cybersecurity/notebooks/01_automotive_cybersecurity.ipynb) |
| 2 | `02_tara_methodology` | Threat Analysis and Risk Assessment — step-by-step methodology | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/05_Cybersecurity/notebooks/02_tara_methodology.ipynb) |
| 3 | `03_attack_surface_analysis` | Attack surface identification, threat modeling, and mitigations | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/05_Cybersecurity/notebooks/03_attack_surface_analysis.ipynb) |

---

### 06 — AI Safety (ISO/PAS 8800)

Ensuring trustworthiness, reliability, and safety of AI/ML components.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_ai_safety_standards` | ISO/PAS 8800 framework, trustworthiness characteristics | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/06_AI_Safety/notebooks/01_ai_safety_standards.ipynb) |
| 2 | `02_uncertainty_types` | Aleatoric vs. epistemic uncertainty in deep learning | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/06_AI_Safety/notebooks/02_uncertainty_types.ipynb) |
| 3 | `03_mc_dropout_ensembles` | MC Dropout, deep ensembles — uncertainty quantification | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/06_AI_Safety/notebooks/03_mc_dropout_ensembles.ipynb) |
| 4 | `04_calibration_reliability` | Confidence calibration, ECE, reliability diagrams | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/06_AI_Safety/notebooks/04_calibration_reliability.ipynb) |
| 5 | `05_safety_validation_testing` | Safety validation strategies for AI-based systems | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/06_AI_Safety/notebooks/05_safety_validation_testing.ipynb) |

---

### 07 — Integration and Deployment

Bringing safety, security, and AI together — from standards compliance to real-world deployment.

| # | Notebook | Topic | Open |
|---|----------|-------|------|
| 1 | `01_v2x_communication` | Vehicle-to-Everything (V2X) communication and safety | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/01_v2x_communication.ipynb) |
| 2 | `02_explainability_xai` | Explainable AI (XAI) for safety-critical decision-making | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/02_explainability_xai.ipynb) |
| 3 | `03_standards_integration` | Integrating ISO 26262, ISO 21448, and ISO/SAE 21434 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/03_standards_integration.ipynb) |
| 4 | `04_industry_deployment` | Industry deployment challenges and operational readiness | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/04_industry_deployment.ipynb) |
| 5 | `05_odd_runtime_monitoring` | ODD monitoring, runtime safety checks, and degradation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/05_odd_runtime_monitoring.ipynb) |
| 6 | `06_standards_gaps` | Open problems and gaps in current safety/security standards | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/06_standards_gaps.ipynb) |
| 7 | `07_regulations_type_approval` | UNECE R155/R156, EU AI Act, and type approval pathways | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/master/07_Integration_Deployment/notebooks/07_regulations_type_approval.ipynb) |

---

## Templates

Ready-to-use analysis templates for professional safety and security work. Each template follows the structure defined in its reference standard, includes worked examples, and provides guidance for completing each section.

| Template | Standard | Purpose |
|----------|----------|---------|
| [HARA Template](templates/HARA_Template.md) | ISO 26262 | Hazard Analysis and Risk Assessment — hazard identification, ASIL determination, safety goals |
| [TARA Template](templates/TARA_Template.md) | ISO/SAE 21434 | Threat Analysis and Risk Assessment — asset identification, threat scenarios, CAL determination |
| [SOTIF Analysis Template](templates/SOTIF_Analysis_Template.md) | ISO 21448 | SOTIF evaluation — ODD definition, triggering conditions, scenario categorization (S1–S4) |

---

## Learning Paths

Choose a path based on your goals:

**Complete path** (all 33 notebooks):
> 01 Perception → 02 Failure Analysis → 03 Functional Safety → 04 SOTIF → 05 Cybersecurity → 06 AI Safety → 07 Integration

**Perception and AI focus** (16 notebooks):
> 01 Perception → 02 Failure Analysis → 06 AI Safety

**Safety standards focus** (19 notebooks):
> 03 Functional Safety → 04 SOTIF → 05 Cybersecurity → 07 Integration

**Quick standards overview** (4 notebooks):
> `03/01` ISO 26262 Fundamentals → `04/01` SOTIF Fundamentals → `05/01` Automotive Cybersecurity → `06/01` AI Safety Standards

---

## Getting Started

### Prerequisites

- Python 3.8 or later
- Basic familiarity with Python, NumPy, and Matplotlib
- Background in engineering, computer science, or automotive systems (helpful but not required)

### Option A: Google Colab (Recommended)

Click any **Open in Colab** badge in the module tables above. No local setup is needed — each notebook installs its own dependencies automatically.

### Option B: Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git
cd Autonomous-Driving_AI-Safety-and-Security

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter lab
```

> **GPU support:** For local GPU acceleration, install PyTorch with CUDA following the [official instructions](https://pytorch.org/get-started/locally/).

---

## Standards and Regulations Covered

### Safety and Security Standards

| Standard | Scope | Modules |
|----------|-------|---------|
| **ISO 26262:2018** | Functional safety of road vehicles | 03, 07 |
| **ISO 21448:2022** | Safety of the intended functionality (SOTIF) | 04, 07 |
| **ISO/SAE 21434:2021** | Cybersecurity engineering for road vehicles | 05, 07 |
| **ISO/PAS 8800** | Safety and artificial intelligence | 06, 07 |
| **SAE J3016** | Taxonomy of driving automation | 01 |
| **ISO/IEC 24028** | Trustworthiness in AI — overview | 06 |

### Regulatory Frameworks

| Regulation | Scope | Module |
|------------|-------|--------|
| **UNECE R155** | Cybersecurity management system requirements | 07 |
| **UNECE R156** | Software update management system requirements | 07 |
| **EU AI Act** | Risk-based regulation of artificial intelligence systems | 07 |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project, including how to report issues, suggest improvements, and submit pull requests.

---

## Citation

If you use this material in academic or professional work, please cite:

```bibtex
@misc{patel2025av_safety,
  author       = {Patel, Milin},
  title        = {Autonomous Driving: AI Safety and Security},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2025 Milin Patel
