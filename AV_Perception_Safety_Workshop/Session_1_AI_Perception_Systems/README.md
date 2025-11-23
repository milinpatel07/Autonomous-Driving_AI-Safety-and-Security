# Session 1: AI-based Perception Systems in Autonomous Vehicles

**Instructor:** Milin Patel

## 🎯 Session Objectives

By the end of this session, you will:
- ✅ Understand SAE J3016 levels of driving automation
- ✅ Explain autonomous vehicle system architecture
- ✅ Compare sensor modalities (Camera, LiDAR, Radar)
- ✅ Understand sensor fusion concepts
- ✅ Implement object detection with deep learning
- ✅ Explore real autonomous driving datasets
- ✅ Analyze a pedestrian detection case study

## 📋 Session Structure

### Part A: Introduction
- SAE J3016 automation levels
- Autonomous driving architecture
- Role of AI in perception, prediction, planning

### Part B: Perception Systems
- Camera sensors and processing
- LiDAR point clouds
- Radar detection
- Sensor fusion strategies
- Deep learning for object detection
- Training datasets overview

### Part C: Interactive Demonstrations
- **Demo 1:** Live object detection with YOLOv8
- **Demo 2:** Dataset exploration (nuScenes, KITTI, Waymo)
- **Demo 3:** Sensor modality comparison

### Part D: Case Study & Discussion
- Pedestrian detection system analysis
- Preview of failure modes (Session 2)

## 📓 Jupyter Notebooks

Work through these notebooks in order:

| # | Notebook | Topics | Duration |
|---|----------|--------|----------|
| 1 | `01_Introduction_SAE_Levels.ipynb` | SAE levels, AV architecture, AI role | 15 min |
| 2 | `02_Sensor_Modalities_Visualization.ipynb` | Camera, LiDAR, Radar comparison | 15 min |
| 3 | `03_Object_Detection_Demo.ipynb` | YOLOv8, Faster R-CNN, real-time inference | 20 min |
| 4 | `04_Dataset_Exploration.ipynb` | KITTI, nuScenes, Waymo exploration | 20 min |
| 5 | `05_Sensor_Fusion_Basics.ipynb` | Early/late fusion, multi-modal detection | 15 min |
| 6 | `06_Pedestrian_Detection_Case_Study.ipynb` | Safety-critical system analysis | 15 min |

**Total:** ~100 minutes (includes exercises)

## 🚀 Quick Start

### Prerequisites
Ensure you've completed the installation:
```bash
# Activate environment
conda activate av_workshop  # or: source venv/bin/activate

# Verify installation
python ../scripts/verify_installation.py
```

### Launch Notebooks
```bash
# From Session_1_AI_Perception_Systems directory
jupyter lab

# Or from workshop root:
cd AV_Perception_Safety_Workshop
jupyter lab Session_1_AI_Perception_Systems/notebooks/
```

### Running Notebooks
1. Open `01_Introduction_SAE_Levels.ipynb`
2. Select kernel: **"AV Workshop"**
3. Run cells sequentially (Shift + Enter)
4. Complete exercises at the end
5. Proceed to next notebook

## 📂 Directory Structure

```
Session_1_AI_Perception_Systems/
├── README.md                          # This file
│
├── notebooks/                         # Jupyter notebooks (main content)
│   ├── 01_Introduction_SAE_Levels.ipynb
│   ├── 02_Sensor_Modalities_Visualization.ipynb
│   ├── 03_Object_Detection_Demo.ipynb
│   ├── 04_Dataset_Exploration.ipynb
│   ├── 05_Sensor_Fusion_Basics.ipynb
│   └── 06_Pedestrian_Detection_Case_Study.ipynb
│
├── scripts/                           # Python utilities
│   ├── object_detection.py           # Detection inference functions
│   ├── sensor_visualization.py       # LiDAR, camera viz tools
│   ├── dataset_loader.py             # KITTI, nuScenes loaders
│   └── utils.py                      # Helper functions
│
├── data/                             # Sample data (downloaded separately)
│   ├── sample_images/                # Test images for detection
│   │   ├── urban_scene_01.jpg
│   │   ├── highway_traffic.jpg
│   │   ├── pedestrian_crossing.jpg
│   │   └── ...
│   └── sample_pointclouds/           # LiDAR point clouds
│       └── ...
│
├── exercises/                        # Hands-on exercises
│   ├── Exercise_1_SAE_Levels.md
│   ├── Exercise_2_Sensor_Comparison.md
│   ├── Exercise_3_Object_Detection.md
│   ├── Exercise_4_Dataset_Analysis.md
│   └── solutions/                    # Try before looking!
│       ├── exercise_1_solution.md
│       ├── exercise_2_solution.py
│       ├── exercise_3_solution.ipynb
│       └── exercise_4_solution.ipynb
│
├── resources/                        # External links and references
│   ├── links.md                      # Web demos, tools, viewers
│   ├── datasets.md                   # Dataset download instructions
│   ├── references.md                 # Papers, standards docs
│   └── slides_resources.md           # Images, videos for slides
│
└── slides/                           # Presentation materials
    ├── Session_1_Slides.pdf          # Full slide deck
    └── images/                       # Slide images
```

