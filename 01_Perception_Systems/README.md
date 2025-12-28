# Module 01: Perception Systems

How do autonomous vehicles see and understand the world?

This module covers everything you need to know about perception - from sensors to algorithms to datasets.

---

## What's in This Module

**7 notebooks covering:**
- All sensor types (camera, LiDAR, radar)
- AI-based object detection
- Multi-modal sensor fusion
- 3D point cloud processing
- Industry datasets and benchmarking
- Safety-critical applications

---

## Notebooks

### 1. SAE Automation Levels
**[01_sae_automation_levels.ipynb](notebooks/01_sae_automation_levels.ipynb)**

Understand the SAE J3016 standard:
- Levels 0-5 (no automation to full autonomy)
- Operational Design Domain (ODD)
- System architecture overview
- Who's responsible: driver vs system

### 2. Sensor Technologies
**[02_sensor_technologies.ipynb](notebooks/02_sensor_technologies.ipynb)**

Compare all sensor types:
- Cameras: RGB, stereo, strengths/weaknesses
- LiDAR: 3D sensing, point clouds
- Radar: All-weather detection, Doppler velocity
- Why you need all three (sensor fusion)

### 3. Object Detection
**[03_object_detection.ipynb](notebooks/03_object_detection.ipynb)**

AI-based detection algorithms:
- Two-stage detectors (R-CNN, Faster R-CNN)
- One-stage detectors (YOLO v3/v5/v8, SSD)
- Transformer-based (DETR)
- Training and evaluation on KITTI
- Metrics: AP, mAP, IoU

### 4. Sensor Fusion
**[04_sensor_fusion.ipynb](notebooks/04_sensor_fusion.ipynb)**

Combining multiple sensors:
- Early fusion (raw data level)
- Late fusion (decision level)
- Deep fusion (feature level)
- Temporal fusion (tracking)
- Sensor calibration

### 5. Pedestrian Detection
**[05_pedestrian_detection.ipynb](notebooks/05_pedestrian_detection.ipynb)**

Safety-critical case study:
- Why pedestrian detection is ASIL-D (ISO 26262)
- Challenges: occlusion, scale, pose variation
- Multi-modal approaches (camera + LiDAR)
- Uncertainty quantification
- Euro NCAP test protocols

### 6. LiDAR Fundamentals
**[06_lidar_sensor_fundamentals.ipynb](notebooks/06_lidar_sensor_fundamentals.ipynb)**

Deep dive into LiDAR:
- Physics (time-of-flight measurement)
- Scanning mechanisms (mechanical, solid-state, MEMS)
- Point cloud data structures
- Commercial sensors (Velodyne, Ouster, Luminar)
- 3D perception basics

### 7. Dataset Overview
**[07_dataset_overview.ipynb](notebooks/07_dataset_overview.ipynb)**

Industry datasets:
- KITTI 3D Object Detection
- nuScenes (360° multi-sensor)
- Waymo Open Dataset
- Dataset comparison and selection
- Working with devkits
- Evaluation metrics

---

## Recommended Learning Path

**Start to finish:**
```
01 SAE Levels → 02 Sensors → 06 LiDAR → 03 Detection →
04 Fusion → 05 Pedestrian → 07 Datasets
```

**Just sensors:**
01 → 02 → 06 → 04

**Just algorithms:**
01 → 03 → 04 → 05

---

## What You'll Learn

By completing this module:
- Compare sensor technologies and understand trade-offs
- Implement state-of-the-art object detection (YOLO, R-CNN, DETR)
- Process 3D LiDAR point clouds
- Design multi-modal sensor fusion systems
- Work with industry datasets (KITTI, nuScenes, Waymo)
- Understand safety-critical requirements (ISO 26262)

---

## Prerequisites

**Required:**
- Python (intermediate level)
- Machine learning basics
- Deep learning fundamentals (CNNs)
- Linear algebra and probability

**Recommended:**
- PyTorch or TensorFlow experience
- Computer vision basics

---

## Tools and Frameworks

- PyTorch / TensorFlow - Deep learning
- Ultralytics YOLOv8 - Real-time detection
- MMDetection / Detectron2 - Detection frameworks
- Open3D - Point cloud processing
- KITTI / nuScenes / Waymo DevKits - Dataset tools

---

## After This Module

Continue to:
- **Module 02** - Learn what can go wrong (edge cases, adversarial attacks, OOD detection)
- **Module 03** - Apply ISO 26262 standards to perception systems
- **Module 06** - Uncertainty quantification for ML models

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
