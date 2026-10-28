# Module 01 · Perception Systems

How an automated vehicle senses and understands its surroundings — and where that understanding can fail. From SAE levels and the operational design domain through cameras, LiDAR and radar to detection, fusion, tracking and the datasets the field is built on.

**8 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [SAE Levels of Driving Automation and the Operational Design Domain](01_sae_levels_and_odd.ipynb) | Beginner | SAE J3016 (2021); ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/01_sae_levels_and_odd.ipynb) |
| 02 | [Sensor Modalities: Camera, LiDAR and Radar](02_sensor_modalities.ipynb) | Beginner | ISO 21448:2022 (context) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/02_sensor_modalities.ipynb) |
| 03 | [LiDAR Sensors and Point Clouds](03_lidar_point_clouds.ipynb) | Intermediate | IEC 60825-1:2014; ISO 8855:2011; ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/03_lidar_point_clouds.ipynb) |
| 04 | [Object Detection: from IoU to mAP with YOLO](04_object_detection.ipynb) | Intermediate | ISO 21448:2022; ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/04_object_detection.ipynb) |
| 05 | [Vulnerable Road User Detection: a Safety-Critical Case Study](05_vulnerable_road_user_detection.ipynb) | Intermediate | ISO 26262-3:2018; ISO 21448:2022; ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/05_vulnerable_road_user_detection.ipynb) |
| 06 | [Sensor Fusion: Calibration, Association and Late Fusion](06_sensor_fusion.ipynb) | Intermediate | ISO 26262-9:2018; ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/06_sensor_fusion.ipynb) |
| 07 | [Multi-Object Tracking and State Estimation](07_multi_object_tracking.ipynb) | Intermediate | ISO 21448:2022 (context: performance insufficiencies, triggering conditions) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/07_multi_object_tracking.ipynb) |
| 08 | [Driving Datasets and 3D Detection Metrics](08_driving_datasets.ipynb) | Intermediate | ISO/PAS 8800:2024; ISO 21448:2022; ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/08_driving_datasets.ipynb) |

## What you will learn

### 01 · SAE Levels of Driving Automation and the Operational Design Domain

- Describe SAE J3016 and its six levels of driving automation (0–5) in terms of roles, not percentages
- Distinguish driver support (L0–L2) from automated driving (L3–L5) and explain the DDT fallback
- Classify real-world systems by SAE level, using current (2026) examples
- Define the Operational Design Domain (ODD), its dimensions, and how a system can check it at runtime
- Outline the sense → perceive → predict → plan → act architecture and where machine learning is used
- Explain why ML-based perception creates new safety questions (ISO 21448, ISO/PAS 8800)

### 02 · Sensor Modalities: Camera, LiDAR and Radar

- Describe the operating principles of camera, LiDAR and radar (incl. 4D imaging radar and FMCW LiDAR)
- Compare sensor capabilities and limitations across weather and lighting conditions
- Generate and visualise a ray-cast LiDAR scan, its bird's-eye view (BEV) and a matching camera view
- Compute the radar Doppler shift and explain why radar measures velocity directly
- Quantify redundancy with and without common-cause failures
- Explain why sensor diversity supports, but does not by itself establish, a safety argument

### 03 · LiDAR Sensors and Point Clouds

- Explain the physics of LiDAR ranging (pulsed time of flight, phase shift, FMCW) and the LiDAR range equation
- Describe scanning mechanisms (spinning, mirror/prism scanning, MEMS, flash, OPA) and their trade-offs
- Compute point density and the number of returns on an object as a function of distance
- Transform points between sensor and vehicle frames and quantify the effect of extrinsic calibration error
- Segment the ground and cluster obstacles in a point cloud
- Identify LiDAR failure modes as SOTIF triggering conditions

### 04 · Object Detection: from IoU to mAP with YOLO

- Describe what a 2D object detector outputs and how one-stage, two-stage and transformer detectors differ
- Run a pretrained YOLO model on a street scene and interpret boxes, classes and confidence scores
- Implement Intersection over Union (IoU) and Non-Maximum Suppression (NMS) from scratch
- Compute precision, recall, the precision–recall curve and Average Precision (AP, mAP@[.5:.95]) from scratch
- Distinguish throughput (FPS) from latency and relate both to the driving task
- Explain why detector confidence is not a calibrated probability and why that matters for safety

### 05 · Vulnerable Road User Detection: a Safety-Critical Case Study

- Explain why detecting vulnerable road users (VRUs) is safety-critical, using sourced accident data
- Measure how a pretrained detector degrades under darkness, fog and occlusion on a real street image
- Determine ASILs correctly with the ISO 26262-3 risk graph and keep the ISO 26262 / ISO 21448 / ISO/PAS 8800 boundary sharp
- Choose an operating threshold from a precision–recall curve for a recall target
- Translate per-frame recall into distance travelled without seeing a pedestrian, and relate it to stopping distance
- Distinguish frame-level from track-level recall and propose mitigations

### 06 · Sensor Fusion: Calibration, Association and Late Fusion

- Explain what sensor fusion can and cannot contribute to safety
- Distinguish early, late and intermediate (feature-level / BEV) fusion and name current architectures
- Project 3D LiDAR objects into a camera image using intrinsic and extrinsic calibration
- Implement late fusion with class-agnostic Hungarian association, principled confidence combination and class-specific thresholds
- Evaluate single-sensor vs fused detection with correct one-to-one matching, and draw data-derived conclusions
- Quantify the effect of calibration and time-synchronisation errors on fusion

### 07 · Multi-Object Tracking and State Estimation

- Explain why a detector alone is not enough, and why **temporal consistency** of object hypotheses is a safety property.
- Derive and implement a **constant-velocity Kalman filter** (predict, update, covariance propagation) from scratch in NumPy.
- Check filter **consistency** with the NEES and NIS statistics and recognise a mistuned filter.
- Implement **data association** with Mahalanobis gating and optimal (Hungarian) assignment.
- Implement **track management** (tentative, confirmed, deleted; M-of-N confirmation; coasting through occlusion).
- Evaluate a tracker with **MOTA, ID switches and HOTA**, and explain what AMOTA adds.
- Quantify how **detection dropout and noise** delay track confirmation and break track continuity, and relate this to SOTIF triggering conditions.

### 08 · Driving Datasets and 3D Detection Metrics

- Describe the major public driving datasets (KITTI, nuScenes, Waymo Open, BDD100K, Argoverse 2) and recent European datasets
- Read dataset statistics critically: scenes vs frames vs annotated keyframes, sensor setups, licences
- Analyse class imbalance and the long tail, and explain their safety implications
- Compute nuScenes-style 3D detection metrics (centre-distance AP, mAP, TP errors, NDS) from scratch
- Select datasets for a given ODD and identify coverage gaps
- Relate dataset properties to ISO/PAS 8800 data requirements and ISO 21448 triggering conditions

---

[Course home](../README.md) · [Module 02 · Failures and Robustness](../02_Failures_and_Robustness/README.md) →
