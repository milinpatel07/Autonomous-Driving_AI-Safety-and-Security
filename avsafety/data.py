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
* **ROAD** CAN intrusion dataset (Oak Ridge National Laboratory): real CAN logs of
  one vehicle with physically verified fuzzing, targeted-injection and masquerade
  attacks. Single captures are read out of the 557 MB archive by range requests.
  Verma et al. (2024), PLOS ONE. Licence: CC BY 4.0 — https://doi.org/10.5281/zenodo.10462796
* **VeReMi Extension** V2X misbehaviour benchmark: simulated (VEINS/SUMO, LuST
  scenario) BSM logs with sensor-error models and labelled attacks. Single receiver
  logs are read out of the per-attack archives by range requests.
  Kamel et al. (2020), IEEE ICC. Licence: CC BY 4.0 — https://doi.org/10.5281/zenodo.20090854

Each function raises :class:`DataUnavailable` with a clear message when the
network is unreachable, so notebooks can explain what happened.
"""
from __future__ import annotations

import hashlib
import http.client
import io
import json
import os
import re
import struct
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
ROAD_URL = "https://zenodo.org/api/records/10462796/files/road.zip/content"
VEREMI_URL = "https://zenodo.org/api/records/20090854/files/{subset}.zip/content"

LICENCES = {
    "KITTI": "KITTI Vision Benchmark Suite (Geiger et al., CVPR 2012 / IJRR 2013), CC BY-NC-SA 3.0, "
             "https://www.cvlibs.net/datasets/kitti/",
    "NHTSA SGO": "NHTSA Standing General Order 2021-01 crash reports, public US government data, "
                 "https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting",
    "NGSIM": "US DOT Next Generation Simulation (NGSIM) vehicle trajectories, public domain, "
             "https://data.transportation.gov/d/8ect-6jqj",
    "ROAD": "ROAD CAN intrusion dataset, Oak Ridge National Laboratory (Verma et al., PLOS ONE 2024, "
            "doi:10.1371/journal.pone.0296879), CC BY 4.0, https://doi.org/10.5281/zenodo.10462796",
    "VeReMi Extension": "VeReMi Extension V2X misbehaviour dataset, Institute of Distributed Systems, Ulm University "
                        "(Kamel et al., IEEE ICC 2020, doi:10.1109/ICC40277.2020.9149132), simulated with "
                        "VEINS/SUMO (LuST scenario), CC BY 4.0, https://doi.org/10.5281/zenodo.20090854",
}

KITTI_CLASSES = ("Car", "Van", "Truck", "Pedestrian", "Person_sitting", "Cyclist", "Tram", "Misc", "DontCare")


class DataUnavailable(RuntimeError):
    """Raised when a dataset cannot be downloaded (offline, blocked or moved)."""


def cache_dir() -> Path:
    path = Path(os.environ.get("AVSAFETY_CACHE", Path.home() / ".cache" / "avsafety"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _atomic_write(target: Path, data: bytes) -> None:
    """Write via a temporary file so concurrent readers never see a partial file."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, target)


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
        except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
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
            except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
                if attempt == 2:
                    raise DataUnavailable(f"download failed for {self.url}: {exc}") from None
        buffer[: len(data)] = data
        self.pos += len(data)
        return len(data)


class _SubFile(io.RawIOBase):
    """A read-only window [offset, offset + size) of another seekable file."""

    def __init__(self, base, offset: int, size: int):
        self.base, self.offset, self.size, self.pos = base, offset, size, 0

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        self.pos = {0: 0, 1: self.pos, 2: self.size}[whence] + offset
        return self.pos

    def readinto(self, buffer) -> int:
        n = min(len(buffer), self.size - self.pos)
        if n <= 0:
            return 0
        self.base.seek(self.offset + self.pos)
        data = self.base.read(n)
        buffer[: len(data)] = data
        self.pos += len(data)
        return len(data)


@lru_cache(maxsize=16)
def _remote_zip_url(url: str, buffer_size: int = 1 << 20) -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BufferedReader(_HTTPRangeFile(url), buffer_size=buffer_size))


def _remote_zip(archive: str) -> zipfile.ZipFile:
    return _remote_zip_url(KITTI_BASE + archive)


