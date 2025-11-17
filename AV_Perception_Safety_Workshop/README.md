# AI and Safety Aspects in Autonomous Driving - Workshop

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**Duration:** 3.5 hours (09:00 - 12:30)

## 🎯 Workshop Overview

This hands-on workshop provides a comprehensive introduction to AI-based perception systems in autonomous vehicles, their failure modes, safety standards, and uncertainty estimation techniques. Participants will gain practical experience through interactive demonstrations, real datasets, and Jupyter notebook exercises.

## 📋 Workshop Schedule

| Time | Duration | Session |
|------|----------|---------|
| 09:00 - 10:30 | 90 min | **Session 1:** AI-based Perception Systems in Autonomous Vehicles |
| 10:30 - 10:45 | 15 min | ☕ Coffee Break |
| 10:45 - 11:30 | 45 min | **Session 2:** Failure Modes in Machine Learning-based Perception |
| 11:30 - 12:00 | 30 min | **Session 3:** Safety Standards for Autonomous Driving Systems |
| 12:00 - 12:30 | 30 min | **Session 4:** Uncertainty Estimation in Object Detection |

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

## 📚 Session Contents

### Session 1: AI-based Perception Systems (90 min)
**Location:** `Session_1_AI_Perception_Systems/`

- **Notebooks (6):**
  1. Introduction & SAE Levels
  2. Sensor Modalities Visualization
  3. Object Detection Demo (YOLOv8, Faster R-CNN)
  4. Dataset Exploration (KITTI, nuScenes, Waymo)
  5. Sensor Fusion Basics
  6. Pedestrian Detection Case Study

- **Interactive Demos:**
  - Live object detection with webcam
  - 3D LiDAR point cloud visualization
  - Multi-sensor data fusion
  - Real-time inference benchmarking

- **Exercises:**
  - Compare SAE automation levels
  - Analyze sensor trade-offs
  - Train object detector on custom data
  - Evaluate detection performance (mAP, precision, recall)

### Session 2: Failure Modes in ML Perception (45 min)
**Location:** `Session_2_Failure_Modes/`

- **Real Accident Analysis:**
  - Uber ATG Tempe crash (2018) - NTSB report breakdown
  - Tesla Autopilot incidents
  - Cruise SF accident (2023)

- **Failure Types:**
  - False positives/negatives
  - Misclassification
  - Out-of-distribution (OOD) scenarios
  - Adversarial examples

- **Root Causes:**
  - Training data gaps
  - Weather/lighting conditions
  - Sensor limitations
  - Algorithm design choices

### Session 3: Safety Standards (30 min)
**Location:** `Session_3_Safety_Standards/`

- **ISO 26262** - Functional Safety
- **ISO 21448 (SOTIF)** - Safety of the Intended Functionality
- **ISO 8800** - Safety & AI in Road Vehicles
- **ISO 21434** - Cybersecurity

- **Integrated Case Study:**
  - Apply ALL standards to pedestrian detection system
  - Hazard analysis and risk assessment (HARA)
  - Define Operational Design Domain (ODD)
  - SOTIF scenario space (Known/Unknown Safe/Unsafe)

### Session 4: Uncertainty Estimation (30 min)
**Location:** `Session_4_Uncertainty_Estimation/`

- **Uncertainty Types:**
  - Aleatoric (data) uncertainty
  - Epistemic (model) uncertainty

- **Quantification Methods:**
  - Monte Carlo Dropout
  - Deep Ensembles
  - Bayesian Neural Networks (intro)

- **Implementation:**
  - Add uncertainty to YOLOv8
  - Visualize confidence vs uncertainty
  - Uncertainty-aware decision making

- **Live Demo:**
  - Raspberry Pi with camera
  - Real-time detection + uncertainty
  - Change conditions → observe uncertainty

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
