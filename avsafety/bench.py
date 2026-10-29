"""SOTIF perception benchmark: a standard triggering-condition report for any detector.

A detector is evaluated on a fixed, versioned set of real KITTI frames under
physically grounded triggering conditions (fog from LiDAR depth, low light with
sensor noise, lens dirt; see :mod:`avsafety.perturb`). The report gives recall by
distance band, KITTI occlusion level and truncation, false positives per frame,
confidence intervals, a triggering-condition table with verdicts against a declared
requirement, the speed limit (ODD restriction) the evidence supports per condition,
and a release verdict.

Detector API (camera track)
---------------------------
``detector(image) -> iterable of (box, score, label)`` where ``image`` is an
``H x W x 3`` ``uint8`` RGB array, ``box`` is ``(x1, y1, x2, y2)`` in pixels,
``score`` is in [0, 1] and ``label`` is one of ``"pedestrian"``, ``"cyclist"``,
``"car"`` (other labels are ignored). Return every detection with score >= 0.05;
the operating threshold is applied by the benchmark.

Command line
------------
``python -m avsafety.bench --model torchvision:fasterrcnn_mobilenet_v3_large_fpn --out results.json``
``python -m avsafety.bench --callable mypackage.mymodule:detect --name "my detector" --out results.json``
``python -m avsafety.bench --rescore results.objects.csv.gz --requirement TC-04-02``
``python -m avsafety.bench --validate results.json``

LiDAR track (optional): :func:`evaluate_lidar` evaluates a point-cloud detector on a
KITTI-format directory such as SOTIF-PCOD (Patel & Jung, VEHITS 2024,
https://doi.org/10.5220/0012707300003702; data doi:10.21227/j43q-z578).

Statistics: Clopper, C. J., Pearson, E. S. (1934), Biometrika 26(4), 404-413,
https://doi.org/10.1093/biomet/26.4.404; Wilson, E. B. (1927), JASA 22, 209-212,
https://doi.org/10.1080/01621459.1927.10502953.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

import numpy as np

from . import perturb, sotif, validation

CLASSES = ("pedestrian", "cyclist", "car")
SCHEMA_VERSION = "1.0"
VERDICTS = ("meets", "does not meet", "inconclusive", "no data")
RELEASE_VERDICTS = ("RELEASE", "RELEASE WITH ODD RESTRICTION", "DO NOT RELEASE")


# =========================================================================== specification
def _spec_v1() -> dict:
    frames = [134, 145, 189, 251, 287, 311, 342, 412, 436, 462, 464, 780, 874, 928, 937, 1046, 1070, 1207, 1221,
              1252, 1409, 1426, 1433, 1468, 1487, 1525, 1558, 1611, 1682, 1912, 1958, 2133, 2149, 2161, 2175, 2440,
              2536, 2725, 2775, 2851, 2870, 2889, 2915, 2920, 2943, 3074, 3133, 3146, 3171, 3267, 3294, 3298, 3367,
              3390, 3437, 3438, 3466, 3511, 3550, 3555, 3628, 3632, 3668, 3753, 3765, 3784, 3800, 3876, 4002, 4014,
              4028, 4177, 4400, 4488, 4619, 4897, 4968, 5031, 5075, 5085, 5131, 5245, 5286, 5287, 5336, 5434, 5523,
              5608, 5617, 5670, 5688, 5813, 5824, 5980, 5988, 6070, 6082, 6083, 6088, 6139, 6174, 6189, 6213, 6334,
              6427, 6486, 6511, 6528, 6749, 6752, 6761, 6785, 6980, 7070, 7129, 7189, 7254, 7260, 7265, 7406]
    return {
        "name": "SOTIF perception benchmark (KITTI camera track)",
        "spec_version": "1",
        "dataset": {
            "name": "KITTI object detection benchmark, training split (left colour camera, Velodyne HDL-64E)",
            "licence": "CC BY-NC-SA 3.0 (non-commercial)",
            "citation": "Geiger, Lenz, Urtasun (2012), CVPR, https://doi.org/10.1109/CVPR.2012.6248074",
        },
        "frame_rule": {
            "description": ("All KITTI object training frames with at least 2 'Pedestrian' labels whose distance "
                            "sqrt(x^2 + z^2) is <= 40 m form the pool; 120 frames are drawn without replacement "
                            "with numpy.random.default_rng(21448).choice(pool, 120, replace=False) and sorted."),
            "min_pedestrians": 2, "max_distance_m": 40.0, "pool_size": 708, "n_frames": 120, "seed": 21448,
        },
        "frames": frames,
        "classes": {
            "pedestrian": {"kitti": ["Pedestrian"], "ignore": ["Person_sitting", "Cyclist"]},
            "cyclist": {"kitti": ["Cyclist"], "ignore": []},
            "car": {"kitti": ["Car"], "ignore": ["Van", "Truck"]},
        },
        "population": {"min_height_px": 25.0, "max_truncation": 0.5, "occlusion_levels": [0, 1, 2]},
        "matching": {
            "rule": "2d_iou", "iou": 0.5, "order": "descending score, one-to-one, best IoU among free labels",
            "ignore_iou": 0.5, "dontcare_ioa": 0.5,
            "note": ("A detection matched to a label outside the population, overlapping an 'ignore' class "
                     "(IoU >= 0.5) or covered by a DontCare region (>= 50 % of its area) is neither TP nor FP."),
        },
        "distance_bands_m": [[0, 10], [10, 20], [20, 30], [30, 40], [40, None]],
        "truncation_bins": [[0.0, 0.15], [0.15, 0.30], [0.30, 0.50]],
        "conditions": [
            {"id": "clear", "type": "clear", "label": "clear (original image)"},
            {"id": "fog_200", "type": "fog", "visibility_m": 200, "airlight": 0.8, "label": "fog, V = 200 m"},
            {"id": "fog_100", "type": "fog", "visibility_m": 100, "airlight": 0.8, "label": "fog, V = 100 m"},
            {"id": "fog_50", "type": "fog", "visibility_m": 50, "airlight": 0.8, "label": "fog, V = 50 m"},
            {"id": "fog_25", "type": "fog", "visibility_m": 25, "airlight": 0.8, "label": "fog, V = 25 m"},
            {"id": "low_light_64", "type": "low_light", "light_factor": 1 / 64, "full_well_e": 4000.0,
             "read_noise_e": 4.0, "label": "low light, k = 1/64"},
            {"id": "low_light_256", "type": "low_light", "light_factor": 1 / 256, "full_well_e": 4000.0,
             "read_noise_e": 4.0, "label": "low light, k = 1/256"},
            {"id": "lens_dirt_25", "type": "lens_dirt", "coverage": 0.25, "label": "lens dirt, 25 % covered"},
        ],
        "randomness": "stochastic conditions use numpy.random.default_rng(frame_index), one fresh generator per frame and condition",
        "score_threshold_policy": ("One operating threshold for all classes and conditions, declared with the "
                                   "submission before evaluation (default 0.5). Detections with score >= 0.05 are "
                                   "stored so that the report can be recomputed at the declared threshold."),
        "min_stored_score": 0.05,
        "confidence": 0.95,
        "interval": "clopper-pearson",
    }


SPEC_V1 = _spec_v1()


def spec_hash(spec: dict) -> str:
    """SHA-256 of the canonical JSON form of a spec (identifies the exact benchmark version)."""
    return hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_spec(path=None) -> dict:
    """The built-in v1 spec, or a spec read from a JSON file."""
    return SPEC_V1 if path is None else json.loads(Path(path).read_text())


def select_frames(labels, min_pedestrians: int = 2, max_distance_m: float = 40.0, n: int = 120,
                  seed: int = 21448) -> list[int]:
    """Re-derive the frame list from all KITTI labels (``avsafety.data.kitti_object_labels_all()``)."""
    ped = labels[labels["type"] == "Pedestrian"]
    counts = ped[ped["distance_m"] <= max_distance_m].groupby("frame").size()
    pool = sorted(int(f) for f in counts[counts >= min_pedestrians].index)
    return sorted(np.random.default_rng(seed).choice(pool, n, replace=False).tolist())


# =========================================================================== statistics
def binomial_interval(k: int, n: int, confidence: float = 0.95, method: str = "clopper-pearson",
                      sides: int = 2) -> tuple[float, float]:
    """Confidence interval for a binomial proportion k / n.

    ``method`` 'clopper-pearson' (exact) or 'wilson' (score interval). With ``sides=1``
    each bound is the one-sided bound at ``confidence`` (lower and upper returned
    together). n = 0 returns (0, 1).
    """
    if n < 0 or not 0 <= k <= n or not 0 < confidence < 1:
        raise ValueError("need 0 <= k <= n and 0 < confidence < 1")
    if n == 0:
        return 0.0, 1.0
    from scipy import stats
    alpha = (1 - confidence) / (2 if sides == 2 else 1)
    if method == "clopper-pearson":
        lo = 0.0 if k == 0 else float(stats.beta.ppf(alpha, k, n - k + 1))
        hi = 1.0 if k == n else float(stats.beta.ppf(1 - alpha, k + 1, n - k))
        return lo, hi
    if method == "wilson":
        z = float(stats.norm.ppf(1 - alpha))
        p = k / n
        centre = (p + z * z / (2 * n)) / (1 + z * z / n)
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        return max(0.0, centre - half), min(1.0, centre + half)
    raise ValueError("method must be 'clopper-pearson' or 'wilson'")


def verdict(k: int, n: int, target: float, confidence: float = 0.95, method: str = "clopper-pearson") -> str:
    """'meets' if the one-sided lower bound >= target, 'does not meet' if the one-sided upper
    bound < target, otherwise 'inconclusive' ('no data' if n = 0)."""
    if n == 0:
        return "no data"
    lo, hi = binomial_interval(k, n, confidence, method, sides=1)
    if lo >= target:
        return "meets"
    if hi < target:
        return "does not meet"
    return "inconclusive"


# =========================================================================== geometry and matching
def box_iou(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Pairwise IoU of boxes a (N x 4) and b (M x 4) in xyxy pixels."""
    a, b = np.asarray(a, float).reshape(-1, 4), np.asarray(b, float).reshape(-1, 4)
    lt = np.maximum(a[:, None, :2], b[None, :, :2])
    rb = np.minimum(a[:, None, 2:], b[None, :, 2:])
    inter = np.prod(np.clip(rb - lt, 0, None), axis=2)
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    union = area_a[:, None] + area_b[None, :] - inter
    return np.where(union > 0, inter / np.where(union > 0, union, 1), 0.0)