## 📚 Notebook Details

### Notebook 1: Introduction & SAE Levels
**File:** `01_Introduction_SAE_Levels.ipynb`

**Content:**
- Interactive SAE J3016 level selector
- Comparison table: Levels 0-5
- Current vehicle examples (Tesla, Waymo, Mercedes)
- Driver responsibility vs system capability
- Autonomous driving architecture diagram
- AI's role in perception, prediction, planning

**Key Concepts:**
- Operational Design Domain (ODD)
- Conditional vs High automation
- Fallback mechanisms

**Exercises:**
- Classify real vehicles by SAE level
- Identify ODD limitations
- Analyze system architecture components

---

### Notebook 2: Sensor Modalities Visualization
**File:** `02_Sensor_Modalities_Visualization.ipynb`

**Content:**
- Load camera, LiDAR, radar data
- Visualize same scene from all sensors
- Interactive 3D point cloud viewer
- Sensor comparison table (range, resolution, weather)
- Sensor fusion motivation

**Key Concepts:**
- Camera: Rich semantic info, weather-dependent
- LiDAR: Accurate 3D, expensive, affected by fog
- Radar: All-weather, low resolution
- Complementary strengths → fusion

**Exercises:**
- Compare sensor outputs in different weather
- Identify objects visible in LiDAR but not camera
- Design sensor suite for urban vs highway

**Interactive Elements:**
- Rotate 3D point clouds
- Toggle sensor layers
- Adjust visualization parameters

---

### Notebook 3: Object Detection Demo
**File:** `03_Object_Detection_Demo.ipynb`

**Content:**
- YOLOv8 object detection on driving scenes
- Faster R-CNN comparison
- Confidence score interpretation
- Bounding box visualization
- Real-time inference speed benchmarking
- Webcam live detection (optional)

**Key Concepts:**
- Deep neural networks for detection
- Training vs inference
- Precision, recall, mAP metrics
- Confidence thresholds

**Exercises:**
- Detect objects in test images
- Compare YOLOv8 vs Faster R-CNN performance
- Adjust confidence threshold
- Analyze false positives/negatives

**Interactive Elements:**
- Upload custom images
- Real-time webcam detection
- Confidence slider
- Class filtering

---

### Notebook 4: Dataset Exploration
**File:** `04_Dataset_Exploration.ipynb`

**Content:**
- KITTI dataset structure and loading
- nuScenes API usage and visualization
- Waymo Open Dataset browser
- Dataset statistics (object counts, scene types)
- Annotation quality analysis

**Key Concepts:**
- Why diverse datasets matter for AI
- Geographic, weather, temporal diversity
- Annotation quality impact on learning
- Train/validation/test splits

**Exercises:**
- Load and visualize KITTI frame
- Explore nuScenes scene with all sensors
- Compare dataset characteristics
- Identify potential data gaps

**Interactive Elements:**
- Dataset browser interface
- Filter by weather/time/location
- View annotations overlay
- Statistics dashboard

---

### Notebook 5: Sensor Fusion Basics
**File:** `05_Sensor_Fusion_Basics.ipynb`

**Content:**
- Early fusion: Combine raw sensor data
- Late fusion: Combine detection results
- Deep fusion: Neural network learns fusion
- Multi-modal object detection
- Fusion evaluation metrics

**Key Concepts:**
- Redundancy for safety
- Improved robustness
- Sensor calibration and synchronization
- Trade-offs: complexity vs performance

