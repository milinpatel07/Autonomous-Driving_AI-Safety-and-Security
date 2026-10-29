"""Offline tests for avsafety.bench: matching, statistics, verdicts, report and schema."""
import json
from pathlib import Path

import numpy as np
import pytest

pd = pytest.importorskip("pandas")
from avsafety import bench as B  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------ statistics
def test_clopper_pearson_known_values():
    lo, hi = B.binomial_interval(0, 10)
    assert lo == 0 and hi == pytest.approx(1 - 0.025 ** (1 / 10), abs=1e-9)
    lo, hi = B.binomial_interval(10, 10, sides=1)
    assert lo == pytest.approx(0.05 ** (1 / 10), abs=1e-9) and hi == 1
    lo, hi = B.binomial_interval(50, 100)
    assert lo == pytest.approx(0.3983, abs=1e-3) and hi == pytest.approx(0.6017, abs=1e-3)


def test_wilson_inside_unit_interval_and_narrower_than_exact():
    for k, n in [(0, 5), (3, 20), (19, 20), (60, 100)]:
        wl, wh = B.binomial_interval(k, n, method="wilson")
        cl, ch = B.binomial_interval(k, n)
        assert 0 <= wl <= k / n <= wh <= 1
        assert wh - wl <= ch - cl + 1e-12
    assert B.binomial_interval(0, 0) == (0.0, 1.0)
    with pytest.raises(ValueError):
        B.binomial_interval(5, 3)


def test_verdict_logic():
    assert B.verdict(100, 100, 0.9) == "meets"                 # lower bound 0.970
    assert B.verdict(50, 100, 0.9) == "does not meet"
    assert B.verdict(18, 20, 0.9) == "inconclusive"
    assert B.verdict(0, 0, 0.9) == "no data"
    # zero-failure rule of three: n >= 29 needed for 0.90 at 95 %
    assert B.verdict(28, 28, 0.9) == "inconclusive" and B.verdict(29, 29, 0.9) == "meets"


# ------------------------------------------------------------------ matching
def test_iou_and_ioa():
    a = np.array([[0, 0, 10, 10]])
    b = np.array([[5, 0, 15, 10], [0, 0, 10, 10], [20, 20, 30, 30]])
    np.testing.assert_allclose(B.box_iou(a, b)[0], [50 / 150, 1.0, 0.0])
    np.testing.assert_allclose(B.box_ioa(a, np.array([[0, 0, 5, 10]]))[0], [0.5])


def test_match_class_greedy_by_score_and_statuses():
    gt = [[0, 0, 10, 20], [100, 0, 110, 20], [200, 0, 205, 10]]
    pop = [True, True, False]                                   # third label outside the population
    det = [[0, 0, 10, 20], [1, 0, 11, 20], [200, 0, 205, 10], [300, 0, 310, 20], [400, 0, 410, 20], [500, 0, 510, 20]]
    scores = [0.6, 0.9, 0.8, 0.7, 0.4, 0.3]
    ignore = np.array([[400, 0, 410, 20]])
    dontcare = np.array([[495, 0, 520, 30]])
    gs, st = B.match_class(gt, pop, det, scores, ignore, dontcare)
    assert gs.tolist() == [0.9, 0.0, 0.8]                       # higher-scoring detection wins the label
    assert st.tolist() == ["fp", "tp", "ignored", "fp", "ignored", "ignored"]


def test_match_threshold_prefix_property():
    rng = np.random.default_rng(0)
    gt = rng.uniform(0, 400, (8, 2)); gt = np.hstack([gt, gt + 30])
    det = gt[rng.permutation(8)[:6]] + rng.normal(0, 4, (6, 4))
    sc = rng.uniform(0.05, 1, 6)
    full, _ = B.match_class(gt, [True] * 8, det, sc)
    for tau in (0.2, 0.5, 0.8):
        keep = sc >= tau
        part, _ = B.match_class(gt, [True] * 8, det[keep], sc[keep])
        np.testing.assert_array_equal(part > 0, full >= tau)


def test_coco_mapping_and_cyclist_fusion():
    boxes = [[10, 0, 30, 50], [8, 30, 40, 70], [100, 0, 120, 50], [200, 0, 260, 40], [300, 0, 380, 50], [0, 0, 5, 5]]
    scores = [0.9, 0.64, 0.8, 0.7, 0.6, 0.02]
    labels = [1, 2, 1, 3, 8, 1]                                 # person on bicycle, person, car, truck, weak person
    out = B.coco_to_bench(boxes, scores, labels)
    by = {}
    for b, s, l in out:
        by.setdefault(l, []).append((b, s))
    assert len(by["cyclist"]) == 1 and by["cyclist"][0][1] == pytest.approx(np.sqrt(0.9 * 0.64))
    assert by["cyclist"][0][0] == (8, 0, 40, 70)
    assert [s for _, s in by["pedestrian"]] == [0.8]           # rider consumed, weak person dropped
    assert len(by["car"]) == 2


