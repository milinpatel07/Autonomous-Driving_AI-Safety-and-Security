# Module 01 · Perception and Prediction

How an automated vehicle senses, understands and anticipates its surroundings — and where that can fail. From SAE levels and the operational design domain through real camera images and LiDAR scans (KITTI) to detection, fusion, tracking, the datasets the field is built on, and trajectory prediction on real highway traffic (NGSIM).

**9 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [SAE Levels of Driving Automation and the Operational Design Domain](01_sae_levels_and_odd.ipynb) | Beginner | SAE J3016 (2021); ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/01_sae_levels_and_odd.ipynb) |
| 02 | [Sensor Modalities: Camera, LiDAR and Radar](02_sensor_modalities.ipynb) | Beginner | ISO 21448:2022; ISO 26262-9:2018 (context) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/02_sensor_modalities.ipynb) |
| 03 | [LiDAR Sensors and Point Clouds](03_lidar_point_clouds.ipynb) | Intermediate | IEC 60825-1:2014; ISO 8855:2011; ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/03_lidar_point_clouds.ipynb) |
| 04 | [Object Detection on Real Driving Images: from IoU to Per-Class AP on KITTI](04_object_detection.ipynb) | Intermediate | ISO 21448:2022; ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/04_object_detection.ipynb) |
| 05 | [Vulnerable Road User Detection on Real Data: Recall, Range and AEB](05_vulnerable_road_user_detection.ipynb) | Intermediate | ISO 26262-3:2018; ISO 21448:2022; ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/05_vulnerable_road_user_detection.ipynb) |
| 06 | [Sensor Fusion: Calibration, Association and Late Fusion](06_sensor_fusion.ipynb) | Intermediate | ISO 26262-9:2018; ISO 21448:2022; ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/06_sensor_fusion.ipynb) |
| 07 | [Multi-Object Tracking and State Estimation](07_multi_object_tracking.ipynb) | Intermediate | ISO 21448:2022 (context: performance insufficiencies, triggering conditions) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/07_multi_object_tracking.ipynb) |
| 08 | [Driving Datasets: What KITTI Really Contains, and How to Specify Data for Safety](08_driving_datasets.ipynb) | Intermediate | ISO/PAS 8800:2024; ISO 21448:2022; ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/08_driving_datasets.ipynb) |
| 09 | [Trajectory Prediction on Real Highway Data](09_trajectory_prediction.ipynb) | Intermediate | ISO 21448:2022 (performance insufficiencies); ISO/PAS 8800:2024 (AI components) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/09_trajectory_prediction.ipynb) |

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
- Read a real camera image and LiDAR scan from the KITTI dataset, project the LiDAR into the image and interpret depth and reflectance
- Measure, rather than assume, how LiDAR point density and camera pixel coverage fall with distance
- Identify, object by object, what each sensor misses in a real frame (distance, occlusion, field of view)
- Compute the radar Doppler shift and explain what KITTI cannot tell you about radar and weather
- Quantify how much redundancy two sensors really provide when their weaknesses share a cause

### 03 · LiDAR Sensors and Point Clouds

- Explain the physics of LiDAR ranging (pulsed time of flight, phase shift, FMCW) and the LiDAR range equation
- Describe scanning mechanisms (spinning, mirror/prism scanning, MEMS, flash, OPA) and their trade-offs
- Check datasheet-style density formulas against a real Velodyne HDL-64E scan from KITTI
- Build a classical obstacle pipeline on real scans: bird's-eye-view image, RANSAC ground segmentation, DBSCAN clustering and oriented bounding boxes
- Evaluate the pipeline against KITTI 3D ground truth: recall and points per object by distance, class and occlusion
- Relate the measured weaknesses to SOTIF triggering conditions and to learned 3D detectors

### 04 · Object Detection on Real Driving Images: from IoU to Per-Class AP on KITTI

- Describe what a 2D object detector outputs and how one-stage, two-stage and transformer detectors differ
- Run a pretrained detector on real KITTI images and compare its output with the ground truth
- Implement IoU, non-maximum suppression (NMS), precision–recall and Average Precision from scratch, and check them against reference implementations
- Evaluate a detector the KITTI way: per class, per difficulty, with class-specific IoU thresholds and ignore rules — and explain the pitfalls of mapping COCO classes to KITTI classes
- Analyse real failure cases (missed objects, false positives) and relate them to triggering conditions
- Define a detection KPI precisely enough for it to be used as SOTIF evidence

