# Autonomous Driving: AI Safety and Security

**A Comprehensive Educational Resource on Building Safe Autonomous Vehicles**

**Author:** Milin Patel | **Institution:** Hochschule Kempten - University of Applied Sciences  
**Version:** 3.0.0 | **License:** MIT

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-ASIL%20D-red.svg)](https://www.iso.org/standard/68383.html)
[![ISO 21448](https://img.shields.io/badge/ISO%2021448-SOTIF-orange.svg)](https://www.iso.org/standard/77490.html)
[![ISO/SAE 21434](https://img.shields.io/badge/ISO%2FSAE%2021434-Cybersecurity-blue.svg)](https://www.iso.org/standard/70918.html)

---

## 📖 What This Repository Is About

This repository teaches you **The Complete Story of Building Safe Autonomous Vehicles** - from understanding how vehicles perceive their environment, to analyzing what can go wrong, to applying international safety and security standards.

**Key Focus:**
- ✅ **Perception Systems**: Cameras, LiDAR, Radar, AI-based detection, sensor fusion
- ✅ **Failure Analysis**: Edge cases, adversarial attacks, out-of-distribution detection
- ✅ **Safety Standards**: ISO 26262 (Functional Safety), ISO 21448 (SOTIF)
- ✅ **Security**: ISO/SAE 21434 (Cybersecurity), V2X security
- ✅ **AI Safety**: Uncertainty quantification, model calibration, trustworthiness
- ✅ **Real-World Application**: Integration challenges, deployment, current limitations

---

## 🎯 Who This Is For

- **Graduate Students**: Autonomous systems, robotics, AI safety, computer vision
- **Engineers**: Perception development, ADAS/AD integration, safety engineering
- **Researchers**: AI safety, uncertainty quantification, verification & validation
- **ML Engineers**: Deep learning for safety-critical applications

**Prerequisites:** Python (intermediate), ML fundamentals, deep learning basics, linear algebra

---

## 📚 Repository Structure - The Story

This repository is organized as **a journey through autonomous vehicle development**:

### PART 1: FOUNDATIONS - Understanding the Challenge

**Module 01: [Perception Systems, Sensors, and Datasets](01_Perception_Systems/)** (7 notebooks)
> *How do autonomous vehicles "see" and understand the world?*

- SAE automation levels (0-5) and system architecture
- All sensor technologies: Camera, LiDAR, Radar
- AI-based object detection (YOLO, R-CNN, DETR)
- Multi-modal sensor fusion strategies
- 3D point cloud processing (LiDAR fundamentals)
- Industry datasets (KITTI, nuScenes, Waymo)
- Safety-critical perception (pedestrian detection)

**Module 02: [Failure Analysis](02_Failure_Analysis/)** (4 notebooks)
> *What can go wrong? Why do perception systems fail?*

- Real-world AV failure case studies (Uber ATG, Tesla)
- Out-of-distribution (OOD) detection methods
- Corner cases and edge cases in driving scenarios
- Adversarial attacks on perception systems

---

### PART 2: SAFETY & SECURITY FRAMEWORK - The Solution

**Module 03: [Functional Safety - ISO 26262](03_Functional_Safety/)** (1 notebook)
> *How do we systematically ensure safety?*

- ISO 26262 fundamentals: V-Model, ASIL classification
- Safety lifecycle for automotive systems
- Application to perception and planning systems

**Module 04: [SOTIF - ISO 21448](04_SOTIF/)** (1 notebook)
> *How do we handle performance limitations and unknown scenarios?*

- Safety of the Intended Functionality (SOTIF)
- Known/unknown safe/unsafe scenario quadrants
- Performance limitation analysis
- Validation strategies for AI systems

**Module 05: [Cybersecurity - ISO/SAE 21434](05_Cybersecurity/)** (1 notebook)
> *How do we protect against malicious actors?*

- Automotive cybersecurity threat landscape
- Threat Analysis and Risk Assessment (TARA)
- Attack vectors: Sensor spoofing, V2X attacks
- Secure development lifecycle

**Module 06: [AI Safety and Trustworthiness](06_AI_Safety/)** (5 notebooks)
> *How do we make AI systems we can trust?*

- Uncertainty types in deep learning (aleatoric, epistemic)
- Uncertainty quantification (MC Dropout, Deep Ensembles)
- Model calibration and reliability (Temperature Scaling, ECE)
- Safety validation and testing for AI
- AI safety standards (ISO 8800, ISO/IEC TR 5469)

---

### PART 3: INTEGRATION & DEPLOYMENT - Making It Real

**Module 08: [Advanced Topics and Integration](08_Advanced_Topics/)** (6 notebooks)
> *How do we deploy safe autonomous systems in the real world?*

- V2X Communication security (C-V2X, DSRC)
- Explainability (XAI): LIME, SHAP, Grad-CAM
- Multi-standard integration (26262 + 21448 + 21434)
- ODD runtime monitoring and fallback strategies
- Industry deployment challenges
- Current standards gaps and open research problems

---

## 📊 Content Summary

**Total:** 25 Jupyter Notebooks (all available)

| Module | Topic | Notebooks | Status |
|--------|-------|-----------|--------|
| 01 | Perception, Sensors, Datasets | 7 | ✅ Complete |
| 02 | Failure Analysis | 4 | ✅ Complete |
| 03 | Functional Safety (ISO 26262) | 1 | ⚠️ Fundamentals only |
| 04 | SOTIF (ISO 21448) | 1 | ⚠️ Fundamentals only |
| 05 | Cybersecurity (ISO/SAE 21434) | 1 | ⚠️ Fundamentals only |
| 06 | AI Safety | 5 | ✅ Complete |
| 08 | Advanced Integration | 6 | ✅ Complete |
| **TOTAL** | **7 Modules** | **25** | **All notebooks exist** |

**Note:** Modules 03-05 provide foundational coverage of safety/security standards. Advanced topics (HARA, ASIL decomposition, TARA) are planned for future releases.

---

## 🚀 Quick Start

### Option 1: Google Colab (Recommended - Zero Setup)

1. Navigate to any module (e.g., [Module 01](01_Perception_Systems/))
2. Click on a notebook file
3. Click "Open in Colab" badge
4. Run cells - dependencies install automatically

**Recommended Path:**
```
Start → 01_Perception → 02_Failure_Analysis → 03_Functional_Safety →
04_SOTIF → 05_Cybersecurity → 06_AI_Safety → 08_Advanced_Topics
```

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

## 🎓 Learning Paths

### Path 1: Perception Engineer
**Goal:** Master AI-based perception systems  
01 Perception → 02 Failure Analysis → 06 AI Safety

### Path 2: Safety Engineer
**Goal:** ISO 26262 and SOTIF certification  
03 Functional Safety → 04 SOTIF → 02 Failure Analysis → 08 Advanced Topics

### Path 3: Security Specialist
**Goal:** ISO/SAE 21434 implementation  
05 Cybersecurity → 08 Advanced Topics (V2X) → 02 Failure Analysis

### Path 4: Complete AV Systems
**Goal:** End-to-end understanding  
All modules in order: 01 → 02 → 03 → 04 → 05 → 06 → 08

---

## 🛠️ Technologies and Frameworks

**Deep Learning:** PyTorch, TensorFlow, Ultralytics YOLOv8  
**Computer Vision:** OpenCV, Open3D (point clouds), MMDetection  
**Uncertainty:** TensorFlow Probability, PyTorch Distributions  
**Datasets:** KITTI, nuScenes, Waymo Open Dataset

---

## 📈 What's NEW in v3.0

### Major Reorganization for Clarity and Honesty

**v3.0.0** (2025-12-28)
- ✅ **Merged modules for logical flow:**
  - Module 01 now includes all perception content (sensors, LiDAR, datasets)
  - Removed artificial separation of LiDAR and Datasets
- ✅ **Fixed all broken links:**
  - All 26 Colab badges now work correctly
  - Internal notebook references updated
- ✅ **Honest content inventory:**
  - Removed claims about non-existent notebooks
  - Clear about what's complete vs. planned
  - Module READMEs reflect actual content
- ✅ **Coherent narrative structure:**
  - Story-based organization (Challenge → Framework → Deployment)
  - Clear learning paths for different roles
  - Better cross-module references

**Previous Versions:**
- **v2.0.0** (2025-12-04): Claimed to add LiDAR module (incomplete - only 1 of 8 notebooks created)
- **v1.0.0** (2025-01-18): Initial release with 24 notebooks

---

## ⚠️ Important Notes on Repository History

### What Changed from v2.0 to v3.0?

**Module Consolidation:**
- ❌ **Module 07 (Validation & Verification)**: Was advertised but had ZERO notebooks - removed from main structure
- ❌ **Module 09 (LiDAR)**: Claimed 8 notebooks, had 1 - merged into Module 01 (Perception)
- ❌ **Module 10 (Datasets)**: Claimed 4 notebooks, had 1 - merged into Module 01 (Perception)

**Why?** Modern AV perception requires integrated understanding of all sensors, not artificial separation. This reorganization reflects real-world engineering practice.

---

## 🔬 Standards Coverage

**ISO 26262 (Functional Safety)** - Module 03  
V-Model, ASIL classification, safety lifecycle

**ISO 21448 (SOTIF)** - Module 04  
Performance limitations, scenario-based validation

**ISO/SAE 21434 (Cybersecurity)** - Module 05  
TARA, attack vectors, secure development

**ISO 8800 / ISO/IEC TR 5469 (AI Safety)** - Module 06  
Trustworthiness, uncertainty quantification, model lifecycle

---

## 📧 Contact & Contributing

**Milin Patel** - Hochschule Kempten  
GitHub: [@milinpatel07](https://github.com/milinpatel07)  
Issues: [GitHub Issues](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/issues)

Contributions welcome! Areas: notebooks, case studies, code optimizations, translations.

---

## 📄 Citation

```bibtex
@misc{patel2025av_safety_security,
  author = {Patel, Milin},
  title = {Autonomous Driving: AI Safety and Security},
  year = {2025},
  publisher = {GitHub},
  version = {3.0.0},
  url = {https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}
}
```

---

## 🔗 Quick Navigation

- [**START HERE:** Module 01 - Perception Systems](01_Perception_Systems/)
- [Module 02 - Failure Analysis](02_Failure_Analysis/)
- [Module 03 - Functional Safety](03_Functional_Safety/)
- [Module 04 - SOTIF](04_SOTIF/)
- [Module 05 - Cybersecurity](05_Cybersecurity/)
- [Module 06 - AI Safety](06_AI_Safety/)
- [Module 08 - Advanced Topics](08_Advanced_Topics/)
- [Comprehensive Documentation](docs/)

---

*This repository provides an honest, comprehensive education resource for autonomous vehicle safety and security. All notebook counts are accurate. All links work. The content flows logically. v3.0 represents a commitment to quality and integrity in technical education.*

**Copyright © 2025 Milin Patel. All Rights Reserved.**