def box_ioa(a: np.ndarray, region: np.ndarray) -> np.ndarray:
    """Fraction of each box in a (N x 4) covered by each region (M x 4)."""
    a, region = np.asarray(a, float).reshape(-1, 4), np.asarray(region, float).reshape(-1, 4)
    lt = np.maximum(a[:, None, :2], region[None, :, :2])
    rb = np.minimum(a[:, None, 2:], region[None, :, 2:])
    inter = np.prod(np.clip(rb - lt, 0, None), axis=2)
    area = np.clip((a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1]), 1e-9, None)
    return inter / area[:, None]


def match_class(gt_boxes, gt_in_population, det_boxes, det_scores, ignore_boxes=None, dontcare_boxes=None,
                iou: float = 0.5, ignore_iou: float = 0.5, dontcare_ioa: float = 0.5):
    """Match the detections of one class to the labels of that class in one image.

    Greedy in order of descending score; each detection takes the free label with the
    highest IoU >= ``iou``. Because of the greedy order, the matching at any threshold is
    a prefix of this matching, so the returned per-label score decides detection at
    every threshold (detected at tau iff score >= tau).

    Returns
    -------
    gt_score : float array (len gt): score of the matched detection, 0 if never matched.
    det_status : str array (len det): 'tp', 'ignored' or 'fp'.
    """
    gt_boxes = np.asarray(gt_boxes, float).reshape(-1, 4)
    det_boxes = np.asarray(det_boxes, float).reshape(-1, 4)
    det_scores = np.asarray(det_scores, float).reshape(-1)
    pop = np.asarray(gt_in_population, bool).reshape(-1)
    gt_score = np.zeros(len(gt_boxes))
    status = np.full(len(det_boxes), "fp", dtype=object)
    if len(det_boxes) == 0:
        return gt_score, status.astype(str)
    M = box_iou(det_boxes, gt_boxes) if len(gt_boxes) else np.zeros((len(det_boxes), 0))
    ign = (box_iou(det_boxes, ignore_boxes).max(axis=1) >= ignore_iou
           if ignore_boxes is not None and len(ignore_boxes) else np.zeros(len(det_boxes), bool))
    dc = (box_ioa(det_boxes, dontcare_boxes).max(axis=1) >= dontcare_ioa
          if dontcare_boxes is not None and len(dontcare_boxes) else np.zeros(len(det_boxes), bool))
    free = np.ones(len(gt_boxes), bool)
    for j in np.argsort(-det_scores, kind="stable"):
        cand = np.flatnonzero(free & (M[j] >= iou)) if len(gt_boxes) else []
        if len(cand):
            g = cand[np.argmax(M[j, cand])]
            free[g] = False
            gt_score[g] = det_scores[j]
            status[j] = "tp" if pop[g] else "ignored"
        elif ign[j] or dc[j]:
            status[j] = "ignored"
    return gt_score, status.astype(str)


def in_population(label: dict, spec: dict = SPEC_V1) -> bool:
    """Whether a KITTI label belongs to the evaluated population of the spec."""
    p = spec["population"]
    return (label["y2"] - label["y1"] >= p["min_height_px"] and label["truncated"] <= p["max_truncation"]
            and int(label["occluded"]) in p["occlusion_levels"])


# =========================================================================== detectors
COCO_TO_BENCH = {1: "pedestrian", 3: "car", 8: "car"}   # COCO person, car, truck
COCO_BICYCLE = 2


def coco_to_bench(boxes, scores, labels, min_score: float = 0.05):
    """Map COCO detections (torchvision label ids) to benchmark classes.

    person -> pedestrian; car and truck -> car (KITTI 'Van' and 'Truck' are ignore regions
    for car); a person whose box centre lies over a bicycle box and overlaps it by >= 20 %
    of the person's area is fused with the bicycle into one 'cyclist' (box = union,
    score = geometric mean). COCO has no rider class, so this pairing is a heuristic.
    """
    boxes, scores, labels = np.asarray(boxes, float).reshape(-1, 4), np.asarray(scores, float), np.asarray(labels)
    keep = scores >= min_score
    boxes, scores, labels = boxes[keep], scores[keep], labels[keep]
    persons = np.flatnonzero(labels == 1)
    bikes = list(np.flatnonzero(labels == COCO_BICYCLE))
    used_person, out = set(), []
    for p in persons[np.argsort(-scores[persons], kind="stable")]:
        if not bikes:
            break
        pb = boxes[p]
        cx = 0.5 * (pb[0] + pb[2])
        ioa = box_ioa(pb[None], boxes[bikes])[0]
        ok = [i for i, b in enumerate(bikes) if ioa[i] >= 0.2 and boxes[b][0] <= cx <= boxes[b][2]]
        if ok:
            b = bikes.pop(max(ok, key=lambda i: scores[bikes[i]]))
            union = [min(pb[0], boxes[b][0]), min(pb[1], boxes[b][1]), max(pb[2], boxes[b][2]), max(pb[3], boxes[b][3])]
            out.append((tuple(union), float(math.sqrt(scores[p] * scores[b])), "cyclist"))
            used_person.add(int(p))
    for i, (b, s, l) in enumerate(zip(boxes, scores, labels)):
        cls = COCO_TO_BENCH.get(int(l))
        if cls and i not in used_person:
            out.append((tuple(b), float(s), cls))
    return out