### 05 · Vulnerable Road User Detection on Real Data: Recall, Range and AEB

- Explain why detecting vulnerable road users (VRUs) is safety-critical, using sourced accident data
- Select real KITTI frames that contain pedestrians and cyclists over a range of distances, using the label table
- Measure a pretrained detector's VRU recall as a function of distance, box height, occlusion and truncation, with confidence intervals
- Compare the measured detection range with the range an AEB function needs at 30 and 50 km/h
- Place the findings correctly: SOTIF and ISO/PAS 8800 for performance insufficiencies; ISO 26262 safety goals SG-02 (ASIL B) and SG-01 (ASIL D)
- Choose an operating threshold from a measured precision–recall curve and distinguish frame-level from track-level recall

### 06 · Sensor Fusion: Calibration, Association and Late Fusion

- Explain what sensor fusion can and cannot contribute to safety, and distinguish early, late and BEV feature-level fusion
- Project LiDAR points and 3D boxes into a camera image with real KITTI calibration
- Build a camera–LiDAR late fusion on real data: a pretrained 2D detector, LiDAR clusters, frustum association and depth from LiDAR
- Evaluate single-sensor and fused object lists against KITTI 3D labels and draw conclusions from the measured numbers
- Measure how extrinsic calibration errors destroy association, and estimate time-synchronisation errors for the KITTI rig
- Turn the measured weaknesses into inputs for a fusion design FMEA

### 07 · Multi-Object Tracking and State Estimation

- Explain why a detector alone is not enough, and why **temporal consistency** of object hypotheses is a safety property.
- Derive and implement a **constant-velocity Kalman filter** (predict, update, covariance propagation) from scratch in NumPy.
- Check filter **consistency** with the NEES and NIS statistics and recognise a mistuned filter.
- Implement **data association** with Mahalanobis gating and optimal (Hungarian) assignment.
- Implement **track management** (tentative, confirmed, deleted; M-of-N confirmation; coasting through occlusion).
- Evaluate a tracker with **MOTA, ID switches and HOTA**, and explain what AMOTA adds.
- Quantify how **detection dropout and noise** delay track confirmation and break track continuity, and relate this to SOTIF triggering conditions.
- Run the tracker on a **real KITTI sequence** with a pretrained detector, score it against the real track IDs, and trace real identity switches to occlusion.

### 08 · Driving Datasets: What KITTI Really Contains, and How to Specify Data for Safety

- Read dataset statistics critically: scenes vs sensor frames vs annotated keyframes vs boxes, sensors, licences
- Analyse all 51,865 KITTI object labels: class imbalance, long tail, distance, occlusion, truncation and objects per frame
- Identify what a dataset does **not** contain (night, rain, distant VRUs) and quantify how many samples a recall claim would need
- Compare KITTI with nuScenes, Waymo Open, Argoverse 2 and ONCE using published, verified figures
- Decide whether a dataset licence allows industrial use
- Write a dataset specification entry that feeds an ISO/PAS 8800 / ISO 21448 safety argument

### 09 · Trajectory Prediction on Real Highway Data

- Prepare real NGSIM vehicle trajectories for prediction: units, time base, re-used vehicle IDs, measurement noise and smoothing without information leakage.
- Implement physics-based baselines (constant velocity, constant acceleration, constant turn rate and velocity) and explain where each one fails.
- Train a small multimodal predictor (a mixture density network) on CPU and compare it with a manoeuvre-based baseline.
- Compute ADE, FDE, minADE$_K$, minFDE$_K$, miss rate and negative log-likelihood, and explain what each metric rewards and hides.
- Check whether predicted uncertainty is **calibrated** (coverage of prediction regions) and repair marginal coverage with split conformal prediction.
- Analyse failures on real lane changes and stop-and-go waves, and translate prediction error into planning risk (RSS safety distance, cut-in recognition).

---

[Course home](../README.md) · [Module 02 · Failures and Robustness](../02_Failures_and_Robustness/README.md) →
