#!/usr/bin/env python3
"""Execute notebooks top to bottom on CPU.

    python scripts/execute_notebooks.py                 # check all notebooks, do not write
    python scripts/execute_notebooks.py --write         # execute and store outputs in place
    python scripts/execute_notebooks.py 03_*/*.ipynb    # a subset

Outputs are committed so that figures render on GitHub, in Colab and on the website.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
import time
from pathlib import Path

import base64
import io

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parents[1]
PHOTO_BYTES = 350_000  # PNG outputs larger than this are usually photographs


def compress_outputs(nb) -> None:
    """Shrink stored figures: optimise PNGs, and store photo-like images as JPEG."""
    try:
        from PIL import Image
    except ImportError:
        return
    for cell in nb.cells:
        for out in cell.get("outputs", []):
            data = out.get("data", {})
            if "image/png" not in data:
                continue
            raw = base64.b64decode(data["image/png"])
            img = Image.open(io.BytesIO(raw))
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True)
            best_key, best = "image/png", min(raw, buf.getvalue(), key=len)
            if len(best) > PHOTO_BYTES:
                jbuf = io.BytesIO()
                img.convert("RGB").save(jbuf, format="JPEG", quality=85, optimize=True)
                best_key, best = "image/jpeg", jbuf.getvalue()
            if best_key == "image/jpeg":
                del data["image/png"]
            data[best_key] = base64.b64encode(best).decode("ascii")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--write", action="store_true", help="save executed notebooks in place")
    ap.add_argument("--timeout", type=int, default=600, help="per-cell timeout in seconds")
    ap.add_argument("--compress-only", action="store_true", help="only shrink stored figures, do not execute")
    args = ap.parse_args()
    os.environ.setdefault("MPLBACKEND", "module://matplotlib_inline.backend_inline")
    paths = [Path(p) for p in (args.paths or sorted(glob.glob(str(ROOT / "[0-9][0-9]_*/*.ipynb"))))]
    if args.compress_only:
        for path in paths:
            nb = nbformat.read(path, as_version=4)
            compress_outputs(nb)
            nbformat.write(nb, path)
        print(f"compressed figures in {len(paths)} notebooks")
        return 0
    failures = 0
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        start = time.time()
        client = NotebookClient(nb, timeout=args.timeout, kernel_name="python3",
                                resources={"metadata": {"path": str(path.parent)}})
        try:
            client.execute()
            status = "ok"
        except CellExecutionError as exc:
            failures += 1
            status = "FAILED: " + str(exc).strip().splitlines()[-1][:200]
        print(f"{time.time() - start:6.1f}s  {path}  {status}", flush=True)
        if args.write and status == "ok":
            compress_outputs(nb)
            nbformat.write(nb, path)
    print(f"{len(paths) - failures}/{len(paths)} notebooks executed successfully")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