def torchvision_detector(name: str, threads: int = 2, min_score: float = 0.05, device: str = "cpu"):
    """A benchmark detector from a COCO-pretrained torchvision model (e.g. 'fasterrcnn_mobilenet_v3_large_fpn').

    Weights are downloaded once from download.pytorch.org (torchvision ``weights="DEFAULT"``).
    """
    import torch
    from torchvision.models import detection as tvd

    torch.set_num_threads(threads)
    builder = getattr(tvd, name, None)
    if builder is None:
        raise ValueError(f"torchvision.models.detection has no model '{name}'")
    kwargs = {"box_score_thresh": min_score} if "rcnn" in name else {"score_thresh": min_score}
    model = builder(weights="DEFAULT", **kwargs).eval().to(device)
    import torchvision
    weights = torchvision.models.get_model_weights(name).DEFAULT

    def detect(image: np.ndarray):
        x = torch.from_numpy(np.array(image, dtype=np.uint8)).permute(2, 0, 1).float().div(255).to(device)
        with torch.inference_mode():
            out = model([x])[0]
        return coco_to_bench(out["boxes"].cpu().numpy(), out["scores"].cpu().numpy(), out["labels"].cpu().numpy(),
                             min_score)

    detect.meta = {"model": f"torchvision:{name}", "weights": f"{weights} (COCO)",
                   "framework": f"torch {torch.__version__}, torchvision {torchvision.__version__}",
                   "training_data": "COCO 2017 train (no KITTI)"}
    return detect


def load_callable(spec: str):
    """Import ``module:function`` (``module`` may be a dotted name or a path to a .py file)."""
    mod_name, _, attr = spec.partition(":")
    if not attr:
        raise ValueError("use the form module:function")
    if mod_name.endswith(".py"):
        path = Path(mod_name).resolve()
        sys.path.insert(0, str(path.parent))
        mod_name = path.stem
    module = importlib.import_module(mod_name)
    fn = getattr(module, attr)
    if not callable(fn):
        raise TypeError(f"{spec} is not callable")
    return fn


# =========================================================================== conditions
def apply_condition(frame, condition: dict, depth=None):
    """Image of ``frame`` under ``condition`` (a spec entry); returns (image, dirt opacity or None)."""
    kind, img = condition["type"], frame.image
    if kind == "clear":
        return img, None
    if kind == "fog":
        if depth is None:
            depth = perturb.dense_range(frame)
        return perturb.fog(img, depth, condition["visibility_m"], condition.get("airlight", perturb.AIRLIGHT)), None
    rng = np.random.default_rng(int(frame.index))
    if kind == "low_light":
        return perturb.low_light(img, condition["light_factor"], rng, condition.get("full_well_e", 4000.0),
                                 condition.get("read_noise_e", 4.0)), None
    if kind == "lens_dirt":
        alpha = perturb.dirt_mask(img.shape, condition["coverage"], rng)
        return perturb.lens_dirt(img, alpha), alpha
    raise ValueError(f"unknown condition type {kind}")


