"""Real public datasets for the course, fetched on demand and cached.

Nothing is bundled with the repository: each loader downloads only what it needs
and keeps it in a local cache (``~/.cache/avsafety`` or ``$AVSAFETY_CACHE``).

* **KITTI** object detection and tracking benchmarks (camera, LiDAR, labels,
  calibration, GPS/IMU). The official archives are 12-37 GB; HTTP range requests
  read single frames out of them, about 1-2 s per file.
  Geiger, Lenz, Urtasun (2012), CVPR; Geiger et al. (2013), IJRR.
  Licence: CC BY-NC-SA 3.0 — https://www.cvlibs.net/datasets/kitti/
* **NHTSA Standing General Order** crash reports for ADS and Level 2 ADAS.
  Public US government data — https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting
* **NGSIM** vehicle trajectories (US-101, I-80, Lankershim, Peachtree) via the
  US DOT open-data API. Public domain — https://data.transportation.gov/d/8ect-6jqj

Each function raises :class:`DataUnavailable` with a clear message when the
network is unreachable, so notebooks can explain what happened.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

KITTI_BASE = "https://s3.eu-central-1.amazonaws.com/avg-kitti/"
SGO_URLS = {
    "ADS": "https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv",
    "ADAS": "https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADAS.csv",
}
NGSIM_API = "https://data.transportation.gov/resource/8ect-6jqj.json"

LICENCES = {
    "KITTI": "KITTI Vision Benchmark Suite (Geiger et al., CVPR 2012 / IJRR 2013), CC BY-NC-SA 3.0, "
             "https://www.cvlibs.net/datasets/kitti/",
    "NHTSA SGO": "NHTSA Standing General Order 2021-01 crash reports, public US government data, "
                 "https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting",
    "NGSIM": "US DOT Next Generation Simulation (NGSIM) vehicle trajectories, public domain, "
             "https://data.transportation.gov/d/8ect-6jqj",
}

KITTI_CLASSES = ("Car", "Van", "Truck", "Pedestrian", "Person_sitting", "Cyclist", "Tram", "Misc", "DontCare")


class DataUnavailable(RuntimeError):
    """Raised when a dataset cannot be downloaded (offline, blocked or moved)."""


def cache_dir() -> Path:
    path = Path(os.environ.get("AVSAFETY_CACHE", Path.home() / ".cache" / "avsafety"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def attribution(*names: str) -> str:
    """Licence and citation lines for the datasets used."""
    return "\n".join(f"Data: {LICENCES[n]}" for n in (names or LICENCES))


# --------------------------------------------------------------------------- remote zip access
class _HTTPRangeFile(io.RawIOBase):
    """A seekable read-only file over HTTP range requests."""

    def __init__(self, url: str, timeout: float = 60.0):
        self.url, self.timeout, self.pos = url, timeout, 0
        try:
            head = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=timeout)
        except (urllib.error.URLError, OSError) as exc:
            raise DataUnavailable(f"cannot reach {url}: {exc}") from None
        self.size = int(head.headers["Content-Length"])

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        base = {0: 0, 1: self.pos, 2: self.size}[whence]
        self.pos = base + offset
        return self.pos

    def readinto(self, buffer) -> int:
        if self.pos >= self.size or len(buffer) == 0:
            return 0
        end = min(self.pos + len(buffer), self.size) - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        for attempt in range(3):
            try:
                data = urllib.request.urlopen(req, timeout=self.timeout).read()
                break
            except (urllib.error.URLError, OSError) as exc:
                if attempt == 2:
                    raise DataUnavailable(f"download failed for {self.url}: {exc}") from None
        buffer[: len(data)] = data
        self.pos += len(data)
        return len(data)


@lru_cache(maxsize=16)
def _remote_zip(archive: str) -> zipfile.ZipFile:
    raw = _HTTPRangeFile(KITTI_BASE + archive)
    return zipfile.ZipFile(io.BufferedReader(raw, buffer_size=1 << 20))


def fetch_kitti_file(archive: str, member: str) -> bytes:
    """Return one file from a KITTI archive, downloading it once and caching it."""
    target = cache_dir() / "kitti" / archive.replace(".zip", "") / member
    if target.exists():
        return target.read_bytes()
    try:
        data = _remote_zip(archive).read(member)
    except KeyError:
        raise DataUnavailable(f"{member} is not in {archive}") from None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return data


def _fetch_url(url: str, filename: str) -> Path:
    target = cache_dir() / filename
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                target.write_bytes(resp.read())
        except (urllib.error.URLError, OSError) as exc:
            raise DataUnavailable(f"cannot download {url}: {exc}") from None
    return target


# --------------------------------------------------------------------------- KITTI parsing
def parse_calib(text: str) -> dict:
    """Parse a KITTI calibration file (object or tracking format) into matrices.

    Returns P2 (3x4), R0 (4x4, rectification) and Tr_velo_to_cam (4x4).
    """
    raw = {}
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        key, _, values = line.replace(":", " ", 1).partition(" ")
        raw[key.strip()] = np.array([float(v) for v in values.split()])
    r0 = raw.get("R0_rect", raw.get("R_rect"))
    tr = raw.get("Tr_velo_to_cam", raw.get("Tr_velo_cam"))
    R0 = np.eye(4)
    R0[:3, :3] = r0.reshape(3, 3)
    Tr = np.eye(4)
    Tr[:3, :4] = tr.reshape(3, 4)
    return {"P2": raw["P2"].reshape(3, 4), "R0": R0, "Tr_velo_to_cam": Tr}


_LABEL_COLS = ["type", "truncated", "occluded", "alpha", "x1", "y1", "x2", "y2",
               "h", "w", "l", "x", "y", "z", "rotation_y"]


def parse_object_labels(text: str) -> list[dict]:
    """Parse KITTI object labels (one object per line)."""
    out = []
    for line in text.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        rec = {"type": parts[0]}
        rec.update({k: float(v) for k, v in zip(_LABEL_COLS[1:], parts[1:15])})
        rec["occluded"] = int(rec["occluded"])
        if len(parts) > 15:
            rec["score"] = float(parts[15])
        out.append(rec)
    return out


def kitti_difficulty(label: dict) -> str:
    """KITTI benchmark difficulty: Easy / Moderate / Hard, or 'Ignored'.

    Easy: box height >= 40 px, fully visible, truncation <= 15 %.
    Moderate: >= 25 px, partly occluded, truncation <= 30 %.
    Hard: >= 25 px, difficult to see, truncation <= 50 %.
    """
    height = label["y2"] - label["y1"]
    occ, trunc = label["occluded"], label["truncated"]
    if height >= 40 and occ <= 0 and trunc <= 0.15:
        return "Easy"
    if height >= 25 and occ <= 1 and trunc <= 0.30:
        return "Moderate"
    if height >= 25 and occ <= 2 and trunc <= 0.50:
        return "Hard"
    return "Ignored"


def box3d_corners(label: dict) -> np.ndarray:
    """Eight corners (3x8) of a KITTI 3D box in rectified camera coordinates."""
    h, w, l, ry = label["h"], label["w"], label["l"], label["rotation_y"]
    x = np.array([l, l, -l, -l, l, l, -l, -l]) / 2
    y = np.array([0, 0, 0, 0, -h, -h, -h, -h])
    z = np.array([w, -w, -w, w, w, -w, -w, w]) / 2
    rot = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]])
    return rot @ np.vstack([x, y, z]) + np.array([[label["x"]], [label["y"]], [label["z"]]])


@dataclass
class KittiFrame:
    """One KITTI frame: image (H x W x 3, uint8), LiDAR points (N x 4: x, y, z, reflectance),
    labels and calibration."""

    index: str
    image: np.ndarray | None = None
    points: np.ndarray | None = None
    labels: list = field(default_factory=list)
    calib: dict | None = None

    def velo_to_rect(self, pts: np.ndarray) -> np.ndarray:
        """LiDAR xyz (N x 3) to rectified camera coordinates (N x 3)."""
        homo = np.hstack([pts[:, :3], np.ones((len(pts), 1))])
        return (self.calib["R0"] @ self.calib["Tr_velo_to_cam"] @ homo.T).T[:, :3]

    def rect_to_image(self, pts_rect: np.ndarray) -> np.ndarray:
        """Rectified camera coordinates (N x 3) to pixel coordinates (N x 2)."""
        homo = np.hstack([pts_rect, np.ones((len(pts_rect), 1))])
        uvw = (self.calib["P2"] @ homo.T).T
        return uvw[:, :2] / uvw[:, 2:3]

    def lidar_in_image(self, max_depth: float = 80.0):
        """LiDAR points visible in the camera image: (uv pixels, depth in m, original points)."""
        rect = self.velo_to_rect(self.points)
        front = (rect[:, 2] > 0.5) & (rect[:, 2] < max_depth)
        uv = self.rect_to_image(rect[front])
        h, w = self.image.shape[:2]
        inside = (uv[:, 0] >= 0) & (uv[:, 0] < w) & (uv[:, 1] >= 0) & (uv[:, 1] < h)
        return uv[inside], rect[front][inside, 2], self.points[front][inside]


def _decode_png(data: bytes) -> np.ndarray:
    from PIL import Image
    return np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))


def kitti_object(index: int, parts=("image", "points", "labels", "calib")) -> KittiFrame:
    """Load one frame (0-7480) of the KITTI object-detection training set."""
    idx = f"{index:06d}"
    frame = KittiFrame(index=idx)
    if "image" in parts:
        frame.image = _decode_png(fetch_kitti_file("data_object_image_2.zip", f"training/image_2/{idx}.png"))
    if "points" in parts:
        raw = fetch_kitti_file("data_object_velodyne.zip", f"training/velodyne/{idx}.bin")
        frame.points = np.frombuffer(raw, dtype=np.float32).reshape(-1, 4).copy()
    if "labels" in parts:
        frame.labels = parse_object_labels(fetch_kitti_file("data_object_label_2.zip",
                                                            f"training/label_2/{idx}.txt").decode())
    if "calib" in parts:
        frame.calib = parse_calib(fetch_kitti_file("data_object_calib.zip", f"training/calib/{idx}.txt").decode())
    return frame


def kitti_object_labels_all():
    """All 7,481 KITTI object training labels as a pandas DataFrame (one row per object).

    Downloads the 5 MB label archive once.
    """
    import pandas as pd
    path = _fetch_url(KITTI_BASE + "data_object_label_2.zip", "kitti/data_object_label_2.zip")
    rows = []
    with zipfile.ZipFile(path) as z:
        for name in sorted(n for n in z.namelist() if n.endswith(".txt")):
            frame = Path(name).stem
            for rec in parse_object_labels(z.read(name).decode()):
                rec["frame"] = frame
                rows.append(rec)
    df = pd.DataFrame(rows)
    df["difficulty"] = [kitti_difficulty(r) for r in df.to_dict("records")]
    df["box_height_px"] = df["y2"] - df["y1"]
    df["distance_m"] = np.hypot(df["x"], df["z"])
    return df


def kitti_tracking(sequence: int, frames=None, images: bool = True, points: bool = False):
    """Load a KITTI tracking training sequence (0-20).

    Returns a dict with ``labels`` (DataFrame), ``calib``, ``oxts`` (GPS/IMU DataFrame),
    and lists ``images`` / ``points`` for the requested frame numbers.
    """
    import pandas as pd
    seq = f"{sequence:04d}"
    cols = ["frame", "track_id", "type", "truncated", "occluded", "alpha", "x1", "y1", "x2", "y2",
            "h", "w", "l", "x", "y", "z", "rotation_y"]
    text = fetch_kitti_file("data_tracking_label_2.zip", f"training/label_02/{seq}.txt").decode()
    labels = pd.read_csv(io.StringIO(text), sep=" ", header=None, usecols=range(17), names=cols)
    calib = parse_calib(fetch_kitti_file("data_tracking_calib.zip", f"training/calib/{seq}.txt").decode())
    oxts_cols = ["lat", "lon", "alt", "roll", "pitch", "yaw", "vn", "ve", "vf", "vl", "vu", "ax", "ay", "az",
                 "af", "al", "au", "wx", "wy", "wz", "wf", "wl", "wu", "pos_accuracy", "vel_accuracy",
                 "navstat", "numsats", "posmode", "velmode", "orimode"]
    oxts = pd.read_csv(io.StringIO(fetch_kitti_file("data_tracking_oxts.zip", f"training/oxts/{seq}.txt").decode()),
                       sep=" ", header=None, names=oxts_cols)
    frames = list(range(int(labels["frame"].max()) + 1)) if frames is None else list(frames)
    out = {"sequence": seq, "labels": labels, "calib": calib, "oxts": oxts, "frames": frames}
    if images:
        out["images"] = [_decode_png(fetch_kitti_file("data_tracking_image_2.zip",
                                                      f"training/image_02/{seq}/{f:06d}.png")) for f in frames]
    if points:
        out["points"] = [np.frombuffer(fetch_kitti_file("data_tracking_velodyne.zip",
                                                        f"training/velodyne/{seq}/{f:06d}.bin"),
                                       dtype=np.float32).reshape(-1, 4) for f in frames]
    return out


# --------------------------------------------------------------------------- NHTSA and NGSIM
def nhtsa_sgo(kind: str = "ADS"):
    """NHTSA Standing General Order crash reports as a DataFrame (kind 'ADS' or 'ADAS').

    Reports are not rates: they lack exposure (miles driven) and one crash can produce
    several reports (see the 'Same Incident ID' column).
    """
    import pandas as pd
    if kind not in SGO_URLS:
        raise ValueError("kind must be 'ADS' or 'ADAS'")
    path = _fetch_url(SGO_URLS[kind], f"nhtsa/SGO_{kind}.csv")
    return pd.read_csv(path, low_memory=False)


def ngsim(location: str = "us-101", where: str | None = None, limit: int = 200_000,
          select: str | None = None):
    """Query NGSIM trajectories (US customary units: feet, ft/s, milliseconds).

    ``location`` is one of 'us-101', 'i-80', 'lankershim', 'peachtree'.
    ``where`` is an optional SoQL filter, e.g. "vehicle_id < 500".
    """
    import pandas as pd
    clauses = [f"location='{location}'"] + ([where] if where else [])
    params = {"$where": " AND ".join(clauses), "$limit": str(limit), "$order": "vehicle_id,frame_id"}
    if select:
        params["$select"] = select
    url = NGSIM_API + "?" + urllib.parse.urlencode(params)
    key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:16]
    path = _fetch_url(url, f"ngsim/{key}.json")
    df = pd.DataFrame(json.loads(path.read_text()))
    for col in df.columns:
        if col != "location":
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
    return df
