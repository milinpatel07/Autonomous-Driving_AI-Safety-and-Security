#!/usr/bin/env python3
"""Generate module README.md files and the course table in the root README.md
from the notebook headers, so that the overview can never drift from the content.

    python scripts/build_readmes.py           # write files
    python scripts/build_readmes.py --check   # exit 1 if any file is out of date (used in CI)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "milinpatel07/Autonomous-Driving_AI-Safety-and-Security"
COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
SITE = "https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security"

MODULES = {
    "01_Perception": (
        "Perception Systems",
        "How an automated vehicle senses and understands its surroundings — and where that understanding can fail. "
        "From SAE levels and the operational design domain through cameras, LiDAR and radar to detection, fusion, "
        "tracking and the datasets the field is built on.",
    ),
    "02_Failures_and_Robustness": (
        "Failures and Robustness",
        "What goes wrong in the real world and why: documented incidents and their investigations, corner cases, "
        "out-of-distribution inputs and adversarial attacks on perception.",
    ),
    "03_Functional_Safety_ISO26262": (
        "Functional Safety (ISO 26262)",
        "Hazards caused by malfunctioning E/E systems: the ISO 26262 lifecycle, hazard analysis and risk "
        "assessment (HARA), FMEA/FMEDA and hardware metrics, fault tree analysis, and verification and validation.",
    ),
    "04_SOTIF_ISO21448": (
        "SOTIF (ISO 21448)",
        "Hazards without a fault: functional insufficiencies, triggering conditions and reasonably foreseeable misuse. "
        "Scenario spaces, OOD monitoring as a safety measure, simulation-based validation, criticality metrics and RSS.",
    ),
    "05_Cybersecurity_ISO21434": (
        "Cybersecurity (ISO/SAE 21434)",
        "Protecting the vehicle over its lifecycle: the ISO/SAE 21434 framework, threat analysis and risk "
        "assessment (TARA), attack surfaces and hands-on intrusion detection on the CAN bus.",
    ),
    "06_AI_Safety_ISO_PAS_8800": (
        "AI Safety (ISO/PAS 8800)",
        "Making machine-learning components trustworthy enough for a safety argument: the AI-safety standards, "
        "uncertainty and its decomposition, ensembles, calibration, conformal guarantees, explainability and "
        "statistical validation.",
    ),
    "07_Runtime_Assurance_and_Operations": (
        "Runtime Assurance and Operations",
        "Safety after start of production: monitoring the ODD at runtime and falling back to a minimal risk "
        "condition, cooperative driving with V2X, and how automated driving is being deployed today.",
    ),
    "08_Standards_Regulation_and_Safety_Case": (
        "Standards, Regulation and Safety Case",
        "Bringing it together: how the standards interlock, what type approval and regulation require, where the "
        "standards still have gaps, and how to argue safety with a structured safety case.",
    ),
}


def src(cell) -> str:
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else s


def header_info(path: Path) -> dict:
    nb = json.loads(path.read_text(encoding="utf-8"))
    head = src(nb["cells"][0]) if nb.get("cells") else ""
    title = next((l[2:].strip() for l in head.splitlines() if l.startswith("# ")), path.stem)
    info = {"title": title, "level": "", "time": "", "standards": "", "objectives": []}
    lines = head.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"\|\s*Level\s*\|", line, re.I) and i + 2 < len(lines):
            keys = [c.strip().lower() for c in line.strip().strip("|").split("|")]
            vals = [c.strip() for c in lines[i + 2].strip().strip("|").split("|")]
            row = dict(zip(keys, vals))
            info["level"] = row.get("level", "")
            info["time"] = row.get("time", "")
            info["standards"] = row.get("standards", "")
            break
    # learning objectives: header cell or the first cell containing the heading
    text = head
    if "learning objectives" not in head.lower():
        text = next((src(c) for c in nb["cells"][:4] if "learning objectives" in src(c).lower()), "")
    m = re.search(r"#+\s*Learning objectives\s*\n(.*?)(\n#|\Z)", text, re.I | re.S)
    if m:
        info["objectives"] = [re.sub(r"^\s*(\d+\.|[-*])\s*", "", l).strip()
                              for l in m.group(1).splitlines() if re.match(r"^\s*(\d+\.|[-*])\s+", l)]
    return info


def colab(path: str) -> str:
    return f"[![Open In Colab]({COLAB_BADGE})](https://colab.research.google.com/github/{REPO}/blob/main/{path})"


def clean_title(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def module_readme(folder: str, notebooks: list[Path], n: int) -> str:
    name, intro = MODULES[folder]
    out = [f"# Module {folder[:2]} · {name}", "", intro, "",
           f"**{len(notebooks)} notebooks** · each runs in Google Colab on CPU, without dataset downloads.", "",
           "| # | Notebook | Level | Standards | Open |", "|---|---|---|---|---|"]
    details = []
    for nb in notebooks:
        info = header_info(nb)
        rel = f"{folder}/{nb.name}"
        out.append(f"| {nb.name[:2]} | [{clean_title(info['title'])}]({nb.name}) | {info['level']} | {info['standards'] or '–'} | {colab(rel)} |")
        if info["objectives"]:
            details.append(f"### {nb.name[:2]} · {clean_title(info['title'])}\n")
            details.extend(f"- {o}" for o in info["objectives"])
            details.append("")
    out += ["", "## What you will learn", ""] + details
    prev_mod = sorted(MODULES)[n - 1] if n > 0 else None
    next_mod = sorted(MODULES)[n + 1] if n + 1 < len(MODULES) else None
    nav = ["[Course home](../README.md)"]
    if prev_mod:
        nav.insert(0, f"← [Module {prev_mod[:2]} · {MODULES[prev_mod][0]}](../{prev_mod}/README.md)")
    if next_mod:
        nav.append(f"[Module {next_mod[:2]} · {MODULES[next_mod][0]}](../{next_mod}/README.md) →")
    out += ["---", "", " · ".join(nav), ""]
    return "\n".join(out)


def course_table() -> str:
    rows = []
    for folder, (name, _) in MODULES.items():
        nbs = sorted((ROOT / folder).glob("*.ipynb"))
        rows.append(f"<details>\n<summary><b>{folder[:2]} · {name}</b> — {len(nbs)} notebooks</summary>\n")
        rows.append("| # | Notebook | Level | Open |\n|---|---|---|---|")
        for nb in nbs:
            info = header_info(nb)
            rel = f"{folder}/{nb.name}"
            rows.append(f"| {folder[:2]}-{nb.name[:2]} | [{clean_title(info['title'])}]({rel}) | {info['level']} | "
                        f"{colab(rel)} |")
        rows.append("\n</details>\n")
    return "\n".join(rows)


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    targets = {}
    for n, folder in enumerate(sorted(MODULES)):
        nbs = sorted((ROOT / folder).glob("*.ipynb"))
        targets[ROOT / folder / "README.md"] = module_readme(folder, nbs, n)
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- COURSE-TABLE:START -->", "<!-- COURSE-TABLE:END -->"
    if start in text and end in text:
        pre, rest = text.split(start, 1)
        _, post = rest.split(end, 1)
        targets[readme] = f"{pre}{start}\n{course_table()}\n{end}{post}"
    for path, content in targets.items():
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if old != content:
            stale.append(path.relative_to(ROOT).as_posix())
            if not check:
                path.write_text(content, encoding="utf-8")
    if check and stale:
        print("Out of date (run python scripts/build_readmes.py):", ", ".join(stale))
        return 1
    print("updated: " + ", ".join(stale) if stale else "all READMEs up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