**Exercises:**
- Implement simple late fusion
- Compare single-sensor vs fused results
- Analyze fusion failure cases
- Design fusion strategy for scenario

**Code Implementation:**
```python
# Example: Late fusion of camera and LiDAR detections
camera_boxes = detect_camera(image)
lidar_boxes = detect_lidar(pointcloud)
fused_boxes = fusion_algorithm(camera_boxes, lidar_boxes)
```

---

### Notebook 6: Pedestrian Detection Case Study
**File:** `06_Pedestrian_Detection_Case_Study.ipynb`

**Content:**
- Pedestrian detection system design
- Camera-based AEB (Automatic Emergency Braking)
- YOLOv8 pedestrian detection
- Decision logic: detection → brake
- Evaluation on pedestrian datasets
- Connection to Sessions 2-4

**Key Concepts:**
- Safety-critical perception
- Real-world accident analysis (preview)
- Performance requirements (ISO 26262)
- Uncertainty in detection (preview Session 4)

**Exercises:**
- Implement pedestrian detector
- Test on challenging scenarios
- Analyze failure modes (what fails and why)
- Define acceptance criteria

**Case Study:**
This system will be used throughout the workshop:
- **Session 2:** Analyze failures (Uber crash)
- **Session 3:** Apply ISO standards
- **Session 4:** Add uncertainty estimation

---

## 🛠️ Python Scripts

### `object_detection.py`
Functions for running object detection:
```python
from scripts.object_detection import detect_objects, load_model

# Load YOLOv8 model
model = load_model('yolov8n.pt')

# Detect objects in image
results = detect_objects(image, model, conf_threshold=0.5)
```

### `sensor_visualization.py`
Visualization tools for sensor data:
```python
from scripts.sensor_visualization import visualize_pointcloud, overlay_projection

# Visualize 3D point cloud
visualize_pointcloud(pointcloud, colors='distance')

# Project LiDAR onto camera image
overlay = overlay_projection(image, pointcloud, calibration)
```

### `dataset_loader.py`
Load KITTI, nuScenes, Waymo data:
```python
from scripts.dataset_loader import KITTILoader, NuScenesLoader

# Load KITTI frame
kitti = KITTILoader('data/kitti')
image, pointcloud, labels = kitti.get_frame(index=100)

# Load nuScenes scene
nuscenes = NuScenesLoader('data/nuscenes', version='v1.0-mini')
sample = nuscenes.get_sample(scene_token, timestamp)
```

### `utils.py`
Helper functions:
```python
from scripts.utils import download_image, compute_metrics, visualize_boxes

# Download sample image
img = download_image(url)

# Compute detection metrics
precision, recall, ap = compute_metrics(predictions, ground_truth)
```

---

## 🧪 Exercises

### Exercise 1: SAE Level Classification
**File:** `exercises/Exercise_1_SAE_Levels.md`

Classify these vehicles by SAE level:
1. Tesla Model 3 with Autopilot
2. Waymo autonomous taxi (Phoenix, AZ)
3. Mercedes Drive Pilot (Germany highways)
4. Traditional car with adaptive cruise control

**Learning Goals:** Understand differences between levels

---

### Exercise 2: Sensor Trade-off Analysis
**File:** `exercises/Exercise_2_Sensor_Comparison.md`

Given scenarios, choose optimal sensor suite:
1. Urban robotaxi (all-weather operation)
2. Highway truck platooning
3. Low-cost ADAS system

**Learning Goals:** Apply sensor characteristics to design

---

### Exercise 3: Object Detection Tuning
**File:** `exercises/Exercise_3_Object_Detection.md`

Using YOLOv8:
1. Run detection on 10 test images
2. Adjust confidence threshold for zero false positives
3. Compute precision, recall, F1 score
4. Find optimal threshold for your use case

**Learning Goals:** Understand detection trade-offs

---

### Exercise 4: Dataset Gap Analysis
**File:** `exercises/Exercise_4_Dataset_Analysis.md`

Analyze nuScenes dataset:
1. Count pedestrian instances by weather
2. Identify underrepresented scenarios
3. Propose data collection plan
4. Estimate safety impact of gaps

**Learning Goals:** Data quality impacts AI safety

---

## 📖 Resources

