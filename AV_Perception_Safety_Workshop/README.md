# AI and Safety Aspects in Autonomous Driving - Workshop

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**Total **Status:** ✅ **COMPLETE - All 4 Sessions Ready!**

[![All Sessions Complete](https://img.shields.io/badge/Sessions-4%2F4%20Complete-success.svg)]()
[![Notebooks](https://img.shields.io/badge/Notebooks-18%20Total-blue.svg)]()
[![Google Colab Ready](https://img.shields.io/badge/Google%20Colab-Ready-orange.svg)](https://colab.research.google.com/)

## 🎯 Workshop Overview

This comprehensive, hands-on workshop provides complete coverage of AI-based perception systems in autonomous vehicles, their failure modes, safety and security standards, uncertainty estimation, and validation techniques. Participants will gain both theoretical knowledge and practical implementation experience through 18 interactive Jupyter notebooks, all runnable in Google Colab.

## 📋 Workshop Schedule (All Sessions Available)

| Session | Duration | Topic | Notebooks |
|---------|----------|-------|-----------|
| **Session 1** | 90-100 min | **AI-based Perception Systems** | 01-06 (6 notebooks) |
| **Session 2** | 90 min | **Failure Modes and Edge Cases** | 07-10 (4 notebooks) |
| **Session 3** | 120 min | **Safety and Security Standards** | 11-14 (4 notebooks) |
| **Session 4** | 90 min | **Uncertainty Estimation and Validation** | 15-18 (4 notebooks) |
| **TOTAL** | **6-7 hours** | **Complete Workshop** | **18 notebooks** |

### Recommended Workshop Formats

**Option A: Full-Day Workshop** (6-7 hours with breaks)
- Morning: Sessions 1 & 2 (3 hours + 15 min break)
- Afternoon: Sessions 3 & 4 (3.5 hours + 15 min break)

**Option B: Multi-Day Workshop** (2 days)
- Day 1: Sessions 1 & 2 (AI Perception + Failures)
- Day 2: Sessions 3 & 4 (Standards + Validation)

**Option C: Self-Paced Online Learning**
- Work through all 18 notebooks at your own pace
- All notebooks work independently in Google Colab

## 🎓 Learning Objectives

By the end of this workshop, participants will be able to:

### Technical Knowledge
- ✅ Understand SAE J3016 levels of driving automation
- ✅ Explain autonomous vehicle perception architecture
- ✅ Compare sensor modalities (Camera, LiDAR, Radar) and sensor fusion
- ✅ Implement and evaluate object detection models
- ✅ Explore and analyze autonomous driving datasets

### Safety & Standards
- ✅ Identify failure modes in ML-based perception systems
- ✅ Apply ISO 26262, ISO 21448 (SOTIF), ISO 8800, and ISO 21434 standards
- ✅ Analyze real-world autonomous vehicle accidents
- ✅ Understand Operational Design Domain (ODD)

### Uncertainty & Robustness
- ✅ Quantify uncertainty in object detection
- ✅ Implement Monte Carlo Dropout and ensemble methods
- ✅ Build safer decision-making systems with uncertainty estimates
- ✅ Deploy real-time perception on embedded systems (Raspberry Pi)

## 📂 Repository Structure

```
AV_Perception_Safety_Workshop/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── setup_instructions.md              # Installation guide
├── LICENSE                            # MIT License
│
├── Session_1_AI_Perception_Systems/
│   ├── README.md                      # Session 1 detailed guide
│   ├── notebooks/                     # Interactive Jupyter notebooks (6)
│   ├── scripts/                       # Python utilities
│   ├── data/                          # Sample images and point clouds
│   ├── exercises/                     # Hands-on exercises + solutions
│   ├── resources/                     # Links, datasets, references
│   └── slides/                        # Presentation materials
│
├── Session_2_Failure_Modes/
│   ├── README.md
│   ├── notebooks/                     # Failure analysis notebooks
│   ├── case_studies/                  # Uber ATG, Tesla accidents
│   └── exercises/
│
├── Session_3_Safety_Standards/
│   ├── README.md
│   ├── notebooks/                     # Standards application
│   ├── standards_docs/                # ISO summaries
│   └── exercises/
│
└── Session_4_Uncertainty_Estimation/
    ├── README.md
    ├── notebooks/                     # Uncertainty quantification
    ├── scripts/                       # MC Dropout, ensembles
    ├── raspberry_pi_demo/             # Embedded deployment
    └── exercises/
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Jupyter Lab or Jupyter Notebook
- GPU recommended (not required for most exercises)
- 10 GB free disk space for datasets

### Installation

1. **Clone this repository**
```bash
git clone <repository-url>
cd AV_Perception_Safety_Workshop
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download sample datasets** (optional, for offline use)
```bash
python scripts/download_datasets.py
```

5. **Launch Jupyter**
```bash
jupyter lab
```

6. **Navigate to Session 1** and open the first notebook!

## 📚 Complete Session Contents

### Session 1: AI-based Perception Systems (90-100 min) ✅
**Location:** `Session_1_AI_Perception_Systems/`

**All 6 Notebooks:**
1. **01_Introduction_SAE_Levels.ipynb** - SAE J3016 automation levels, ODD, AV architecture
2. **02_Sensor_Modalities_Visualization.ipynb** (15-20 min) - Camera, LiDAR, Radar comparison with 3D visualizations
3. **03_Object_Detection_Demo.ipynb** - YOLOv8 implementation, real-time inference, failure analysis
4. **04_Dataset_Exploration.ipynb** - KITTI, nuScenes, Waymo datasets analysis and comparison
5. **05_Sensor_Fusion_Basics.ipynb** - Early, late, deep fusion with working code implementations
6. **06_Pedestrian_Detection_Case_Study.ipynb** - Safety-critical pedestrian detection, ISO 26262 ASIL-D

**Key Features:**
- All notebooks work in Google Colab (zero setup!)
- Interactive visualizations and working code
- Real-world AV examples and datasets
- Exercises with solutions
- Links to Hugging Face demos

---

### Session 2: Failure Modes and Edge Cases ✅
**Location:** `Session_2_Failure_Modes_and_Edge_Cases/`

**All 4 Notebooks:**
7. **07_AV_Failure_Case_Studies.ipynb** - Uber ATG, Tesla, Cruise accidents with NTSB analysis
8. **08_OOD_Detection.ipynb** - 4 OOD detection methods with implementations (Mahalanobis, Energy-based, MC Dropout)
9. **09_Corner_Cases_and_Edge_Cases.ipynb** - Long-tail distribution, risk matrices, combinatorial scenarios
10. **10_Adversarial_Attacks_on_Perception.ipynb** - FGSM, PGD attacks, sensor spoofing, defenses, ISO/SAE 21434

**Key Features:**
- Real accident analysis with root causes
- Working implementations of all OOD methods
- Adversarial attack code demonstrations
- Connection to ISO 21448 SOTIF
- Cybersecurity threat analysis (TARA)

---

### Session 3: Safety and Security Standards ✅
**Location:** `Session_3_Safety_and_Security_Standards/`

**All 4 Notebooks:**
11. **11_ISO_26262_Functional_Safety.ipynb** - V-Model, ASIL classification, HARA methodology
12. **12_ISO_21448_SOTIF.ipynb** - Four scenario categories, triggering conditions, SOTIF process
13. **13_ISO_8800_AI_Safety.ipynb** - AI trustworthiness, data quality, model monitoring, human-AI interaction
14. **14_ISO_SAE_21434_Cybersecurity.ipynb** - TARA methodology, CAL levels, penetration testing

**Key Features:**
- Complete HARA and TARA templates (markdown)
- Interactive worksheets for standards compliance
- Real-world safety analysis examples
- Integration guide showing how standards work together
- Professional, standards-compliant terminology

---

### Session 4: Uncertainty Estimation and Validation ✅
**Location:** `Session_4_Uncertainty_Estimation_and_Validation/`

**All 4 Notebooks:**
15. **15_Uncertainty_Types_in_Deep_Learning.ipynb** - Aleatoric vs epistemic uncertainty, sources in AV perception
16. **16_MC_Dropout_and_Ensembles.ipynb** - Complete implementations of Monte Carlo Dropout and Deep Ensembles
17. **17_Calibration_and_Reliability.ipynb** - ECE metric, temperature scaling, reliability diagrams
18. **18_Safety_Validation_and_Testing.ipynb** - Pegasus 6-layer model, scenario-based testing, statistical evidence

**Key Features:**
- Working Python scripts (uncertainty.py, calibration.py, validation.py)
- Production-ready code for uncertainty quantification
- Complete validation plan templates
- Connection to ISO 26262 V&V requirements
- Statistical analysis (Kalra & Paddock "billion miles")

## 🛠️ Technologies Used

- **Deep Learning:** PyTorch, Ultralytics (YOLOv8), Detectron2
- **Data Processing:** NumPy, Pandas, OpenCV
- **3D Visualization:** Open3D, Matplotlib, Plotly
- **Datasets:** KITTI, nuScenes, Waymo Open Dataset, COCO
- **Uncertainty:** PyTorch MC Dropout, Laplace approximation
- **Embedded:** Raspberry Pi 4, picamera2

## 📖 Datasets Used

| Dataset | Sensors | Size | Use Case |
|---------|---------|------|----------|
| **KITTI** | Camera, LiDAR | 15K frames | Classic benchmark, object detection |
| **nuScenes** | Camera, LiDAR, Radar | 1.4M images | Multi-sensor fusion, all-weather |
| **Waymo Open** | Camera, LiDAR | 1000+ scenes | Diverse conditions, large-scale |
| **COCO** | Camera | 330K images | General object detection training |
| **BDD100K** | Camera | 100K videos | Diverse geography, weather |

**Download instructions:** See `Session_1_AI_Perception_Systems/resources/datasets.md`

## 🔗 External Resources

- **Interactive Demos:**
  - nuScenes Explorer: https://www.nuscenes.org/nuscenes#explore
  - Waymo Viewer: https://waymo.com/open/viewer/
  - YOLOv8 Live Demo: https://huggingface.co/spaces/Xenova/yolov9-web

- **Documentation:**
  - SAE J3016 Standard: https://www.sae.org/standards/content/j3016_202104/
  - ISO 26262 Overview: https://www.iso.org/standard/68383.html
  - ISO 21448 (SOTIF): https://www.iso.org/standard/77490.html

- **Code Repositories:**
  - Apollo Auto: https://github.com/ApolloAuto/apollo
  - Autoware: https://github.com/autowarefoundation/autoware
  - OpenPCDet: https://github.com/open-mmlab/OpenPCDet

Full resource list: `Session_1_AI_Perception_Systems/resources/links.md`

## 🧪 Hands-On Exercises

Each session includes practical exercises:

- **Beginner:** Follow guided notebooks, modify parameters
- **Intermediate:** Implement extensions, analyze results
- **Advanced:** Design custom solutions, compare approaches

Solutions provided in `exercises/solutions/` (try first before looking!)

## 🏆 Workshop Outcomes

Participants will leave with:
1. ✅ Working Jupyter notebooks for perception tasks
2. ✅ Trained object detection models
3. ✅ Understanding of safety standards application
4. ✅ Uncertainty-aware perception system prototype
5. ✅ Code repository for future reference
6. ✅ Links to datasets and tools for continued learning

## 🤝 Contributing

This workshop material is designed for educational use. If you find errors or have suggestions:
1. Open an issue describing the problem
2. Submit a pull request with improvements
3. Share your experience using this material

## 📧 Contact

**Milin Patel**
Research Associate
Hochschule Kempten - University of Applied Sciences
Email: [your-email]
GitHub: [@milinpatel07](https://github.com/milinpatel07)

## 📄 License

MIT License - see `LICENSE` file for details.

You are free to:
- ✅ Use this material for teaching
- ✅ Modify and adapt for your needs
- ✅ Share with attribution

## 🙏 Acknowledgments

- **Datasets:** KITTI, nuScenes, Waymo, BDD100K teams
- **Open Source Tools:** PyTorch, Ultralytics, OpenCV, Open3D
- **Standards Organizations:** SAE International, ISO
- **Inspiration:** Real-world autonomous vehicle projects and research

## 📚 References

See `resources/references.md` in each session folder for:
- Academic papers
- Technical reports (NTSB, IIHS)
- Standards documentation
- Online tutorials and courses

---

**Ready to learn about autonomous vehicle perception and safety? Start with Session 1!**

Navigate to: `Session_1_AI_Perception_Systems/README.md`

---

*Last Updated: 2025-01-17*
*Workshop Version: 1.0*