# ------------------------------------------------------------------ report on synthetic outcomes
def _synthetic_report(recall_near=1.0, recall_far=0.5, n=200, threshold=0.5, seed=1, near_m=30.0):
    rng = np.random.default_rng(seed)
    rows = []
    for cond, drop in [("clear", 0.0), ("fog_25", 0.4)]:
        for i in range(n):
            dist = 3 + 50 * i / n
            p = (recall_near if dist <= near_m else recall_far) - drop
            score = 0.9 if rng.random() < p else 0.0
            rows.append(("gt", i % 20, cond, "pedestrian", score, dist, rng.uniform(-3, 3), 0, 0.0, 60.0, True, None))
        rows += [("fp", f, cond, "pedestrian", 0.7, None, None, None, None, None, None, None) for f in range(10)]
    obj = pd.DataFrame(rows, columns=B.OBJECT_COLUMNS)
    return B.Report(objects=obj, submission={"name": "synthetic", "model": "test", "weights": "none",
                                             "training_data": "none", "score_threshold": threshold, "date": "2026-10-29"},
                    run={"n_frames": 20, "conditions": ["clear", "fog_25"], "official": False, "runtime_s": 0.0})


def test_release_with_perfect_detector_is_release():
    rep = _synthetic_report(1.0, 1.0)
    req = B.Requirement(odd_conditions=("clear",))
    assert rep.release(req)["verdict"] == "RELEASE"
    tct = {r["condition"]: r for r in rep.triggering_conditions(req)}
    assert tct["clear"]["v_max_kmh"] == 60 and tct["fog_25"]["verdict"] == "does not meet"


def test_declared_odd_condition_without_evidence_prevents_release():
    rep = _synthetic_report(1.0, 1.0)                     # evaluates clear and fog_25 only
    req = B.Requirement(odd_conditions=("clear", "low_light_64"))
    rel = rep.release(req)
    assert rel["verdict"] != "RELEASE"
    assert rel["not_evaluated"] == ["low_light_64"] and rel["restricted_odd_kmh"]["low_light_64"] is None
    assert any("not evaluated" in r for r in rel["reasons"])


def test_release_restricted_when_only_near_range_is_good():
    rep = _synthetic_report(1.0, 0.0, near_m=20.0)
    req = B.Requirement(odd_conditions=("clear",), lateral_m=None)
    rel = rep.release(req)
    vmax = rep.triggering_conditions(req)[0]["v_max_kmh"]
    assert rel["verdict"] == "RELEASE WITH ODD RESTRICTION"
    assert vmax in (40, 45) and req.range_m(vmax + 5) > 21      # restriction follows the good range


def test_do_not_release_when_clear_air_fails():
    rep = _synthetic_report(0.5, 0.5)
    assert rep.release(B.Requirement(odd_conditions=("clear",), lateral_m=None))["verdict"] == "DO NOT RELEASE"


def test_requirement_is_a_parameter_and_threshold_matters():
    rep = _synthetic_report(0.8, 0.8)
    strict, lax = B.REQUIREMENTS["PR-01"], B.Requirement(min_recall=0.5, lateral_m=None, odd_conditions=("clear",))
    assert rep.release(strict)["verdict"] == "DO NOT RELEASE"
    assert rep.release(lax)["verdict"] == "RELEASE"
    rep.submission["score_threshold"] = 0.95                   # above every score: nothing detected
    assert rep.by_condition()[0]["recall"] == 0


def test_fp_per_frame_and_tables():
    rep = _synthetic_report()
    bc = {(r["condition"], r["class"]): r for r in rep.by_condition()}
    assert bc[("clear", "pedestrian")]["fp_per_frame"] == pytest.approx(0.5)
    lo, hi = bc[("clear", "pedestrian")]["fp_per_frame_ci"]
    assert lo < 0.5 < hi
    bands = [r for r in rep.by_distance() if r["condition"] == "clear" and r["class"] == "pedestrian"]
    assert sum(r["n"] for r in bands) == 200


def test_report_serialises_and_validates(tmp_path):
    rep = _synthetic_report()
    d = rep.save(tmp_path / "r.json", objects_path=tmp_path / "r.objects.csv.gz")
    assert B.validate_result(json.loads((tmp_path / "r.json").read_text())) == []
    again = B.Report.load(tmp_path / "r.objects.csv.gz", tmp_path / "r.json")
    assert again.to_dict()["triggering_conditions"] == d["triggering_conditions"]
    assert "Release verdict" in rep.to_markdown() and rep.to_html().startswith("<!doctype html>")


