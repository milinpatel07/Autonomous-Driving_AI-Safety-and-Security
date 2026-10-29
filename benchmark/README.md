# SOTIF perception benchmark

A reproducible **triggering-condition report** for camera object detectors, in the form a SOTIF analysis
(ISO 21448, clauses 7 and 10) needs: recall per condition with confidence intervals, the parameter at which a
derived requirement stops being met, the speed limit (ODD restriction) the evidence supports, and a release
verdict against a declared requirement. Any detector can be submitted; the result is a JSON file that anyone can
re-check.

| | v1 |
|---|---|
| Data | 120 frames of the KITTI object training set (camera + Velodyne for depth), chosen by a fixed rule (below) |
| Population | box height ≥ 25 px, truncation ≤ 0.5, occlusion 0–2: **520 pedestrians**, 213 cars, 70 cyclists per condition |
| Default requirement | **PR-01** from [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb): per-frame pedestrian recall ≥ 0.90, 95 % one-sided, within the stopping distance at 60 km/h (0.6 s, 6 m/s² → 33.1 m), lateral ≤ 4 m, occlusion ≤ 1, height ≥ 25 px — 246 pedestrians in scope per condition |
| Conditions | clear; fog at meteorological visibility 200, 100, 50, 25 m; low light k = 1/64, 1/256; lens dirt 25 % |
| Matching | 2D IoU ≥ 0.5, greedy by score, one-to-one; DontCare, *Van/Truck* (car) and *Person_sitting/Cyclist* (pedestrian) regions ignored |
| Statistics | Clopper–Pearson intervals (Wilson available); false positives per frame with exact Poisson intervals |
| Runtime | about 9 min on 2 idle CPU threads for `fasterrcnn_mobilenet_v3_large_fpn` (960 detector calls, 4.5 s per frame; the committed run took 19 min on a shared, loaded machine; `ssdlite320_mobilenet_v3_large` took 6 min there, mostly for the perturbations); plus a one-off download of about 330 MB of KITTI files |

The full definition is [`spec_v1.json`](spec_v1.json) (identical to `avsafety.bench.SPEC_V1`; every result
carries its SHA-256). The perturbations are documented, with references and limitations, in
[`avsafety/perturb.py`](../avsafety/perturb.py). Leaderboard: [site/benchmark.md](../site/benchmark.md).
Walk-through: [04-06 SOTIF benchmark](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb).

## Run it

```bash
pip install -e ".[bench]"          # numpy, scipy, torch, torchvision, pillow, pandas
export AVSAFETY_CACHE=~/.cache/avsafety

# a torchvision COCO model
python -m avsafety.bench --model torchvision:fasterrcnn_mobilenet_v3_large_fpn --out results.json

# your own detector
python -m avsafety.bench --callable my_package.detector:detect --name "My detector 1.2" \
    --weights "my-weights-v3.pt (sha256 …)" --training-data "nuScenes train" --threshold 0.5 \
    --out my_detector.json --markdown my_detector.md --html my_detector.html

# re-evaluate saved outcomes against another requirement, without running the detector again
python -m avsafety.bench --rescore my_detector.objects.csv.gz --requirement TC-04-02
python -m avsafety.bench --rescore my_detector.objects.csv.gz --requirement my_requirement.json
```

`--frames 5` runs a smoke test on the first five frames (marked *not official*).

### Detector API

```python
def detect(image):            # image: numpy array, H x W x 3, uint8, RGB
    ...
    return [((x1, y1, x2, y2), score, "pedestrian"), ...]   # labels: "pedestrian", "cyclist", "car"
```

Return every detection with score ≥ 0.05; the benchmark applies the declared threshold. Load the model once at
import time (or lazily on the first call). Torch runs with `--threads` (default 2) threads.

### Requirement as a parameter

A requirement is a small JSON object (fields of `avsafety.bench.Requirement`): class, minimum recall,
confidence, the speed range and the reaction time and deceleration that turn speed into a braking-relevant
range, the scope (lateral corridor, occlusion, height, truncation), the speed grid and the conditions that are
inside the declared ODD. Presets: `PR-01` (08-05 capstone, default) and `TC-04-02` (the 65 % requirement of
[04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb)).

