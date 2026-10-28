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

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--write", action="store_true", help="save executed notebooks in place")
    ap.add_argument("--timeout", type=int, default=600, help="per-cell timeout in seconds")
    args = ap.parse_args()
    os.environ.setdefault("MPLBACKEND", "module://matplotlib_inline.backend_inline")
    paths = [Path(p) for p in (args.paths or sorted(glob.glob(str(ROOT / "[0-9][0-9]_*/*.ipynb"))))]
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
            nbformat.write(nb, path)
    print(f"{len(paths) - failures}/{len(paths)} notebooks executed successfully")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