### Interactive Web Tools
- **nuScenes Explorer:** https://www.nuscenes.org/nuscenes#explore
- **Waymo Viewer:** https://waymo.com/open/viewer/
- **YOLOv8 Demo:** https://huggingface.co/spaces/Xenova/yolov9-web
- **AV Dataset Viewer:** https://avdatasetviewer.com/

See `resources/links.md` for full list.

### Datasets
- **KITTI:** http://www.cvlibs.net/datasets/kitti/
- **nuScenes:** https://www.nuscenes.org/nuscenes
- **Waymo Open:** https://waymo.com/open/
- **BDD100K:** https://bdd-data.berkeley.edu/

See `resources/datasets.md` for download instructions.

### Academic Papers
- **YOLOv8:** https://arxiv.org/abs/2305.09972
- **nuScenes Paper:** https://arxiv.org/abs/1903.11027
- **PointPillars (LiDAR):** https://arxiv.org/abs/1812.05784

See `resources/references.md` for full bibliography.

---

## 🎥 Recommended Videos

Watch before or after session:

1. **Waymo Sensor Visualization**
   https://www.youtube.com/watch?v=B8R148hFxPw

2. **How Tesla Autopilot Works**
   https://www.youtube.com/watch?v=uxLBcPdKfbs

3. **Euro NCAP Pedestrian AEB Tests**
   https://www.youtube.com/watch?v=3_38KHlS1zQ

4. **LiDAR Point Cloud Visualization**
   https://www.youtube.com/watch?v=KXpZ6B1YB_k

---

## ⏱️ Time Management

**Suggested schedule for 90-minute session:**

| Time | Activity | Materials |
|------|----------|-----------|
| 0-5 min | Introduction, setup | Slides 1-3 |
| 5-20 min | SAE levels, architecture | Notebook 1, Slides 4-6 |
| 20-35 min | Sensor modalities | Notebook 2, Slides 7-11 |
| 35-55 min | Object detection demo | Notebook 3, Slides 12-13 |
| 55-70 min | Dataset exploration | Notebook 4, Slides 13-14 |
| 70-80 min | Sensor fusion | Notebook 5, Slide 11 |
| 80-88 min | Case study | Notebook 6, Slide 14 |
| 88-90 min | Wrap-up, preview | Slides 19-20 |

**Flexibility:** Adjust based on audience pace. Priority: Notebooks 1, 3, 4.

---

## 🎯 Learning Outcomes Assessment

After completing Session 1, you should be able to:

- [ ] Explain the difference between SAE Levels 2, 3, and 4
- [ ] Describe when to use camera vs LiDAR vs radar
- [ ] Run object detection on driving scenes
- [ ] Load and visualize KITTI or nuScenes data
- [ ] Explain why sensor fusion improves robustness
- [ ] Identify potential failure modes in pedestrian detection

**Self-check:** Complete exercises and compare with solutions.

---

## 🔗 Connection to Other Sessions

### Session 2: Failure Modes
- **Build on:** Pedestrian detection case study
- **Explore:** What happens when detection fails
- **Example:** Uber ATG crash analysis

### Session 3: Safety Standards
- **Apply standards to:** Our pedestrian detector
- **Learn:** ISO 26262, SOTIF, ISO 8800
- **Outcome:** Safety-compliant system design

### Session 4: Uncertainty Estimation
- **Enhance detector with:** Confidence + uncertainty
- **Implement:** Monte Carlo Dropout
- **Deploy:** Raspberry Pi live demo

---

## 💡 Tips for Success

1. **Run all code cells** - Don't just read, execute!
2. **Experiment** - Change parameters, see what happens
3. **Visualize** - Use plots to understand concepts
4. **Ask questions** - Engage with instructor and peers
5. **Take notes** - Jot down insights for later
6. **Try exercises** - Don't peek at solutions first
7. **Connect concepts** - How does this relate to safety?

---

## 📧 Questions or Issues?

- **During workshop:** Ask instructor
- **After workshop:** Open GitHub issue
- **Technical problems:** Check `setup_instructions.md`

---

**Ready to dive into autonomous vehicle perception? Start with Notebook 1! 🚗**

```bash
jupyter lab notebooks/01_Introduction_SAE_Levels.ipynb
```

---

*Last updated: 2025-01-17*