Verdicts: **meets** if the one-sided lower confidence bound ≥ target; **does not meet** if the one-sided upper
bound < target; otherwise **inconclusive**. The supported speed of a condition is the highest speed of the grid
at which the requirement is met for the range that speed needs. Release: **RELEASE** if met at full speed in
every ODD condition; **RELEASE WITH ODD RESTRICTION** if met in clear air at some speed (each ODD condition is
then claimed only up to its supported speed, or excluded with an ODD monitor); otherwise **DO NOT RELEASE** —
the decision rule of the 08-05 capstone.

## Submit a result

1. Run the full benchmark (no `--frames`) with the threshold you declare **before** looking at the results.
2. Add `benchmark/results/<name>.json` and `<name>.objects.csv.gz` in a pull request.
3. In the pull request, state the model, weights (file name and hash or a release URL), code version, training
   data and the hardware. The CI validates every result against [`schema.json`](schema.json) and the spec hash
   (`python scripts/build_leaderboard.py --check`). A maintainer can re-run it with the *Benchmark* workflow.
4. After merging, `python scripts/build_leaderboard.py` regenerates the leaderboard page.

**Rules.**
- No training, fine-tuning, calibration or threshold selection on the 120 benchmark frames. Models trained on
  KITTI must exclude these frames and say so in `training_data`; otherwise the result is not eligible.
- One operating threshold for all classes and conditions, declared in the submission.
- No condition-specific pre-processing triggered by knowledge of the benchmark (e.g. a de-fogging step tuned on
  these frames). Generic, documented pre-processing that is part of the product is allowed.
- Report the result as produced; partial runs are not listed.

## What it can and cannot claim

- The fog, low light and dirt are **models on real daytime images**. KITTI has no fog, night or rain. A benchmark
  rank says how a detector degrades under these documented models; it is not evidence about real fog until the
  model has been validated against real-condition data (e.g. Bijelic et al., CVPR 2020).
- Recall is **per frame**. 120 frames from one city are not independent encounters; the intervals cover
  sampling noise of the labels, not the dependence between frames or the representativeness of Karlsruhe.
- COCO-pretrained baselines reach KITTI classes through a mapping (person → pedestrian; car, truck → car;
  person on a bicycle → cyclist) that costs them some recall; the cyclist fusion is a heuristic.
- A release verdict from this benchmark is component evidence for a SOTIF argument, never a vehicle release.

## LiDAR track (optional): SOTIF-PCOD

[SOTIF-PCOD](https://doi.org/10.21227/j43q-z578) (Patel, IEEE DataPort, 2024) contains 547 LiDAR frames in KITTI
format generated in CARLA for a highway lane-change scenario under 21 weather presets (Clear, Cloudy, Wet,
WetCloudy, MidRainy, HardRain, SoftRain × Noon, Sunset, Night). It needs an IEEE DataPort login. Then:

```python
import os
from avsafety import bench
os.environ["SOTIF_PCOD_DIR"] = "/path/to/SOTIF_kitti_carla"
report = bench.evaluate_lidar(my_lidar_detector)   # detector(points N x 4) -> [((x, y, z, l, w, h, yaw), score, label)]
```

Matching uses the bird's-eye-view centre distance (≤ 2 m, greedy by score), as in the nuScenes detection metric.
The condition of each frame comes from a folder name containing a CARLA preset (e.g. `HardRainNight/`) or from a
`frame,condition` CSV passed as `conditions_csv`. The loader follows the documented KITTI layout
(`velodyne/`, `label_2/`, `calib/`) and has been run on KITTI itself and on synthetic folders; it has **not yet
been run on the released SOTIF-PCOD archive**. `bench.lidar_cluster_baseline` is a non-learned reference floor
(ground removal, clustering, size rules).

## Licences

- Code: MIT (repository licence).
- KITTI: CC BY-NC-SA 3.0, non-commercial use only (Geiger, Lenz, Urtasun, CVPR 2012). The per-object outcome
  files contain values derived from KITTI labels and are shared under the same terms.
- SOTIF-PCOD: CC BY 4.0, as listed in the course's [data page](../site/datasets.md); check the licence on the
  IEEE DataPort record before redistribution.
