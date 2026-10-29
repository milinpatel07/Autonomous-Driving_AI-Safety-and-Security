"""Offline tests for the dataset parsers (no network access needed)."""
import numpy as np
import pytest

from avsafety import data as D

CALIB_OBJECT = """P0: 7.215377e+02 0 6.095593e+02 0 0 7.215377e+02 1.728540e+02 0 0 0 1 0
P1: 7.215377e+02 0 6.095593e+02 -3.875744e+02 0 7.215377e+02 1.728540e+02 0 0 0 1 0
P2: 7.215377e+02 0 6.095593e+02 4.485728e+01 0 7.215377e+02 1.728540e+02 2.163791e-01 0 0 1 2.745884e-03
P3: 7.215377e+02 0 6.095593e+02 -3.395242e+02 0 7.215377e+02 1.728540e+02 2.199936e+00 0 0 1 2.729905e-03
R0_rect: 9.999239e-01 9.837760e-03 -7.445048e-03 -9.869795e-03 9.999421e-01 -4.278459e-03 7.402527e-03 4.351614e-03 9.999631e-01
Tr_velo_to_cam: 7.533745e-03 -9.999714e-01 -6.166020e-04 -4.069766e-03 1.480249e-02 7.280733e-04 -9.998902e-01 -7.631618e-02 9.998621e-01 7.523790e-03 1.480755e-02 -2.717806e-01
Tr_imu_to_velo: 9.999976e-01 7.553071e-04 -2.035826e-03 -8.086759e-01 -7.854027e-04 9.998898e-01 -1.482298e-02 3.195559e-01 2.024406e-03 1.482454e-02 9.998881e-01 -7.997231e-01
"""
CALIB_TRACKING = CALIB_OBJECT.replace("R0_rect:", "R_rect").replace("Tr_velo_to_cam:", "Tr_velo_cam")
LABELS = """Car 0.00 0 -1.56 564.62 174.59 616.43 224.74 1.61 1.66 3.20 -0.69 1.69 25.01 -1.59
Pedestrian 0.00 1 0.21 423.17 173.67 433.17 224.03 1.60 0.38 0.30 -5.36 1.77 23.39 -0.01
DontCare -1 -1 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10
"""


@pytest.mark.parametrize("text", [CALIB_OBJECT, CALIB_TRACKING])
def test_parse_calib_both_formats(text):
    c = D.parse_calib(text)
    assert c["P2"].shape == (3, 4) and c["R0"].shape == (4, 4) and c["Tr_velo_to_cam"].shape == (4, 4)
    assert c["R0"][3, 3] == 1 and np.allclose(c["Tr_velo_to_cam"][3], [0, 0, 0, 1])


def test_parse_labels_and_difficulty():
    labs = D.parse_object_labels(LABELS)
    assert [l["type"] for l in labs] == ["Car", "Pedestrian", "DontCare"]
    assert labs[0]["occluded"] == 0 and labs[0]["z"] == pytest.approx(25.01)
    assert D.kitti_difficulty(labs[0]) == "Easy"          # 50 px tall, visible, not truncated
    assert D.kitti_difficulty(labs[1]) == "Moderate"      # partly occluded
    assert D.kitti_difficulty({"y1": 0, "y2": 20, "occluded": 0, "truncated": 0}) == "Ignored"


def test_3d_box_projects_onto_2d_box():
    """The projected 3D box of a fully visible object matches its annotated 2D box."""
    frame = D.KittiFrame(index="000000", calib=D.parse_calib(CALIB_OBJECT))
    car = D.parse_object_labels(LABELS)[0]
    uv = frame.rect_to_image(D.box3d_corners(car).T)
    assert uv[:, 0].min() == pytest.approx(car["x1"], abs=6)
    assert uv[:, 0].max() == pytest.approx(car["x2"], abs=6)
    assert uv[:, 1].min() == pytest.approx(car["y1"], abs=6)
    assert uv[:, 1].max() == pytest.approx(car["y2"], abs=6)


def test_velo_to_image_roundtrip_shapes():
    frame = D.KittiFrame(index="0", calib=D.parse_calib(CALIB_OBJECT), image=np.zeros((375, 1242, 3), np.uint8),
                         points=np.array([[10.0, 0.0, -1.0, 0.5], [-10.0, 0.0, 0.0, 0.1]], dtype=np.float32))
    uv, depth, pts = frame.lidar_in_image()
    assert len(uv) == 1 and depth[0] == pytest.approx(9.73, abs=0.02)  # camera is 0.27 m ahead of the LiDAR; the rear point is dropped


def test_attribution_and_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("AVSAFETY_CACHE", str(tmp_path))
    assert D.cache_dir() == tmp_path
    assert "CC BY-NC-SA 3.0" in D.attribution("KITTI")


OXTS_LINE = ("49.009348313921 8.4371337908929 114.45652008057 0.069565 0.018834 -1.4512818 -0.0078693 "
             "0.082893912 0.082894 -0.075015 0.001163 -0.30049 0.25089 9.8202 -0.31117 0.26014 9.8128 "
             "-0.0042093 0.016327 -0.0089452 -0.0045094 0.016301 -0.0087844 0.66468314459811 0.0 4 7 4 4 0 ")


def test_parse_oxts_trailing_space_does_not_shift_columns():
    df = D.parse_oxts(OXTS_LINE + "\n" + OXTS_LINE + "\n")
    assert list(df.columns) == D.OXTS_COLUMNS and len(df) == 2
    assert df["lat"].iloc[0] == pytest.approx(49.009348313921)
    assert df["lon"].iloc[0] == pytest.approx(8.4371337908929)
    assert df["vf"].iloc[0] == pytest.approx(0.082894)       # forward velocity, not the next column
    assert df["orimode"].iloc[0] == 0


def test_fetch_url_retries_transient_errors_then_succeeds(tmp_path, monkeypatch):
    import io
    import urllib.error
    from avsafety import data as D
    monkeypatch.setenv("AVSAFETY_CACHE", str(tmp_path))
    calls = {"n": 0}

    def flaky(url, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise urllib.error.URLError("temporary failure")
        return io.BytesIO(b'[{"ok": 1}]')

    monkeypatch.setattr(D.urllib.request, "urlopen", flaky)
    path = D._fetch_url("https://example.org/x.json", "retry/x.json", attempts=4, backoff_s=0)
    assert calls["n"] == 3 and path.read_bytes() == b'[{"ok": 1}]'


def test_fetch_url_does_not_retry_client_errors(tmp_path, monkeypatch):
    import urllib.error
    import pytest
    from avsafety import data as D
    monkeypatch.setenv("AVSAFETY_CACHE", str(tmp_path))
    calls = {"n": 0}

    def not_found(url, timeout=None):
        calls["n"] += 1
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)

    monkeypatch.setattr(D.urllib.request, "urlopen", not_found)
    with pytest.raises(D.DataUnavailable):
        D._fetch_url("https://example.org/missing.json", "retry/missing.json", attempts=4, backoff_s=0)
    assert calls["n"] == 1
