# Autonomous Driving: AI Safety and Security

A comprehensive educational resource on building safe autonomous vehicles.

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## About This Repository

This repository teaches you how to build safe autonomous vehicles - from perception systems to safety standards. You'll learn how vehicles see the world, what can go wrong, and how to apply international safety and security standards.

**What you'll learn:**
- Perception systems (cameras, LiDAR, radar, sensor fusion)
- AI-based object detection and tracking
- Failure analysis and edge cases
- Safety standards (ISO 26262, ISO 21448, ISO/SAE 21434)
- AI safety (uncertainty quantification, model calibration)
- Real-world deployment challenges

**Who this is for:**
- Graduate students in autonomous systems, robotics, or AI safety
- Engineers working on ADAS/AD systems
- Researchers in computer vision and safety-critical AI
- Anyone who wants to understand how safe autonomous vehicles are built

---

## Repository Structure

**25 Jupyter notebooks across 7 modules:**

### Module 01: Perception Systems (7 notebooks)
How do autonomous vehicles see and understand the world?
- SAE automation levels and system architecture
- Sensor technologies (camera, LiDAR, radar)
- AI-based object detection (YOLO, R-CNN, DETR)
- Sensor fusion strategies
- 3D point cloud processing
- Industry datasets (KITTI, nuScenes, Waymo)
- Pedestrian detection (safety-critical application)

[Start here →](01_Perception_Systems/)

### Module 02: Failure Analysis (4 notebooks)
What can go wrong and why do perception systems fail?
- Real-world AV incidents (Uber ATG, Tesla)
- Out-of-distribution detection
- Corner cases and edge cases
- Adversarial attacks on perception

[Learn more →](02_Failure_Analysis/)

### Module 03: Functional Safety - ISO 26262 (1 notebook)
How do we systematically ensure safety?
- ISO 26262 fundamentals and V-Model
- ASIL classification
- Safety lifecycle for automotive systems

[Learn more →](03_Functional_Safety/)

### Module 04: SOTIF - ISO 21448 (1 notebook)
How do we handle performance limitations and unknown scenarios?
- Safety of the Intended Functionality
- Known/unknown safe/unsafe scenarios
- Validation strategies for AI systems

[Learn more →](04_SOTIF/)

### Module 05: Cybersecurity - ISO/SAE 21434 (1 notebook)
How do we protect against malicious actors?
- Automotive cybersecurity threat landscape
- Threat Analysis and Risk Assessment (TARA)
- Sensor spoofing and V2X attacks

[Learn more →](05_Cybersecurity/)

### Module 06: AI Safety (5 notebooks)
How do we make AI systems we can trust?
- Uncertainty types (aleatoric vs epistemic)
- Uncertainty quantification (MC Dropout, Deep Ensembles)
- Model calibration (Temperature Scaling, ECE)
- Safety validation and testing
- AI safety standards (ISO/PAS 8800, ISO/IEC TR 5469)

[Learn more →](06_AI_Safety/)

### Module 08: Advanced Topics (6 notebooks)
How do we deploy safe systems in the real world?
- V2X communication security
- Explainability (LIME, SHAP, Grad-CAM)
- Multi-standard integration (26262 + 21448 + 21434)
- Runtime monitoring and fallback strategies
- Industry deployment challenges
- Current standards gaps and open problems

[Learn more →](08_Advanced_Topics/)

---

## Quick Start

### Option 1: Google Colab (Recommended)
1. Navigate to any module folder
2. Click on a notebook
3. Click the "Open in Colab" badge
4. Run the cells - dependencies install automatically

**Start with:** [Module 01 - Perception Systems](01_Perception_Systems/)

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
01 → 02 → 03 → 04 → 05 → 06 → 08

**Perception Focus:**
01 Perception → 02 Failure Analysis → 06 AI Safety

**Safety Focus:**
03 Functional Safety → 04 SOTIF → 02 Failure Analysis → 08 Advanced Topics

**Security Focus:**
05 Cybersecurity → 08 Advanced Topics → 02 Failure Analysis

---

## Standards Covered

- **ISO 26262** - Functional Safety for Road Vehicles
- **ISO 21448 (SOTIF)** - Safety of the Intended Functionality
- **ISO/SAE 21434** - Cybersecurity Engineering
- **ISO/PAS 8800** - Safety and Artificial Intelligence
- **ISO/IEC TR 5469** - AI Management System

---

## Technologies Used

**Deep Learning:** PyTorch, TensorFlow, Ultralytics YOLOv8
**Computer Vision:** OpenCV, Open3D, MMDetection
**Datasets:** KITTI, nuScenes, Waymo Open Dataset
**Uncertainty:** TensorFlow Probability, PyTorch Distributions

---

## Version History

**v3.0.0** (2025-12-28) - Clean, honest, focused
- Removed fake/empty modules
- Simplified structure to 7 modules with 25 real notebooks
- All links verified and working
- Authentic documentation

**v2.0.0** (2025-12-04) - Overambitious claims
- Claimed many notebooks that didn't exist
- Confusing structure with deprecated modules

**v1.0.0** (2025-01-18) - Initial release
- 24 notebooks across 8 modules

---

## Contact

**Milin Patel**
Hochschule Kempten - University of Applied Sciences
GitHub: [@milinpatel07](https://github.com/milinpatel07)

Found a bug or have a suggestion? [Open an issue](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues)

---

## Citation

```bibtex
@misc{patel2025av_safety,
  author = {Patel, Milin},
  title = {Autonomous Driving: AI Safety and Security},
  year = {2025},
  publisher = {GitHub},
  version = {3.0.0},
  url = {https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}
}
```

---

**Copyright © 2025 Milin Patel. All Rights Reserved.**
