#!/usr/bin/env python3
"""Course linter: structural checks for every notebook and Markdown file.

Checks
  * every code cell parses (IPython magics/shell lines tolerated)
  * the first cell is the standard header with an "Open in Colab" badge whose
    path matches the notebook's real path on the ``main`` branch
  * relative links in notebooks and Markdown files resolve to existing files
  * no leftovers from the original workshop format ("Session 3", "Notebook 14", ...)

Usage:  python scripts/check_course.py            (exit code 1 on any error)
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "milinpatel07/Autonomous-Driving_AI-Safety-and-Security"
COLAB = re.compile(r"colab\.research\.google\.com/github/" + re.escape(REPO) + r"/blob/([^/]+)/([^)\s\"']+\.ipynb)")
LINK = re.compile(r"\]\(([^)\s]+)\)|href=\"([^\"]+)\"")
LEFTOVERS = [
    (re.compile(r"\bSession\s+\d\b"), "workshop 'Session N' reference"),
    (re.compile(r"\bEnd of Notebook \d+"), "workshop 'End of Notebook N'"),
    (re.compile(r"All Rights Reserved", re.I), "'All Rights Reserved' conflicts with the MIT licence"),
    (re.compile(r"/blob/master/"), "link to non-existent 'master' branch"),
    (re.compile(r"AV_Perception_Safety_Workshop/"), "path from the original workshop repo"),
    (re.compile(r"ISO/IEC 8800"), "use 'ISO/PAS 8800:2024'"),
    (re.compile(r"ISO/PAS 21448:2019"), "superseded by ISO 21448:2022"),
]
MODULE_DIRS = sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"\d\d_", p.name))


def cell_source(cell) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def parses(src: str) -> bool:
    lines = []
    for line in src.split("\n"):
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        lines.append(indent + "pass" if stripped.startswith(("!", "%")) else line)
    try:
        ast.parse("\n".join(lines))
        return True
    except SyntaxError:
        return False


def check_links(text: str, base: Path, where: str, errors: list[str]) -> None:
    for m in LINK.finditer(text):
        target = (m.group(1) or m.group(2) or "").split("#")[0]
        if not target or re.match(r"^[a-z]+:", target) or target.startswith(("/", "{")):
            continue
        if not (base / target).resolve().exists():
            errors.append(f"{where}: broken relative link -> {target}")


def check_notebook(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    if not cells or cells[0].get("cell_type") != "markdown":
        errors.append(f"{rel}: first cell must be the markdown header")
        return
    header = cell_source(cells[0])
    if not header.lstrip().startswith("# "):
        errors.append(f"{rel}: header must start with a '# ' title")
    m = COLAB.search(header)
    if not m:
        errors.append(f"{rel}: header lacks an Open-in-Colab badge for {REPO}")
    elif m.group(1) != "main" or m.group(2) != rel:
        errors.append(f"{rel}: Colab badge points to {m.group(1)}/{m.group(2)}")
    for i, cell in enumerate(cells):
        src = cell_source(cell)
        if cell.get("cell_type") == "code" and not parses(src):
            errors.append(f"{rel}: cell {i} does not parse")
        if cell.get("cell_type") == "markdown":
            check_links(src, path.parent, f"{rel} cell {i}", errors)
        for pattern, why in LEFTOVERS:
            if pattern.search(src):
                errors.append(f"{rel} cell {i}: {why}")


def main() -> int:
    errors: list[str] = []
    notebooks = sorted(p for d in MODULE_DIRS for p in d.glob("*.ipynb"))
    for nb in notebooks:
        check_notebook(nb, errors)
    for md in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("*/*.md")):
        if "_build" in md.parts or "node_modules" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        check_links(text, md.parent, md.relative_to(ROOT).as_posix(), errors)
        for pattern, why in LEFTOVERS[2:4]:
            if pattern.search(text):
                errors.append(f"{md.relative_to(ROOT)}: {why}")
    for d in MODULE_DIRS:
        if not (d / "README.md").exists():
            errors.append(f"{d.name}: missing module README.md")
    print(f"Checked {len(notebooks)} notebooks in {len(MODULE_DIRS)} modules.")
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