@lru_cache(maxsize=32)
def _remote_inner_zip(url: str, member: str) -> zipfile.ZipFile:
    """Open a zip that is *stored* (not compressed) inside a remote zip, without downloading either."""
    outer = _remote_zip_url(url, 1 << 16)
    info = outer.getinfo(member)
    if info.compress_type != zipfile.ZIP_STORED:
        raise DataUnavailable(f"{member} is compressed inside {url}; cannot read it by range requests")
    raw = _HTTPRangeFile(url)
    raw.seek(info.header_offset)
    header = raw.read(30)
    name_len, extra_len = struct.unpack("<HH", header[26:30])
    start = info.header_offset + 30 + name_len + extra_len
    return zipfile.ZipFile(io.BufferedReader(_SubFile(raw, start, info.compress_size), buffer_size=4 << 20))


def fetch_kitti_file(archive: str, member: str) -> bytes:
    """Return one file from a KITTI archive, downloading it once and caching it."""
    target = cache_dir() / "kitti" / archive.replace(".zip", "") / member
    if target.exists():
        return target.read_bytes()
    try:
        data = _remote_zip(archive).read(member)
    except KeyError:
        raise DataUnavailable(f"{member} is not in {archive}") from None
    _atomic_write(target, data)
    return data


def _fetch_url(url: str, filename: str) -> Path:
    target = cache_dir() / filename
    if not target.exists():
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                _atomic_write(target, resp.read())
        except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
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


OXTS_COLUMNS = ["lat", "lon", "alt", "roll", "pitch", "yaw", "vn", "ve", "vf", "vl", "vu", "ax", "ay", "az",
                "af", "al", "au", "wx", "wy", "wz", "wf", "wl", "wu", "pos_accuracy", "vel_accuracy",
                "navstat", "numsats", "posmode", "velmode", "orimode"]


def parse_oxts(text: str):
    """Parse KITTI OXTS GPS/IMU records (30 values per line) into a DataFrame.

    Lines end with a trailing space, so split on runs of whitespace; splitting on a
    single space would create a 31st empty field and shift every column by one.
    """
    import pandas as pd
    rows = [line.split() for line in text.strip().splitlines() if line.strip()]
    if any(len(r) != len(OXTS_COLUMNS) for r in rows):
        raise ValueError("unexpected number of OXTS fields")
    return pd.DataFrame(np.array(rows, dtype=float), columns=OXTS_COLUMNS)


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
    oxts = parse_oxts(fetch_kitti_file("data_tracking_oxts.zip", f"training/oxts/{seq}.txt").decode())
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


# --------------------------------------------------------------------------- ROAD CAN intrusion dataset
ROAD_ATTACK_FAMILY = {
    "fuzzing": "fuzzing",
    "correlated_signal": "targeted injection",
    "max_speedometer": "targeted injection",
    "max_engine_coolant_temp": "targeted injection",
    "reverse_light_on": "targeted injection",
    "reverse_light_off": "targeted injection",
    "accelerator": "unlabelled (no injected frames)",
}
_CANDUMP = re.compile(r"^\((\d+\.\d+)\)\s+\S+\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*$")
_HEX = np.full(256, 255, dtype=np.uint8)
for _i, _c in enumerate(b"0123456789ABCDEF"):
    _HEX[_c] = _i
for _i, _c in enumerate(b"abcdef"):
    _HEX[_c] = 10 + _i


