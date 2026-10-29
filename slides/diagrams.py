"""Diagrams drawn for the lecture slides (everything else on the slides comes from notebook outputs).

Each function returns a Matplotlib figure; ``render_all`` writes them as SVG to slides/_build/diagrams/. Colours
follow the notebooks: ISO 26262 blue, ISO 21448 orange, ISO/SAE 21434 vermillion, ISO/PAS 8800 green
(Okabe-Ito palette, readable with colour-vision deficiency).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

BLUE, ORANGE, GREEN, VERMILLION = "#0072B2", "#E69F00", "#009E73", "#D55E00"
SKY, PURPLE, GREY, INK = "#56B4E9", "#CC79A7", "#7F7F7F", "#1F2937"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "path", "figure.dpi": 100,
})

MODULES = {
    "01": ("Perception and Prediction", "What does the vehicle perceive,\nand how well?", SKY),
    "02": ("Failures and Robustness", "How does it fail\nin practice?", SKY),
    "03": ("Functional Safety\nISO 26262", "What if hardware or\nsoftware malfunctions?", BLUE),
    "04": ("SOTIF\nISO 21448", "What if it works as specified\nand is still unsafe?", ORANGE),
    "05": ("Cybersecurity\nISO/SAE 21434", "What if someone\nattacks it?", VERMILLION),
    "06": ("AI Safety\nISO/PAS 8800", "What is specific to\nmachine learning?", GREEN),
    "07": ("Runtime Assurance\nand Operations", "How is safety kept\nduring operation?", PURPLE),
    "08": ("Standards, Regulation\nand Safety Case", "How is it argued,\napproved and maintained?", GREY),
}


def _box(ax, x, y, w, h, color, alpha=1.0, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=color, edgecolor=INK, linewidth=lw, alpha=alpha))


def _arrow(ax, p, q, alpha=1.0, color=INK, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=14, color=color, alpha=alpha,
                                 linewidth=1.3, linestyle=ls, shrinkA=2, shrinkB=2))


def course_map(highlight: str | None = None):
    """Eight modules in three stages; ``highlight`` fades all other modules."""
    fig, ax = plt.subplots(figsize=(13, 6.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.1)
    ax.axis("off")
    w, h = 3.4, 1.05
    pos = {"01": (0.2, 3.0), "02": (0.2, 1.5),
           "03": (4.8, 4.3), "04": (4.8, 3.0), "05": (4.8, 1.7), "06": (4.8, 0.4),
           "07": (9.4, 3.0), "08": (9.4, 1.5)}
    for x, label in ((1.9, "How the system works\nand how it fails"), (6.5, "Four standards,\nfour causes of harm"),
                     (11.1, "Operation and the\nsafety argument")):
        ax.text(x, 6.05, label, ha="center", va="top", fontsize=11, color=GREY,
                fontweight="bold")
    for m, (x, y) in pos.items():
        name, question, color = MODULES[m]
        a = 1.0 if highlight in (None, m) else 0.18
        _box(ax, x, y, w, h, color, alpha=0.30 * a + (0.25 if highlight == m else 0),
             lw=2.6 if highlight == m else 1.0)
        ax.text(x + 0.12, y + h - 0.12, m, ha="left", va="top", fontsize=17, fontweight="bold",
                color=INK, alpha=max(a, 0.35))
        ax.text(x + 0.75, y + h - 0.13, name, ha="left", va="top", fontsize=10.5, fontweight="bold",
                color=INK, alpha=max(a, 0.35), linespacing=1.05)
        ax.text(x + w - 0.1, y + 0.08, question, ha="right", va="bottom", fontsize=8.6, color=INK,
                alpha=max(a, 0.35), style="italic", linespacing=1.0)
    fa = 0.25 if highlight else 1.0
    _arrow(ax, (1.9, 3.0), (1.9, 2.55), alpha=fa)
    for m in ("03", "04", "05", "06"):
        _arrow(ax, (3.6, 2.6), (4.8, pos[m][1] + h / 2), alpha=fa)
        _arrow(ax, (8.2, pos[m][1] + h / 2), (9.4, 2.85), alpha=fa)
    _arrow(ax, (11.1, 3.0), (11.1, 2.55), alpha=fa)
    ax.text(11.1, 0.95, "every module adds evidence\nto one safety case (08-04 to 08-06)", ha="center",
            va="top", fontsize=9, color=GREY)
    fig.tight_layout(pad=0.2)
    return fig


def aeb_thread():
    """The pedestrian AEB example as it runs through the eight modules."""
    steps = [
        ("01", "Recall of a real detector\nfalls with distance and\nocclusion (KITTI)", "01-05"),
        ("02", "Tempe 2018: detection\nwithout a usable prediction;\nOOD inputs", "02-01, 02-03"),
        ("03", "HARA: unintended braking\nASIL D, missed pedestrian\nASIL B", "03-02"),
        ("04", "Fog and low light are\ntriggering conditions;\nsupported speed", "04-02, 04-06"),
        ("05", "TARA of the perception-\nto-brake path; one risk\nstill open", "05-02"),
        ("06", "Calibration and a\nconformal threshold for\nthe detector", "06-04, 06-05"),
        ("07", "ODD monitor, fallback,\nfield safety indicators", "07-01, 07-05"),
        ("08", "Release decision with\nreasons: DO NOT\nRELEASE", "08-05"),
    ]
    fig, ax = plt.subplots(figsize=(13, 4.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    w, h = 2.9, 1.65
    coords = [(0.2 + i * 3.2, 2.55) for i in range(4)] + [(0.2 + (3 - i) * 3.2, 0.35) for i in range(4)]
    for (m, text, nbs), (x, y) in zip(steps, coords):
        color = MODULES[m][2]
        _box(ax, x, y, w, h, color, alpha=0.30)
        ax.text(x + 0.12, y + h - 0.1, m, fontsize=15, fontweight="bold", va="top", color=INK)
        ax.text(x + w - 0.1, y + h - 0.12, nbs, fontsize=8.5, va="top", ha="right", color=GREY)
        ax.text(x + w / 2, y + 0.62, text, fontsize=10, ha="center", va="center", color=INK, linespacing=1.2)
    for i in range(3):
        _arrow(ax, (coords[i][0] + w, 2.55 + h / 2), (coords[i + 1][0], 2.55 + h / 2))
    _arrow(ax, (coords[3][0] + w / 2, 2.55), (coords[4][0] + w / 2, 0.35 + h))
    for i in range(4, 7):
        _arrow(ax, (coords[i][0], 0.35 + h / 2), (coords[i + 1][0] + w, 0.35 + h / 2))
    fig.tight_layout(pad=0.2)
    return fig


CONCEPTS = [  # label, where it is taught in depth, regular expression searched in the notebooks' text
    ("Operational design domain (ODD)", "01-01", r"\bODD\b|operational design domain"),
    ("Recall, precision, confidence bounds", "01-04, 01-05", r"\brecall\b"),
    ("Out-of-distribution input", "02-03", r"out-of-distribution|\bOOD\b"),
    ("Hazard, HARA, ASIL", "03-02", r"\bASIL\b|\bHARA\b"),
    ("Triggering condition", "04-01, 04-02", r"triggering condition"),
    ("Criticality metrics, RSS", "04-05", r"\bRSS\b|\bTTC\b"),
    ("Threat, TARA, CAL", "05-02", r"\bTARA\b|\bCAL\b"),
    ("Calibration, conformal prediction", "06-04, 06-05", r"\bconformal\b|\bECE\b|calibration error"),
    ("Runtime monitor, fallback", "04-03, 07-01", r"runtime monitor|minimal risk|\bMRM\b|fallback"),
    ("Field data, safety indicators", "07-05", r"Standing General Order|\bSGO\b|safety performance indicator|\bSPI"),
    ("Safety case (GSN)", "08-04", r"safety case|\bGSN\b"),
]


def concept_counts() -> np.ndarray:
    """Number of notebooks per module whose text uses each concept at least three times."""
    counts = np.zeros((len(CONCEPTS), 8), dtype=int)
    for path in sorted(ROOT.glob("0[1-8]_*/*.ipynb")):
        m = int(path.parent.name[:2]) - 1
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        text = " ".join("".join(c["source"]) for c in cells if c["cell_type"] == "markdown")
        for i, (_, _, rx) in enumerate(CONCEPTS):
            if len(re.findall(rx, text, flags=re.I)) >= 3:
                counts[i, m] += 1
    return counts


def concept_map():
    counts = concept_counts()
    fig, ax = plt.subplots(figsize=(13, 5.4))
    ax.imshow(np.where(counts > 0, counts, np.nan), cmap="Blues", vmin=-1, vmax=counts.max() + 1, aspect="auto")
    for i, (label, taught, _) in enumerate(CONCEPTS):
        for j in range(8):
            if counts[i, j]:
                ax.text(j, i, str(counts[i, j]), ha="center", va="center", fontsize=10.5, color=INK)
        tm = {int(t.strip()[:2]) - 1 for t in taught.split(",")}
        for j in tm:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=VERMILLION, linewidth=2.4, zorder=5))
    ax.set_yticks(range(len(CONCEPTS)), [f"{c[0]}  ({c[1]})" for c in CONCEPTS], fontsize=10.5)
    short = ["Perception", "Failures", "ISO 26262", "SOTIF", "Security", "AI safety", "Operations", "Safety case"]
    ax.set_xticks(range(8), [f"{m}\n{t}" for m, t in zip(MODULES, short)], fontsize=10)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, 8), minor=True)
    ax.set_yticks(np.arange(-0.5, len(CONCEPTS)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.set_xlabel("number = notebooks in the module that use the concept (at least three mentions); "
                  "red frame = where it is taught", fontsize=9.5, color=GREY)
    fig.tight_layout(pad=0.3)
    return fig


def four_causes():
    """Four sources of hazardous behaviour, the standard for each, one argument."""
    fig, ax = plt.subplots(figsize=(13, 4.4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    rows = [("E/E malfunction", "a random hardware fault or a\nsystematic software error", "ISO 26262", BLUE, "03"),
            ("Functional insufficiency", "the function works as specified, but\nthe specification or performance\nis not enough",
             "ISO 21448 (SOTIF)", ORANGE, "04"),
            ("Malicious manipulation", "an attacker changes inputs,\nmessages or software", "ISO/SAE 21434", VERMILLION, "05"),
            ("ML-specific insufficiency", "data, training or model\nproperties of an AI component", "ISO/PAS 8800", GREEN, "06")]
    for i, (cause, example, std, color, m) in enumerate(rows):
        x = 0.15 + i * 3.2
        _box(ax, x, 1.75, 3.0, 2.5, color, alpha=0.28)
        ax.text(x + 1.5, 4.1, cause, ha="center", va="top", fontsize=11.5, fontweight="bold", color=INK)
        ax.text(x + 1.5, 3.55, example, ha="center", va="top", fontsize=9.5, color=INK, linespacing=1.15)
        ax.text(x + 1.5, 2.0, f"{std}\nModule {m}", ha="center", va="bottom", fontsize=10.5, color=INK,
                fontweight="bold", linespacing=1.2)
        _arrow(ax, (x + 1.5, 1.75), (6.5, 1.05))
    _box(ax, 3.6, 0.15, 5.8, 0.9, "#E5E7EB")
    ax.text(6.5, 0.6, "one hazard list, one architecture, one safety case (Module 08)", ha="center",
            va="center", fontsize=11, color=INK, fontweight="bold")
    fig.tight_layout(pad=0.2)
    return fig


def recall_interval():
    """How wide is a 95 % interval on recall, for the sample sizes used in the course?"""
    from scipy import stats
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ns = np.logspace(1, 4, 200)
    for p, color in ((0.65, ORANGE), (0.90, BLUE), (0.99, GREEN)):
        k = p * ns  # non-integer k gives a smooth curve between the exact values at integer k
        lo = stats.beta.ppf(0.025, k, ns - k + 1)
        hi = stats.beta.ppf(0.975, k + 1, ns - k)
        ax.plot(ns, (hi - lo) / 2, color=color, lw=2.2, label=f"measured recall {p:.2f}")
    for n, label in ((144, "04-02: 144 pedestrians\nper fog level"), (1000, "1,000 labelled\npedestrians")):
        ax.axvline(n, color=GREY, ls=":", lw=1.2)
        ax.text(n * 1.06, 0.215, label, fontsize=9.5, color=GREY, va="top")
    ax.set_xscale("log")
    ax.set_xlabel("number of labelled objects n")
    ax.set_ylabel("half-width of the 95 % interval")
    ax.set_ylim(0, 0.22)
    ax.grid(alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("Exact (Clopper–Pearson) 95 % interval on a measured recall", fontsize=12)
    fig.tight_layout()
    return fig


def stopping_distance():
    """Reaction plus braking distance: the range in which a pedestrian must be detected."""
    fig, ax = plt.subplots(figsize=(12, 4.6))
    v = np.linspace(10, 100, 200)
    for t, a, color, label in ((0.5, 6.0, ORANGE, "reaction 0.5 s, 6 m/s² (04-02)"),
                               (1.0, 6.0, BLUE, "reaction 1.0 s, 6 m/s²"),
                               (0.5, 4.0, VERMILLION, "reaction 0.5 s, 4 m/s² (wet road)")):
        ms = v / 3.6
        ax.plot(v, ms * t + ms ** 2 / (2 * a), color=color, lw=2.2, label=label)
    d60 = 60 / 3.6 * 0.5 + (60 / 3.6) ** 2 / 12
    ax.plot([60, 60, 10], [0, d60, d60], color=GREY, ls=":", lw=1.2)
    ax.text(62, 6, f"60 km/h → {d60:.1f} m:\npedestrians within 32 m\nmust be detected", fontsize=10)
    ax.set_xlabel("speed (km/h)")
    ax.set_ylabel("stopping distance (m)")
    ax.set_xlim(10, 100)
    ax.set_ylim(0, 120)
    ax.grid(alpha=0.3)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    return fig


def scenario_levels():
    """Functional, logical and concrete scenario for the AEB pedestrian crossing."""
    fig, ax = plt.subplots(figsize=(13, 4.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.0)
    ax.axis("off")
    cols = [("Functional", "words, for experts", "Ego vehicle drives on an urban\nroad; a pedestrian steps out\nbehind a parked car.", SKY),
            ("Logical", "parameters with ranges", "ego speed 20–60 km/h\npedestrian speed 1–3 m/s\noccluder: none, car, van\nvisibility 25 m – clear", ORANGE),
            ("Concrete", "one value per parameter", "ego 50 km/h, pedestrian 1.4 m/s,\nparked car, visibility 80 m,\nstep-out 18 m ahead", GREEN)]
    for i, (name, sub, body, color) in enumerate(cols):
        x = 0.2 + i * 4.35
        _box(ax, x, 0.25, 3.9, 3.5, color, alpha=0.28)
        ax.text(x + 1.95, 3.55, name, ha="center", va="top", fontsize=14, fontweight="bold", color=INK)
        ax.text(x + 1.95, 3.0, sub, ha="center", va="top", fontsize=10, color=GREY, style="italic")
        ax.text(x + 1.95, 1.55, body, ha="center", va="center", fontsize=10.5, color=INK, linespacing=1.3)
        if i < 2:
            _arrow(ax, (x + 3.9, 2.0), (x + 4.35, 2.0))
    fig.tight_layout(pad=0.2)
    return fig


DIAGRAMS = {
    "course_map": course_map,
    **{f"course_map_{m}": (lambda m=m: course_map(m)) for m in MODULES},
    "aeb_thread": aeb_thread,
    "concept_map": concept_map,
    "four_causes": four_causes,
    "recall_interval": recall_interval,
    "stopping_distance": stopping_distance,
    "scenario_levels": scenario_levels,
}


def render_all(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, make in DIAGRAMS.items():
        fig = make()
        fig.savefig(out_dir / f"{name}.svg", format="svg")
        plt.close(fig)