# =========================================================================== requirement
@dataclass(frozen=True)
class Requirement:
    """A declared per-frame recall requirement and the ODD it is claimed for.

    The scope is the class within the braking-relevant range, i.e. the stopping
    distance ``avsafety.sotif.stopping_distance(v, reaction_s, decel_mps2)`` at the speed
    considered. ``odd_conditions`` are the benchmark conditions inside the specified ODD;
    the others are triggering conditions outside it (they need an ODD monitor).
    """

    id: str = "PR-01"
    cls: str = "pedestrian"
    min_recall: float = 0.90
    confidence: float = 0.95
    method: str = "clopper-pearson"
    max_speed_kmh: float = 60.0
    reaction_s: float = 0.6
    decel_mps2: float = 6.0
    lateral_m: float | None = 4.0
    min_height_px: float = 25.0
    max_occlusion: int = 1
    max_truncation: float | None = None
    speeds_kmh: tuple = (10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
    odd_conditions: tuple = ("clear", "low_light_64")
    max_fp_per_frame: float | None = None
    source: str = ("08-05 capstone PR-01: per-frame pedestrian recall >= 0.90 with 95 % one-sided confidence "
                   "within the stopping distance at 60 km/h (0.6 s, 6 m/s^2), |lateral| <= 4 m, "
                   "occlusion <= 1, height >= 25 px")

    def range_m(self, speed_kmh: float | None = None) -> float:
        v = self.max_speed_kmh if speed_kmh is None else speed_kmh
        return sotif.stopping_distance(v / 3.6, self.reaction_s, self.decel_mps2)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["speeds_kmh"], d["odd_conditions"] = list(self.speeds_kmh), list(self.odd_conditions)
        d["range_m"] = round(self.range_m(), 2)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Requirement":
        d = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        for k in ("speeds_kmh", "odd_conditions"):
            if k in d:
                d[k] = tuple(d[k])
        return cls(**d)


REQUIREMENTS = {
    "PR-01": Requirement(),
    "TC-04-02": Requirement(
        id="TC-04-02", min_recall=0.65, confidence=0.975, reaction_s=0.5, lateral_m=None, max_occlusion=1,
        max_truncation=0.30, source=("04-02 derived requirement (illustrative): per-frame pedestrian recall >= 0.65 "
                                     "for KITTI Easy/Moderate pedestrians within the stopping distance at 60 km/h "
                                     "(0.5 s, 6 m/s^2); 97.5 % one-sided = the two-sided 95 % interval of 04-02")),
}


def get_requirement(req) -> Requirement:
    """A :class:`Requirement` from an instance, a preset name, a dict or a JSON file path."""
    if isinstance(req, Requirement):
        return req
    if req is None:
        return REQUIREMENTS["PR-01"]
    if isinstance(req, dict):
        return Requirement.from_dict(req)
    if req in REQUIREMENTS:
        return REQUIREMENTS[req]
    return Requirement.from_dict(json.loads(Path(req).read_text()))


# =========================================================================== evaluation
OBJECT_COLUMNS = ["kind", "frame", "condition", "cls", "score", "distance_m", "lateral_m", "occluded",
                  "truncated", "height_px", "in_population", "under_dirt"]


def _evaluate_image(dets, labels, spec, frame_id, condition_id, dirt=None):
    """Rows (label outcomes and stored false positives) for one image."""
    rows = []
    min_score = spec["min_stored_score"]
    m = spec["matching"]
    dontcare = np.array([[l["x1"], l["y1"], l["x2"], l["y2"]] for l in labels if l["type"] == "DontCare"]).reshape(-1, 4)
    for cls, c in spec["classes"].items():
        gts = [l for l in labels if l["type"] in c["kitti"]]
        ign = np.array([[l["x1"], l["y1"], l["x2"], l["y2"]] for l in labels if l["type"] in c["ignore"]]).reshape(-1, 4)
        d = [(b, s) for b, s, lab in dets if lab == cls and s >= min_score]
        db = np.array([b for b, _ in d], float).reshape(-1, 4)
        ds = np.array([s for _, s in d], float)
        gb = np.array([[l["x1"], l["y1"], l["x2"], l["y2"]] for l in gts]).reshape(-1, 4)
        pop = [in_population(l, spec) for l in gts]
        gscore, status = match_class(gb, pop, db, ds, ign, dontcare, m["iou"], m["ignore_iou"], m["dontcare_ioa"])
        for l, s, p in zip(gts, gscore, pop):
            under = None
            if dirt is not None:
                cy = min(int((l["y1"] + l["y2"]) / 2), dirt.shape[0] - 1)
                cx = min(int((l["x1"] + l["x2"]) / 2), dirt.shape[1] - 1)
                under = bool(dirt[cy, cx] > 0.5)
            rows.append(("gt", frame_id, condition_id, cls, float(s), float(math.hypot(l["x"], l["z"])), float(l["x"]),
                         int(l["occluded"]), float(l["truncated"]), float(l["y2"] - l["y1"]), bool(p), under))
        for s in ds[status == "fp"]:
            rows.append(("fp", frame_id, condition_id, cls, float(s), None, None, None, None, None, None, None))
    return rows


def evaluate(detector, spec: dict = SPEC_V1, frames=None, conditions=None, threshold: float = 0.5,
             submission: dict | None = None, progress=None) -> "Report":
    """Run ``detector`` on the benchmark frames under every condition and return a :class:`Report`.

    ``frames`` / ``conditions`` restrict the run (a smoke test); an official result uses
    all of them. ``progress`` is an optional callable(done, total) for a progress display.
    """
    import pandas as pd
    from . import data as D

    frames = list(spec["frames"] if frames is None else frames)
    conds = [c for c in spec["conditions"] if conditions is None or c["id"] in conditions]
    rows, t0 = [], time.time()
    for n_done, idx in enumerate(frames):
        frame = D.kitti_object(int(idx))
        depth = perturb.dense_range(frame) if any(c["type"] == "fog" for c in conds) else None
        for cond in conds:
            img, dirt = apply_condition(frame, cond, depth)
            dets = [(tuple(map(float, b)), float(s), str(lab)) for b, s, lab in detector(img)]
            rows += _evaluate_image(dets, frame.labels, spec, int(idx), cond["id"], dirt)
        if progress:
            progress(n_done + 1, len(frames))
    objects = pd.DataFrame(rows, columns=OBJECT_COLUMNS)
    sub = dict(submission or {})
    sub.setdefault("score_threshold", threshold)
    meta = {"runtime_s": round(time.time() - t0, 1), "n_frames": len(frames), "conditions": [c["id"] for c in conds],
            "official": len(frames) == len(spec["frames"]) and len(conds) == len(spec["conditions"]),
            "hardware": f"{platform.machine()}, {platform.system()}, Python {platform.python_version()}"}
    return Report(objects=objects, spec=spec, submission=sub, run=meta)


# =========================================================================== report
def _fmt_band(band):
    lo, hi = band
    return f"{lo}-{hi} m" if hi is not None else f">= {lo} m"


@dataclass
class Report:
    """Per-object outcomes of one benchmark run and every table derived from them."""

    objects: object                       # pandas DataFrame with OBJECT_COLUMNS
    spec: dict = field(default_factory=lambda: SPEC_V1)
    submission: dict = field(default_factory=dict)
    run: dict = field(default_factory=dict)

    # ------------------------------------------------------------------ helpers
    @property
    def threshold(self) -> float:
        return float(self.submission.get("score_threshold", 0.5))

    @property
    def n_frames(self) -> int:
        return int(self.run.get("n_frames", self.objects["frame"].nunique()))

    def _gt(self):
        g = self.objects[self.objects["kind"] == "gt"].copy()
        g["detected"] = g["score"] >= self.threshold
        return g

    def _ci(self, k, n):
        return binomial_interval(int(k), int(n), self.spec.get("confidence", 0.95), self.spec.get("interval", "clopper-pearson"))

    def _stat(self, df) -> dict:
        n, k = len(df), int(df["detected"].sum())
        lo, hi = self._ci(k, n)
        return {"n": n, "detected": k, "recall": round(k / n, 4) if n else None, "ci_low": round(lo, 4), "ci_high": round(hi, 4)}

    def _conditions(self):
        ids = self.run.get("conditions") or list(dict.fromkeys(self.objects["condition"]))
        return [c for c in self.spec["conditions"] if c["id"] in ids]

    # ------------------------------------------------------------------ tables
    def by_condition(self) -> list[dict]:
        g = self._gt()
        g = g[g["in_population"].astype(bool)]
        fp = self.objects[(self.objects["kind"] == "fp") & (self.objects["score"] >= self.threshold)]
        out = []
        for c in self._conditions():
            for cls in CLASSES:
                s = self._stat(g[(g["condition"] == c["id"]) & (g["cls"] == cls)])
                n_fp = int(((fp["condition"] == c["id"]) & (fp["cls"] == cls)).sum())
                lo, hi = validation.poisson_rate_interval(n_fp, self.n_frames, self.spec.get("confidence", 0.95))
                out.append({"condition": c["id"], "class": cls, **s, "fp": n_fp,
                            "fp_per_frame": round(n_fp / self.n_frames, 4),
                            "fp_per_frame_ci": [round(lo, 4), round(hi, 4)]})
        return out

    def by_distance(self) -> list[dict]:
        g = self._gt()
        g = g[g["in_population"].astype(bool)]
        out = []
        for c in self._conditions():
            for cls in CLASSES:
                sub = g[(g["condition"] == c["id"]) & (g["cls"] == cls)]
                for band in self.spec["distance_bands_m"]:
                    lo, hi = band
                    sel = sub[(sub["distance_m"] >= lo) & ((sub["distance_m"] < hi) if hi is not None else True)]
                    out.append({"condition": c["id"], "class": cls, "band": _fmt_band(band), **self._stat(sel)})
        return out

    def by_occlusion(self, condition: str = "clear") -> list[dict]:
        g = self._gt()
        p = self.spec["population"]
        g = g[(g["condition"] == condition) & (g["height_px"] >= p["min_height_px"]) & (g["truncated"] <= p["max_truncation"])]
        return [{"class": cls, "occlusion": lvl, **self._stat(g[(g["cls"] == cls) & (g["occluded"] == lvl)])}
                for cls in CLASSES for lvl in (0, 1, 2)]

    def by_truncation(self, condition: str = "clear") -> list[dict]:
        g = self._gt()
        p = self.spec["population"]
        g = g[(g["condition"] == condition) & (g["height_px"] >= p["min_height_px"]) & g["occluded"].isin(p["occlusion_levels"])]
        out = []
        for cls in CLASSES:
            for i, (lo, hi) in enumerate(self.spec["truncation_bins"]):
                sel = g[(g["cls"] == cls) & (g["truncated"] <= hi) & ((g["truncated"] > lo) if i else True)]
                out.append({"class": cls, "truncation": f"{lo:.2f}-{hi:.2f}", **self._stat(sel)})
        return out

    def lens_dirt_split(self) -> list[dict]:
        g = self._gt()
        g = g[g["in_population"].astype(bool) & g["condition"].str.startswith("lens_dirt")]
        out = []
        for cid in dict.fromkeys(g["condition"]):
            for cls in CLASSES:
                for where, flag in (("outside dirt", False), ("behind dirt", True)):
                    sel = g[(g["condition"] == cid) & (g["cls"] == cls) & (g["under_dirt"].astype(bool) == flag)]
                    out.append({"condition": cid, "class": cls, "where": where, **self._stat(sel)})
        return out

    # ------------------------------------------------------------------ requirement
    def _scope(self, g, req: Requirement, range_m: float):
        sel = (g["cls"] == req.cls) & (g["height_px"] >= req.min_height_px) & (g["occluded"] <= req.max_occlusion) \
            & (g["distance_m"] <= range_m)
        if req.lateral_m is not None:
            sel &= g["lateral_m"].abs() <= req.lateral_m
        if req.max_truncation is not None:
            sel &= g["truncated"] <= req.max_truncation
        return g[sel]

    def triggering_conditions(self, requirement=None) -> list[dict]:
        """Condition -> measured recall in the requirement scope -> verdict -> supported speed limit."""
        req = get_requirement(requirement)
        g = self._gt()
        fp = self.objects[(self.objects["kind"] == "fp") & (self.objects["score"] >= self.threshold)
                          & (self.objects["cls"] == req.cls)]
        out = []
        for c in self._conditions():
            gc = g[g["condition"] == c["id"]]
            s = self._scope(gc, req, req.range_m())
            k, n = int(s["detected"].sum()), len(s)
            lo, hi = binomial_interval(k, n, req.confidence, req.method, sides=1)
            v = verdict(k, n, req.min_recall, req.confidence, req.method)
            ok_speeds = [sp for sp in req.speeds_kmh if sp <= req.max_speed_kmh and
                         verdict(*(lambda d: (int(d["detected"].sum()), len(d)))(self._scope(gc, req, req.range_m(sp))),
                                 req.min_recall, req.confidence, req.method) == "meets"]
            vmax = max(ok_speeds) if ok_speeds else None
            fp_rate = float((fp["condition"] == c["id"]).sum()) / self.n_frames
            in_odd = c["id"] in req.odd_conditions
            if v == "meets":
                measure = "none (requirement demonstrated in full scope)"
            elif vmax is not None:
                measure = f"ODD restriction: claim function only up to {vmax:g} km/h in this condition"
            elif v == "inconclusive":
                measure = "more data needed; until demonstrated, exclude from the ODD (ODD monitor) or improve the design"
            else:
                measure = "exclude condition from the ODD (needs an ODD monitor) or improve the design"
            out.append({"condition": c["id"], "label": c.get("label", c["id"]), "in_odd": in_odd,
                        "n": n, "detected": k, "recall": round(k / n, 4) if n else None,
                        "lower_bound": round(lo, 4), "upper_bound": round(hi, 4), "verdict": v,
                        "v_max_kmh": vmax, "range_at_v_max_m": round(req.range_m(vmax), 1) if vmax else None,
                        "fp_per_frame": round(fp_rate, 4), "measure": measure})
        return out

    def release(self, requirement=None) -> dict:
        """Release verdict for the declared requirement (decision rule of the 08-05 capstone).

        RELEASE: met at the full speed in every ODD condition (and the FP limit, if any, holds).
        RELEASE WITH ODD RESTRICTION: met in clear air at some speed; each ODD condition is then
        claimed only up to its supported speed, or excluded (monitor needed) if there is none.
        DO NOT RELEASE: not demonstrated in clear air at any speed of the grid.
        """
        req = get_requirement(requirement)
        tct = {r["condition"]: r for r in self.triggering_conditions(req)}
        odd = [c for c in req.odd_conditions if c in tct]
        reasons = []
        fp_ok = True
        if req.max_fp_per_frame is not None:
            n_fp = sum(int(round(tct[c]["fp_per_frame"] * self.n_frames)) for c in odd)
            ub = validation.poisson_upper_bound(n_fp, self.n_frames * max(len(odd), 1), req.confidence)
            fp_ok = ub <= req.max_fp_per_frame
            reasons.append(f"false positives per frame (upper {req.confidence:.0%} bound) {ub:.3f} vs limit {req.max_fp_per_frame}")
        full = all(tct[c]["verdict"] == "meets" for c in odd) and bool(odd) and fp_ok
        clear = tct.get("clear")
        if full:
            v = "RELEASE"
        elif clear is not None and clear["v_max_kmh"] is not None and fp_ok:
            v = "RELEASE WITH ODD RESTRICTION"
        else:
            v = "DO NOT RELEASE"
        restricted = {c: tct[c]["v_max_kmh"] for c in odd}
        for c in odd:
            r = tct[c]
            reasons.append(f"{r['label']}: recall {r['recall']} (n = {r['n']}, one-sided lower bound "
                           f"{r['lower_bound']:.3f} vs {req.min_recall}) -> {r['verdict']}; supported up to "
                           + (f"{r['v_max_kmh']:g} km/h" if r["v_max_kmh"] else "no speed in the grid"))
        outside = [r["label"] for r in tct.values() if not r["in_odd"] and r["verdict"] != "meets"]
        return {"verdict": v, "requirement": req.id, "odd_conditions": odd, "restricted_odd_kmh": restricted,
                "outside_odd_not_met": outside, "reasons": reasons,
                "rule": "RELEASE if met at full speed in all ODD conditions; RELEASE WITH ODD RESTRICTION if met in "
                        "clear air at some speed; otherwise DO NOT RELEASE"}

    # ------------------------------------------------------------------ serialisation
    def to_dict(self, requirement=None) -> dict:
        req = get_requirement(requirement)
        return {
            "schema_version": SCHEMA_VERSION,
            "benchmark": {"name": self.spec["name"], "spec_version": self.spec["spec_version"],
                          "spec_sha256": spec_hash(self.spec)},
            "submission": self.submission,
            "run": self.run,
            "requirement": req.to_dict(),
            "metrics": {"by_condition": self.by_condition(), "by_distance": self.by_distance(),
                        "by_occlusion": self.by_occlusion(), "by_truncation": self.by_truncation(),
                        "lens_dirt": self.lens_dirt_split()},
            "triggering_conditions": self.triggering_conditions(req),
            "release": self.release(req),
        }

    def save(self, path, requirement=None, objects_path=None) -> dict:
        """Write the JSON result (and, optionally, the per-object outcomes as CSV, .gz allowed)."""
        d = self.to_dict(requirement)
        Path(path).write_text(json.dumps(d, indent=1, default=_json_default) + "\n")
        if objects_path:
            self.objects.to_csv(objects_path, index=False, float_format="%.4f")
        return d

    @classmethod
    def load(cls, objects_path, result_path=None) -> "Report":
        """Rebuild a report from saved per-object outcomes (and the JSON for submission/run metadata)."""
        import pandas as pd
        objects = pd.read_csv(objects_path)
        for col in ("in_population", "under_dirt"):
            objects[col] = objects[col].map({True: True, False: False, "True": True, "False": False})
        meta = json.loads(Path(result_path).read_text()) if result_path else {}
        return cls(objects=objects, spec=SPEC_V1, submission=meta.get("submission", {}), run=meta.get("run", {}))

    def to_markdown(self, requirement=None) -> str:
        return render_markdown(self.to_dict(requirement))

    def to_html(self, requirement=None) -> str:
        return render_html(self.to_dict(requirement))


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


# =========================================================================== rendering
def _pct(x):
    return "–" if x is None else f"{100 * x:.1f} %"


def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _report_sections(d: dict):
    """(title, headers, rows) sections of a result dict, shared by Markdown and HTML."""
    labels = {c["id"]: c["label"] for c in SPEC_V1["conditions"]}
    req = d["requirement"]
    secs = []
    secs.append(("Triggering-condition table",
                 ["Condition", "In ODD", "n", "Recall", f"Lower bound ({req['confidence']:.1%})", "Verdict",
                  "Supported speed", "FP/frame", "Measure"],
                 [[r["label"], "yes" if r["in_odd"] else "no", r["n"], _pct(r["recall"]), _pct(r["lower_bound"]),
                   r["verdict"], f"{r['v_max_kmh']:g} km/h" if r["v_max_kmh"] else "none", f"{r['fp_per_frame']:.2f}",
                   r["measure"]] for r in d["triggering_conditions"]]))
    bc = d["metrics"]["by_condition"]
    secs.append(("Recall and false positives by condition (evaluated population, 95 % CI)",
                 ["Condition", "Class", "n", "Recall", "95 % CI", "FP/frame"],
                 [[labels.get(r["condition"], r["condition"]), r["class"], r["n"], _pct(r["recall"]),
                   f"{_pct(r['ci_low'])} – {_pct(r['ci_high'])}", f"{r['fp_per_frame']:.2f}"] for r in bc]))
    bd = [r for r in d["metrics"]["by_distance"] if r["class"] == "pedestrian"]
    secs.append(("Pedestrian recall by distance band",
                 ["Condition", "Band", "n", "Recall", "95 % CI"],
                 [[labels.get(r["condition"], r["condition"]), r["band"], r["n"], _pct(r["recall"]),
                   f"{_pct(r['ci_low'])} – {_pct(r['ci_high'])}"] for r in bd]))
    secs.append(("Recall by KITTI occlusion level (clear)", ["Class", "Occlusion", "n", "Recall", "95 % CI"],
                 [[r["class"], r["occlusion"], r["n"], _pct(r["recall"]), f"{_pct(r['ci_low'])} – {_pct(r['ci_high'])}"]
                  for r in d["metrics"]["by_occlusion"]]))
    secs.append(("Recall by truncation (clear)", ["Class", "Truncation", "n", "Recall", "95 % CI"],
                 [[r["class"], r["truncation"], r["n"], _pct(r["recall"]), f"{_pct(r['ci_low'])} – {_pct(r['ci_high'])}"]
                  for r in d["metrics"]["by_truncation"]]))
    secs.append(("Lens dirt: inside versus outside the dirty area", ["Class", "Where", "n", "Recall", "95 % CI"],
                 [[r["class"], r["where"], r["n"], _pct(r["recall"]), f"{_pct(r['ci_low'])} – {_pct(r['ci_high'])}"]
                  for r in d["metrics"]["lens_dirt"]]))
    return secs


def _header_lines(d: dict):
    s, r, rel, req = d["submission"], d["run"], d["release"], d["requirement"]
    return [
        ("Model", f"{s.get('name', '?')} ({s.get('model', '?')})"),
        ("Weights / training data", f"{s.get('weights', '?')}; {s.get('training_data', '?')}"),
        ("Score threshold", s.get("score_threshold")),
        ("Benchmark", f"{d['benchmark']['name']}, spec v{d['benchmark']['spec_version']} "
                      f"(sha256 {d['benchmark']['spec_sha256'][:12]}), {r.get('n_frames')} frames, "
                      f"{'official run' if r.get('official') else 'partial run (not comparable)'}"),
        ("Requirement", f"{req['id']}: {req['source']}"),
        ("Release verdict", f"**{rel['verdict']}**"),
    ]


def render_markdown(d: dict) -> str:
    """A Markdown report from a result dict."""
    lines = [f"# SOTIF perception report — {d['submission'].get('name', 'detector')}", ""]
    lines += [f"- **{k}:** {v}" for k, v in _header_lines(d)]
    lines += ["", "## Release verdict", "", f"**{d['release']['verdict']}** — {d['release']['rule']}.", ""]
    lines += [f"- {x}" for x in d["release"]["reasons"]]
    if d["release"]["outside_odd_not_met"]:
        lines += [f"- Outside the declared ODD and not met (ODD monitor needed): "
                  + ", ".join(d["release"]["outside_odd_not_met"])]
    for title, headers, rows in _report_sections(d):
        lines += ["", f"## {title}", "", _table(headers, rows)]
    lines += ["", "Synthetic conditions on real KITTI images (Koschmieder fog from LiDAR depth, Poisson-Gaussian "
              "low-light noise, lens dirt); KITTI itself contains daytime, dry weather only. Recall is per frame; "
              "frames are not independent encounters.", ""]
    return "\n".join(lines)


def render_html(d: dict) -> str:
    """A self-contained HTML report from a result dict."""
    import html as H
    css = ("body{font-family:system-ui,sans-serif;max-width:1100px;margin:2em auto;padding:0 16px;color:#111;background:#fff}"
           "table{border-collapse:collapse;margin:1em 0;font-size:14px}td,th{border:1px solid #bbb;padding:4px 8px;text-align:left}"
           "th{background:#eee}")
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><title>SOTIF report</title><style>{css}</style></head><body>",
             f"<h1>SOTIF perception report — {H.escape(str(d['submission'].get('name', 'detector')))}</h1><ul>"]
    parts += [f"<li><b>{H.escape(k)}:</b> {H.escape(str(v)).replace('**', '')}</li>" for k, v in _header_lines(d)]
    parts.append("</ul><h2>Release verdict</h2><p><b>" + H.escape(d["release"]["verdict"]) + "</b></p><ul>")
    parts += [f"<li>{H.escape(x)}</li>" for x in d["release"]["reasons"]]
    parts.append("</ul>")
    for title, headers, rows in _report_sections(d):
        parts.append(f"<h2>{H.escape(title)}</h2><table><tr>" + "".join(f"<th>{H.escape(h)}</th>" for h in headers) + "</tr>")
        parts += ["<tr>" + "".join(f"<td>{H.escape(str(c))}</td>" for c in r) + "</tr>" for r in rows]
        parts.append("</table>")
    parts.append("</body></html>")
    return "\n".join(parts)