def parse_candump(text: str):
    """Parse a Linux ``candump -l`` log into a DataFrame.

    Each line looks like ``(1000000000.001000) can0 0D0#427504646C018700``.
    Returns columns ``t`` (s, relative to the first frame), ``can_id`` (int), ``dlc``
    (bytes), ``data`` (upper-case hex string) and ``b0``..``b7`` (uint8, zero-padded
    beyond the DLC). Malformed lines raise ``ValueError``.
    """
    import pandas as pd
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rows = [_CANDUMP.match(ln) for ln in lines]
    bad = [ln for ln, m in zip(lines, rows) if m is None]
    if bad:
        raise ValueError(f"not a candump line: {bad[0]!r}")
    stamp = np.array([float(m.group(1)) for m in rows])
    data = [m.group(3).upper() for m in rows]
    dlc = np.array([len(d) // 2 for d in data], dtype=np.int16)
    if (dlc > 8).any():
        raise ValueError("classic CAN payloads have at most 8 bytes")
    padded = np.frombuffer("".join(d.ljust(16, "0") for d in data).encode(), dtype=np.uint8).reshape(-1, 16)
    nib = _HEX[padded]
    pay = (nib[:, 0::2] << 4) | nib[:, 1::2]
    df = pd.DataFrame({"t": stamp - (stamp[0] if len(stamp) else 0.0),
                       "can_id": np.array([int(m.group(2), 16) for m in rows], dtype=np.int32),
                       "dlc": dlc, "data": data})
    for k in range(8):
        df[f"b{k}"] = pay[:, k]
    return df


def road_label(df, meta: dict, tol: float = 1e-3):
    """Ground-truth labels for one ROAD capture from its ``capture_metadata.json`` entry.

    A frame is labelled injected (1) when it lies inside ``injection_interval``, carries the
    injected identifier (``'XXX'`` = any identifier, used for fuzzing) and its payload matches
    ``injection_data_str``, where ``X`` is a wildcard nibble. This reconstructs the injected
    frames from the published metadata; a genuine frame that happens to match the pattern inside
    the interval would also be labelled 1 (rare, but a limitation to state). ``tol`` (s) widens
    the interval because the published bounds are rounded to the microsecond and the first
    injected frame can carry exactly the start time. Returns an int8 array.
    """
    label = np.zeros(len(df), dtype=np.int8)
    interval, pattern, aid = meta.get("injection_interval"), meta.get("injection_data_str"), meta.get("injection_id")
    if not interval or not pattern:
        return label
    t = df["t"].to_numpy()
    sel = (t >= interval[0] - tol) & (t <= interval[1] + tol)
    if aid and "X" not in aid.upper():
        sel &= df["can_id"].to_numpy() == int(aid, 16)
    data = df["data"].to_numpy()
    pattern = pattern.upper()
    for i in np.flatnonzero(sel):
        d = data[i]
        if len(d) == len(pattern) and all(p == "X" or p == c for p, c in zip(pattern, d)):
            label[i] = 1
    return label


def _road_family(capture: str) -> str:
    base = re.sub(r"(_attack.*|_masquerade)$", "", capture)
    if capture.startswith("ambient"):
        return "none"
    family = ROAD_ATTACK_FAMILY.get(base, "unknown")
    return "masquerade" if capture.endswith("_masquerade") else family


def _road_member(member: str) -> bytes:
    """One file of the ROAD archive, cached gzip-compressed (the logs compress about 6:1)."""
    import gzip
    target = cache_dir() / "road" / (member + ".gz")
    if target.exists():
        return gzip.decompress(target.read_bytes())
    try:
        data = _remote_zip_url(ROAD_URL).read(member)
    except KeyError:
        raise DataUnavailable(f"{member} is not in the ROAD archive") from None
    _atomic_write(target, gzip.compress(data, compresslevel=3))
    return data


@lru_cache(maxsize=2)
def road_metadata(kind: str = "attacks") -> dict:
    """``capture_metadata.json`` of the ROAD ``'attacks'`` or ``'ambient'`` folder (elapsed time,
    injected identifier, payload pattern and injection interval in s per capture)."""
    if kind not in ("attacks", "ambient"):
        raise ValueError("kind must be 'attacks' or 'ambient'")
    return json.loads(_road_member(f"road/{kind}/capture_metadata.json").decode())


def can_ids(captures="fuzzing_attack_1"):
    """Real CAN traffic with labelled attacks from the ROAD dataset (Verma et al., 2024).

    ``captures`` is one capture name or a list, e.g. ``'ambient_dyno_drive_basic_short'``,
    ``'fuzzing_attack_1'``, ``'max_speedometer_attack_1'``,
    ``'max_speedometer_attack_1_masquerade'`` (see :func:`road_metadata`). Only the requested
    logs are downloaded (0.1-73 MB compressed each) and cached.

    Returns a DataFrame with ``capture``, ``t`` (s from capture start), ``can_id``, ``dlc``,
    ``data``, ``b0``..``b7``, ``label`` (1 = injected frame) and ``attack`` (family:
    'none', 'fuzzing', 'targeted injection', 'masquerade'). In the ``_masquerade`` variants the
    genuine frames of the target identifier were removed during the injection interval, which
    emulates a silenced sender (the dataset's "simulated masquerade").
    """
    import pandas as pd
    names = [captures] if isinstance(captures, str) else list(captures)
    parts = []
    for name in names:
        kind = "ambient" if name.startswith("ambient") else "attacks"
        meta = road_metadata(kind)
        if name not in meta:
            raise ValueError(f"unknown ROAD capture {name!r}")
        df = parse_candump(_road_member(f"road/{kind}/{name}.log").decode())
        df["label"] = road_label(df, meta[name])
        df["attack"] = _road_family(name)
        df.insert(0, "capture", name)
        parts.append(df)
    return pd.concat(parts, ignore_index=True)


# --------------------------------------------------------------------------- VeReMi Extension (V2X)
VEREMI_ATTACKS = {
    0: "Genuine", 1: "ConstPos", 2: "ConstPosOffset", 3: "RandomPos", 4: "RandomPosOffset",
    5: "ConstSpeed", 6: "ConstSpeedOffset", 7: "RandomSpeed", 8: "RandomSpeedOffset",
    9: "EventualStop", 10: "Disruptive", 11: "DataReplay", 12: "DelayedMessages",
    13: "DoS", 14: "DoSRandom", 15: "DoSDisruptive", 16: "GridSybil", 17: "DataReplaySybil",
    18: "DoSRandomSybil", 19: "DoSDisruptiveSybil",
}
_TRACE = re.compile(r"traceJSON-(\d+)-(\d+)-A(\d+)-(\d+)-(\d+)\.json$")


def parse_veremi_trace(text: str, receiver: int = -1):
    """Parse one VeReMi(-Extension) ``traceJSON`` receiver log (one JSON object per line).

    ``type`` 2 rows are the receiver's own GNSS fixes, ``type`` 3 rows are received BSMs.
    Vectors are split into ``_x``/``_y`` columns: ``pos`` (m), ``spd`` (m/s), ``acl`` (m/s^2),
    ``hed`` (unit heading vector) and their ``*_noise`` (the sender's stated error, same units).
    Times ``rcv_time``/``send_time`` are simulation seconds.
    """
    import pandas as pd
    recs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = json.loads(line)
        r = {"receiver": receiver, "type": m["type"], "rcv_time": m.get("rcvTime", np.nan),
             "send_time": m.get("sendTime", np.nan), "sender": m.get("sender", -1),
             "sender_pseudo": m.get("senderPseudo", -1), "message_id": m.get("messageID", -1)}
        for key in ("pos", "spd", "acl", "hed", "pos_noise", "spd_noise", "acl_noise", "hed_noise"):
            v = m.get(key, (np.nan, np.nan))
            r[f"{key}_x"], r[f"{key}_y"] = v[0], v[1]
        recs.append(r)
    df = pd.DataFrame(recs)
    for col in ("receiver", "type", "sender", "sender_pseudo", "message_id"):
        if col in df:
            df[col] = df[col].astype("int64")
    return df


def _veremi_inner(attack: str, density: str, hour: int):
    """The stored inner zip of one VeReMi Extension subset for simulation hour 0 or 1."""
    url = VEREMI_URL.format(subset=f"{attack}_{density}")
    start = {"0709": 25200, "1416": 50400}[density] + 3600 * hour
    outer = _remote_zip_url(url, 1 << 16)
    members = [n for n in outer.namelist() if f"/VeReMi_{start}_" in n and n.endswith(".zip")]
    if not members:
        raise DataUnavailable(f"no simulation hour {hour} in {attack}_{density}")
    return url, members[0], _remote_inner_zip(url, members[0])


def _veremi_index(attack: str, density: str) -> dict:
    """Map vehicle id -> attacker type for every vehicle of a subset (from the log file names)."""
    target = cache_dir() / "veremi" / f"{attack}_{density}" / "attacker_types.json"
    if target.exists():
        return {int(k): v for k, v in json.loads(target.read_text()).items()}
    url = VEREMI_URL.format(subset=f"{attack}_{density}")
    outer = _remote_zip_url(url, 1 << 16)
    index = {}
    for member in outer.namelist():
        if member.endswith(".zip"):
            for name in _remote_inner_zip(url, member).namelist():
                m = _TRACE.search(name)
                if m:
                    index[int(m.group(1))] = int(m.group(3))
    _atomic_write(target, json.dumps(index).encode())
    return index


def veremi(attack: str = "ConstPosOffset", density: str = "1416", hour: int = 1, n_receivers: int = 40,
           genuine_receivers_only: bool = True):
    """Received V2X messages (BSMs) from the VeReMi Extension benchmark, labelled per sender.

    ``attack`` names a VeReMi Extension subset (a value of :data:`VEREMI_ATTACKS`, e.g.
    'ConstPos', 'ConstPosOffset', 'RandomPosOffset', 'ConstSpeedOffset', 'EventualStop',
    'DataReplay', 'DoS'); ``density`` is '1416' (14:00-16:00, lighter traffic) or '0709'
    (rush hour); ``hour`` selects the first (0) or second (1) simulated hour, which gives a
    time-separated train/test split. In every subset 30 % of vehicles misbehave.

    Only the first ``n_receivers`` receiver logs (each 20-100 kB compressed) are downloaded.
    The data are **simulated** (VEINS/SUMO on the LuST scenario, with GNSS-like sensor error
    models): real benchmark data, not field measurements.

    Returns a DataFrame from :func:`parse_veremi_trace` plus ``attacker_type`` (sender's type,
    0 = genuine; -1 for the receiver's own fixes) and ``attack`` (its name).
    """
    import pandas as pd
    if attack not in VEREMI_ATTACKS.values() or attack == "Genuine":
        raise ValueError(f"unknown VeReMi Extension attack {attack!r}")
    if density not in ("1416", "0709") or hour not in (0, 1):
        raise ValueError("density must be '1416' or '0709' and hour 0 or 1")
    index = _veremi_index(attack, density)
    folder = cache_dir() / "veremi" / f"{attack}_{density}" / f"hour{hour}"
    listing = folder / "receivers.json"
    if listing.exists():
        names = json.loads(listing.read_text())
    else:
        _, _, inner = _veremi_inner(attack, density, hour)
        names = [n for n in inner.namelist() if _TRACE.search(n)]
        _atomic_write(listing, json.dumps(names).encode())
    if genuine_receivers_only:
        names = [n for n in names if _TRACE.search(n).group(3) == "0"]
    import gzip
    parts = []
    for name in names[:n_receivers]:
        target = folder / (Path(name).name + ".gz")
        if not target.exists():
            _, _, inner = _veremi_inner(attack, density, hour)
            _atomic_write(target, gzip.compress(inner.read(name), compresslevel=3))
        parts.append(parse_veremi_trace(gzip.decompress(target.read_bytes()).decode(),
                                        int(_TRACE.search(name).group(1))))
    df = pd.concat(parts, ignore_index=True)
    df["attacker_type"] = np.where(df["type"] == 3, df["sender"].map(index).fillna(-1), -1).astype(int)
    df["attack"] = np.where(df["type"] == 2, "own GNSS", df["attacker_type"].map(VEREMI_ATTACKS).fillna("unknown"))
    return df


def veremi_ground_truth(attack: str = "ConstPosOffset", density: str = "1416", hour: int = 1):
    """True sender states for every message of one VeReMi Extension subset and simulated hour.

    Reads the ``traceGroundTruthJSON`` file (about 11 MB compressed) and returns one row per
    message: ``message_id``, ``sender``, ``send_time`` and the *true* ``pos``/``spd``/``acl``/``hed``
    columns (same names as :func:`parse_veremi_trace`). Join on ``message_id`` to compare what a
    sender claimed with where it really was.
    """
    folder = cache_dir() / "veremi" / f"{attack}_{density}" / f"hour{hour}"
    import gzip
    target = folder / "ground_truth.json.gz"
    if not target.exists():
        _, _, inner = _veremi_inner(attack, density, hour)
        names = [n for n in inner.namelist() if "traceGroundTruthJSON" in n]
        if not names:
            raise DataUnavailable(f"no ground-truth file in {attack}_{density}, hour {hour}")
        _atomic_write(target, gzip.compress(inner.read(names[0]), compresslevel=3))
    df = parse_veremi_trace(gzip.decompress(target.read_bytes()).decode())
    return df.drop(columns=["receiver", "rcv_time", "type"])