def test_schema_rejects_invalid_results():
    rep = _synthetic_report()
    d = json.loads(json.dumps(rep.to_dict(), default=B._json_default))
    bad = json.loads(json.dumps(d)); bad["release"]["verdict"] = "SHIP IT"
    assert B.validate_result(bad)
    bad = json.loads(json.dumps(d)); del bad["submission"]["weights"]
    assert B.validate_result(bad)
    bad = json.loads(json.dumps(d)); bad["metrics"]["by_condition"][0]["recall"] = 1.5
    assert B.validate_result(bad)
    bad = json.loads(json.dumps(d)); bad["benchmark"]["spec_sha256"] = "0" * 64
    assert B.validate_result(bad)


def test_minimal_validator_agrees_with_jsonschema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "benchmark" / "schema.json").read_text())
    d = json.loads(json.dumps(_synthetic_report().to_dict(), default=B._json_default))
    jsonschema.validate(d, schema)
    d["submission"]["score_threshold"] = 2
    assert B.validate(d, schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(d, schema)


# ------------------------------------------------------------------ spec and committed files
def test_spec_file_matches_builtin_spec():
    on_disk = json.loads((ROOT / "benchmark" / "spec_v1.json").read_text())
    assert B.spec_hash(on_disk) == B.spec_hash(B.SPEC_V1)
    s = B.SPEC_V1
    assert len(s["frames"]) == s["frame_rule"]["n_frames"] == len(set(s["frames"])) and s["frames"] == sorted(s["frames"])


def test_committed_results_are_valid():
    for p in sorted((ROOT / "benchmark" / "results").glob("*.json")):
        assert B.validate_result(json.loads(p.read_text())) == [], p.name


# ------------------------------------------------------------------ LiDAR track
def test_lidar_track_on_synthetic_kitti_folder(tmp_path):
    base = tmp_path / "HardRainNight" / "training"
    for sub in ("velodyne", "label_2", "calib"):
        (base / sub).mkdir(parents=True)
    calib = ("P2: 700 0 600 0 0 700 180 0 0 0 1 0\nR0_rect: 1 0 0 0 1 0 0 0 1\n"
             "Tr_velo_to_cam: 0 -1 0 0 0 0 -1 0 1 0 0 0\n")
    # car 10 m ahead (camera z = 10), pedestrian 5 m ahead and 2 m to the left (camera x = -2)
    labels = ("Car 0 0 0 0 0 10 10 1.5 1.8 4.0 0 1.0 10 0\n"
              "Pedestrian 0 0 0 0 0 10 10 1.7 0.6 0.6 -2 1.0 5 0\n")
    (base / "calib" / "000000.txt").write_text(calib)
    (base / "label_2" / "000000.txt").write_text(labels)
    np.zeros((10, 4), np.float32).tofile(base / "velodyne" / "000000.bin")
    frames = list(B.kitti_format_frames(tmp_path))
    assert len(frames) == 1 and frames[0]["condition"] == "HardRainNight"

    def det(points):
        return [((10.2, 0.0, -0.7, 4, 1.8, 1.5, 0), 0.9, "car"), ((30.0, 5.0, 0, 4, 1.8, 1.5, 0), 0.8, "car")]

    res = B.evaluate_lidar(det, tmp_path)
    rows = {r["class"]: r for r in res["results"]}
    assert rows["car"]["recall"] == 1.0 and rows["car"]["fp_per_frame"] == 1.0
    assert rows["pedestrian"]["recall"] == 0.0


def test_label_centre_lidar_inverts_calibration():
    from avsafety import data as D
    calib = D.parse_calib("P2: 700 0 600 0 0 700 180 0 0 0 1 0\nR0_rect: 1 0 0 0 1 0 0 0 1\n"
                          "Tr_velo_to_cam: 0 -1 0 0 0 0 -1 0 1 0 0 0\n")
    lab = {"x": -2.0, "y": 1.0, "z": 5.0, "h": 1.7}
    np.testing.assert_allclose(B.label_centre_lidar(lab, calib), [5.0, 2.0, -0.15])


def test_lidar_baseline_finds_a_box_shaped_cluster():
    rng = np.random.default_rng(0)
    ground = np.column_stack([rng.uniform(0, 40, 4000), rng.uniform(-10, 10, 4000), np.full(4000, -1.7), np.ones(4000)])
    car = np.column_stack([rng.uniform(10, 14, 400), rng.uniform(-0.9, 0.9, 400), rng.uniform(-1.2, -0.2, 400), np.ones(400)])
    out = B.lidar_cluster_baseline(np.vstack([ground, car]).astype(np.float32))
    cars = [b for b, s, l in out if l == "car"]
    assert len(cars) == 1 and abs(cars[0][0] - 12) < 0.5