# =========================================================================== schema validation
def validate(instance, schema: dict, path: str = "$") -> list[str]:
    """Minimal JSON-Schema validator for the subset used by ``benchmark/schema.json``.

    Supports type, enum, const, required, properties, additionalProperties (bool),
    items, minItems, minimum, maximum, minLength, pattern and anyOf. Returns a list of
    error messages (empty if valid).
    """
    import re
    errs = []
    types = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    if "anyOf" in schema:
        if all(validate(instance, s, path) for s in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
        return errs
    t = schema.get("type")
    if t is not None:
        ok = False
        for tt in ([t] if isinstance(t, str) else t):
            if tt == "number":
                ok |= isinstance(instance, (int, float)) and not isinstance(instance, bool)
            elif tt == "integer":
                ok |= isinstance(instance, int) and not isinstance(instance, bool)
            else:
                ok |= isinstance(instance, types[tt])
        if not ok:
            return [f"{path}: expected {t}, got {type(instance).__name__}"]
    if "enum" in schema and instance not in schema["enum"]:
        errs.append(f"{path}: {instance!r} not in {schema['enum']}")
    if "const" in schema and instance != schema["const"]:
        errs.append(f"{path}: must be {schema['const']!r}")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errs.append(f"{path}: {instance} < {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errs.append(f"{path}: {instance} > {schema['maximum']}")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errs.append(f"{path}: string too short")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errs.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(instance, dict):
        for k in schema.get("required", []):
            if k not in instance:
                errs.append(f"{path}: missing '{k}'")
        props = schema.get("properties", {})
        for k, v in instance.items():
            if k in props:
                errs += validate(v, props[k], f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: unexpected property '{k}'")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errs.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, v in enumerate(instance):
                errs += validate(v, schema["items"], f"{path}[{i}]")
    return errs


def validate_result(result: dict, schema_path=None) -> list[str]:
    """Validate a result dict against ``benchmark/schema.json`` and the benchmark's own consistency rules."""
    schema_path = Path(schema_path) if schema_path else Path(__file__).resolve().parents[1] / "benchmark" / "schema.json"
    errs = validate(result, json.loads(schema_path.read_text()))
    if not errs and result["benchmark"]["spec_version"] == SPEC_V1["spec_version"] \
            and result["benchmark"]["spec_sha256"] != spec_hash(SPEC_V1):
        errs.append("$.benchmark.spec_sha256: does not match the v1 spec")
    return errs


# =========================================================================== LiDAR track
CARLA_WEATHER = tuple(f"{w}{t}" for t in ("Noon", "Sunset", "Night") for w in
                      ("Clear", "Cloudy", "Wet", "WetCloudy", "MidRainy", "HardRain", "SoftRain"))


def kitti_format_frames(root, conditions_csv=None):
    """Find KITTI-format frames (velodyne/*.bin with label_2/*.txt and calib/*.txt) below ``root``.

    The condition of a frame is taken from (1) ``conditions_csv`` (columns ``frame,condition``,
    frame as the 6-digit id or relative path) if given, else (2) the nearest parent folder whose
    name contains a CARLA weather preset (e.g. 'HardRainNight'), else 'all'.
    Yields dicts with ``id``, ``condition``, ``velodyne``, ``label``, ``calib`` paths.

    Written for the documented SOTIF-PCOD layout (KITTI format from CARLA, 21 weather presets,
    547 frames); not yet run on the released archive.
    """
    root = Path(root)
    mapping = {}
    if conditions_csv:
        import csv
        with open(conditions_csv, newline="") as fh:
            mapping = {r["frame"]: r["condition"] for r in csv.DictReader(fh)}
    for vel_dir in sorted(p for p in root.rglob("velodyne") if p.is_dir()):
        base = vel_dir.parent
        if not (base / "label_2").is_dir() or not (base / "calib").is_dir():
            continue
        folder_cond = next((w for part in reversed(base.relative_to(root).parts)
                            for w in sorted(CARLA_WEATHER, key=len, reverse=True) if w.lower() in part.lower()), None)
        for bin_path in sorted(vel_dir.glob("*.bin")):
            fid = bin_path.stem
            label, calib = base / "label_2" / f"{fid}.txt", base / "calib" / f"{fid}.txt"
            if not label.exists() or not calib.exists():
                continue
            rel = str(bin_path.relative_to(root))
            cond = mapping.get(fid) or mapping.get(rel) or folder_cond or "all"
            yield {"id": fid, "condition": cond, "velodyne": bin_path, "label": label, "calib": calib}


def label_centre_lidar(label: dict, calib: dict) -> np.ndarray:
    """Geometric centre (x, y, z) of a KITTI 3D label in the LiDAR frame (m)."""
    centre_rect = np.array([label["x"], label["y"] - label["h"] / 2, label["z"], 1.0])
    velo = np.linalg.inv(calib["R0"] @ calib["Tr_velo_to_cam"]) @ centre_rect
    return velo[:3]


def match_centres(gt_xy, det_xy, det_scores, max_dist_m: float = 2.0):
    """Greedy one-to-one BEV centre-distance matching (nuScenes-style rule).

    Returns the matched score per label (0 if missed) and the number of unmatched detections.
    """
    gt_xy, det_xy = np.asarray(gt_xy, float).reshape(-1, 2), np.asarray(det_xy, float).reshape(-1, 2)
    scores = np.zeros(len(gt_xy))
    free = np.ones(len(gt_xy), bool)
    fp = 0
    for j in np.argsort(-np.asarray(det_scores, float), kind="stable"):
        d = np.linalg.norm(gt_xy - det_xy[j], axis=1) if len(gt_xy) else np.array([])
        cand = np.flatnonzero(free & (d <= max_dist_m))
        if len(cand):
            g = cand[np.argmin(d[cand])]
            free[g] = False
            scores[g] = det_scores[j]
        else:
            fp += 1
    return scores, fp


def evaluate_lidar(detector, root=None, conditions_csv=None, threshold: float = 0.5, max_dist_m: float = 2.0,
                   max_range_m: float = 50.0, max_azimuth_deg: float | None = None, confidence: float = 0.95,
                   limit=None) -> dict:
    """Evaluate a LiDAR detector on a KITTI-format directory, per condition.

    ``detector(points) -> iterable of ((x, y, z, l, w, h, yaw), score, label)`` with ``points``
    N x 4 float32 (x forward, y left, z up, intensity) and box centres in the LiDAR frame.
    ``root`` defaults to ``$SOTIF_PCOD_DIR``. Labels of type Car/Van -> car, Pedestrian ->
    pedestrian, Cyclist -> cyclist; labels beyond ``max_range_m`` (BEV) are not evaluated and
    detections there are not counted. ``max_azimuth_deg`` restricts labels and detections to
    |atan2(y, x)| <= that angle (use about 40 deg for KITTI, whose labels cover only the camera's
    field of view; SOTIF-PCOD labels cover the full LiDAR range). Returns per-condition, per-class recall with CIs and
    false positives per frame.
    """
    from . import data as D

    root = root or os.environ.get("SOTIF_PCOD_DIR")
    if not root:
        raise FileNotFoundError("set SOTIF_PCOD_DIR to the extracted SOTIF-PCOD (or another KITTI-format) folder")
    cls_map = {"Car": "car", "Van": "car", "Pedestrian": "pedestrian", "Cyclist": "cyclist"}
    stats, n_frames = {}, {}
    for i, fr in enumerate(kitti_format_frames(root, conditions_csv)):
        if limit is not None and i >= limit:
            break
        points = np.fromfile(fr["velodyne"], dtype=np.float32).reshape(-1, 4)
        labels = D.parse_object_labels(Path(fr["label"]).read_text())
        calib = D.parse_calib(Path(fr["calib"]).read_text())
        dets = [(np.asarray(b, float), float(s), str(l)) for b, s, l in detector(points)]
        cond = fr["condition"]
        n_frames[cond] = n_frames.get(cond, 0) + 1
        for cls in CLASSES:
            gts = [label_centre_lidar(l, calib)[:2] for l in labels if cls_map.get(l["type"]) == cls]
            def keep(xy):
                return np.hypot(*xy) <= max_range_m and (max_azimuth_deg is None or
                                                         abs(np.degrees(np.arctan2(xy[1], xy[0]))) <= max_azimuth_deg)
            gts = [g for g in gts if keep(g)]
            d = [(b[:2], s) for b, s, l in dets if l == cls and s >= threshold and keep(b[:2])]
            sc, fp = match_centres(gts, [x for x, _ in d], [s for _, s in d], max_dist_m)
            st = stats.setdefault((cond, cls), {"n": 0, "detected": 0, "fp": 0})
            st["n"] += len(gts)
            st["detected"] += int((sc > 0).sum())
            st["fp"] += fp
    rows = []
    for (cond, cls), st in sorted(stats.items()):
        lo, hi = binomial_interval(st["detected"], st["n"], confidence)
        rows.append({"condition": cond, "class": cls, "n": st["n"], "detected": st["detected"],
                     "recall": round(st["detected"] / st["n"], 4) if st["n"] else None,
                     "ci_low": round(lo, 4), "ci_high": round(hi, 4),
                     "fp_per_frame": round(st["fp"] / n_frames[cond], 4)})
    return {"root": str(root), "frames_per_condition": n_frames, "threshold": threshold,
            "matching": f"BEV centre distance <= {max_dist_m} m, greedy by score", "results": rows}


def lidar_cluster_baseline(points: np.ndarray, cell_m: float = 0.25, min_points: int = 15):
    """A transparent non-learned LiDAR baseline: ground removal, BEV clustering, size rules.

    Points within 0.3 m of a ground height (10th percentile of z per 4 m tile) are removed,
    as is everything more than 2.5 m above it; the rest is rasterised on a ``cell_m`` grid
    and connected cells are clusters. Clusters with an axis-aligned footprint of 2.5-6 m by
    1.2-2.8 m are 'car', footprints <= 1.2 m with a height of 1.0-2.1 m are 'pedestrian'.
    Score = min(1, points / 100). It shows the floor of what geometry alone achieves; it is
    not a competitive detector (no orientation, merges adjacent objects).
    """
    from scipy import ndimage

    p = points[(np.abs(points[:, 1]) < 40) & (points[:, 0] > -10) & (points[:, 0] < 70)]
    if len(p) == 0:
        return []
    tile = np.floor(p[:, :2] / 4.0).astype(int)
    key = tile[:, 0] * 1000 + tile[:, 1]
    order = np.argsort(key)
    ground = np.empty(len(p))
    uniq, start = np.unique(key[order], return_index=True)
    for s, e in zip(start, list(start[1:]) + [len(order)]):
        idx = order[s:e]
        ground[idx] = np.percentile(p[idx, 2], 10)
    rel = p[:, 2] - ground
    obj = p[(rel > 0.3) & (rel < 2.5)]
    if len(obj) == 0:
        return []
    ij = np.floor((obj[:, :2] - [-10, -40]) / cell_m).astype(int)
    grid = np.zeros((int(80 / cell_m) + 1, int(80 / cell_m) + 1), bool)
    grid[ij[:, 0], ij[:, 1]] = True
    lab, n = ndimage.label(ndimage.binary_closing(grid, iterations=1))
    out = []
    pid = lab[ij[:, 0], ij[:, 1]]
    for k in range(1, n + 1):
        q = obj[pid == k]
        if len(q) < min_points:
            continue
        lo, hi = q[:, :3].min(axis=0), q[:, :3].max(axis=0)
        ext = hi - lo
        length, width = max(ext[0], ext[1]), min(ext[0], ext[1])
        centre = (lo + hi) / 2
        if 2.5 <= length <= 6.0 and 1.2 <= width <= 2.8:
            out.append(((*centre, length, width, ext[2], 0.0), min(1.0, len(q) / 100), "car"))
        elif length <= 1.2 and 1.0 <= ext[2] <= 2.1:
            out.append(((*centre, length, width, ext[2], 0.0), min(1.0, len(q) / 100), "pedestrian"))
    return out


# =========================================================================== CLI
def _progress_printer(start):
    def show(done, total):
        el = time.time() - start
        sys.stderr.write(f"\r{done}/{total} frames, {el:.0f} s elapsed, ~{el / done * (total - done):.0f} s left")
        sys.stderr.flush()
        if done == total:
            sys.stderr.write("\n")
    return show


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m avsafety.bench", description=__doc__.split("\n\n")[0])
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--model", help="torchvision:<model name>, e.g. torchvision:fasterrcnn_mobilenet_v3_large_fpn")
    src.add_argument("--callable", help="module:function implementing the detector API")
    src.add_argument("--rescore", metavar="OBJECTS_CSV", help="recompute a report from saved per-object outcomes")
    src.add_argument("--validate", nargs="+", metavar="RESULT_JSON", help="validate result files against the schema")
    src.add_argument("--write-spec", metavar="PATH", help="write the built-in v1 spec as JSON")
    ap.add_argument("--out", help="result JSON path")
    ap.add_argument("--objects", help="per-object outcomes CSV path (default: <out>.objects.csv.gz)")
    ap.add_argument("--markdown", help="also write a Markdown report")
    ap.add_argument("--html", help="also write an HTML report")
    ap.add_argument("--name", help="display name of the submission")
    ap.add_argument("--threshold", type=float, help="declared operating score threshold (default 0.5)")
    ap.add_argument("--requirement", default="PR-01", help="preset (PR-01, TC-04-02) or a JSON file")
    ap.add_argument("--frames", type=int, help="evaluate only the first N frames (smoke test, not official)")
    ap.add_argument("--threads", type=int, default=2, help="CPU threads for torch (default 2)")
    ap.add_argument("--weights", help="weights description for --callable submissions")
    ap.add_argument("--training-data", help="training data of the submitted model (must exclude the benchmark frames)")
    ap.add_argument("--schema", help="path to schema.json (default: benchmark/schema.json in the repository)")
    a = ap.parse_args(argv)

    if a.write_spec:
        Path(a.write_spec).write_text(json.dumps(SPEC_V1, indent=1) + "\n")
        print(f"wrote {a.write_spec} (sha256 {spec_hash(SPEC_V1)})")
        return 0
    if a.validate:
        bad = 0
        for p in a.validate:
            errs = validate_result(json.loads(Path(p).read_text()), a.schema)
            print(f"{p}: {'valid' if not errs else 'INVALID'}")
            for e in errs:
                print("  ", e)
            bad += bool(errs)
        return 1 if bad else 0
    req = get_requirement(a.requirement)
    if a.rescore:
        guess = Path(str(a.rescore).replace(".objects.csv.gz", ".json").replace(".objects.csv", ".json"))
        rep = Report.load(a.rescore, guess if guess.exists() and guess != Path(a.rescore) else None)
        if a.threshold is not None:
            rep.submission["score_threshold"] = a.threshold
    else:
        a.threshold = 0.5 if a.threshold is None else a.threshold
        if not (a.model or a.callable) or not a.out:
            ap.error("give --model or --callable, and --out")
        if a.model:
            kind, _, name = a.model.partition(":")
            if kind != "torchvision" or not name:
                ap.error("--model must look like torchvision:<name>")
            det = torchvision_detector(name, threads=a.threads)
        else:
            try:
                import torch
                torch.set_num_threads(a.threads)
            except ImportError:
                pass
            det = load_callable(a.callable)
        meta = dict(getattr(det, "meta", {}))
        meta.setdefault("model", a.model or f"callable:{a.callable}")
        if a.weights:
            meta["weights"] = a.weights
        if a.training_data:
            meta["training_data"] = a.training_data
        meta.update({"name": a.name or meta["model"].split(":")[-1], "score_threshold": a.threshold,
                     "date": date.today().isoformat(), "avsafety_version": _version()})
        frames = SPEC_V1["frames"][: a.frames] if a.frames else None
        rep = evaluate(det, frames=frames, threshold=a.threshold, submission=meta,
                       progress=_progress_printer(time.time()))
    d = rep.to_dict(req)
    if a.out:
        objects = a.objects or (None if a.rescore else str(Path(a.out).with_suffix("")) + ".objects.csv.gz")
        rep.save(a.out, req, objects)
        print(f"wrote {a.out}" + (f" and {objects}" if objects else ""))
    if a.markdown:
        Path(a.markdown).write_text(render_markdown(d))
    if a.html:
        Path(a.html).write_text(render_html(d))
    rel = d["release"]
    print(f"{d['submission'].get('name')}: {rel['verdict']} against {rel['requirement']}")
    for r in d["triggering_conditions"]:
        print(f"  {r['label']:<24} recall {_pct(r['recall']):>8} (n={r['n']:>3}) {r['verdict']:<14} "
              f"supported up to {str(r['v_max_kmh']) + ' km/h' if r['v_max_kmh'] else 'none'}")
    return 0


def _version() -> str:
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "unknown"


if __name__ == "__main__":
    sys.exit(main())
