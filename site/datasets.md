---
title: Data and licences
---

The perception, prediction and field-monitoring notebooks use **real public data**. Nothing is stored in the
repository: the `avsafety.data` loaders download exactly what a notebook needs and cache it locally
(`~/.cache/avsafety`). KITTI frames are read straight out of the official archives with HTTP range requests, so a
notebook fetches a few dozen frames instead of tens of gigabytes.

| Dataset | Content used | Notebooks | Licence | Citation |
|---|---|---|---|---|
| **KITTI object detection** | Camera images, Velodyne LiDAR scans, 2D/3D labels, calibration (7,481 training frames; 40,570 labelled objects plus 11,295 DontCare regions) | 01-02, 01-03, 01-04, 01-05, 01-06, 01-08, 02-02, 04-02, 04-03, 06-04, 06-05, 06-06, 08-05 | CC BY-NC-SA 3.0 (non-commercial) | Geiger, Lenz & Urtasun, *Are we ready for autonomous driving? The KITTI vision benchmark suite*, CVPR 2012 |
| **KITTI tracking** | Image sequences with track IDs, GPS/IMU (OXTS) | 01-07, 04-03, 07-02 | CC BY-NC-SA 3.0 (non-commercial) | Geiger et al., *Vision meets robotics: The KITTI dataset*, IJRR 2013 |
| **NGSIM** | Vehicle trajectories on US-101, I-80, Lankershim and Peachtree | 01-09, 06-07, 07-02 | Public domain (US DOT) | US DOT FHWA, Next Generation Simulation (NGSIM) vehicle trajectories, data.transportation.gov |
| **NHTSA Standing General Order** | Crash reports for ADS and Level 2 ADAS | 02-01, 07-03, 07-05 | Public US government data | NHTSA, Standing General Order 2021-01 crash reporting |
| **SOTIF-PCOD** (optional) | LiDAR point clouds in KITTI format generated in CARLA for SOTIF-related conditions | 01-03, 01-08, 04-04 | CC BY 4.0 | Patel, M. (2024). *SOTIF PCOD*, IEEE DataPort, [doi:10.21227/j43q-z578](https://doi.org/10.21227/j43q-z578) |

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
