---
title: Data and licences
---

The perception, prediction, cybersecurity and field-monitoring notebooks, the benchmark and the field-safety statistics use public datasets. Nothing is stored in the
repository: the `avsafety.data` loaders download exactly what a notebook needs and cache it locally
(`~/.cache/avsafety`). KITTI frames are read straight out of the official archives with HTTP range requests, so a
notebook fetches a few dozen frames instead of tens of gigabytes.

| Dataset | Content used | Notebooks | Licence | Citation |
|---|---|---|---|---|
| **KITTI object detection** | Camera images, Velodyne LiDAR scans, 2D/3D labels, calibration (7,481 training frames; 40,570 labelled objects plus 11,295 DontCare regions) | 01-02, 01-03, 01-04, 01-05, 01-06, 01-08, 02-02, 04-02, 04-03, 06-04, 06-05, 06-06, 08-05, 04-06 (benchmark) | CC BY-NC-SA 3.0 (non-commercial) | Geiger, Lenz & Urtasun, *Are we ready for autonomous driving? The KITTI vision benchmark suite*, CVPR 2012 |
| **KITTI tracking** | Image sequences with track IDs, GPS/IMU (OXTS) | 01-07, 04-03, 07-02 | CC BY-NC-SA 3.0 (non-commercial) | Geiger et al., *Vision meets robotics: The KITTI dataset*, IJRR 2013 |
| **NGSIM** | Vehicle trajectories on US-101, I-80, Lankershim and Peachtree | 01-09, 06-07, 07-02 | Public domain (US DOT) | US DOT FHWA, Next Generation Simulation (NGSIM) vehicle trajectories, data.transportation.gov |
| **NHTSA Standing General Order** | Crash reports for ADS and Level 2 ADAS | 02-01, 07-03, 07-05, [observatory](observatory.md) | Public US government data | NHTSA, Standing General Order 2021-01 crash reporting |
| **ROAD CAN intrusion dataset** (Oak Ridge National Laboratory) | Real CAN logs of one vehicle (mostly dynamometer, one on-road drive): ambient captures and 21 fuzzing, targeted-injection and masquerade captures; frame labels reconstructed from the published injection metadata | 05-04 | CC BY 4.0 | Verma et al., *A comprehensive guide to CAN IDS data and introduction of the ROAD dataset*, PLOS ONE 19(1): e0296879, 2024; data [doi:10.5281/zenodo.10462796](https://doi.org/10.5281/zenodo.10462796) |
| **VeReMi Extension** (simulated V2X benchmark) | Received basic safety messages of receivers in seven attack subsets and the ground truth; from a calibrated VEINS/SUMO simulation, not field data | 05-05 | CC BY 4.0 | Kamel et al., *VeReMi Extension: A Dataset for Comparable Evaluation of Misbehavior Detection in VANETs*, IEEE ICC 2020; data [doi:10.5281/zenodo.20090854](https://doi.org/10.5281/zenodo.20090854) |
| **California DMV autonomous vehicle reports** | Annual autonomous test miles and disengagements per manufacturer | [observatory](observatory.md) | Public records of the California DMV (see its conditions of use) | California DMV, Autonomous Vehicle Disengagement Reports |
| **Waymo Safety Impact Data Hub** | Rider-only miles and crashes with SGO identifiers; only derived counts and rates are shown | [observatory](observatory.md) | Published by Waymo for research; files are not redistributed | Waymo, Safety Impact Data Hub; Kusano et al. (2024, 2025) |
| **SOTIF-PCOD** (optional) | LiDAR point clouds in KITTI format generated in CARLA for SOTIF-related conditions | 01-03, 01-08, 04-04, 04-06 (LiDAR track) | CC BY 4.0 | Patel, M. (2024). *SOTIF PCOD*, IEEE DataPort, [doi:10.21227/j43q-z578](https://doi.org/10.21227/j43q-z578) |

Pretrained detectors come from [torchvision](https://pytorch.org/vision/stable/models.html) (trained on COCO);
their weights are downloaded once and cached.

## Using SOTIF-PCOD

SOTIF-PCOD is distributed through IEEE DataPort and needs an IEEE DataPort login. After downloading and extracting
it, point the notebooks to it:

```bash
export SOTIF_PCOD_DIR=/path/to/SOTIF_kitti_carla
```

The notebooks that support it detect the folder automatically and skip the optional cells otherwise.

## Responsible use

- KITTI is **non-commercial**. Learn the methods here, then evaluate on data your organisation is licensed to use.
- Incident reports are not crash rates: they lack exposure and have reporting differences between operators
  (see notebook 07-05).
- Figures derived from KITTI in the notebooks carry the same licence as the data.
