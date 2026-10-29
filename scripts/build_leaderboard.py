#!/usr/bin/env python3
"""Build the benchmark leaderboard page from benchmark/results/*.json.

    python scripts/build_leaderboard.py           # validate, write site/benchmark.md and the figure
    python scripts/build_leaderboard.py --check   # validate only and fail if site/benchmark.md is stale

Every result is validated against benchmark/schema.json and the v1 spec hash; any invalid
file makes the script exit with status 1. Partial (non-official) runs are rejected.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from avsafety import bench as B  # noqa: E402

RESULTS = ROOT / "benchmark" / "results"
PAGE = ROOT / "site" / "benchmark.md"
FIGURE = ROOT / "site" / "benchmark-conditions.svg"
FIG_CONDITIONS = ["clear", "fog_200", "fog_100", "fog_50", "fog_25", "low_light_64", "low_light_256", "lens_dirt_25"]
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9"]


def load_results() -> tuple[list[tuple[Path, dict]], list[str]]:
    good, errors = [], []
    for p in sorted(RESULTS.glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{p.name}: not valid JSON ({exc})")
            continue
        errs = B.validate_result(d)
        if not errs and not d["run"]["official"]:
            errs = ["run.official is false: partial runs are not listed"]
        errors += [f"{p.name}: {e}" for e in errs]
        if not errs:
            good.append((p, d))
    return good, errors


def _get(d, cond, cls="pedestrian"):
    return next(r for r in d["metrics"]["by_condition"] if r["condition"] == cond and r["class"] == cls)


def _cell(r):
    return f"{100 * r['recall']:.1f} [{100 * r['ci_low']:.0f}–{100 * r['ci_high']:.0f}]"


def render(results: list[tuple[Path, dict]]) -> str:
    results = sorted(results, key=lambda x: -_get(x[1], "clear")["recall"])
    head = ["Detector", "τ", "Ped. clear", "Ped. fog 50 m", "Ped. fog 25 m", "Ped. low light 1/256",
            "Ped. lens dirt", "Cyclist clear", "Car clear", "Ped. FP/frame clear", "PR-01 verdict",
            "PR-01 speed, clear"]
    rows = []
    for p, d in results:
        tc = {r["condition"]: r for r in d["triggering_conditions"]}
        s = d["submission"]
        v = tc["clear"]["v_max_kmh"]
        rows.append([f"[{s['name']}](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/benchmark/results/{p.name})",
                     s["score_threshold"], _cell(_get(d, "clear")), _cell(_get(d, "fog_50")), _cell(_get(d, "fog_25")),
                     _cell(_get(d, "low_light_256")), _cell(_get(d, "lens_dirt_25")), _cell(_get(d, "clear", "cyclist")),
                     _cell(_get(d, "clear", "car")), f"{_get(d, 'clear')['fp_per_frame']:.2f}", d["release"]["verdict"],
                     f"{v:g} km/h" if v else "none"])
    n = results[0][1]["metrics"]["by_condition"] if results else []
    n_ped = next((r["n"] for r in n if r["condition"] == "clear" and r["class"] == "pedestrian"), 0)
    lines = [
        "---", "title: SOTIF perception benchmark", "---", "",
        "<!-- Built from benchmark/results/*.json by scripts/build_leaderboard.py; do not edit by hand. -->", "",
        "A reproducible **SOTIF triggering-condition report** for camera object detectors: 120 KITTI frames "
        "(spec v1), evaluated in clear air and under physically modelled fog, low light and lens dirt. Each entry is "
        "a complete report — recall by distance, occlusion and truncation with confidence intervals, false positives "
        "per frame, a triggering-condition table, the speed limit the evidence supports, and a release verdict "
        "against the course's AEB pedestrian requirement PR-01. How to run it and how to submit: "
        "[benchmark/README.md](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/benchmark/README.md); "
        "walk-through: [04-06 SOTIF benchmark](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb).", "",
        "## Leaderboard", "",
        f"Recall in % of the evaluated population [95 % Clopper–Pearson interval]; {n_ped} pedestrians per condition. "
        "Sorted by clear-air pedestrian recall. A higher number is not a release: the verdict column applies the "
        "declared requirement.", "",
        "| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|",
    ]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    lines += ["", "## Pedestrian recall per condition", "", f"![Pedestrian recall per condition]({FIGURE.name})", "",
              "## What the numbers can and cannot claim", "",
              "- The fog, low light and lens dirt are **models applied to real daytime images** (KITTI has no real "
              "fog or night). They rank detectors under controlled, documented conditions; they do not replace "
              "real-condition data.",
              "- Recall is **per frame**; 120 frames are not 120 independent encounters, and the frames come from "
              "one city. The intervals cover sampling noise only.",
              "- The baselines are COCO-pretrained; KITTI classes are reached through a documented mapping "
              "(person → pedestrian, car/truck → car, person on bicycle → cyclist).",
              "- KITTI is licensed CC BY-NC-SA 3.0 (non-commercial).", ""]
    return "\n".join(lines)


def figure(results: list[tuple[Path, dict]]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "sotif-benchmark"
    labels = {c["id"]: c["label"].replace(", ", "\n") for c in B.SPEC_V1["conditions"]}
    fig, ax = plt.subplots(figsize=(10, 4.4))
    k = len(results)
    for i, (p, d) in enumerate(sorted(results, key=lambda x: x[1]["submission"]["name"])):
        rs = [_get(d, c) for c in FIG_CONDITIONS]
        x = [j + (i - (k - 1) / 2) * 0.8 / max(k, 1) for j in range(len(FIG_CONDITIONS))]
        y = [r["recall"] for r in rs]
        ax.errorbar(x, y, yerr=[[r["recall"] - r["ci_low"] for r in rs], [r["ci_high"] - r["recall"] for r in rs]],
                    fmt="o", capsize=3, color=OKABE_ITO[i % len(OKABE_ITO)], label=d["submission"]["name"])
    ax.set_xticks(range(len(FIG_CONDITIONS)), [labels[c] for c in FIG_CONDITIONS], fontsize=8)
    ax.set_ylabel("Pedestrian recall (evaluated population)")
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("SOTIF benchmark v1: pedestrian recall with 95 % intervals")
    fig.tight_layout()
    fig.savefig(FIGURE, metadata={"Date": None})
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate and check that site/benchmark.md is current")
    a = ap.parse_args()
    results, errors = load_results()
    for e in errors:
        print("INVALID", e)
    print(f"{len(results)} valid result(s), {len(errors)} problem(s)")
    if errors:
        return 1
    page = render(results)
    if a.check:
        if not PAGE.exists() or PAGE.read_text() != page:
            print("site/benchmark.md is out of date: run python scripts/build_leaderboard.py")
            return 1
        return 0
    PAGE.write_text(page)
    if results:
        figure(results)
    print(f"wrote {PAGE.relative_to(ROOT)} and {FIGURE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
