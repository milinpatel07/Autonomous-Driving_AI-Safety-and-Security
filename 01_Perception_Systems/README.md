# Perception Systems, Sensors, and Datasets

**Module 01: Complete Perception Pipeline for Autonomous Vehicles**

---

## 📍 What's Here

This module covers **everything you need for perception**:
- ✅ All sensor types (Camera, LiDAR, Radar)
- ✅ AI-based object detection algorithms
- ✅ Multi-modal sensor fusion
- ✅ 3D point cloud processing (LiDAR)
- ✅ Industry datasets and benchmarking
- ✅ Safety-critical applications

**Why all together?** Modern autonomous vehicles require **integrated multi-modal perception** - no single sensor or approach is sufficient for safe operation.

---

## 📓 Notebooks (7 Total - All Available)

### Foundation: Understanding the System

**1. [01_sae_automation_levels.ipynb](notebooks/01_sae_automation_levels.ipynb)** ✅
- SAE J3016 Levels 0-5 (No automation → Full autonomy)
- Operational Design Domain (ODD) and constraints
- Dynamic Driving Task (DDT) and responsibilities
- When and where autonomous features can operate safely

### Sensors: How Vehicles "See"

**2. [02_sensor_technologies.ipynb](notebooks/02_sensor_technologies.ipynb)** ✅
- **Cameras**: RGB, stereo, strengths/weaknesses
- **LiDAR**: 3D sensing, point clouds, how it works
- **Radar**: All-weather detection, Doppler velocity
- **Comparison**: Range, resolution, cost, weather performance
- Why sensor fusion is essential

**6. [06_lidar_sensor_fundamentals.ipynb](notebooks/06_lidar_sensor_fundamentals.ipynb)** ✅
- LiDAR physics (time-of-flight measurement)
- Scanning mechanisms (mechanical, solid-state, MEMS)
- Point cloud data structures (XYZ, XYZI, XYZRGB)
- Specifications: Range, accuracy, resolution, FOV
- Commercial sensors (Velodyne, Ouster, Luminar, Livox)
- 3D perception fundamentals

### Algorithms: Understanding the Environment

**3. [03_object_detection.ipynb](notebooks/03_object_detection.ipynb)** ✅
- Two-stage detectors (R-CNN, Faster R-CNN)
- One-stage detectors (YOLO v3/v5/v8, SSD)
- Transformer-based (DETR)
- Training and evaluation on KITTI
- Metrics: AP, mAP, IoU

**4. [04_sensor_fusion.ipynb](notebooks/04_sensor_fusion.ipynb)** ✅
- Early fusion (raw data level)
- Late fusion (decision level)
- Deep fusion (feature level with attention)
- Temporal fusion (tracking across frames)
- Sensor calibration (intrinsic/extrinsic)

### Real-World Application

**5. [05_pedestrian_detection.ipynb](notebooks/05_pedestrian_detection.ipynb)** ✅
- Safety-critical case study (ISO 26262 ASIL-D)
- Challenges: Occlusion, scale, pose variation
- Multi-modal (Camera + LiDAR) approaches
- Uncertainty quantification
- False positive vs false negative trade-offs
- Euro NCAP test protocols

### Datasets and Benchmarking

**7. [07_dataset_overview.ipynb](notebooks/07_dataset_overview.ipynb)** ✅
- KITTI 3D Object Detection (camera + LiDAR)
- nuScenes (360° multi-sensor suite)
- Waymo Open Dataset (large-scale, diverse)
- Dataset comparison and task support
- Evaluation metrics (AP, mAP, IoU, NDS)
- Working with dataset devkits

---

## 🎯 Learning Path

### Recommended Order (Start to Finish):
```
01 SAE Levels → 02 Sensors → 06 LiDAR → 03 Detection →
04 Fusion → 05 Pedestrian → 07 Datasets
```

### Alternative Paths:

**Sensor-Focused:** 01 → 02 → 06 → 04
**Algorithm-Focused:** 01 → 03 → 04 → 05
**Evaluation-Focused:** 01 → 03 → 07

---

## 🔗 Integration with Other Modules

### After This Module:
- **Module 02 (Failure Analysis)**: Learn what can go wrong - edge cases, adversarial attacks, OOD detection
- **Module 03 (Functional Safety)**: Apply ISO 26262 standards to perception systems
- **Module 04 (SOTIF)**: Handle performance limitations and validation

### Advanced Topics:
- **Module 06 (AI Safety)**: Uncertainty quantification for ML models
- **Module 08 (Advanced Integration)**: Deployment challenges, explainability, runtime monitoring

---

## 📚 What You'll Learn

By completing this module:
✓ Compare all sensor technologies and their trade-offs
✓ Implement state-of-the-art object detection (YOLO, R-CNN, DETR)
✓ Process 3D LiDAR point clouds
✓ Design multi-modal sensor fusion systems
✓ Work with industry datasets (KITTI, nuScenes, Waymo)
✓ Evaluate perception systems using standard metrics
✓ Understand safety-critical requirements (ISO 26262)

---

## 🛠️ Tools and Frameworks

- **PyTorch / TensorFlow**: Deep learning
- **Ultralytics YOLOv8**: Real-time detection
- **MMDetection / Detectron2**: Detection frameworks
- **Open3D**: Point cloud processing
- **KITTI / nuScenes / Waymo DevKits**: Dataset tools

---

## ⚠️ Prerequisites

**Required:**
- Python (intermediate)
- Machine learning basics
- Deep learning fundamentals (CNNs)
- Linear algebra, probability

**Recommended:**
- PyTorch or TensorFlow experience
- Computer vision basics

---

## 📝 Note on Repository Structure

**This module consolidates:**
- Original Module 01 (Perception Systems) ✅
- Original Module 09 (LiDAR Technology) - **merged here** (LiDAR is a sensor!)
- Original Module 10 (Datasets & Benchmarks) - **merged here** (evaluation belongs with perception)

**Rationale:** Modern AV perception is inherently multi-modal. Separating LiDAR from other sensors created artificial boundaries. This integrated approach better reflects real-world perception system development.

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**License:** MIT
**Last Updated:** 2025-12-28
