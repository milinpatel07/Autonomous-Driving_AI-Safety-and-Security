<p align="center">
  <img src="assets/banner.svg" alt="Autonomous Driving: AI Safety and Security — an open course in eight modules, from perception to safety cases" width="100%">
</p>

<p align="center">
  <a href="https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/actions/workflows/ci.yml"><img src="https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/actions/workflows/ci.yml/badge.svg" alt="CI: notebooks execute and tests pass"></a>
  <a href="https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/"><img src="https://img.shields.io/badge/website-course-1f5fae" alt="Course website"></a>
  <a href="https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/01_Perception/01_sae_levels_and_odd.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-2a9d8f" alt="MIT Licence"></a>
  <a href="CITATION.cff"><img src="https://img.shields.io/badge/cite-CITATION.cff-7b5ea7" alt="Cite this repository"></a>
</p>

**An open, runnable course on the safety and security of automated driving** — from how a vehicle perceives the
world to how you argue that it is safe and secure enough to deploy. Forty Jupyter notebooks cover perception,
real-world failures, **ISO 26262**, **ISO 21448 (SOTIF)**, **ISO/SAE 21434**, **ISO/PAS 8800**, runtime assurance,
regulation and safety cases. Every notebook opens in Google Colab with one click and runs on a CPU without
downloading datasets.

<p align="center">
  <a href="https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/"><b>Website</b></a> ·
  <a href="#the-course"><b>Course</b></a> ·
  <a href="#interactive-tools"><b>Interactive tools</b></a> ·
  <a href="#the-avsafety-toolkit"><b>Toolkit</b></a> ·
  <a href="templates/"><b>Templates</b></a> ·
  <a href="#learning-paths"><b>Learning paths</b></a>
</p>

## Why this course

- **End to end.** A recurring worked example, an automatic emergency braking (AEB) function that protects pedestrians, links the modules: from detection and tracking through HARA, fault trees, SOTIF and TARA to a GSN safety case.
- **Correct and sourced.** Every notebook has been reviewed against the standards and primary sources (NTSB, NHTSA, UNECE, EUR-Lex, peer-reviewed papers). Normative tables are implemented once in a tested toolkit, and time-sensitive facts are dated.
- **Runnable and tested.** Continuous integration executes every notebook, runs the toolkit's unit tests and checks every link and Colab badge on each change.
- **Hands-on.** You build things: a Kalman tracker, a fault-tree engine, a TARA pipeline, a CAN intrusion detector, conformal prediction sets, an RSS controller and a safety-case checker.

<p align="center">
  <img src="assets/standards-map.svg" alt="Which standard covers which source of harm: malfunctions → ISO 26262; functional insufficiencies → ISO 21448; ML-specific insufficiencies → ISO/PAS 8800; attacks → ISO/SAE 21434; all feed the safety case (ISO/TS 5083, UL 4600)" width="100%">
</p>

## The course

| Module | Focus | Notebooks |
|---|---|---|
| [01 · Perception Systems](01_Perception/README.md) | SAE levels, ODD, sensors, LiDAR, detection, VRUs, fusion, tracking, datasets | 8 |
| [02 · Failures and Robustness](02_Failures_and_Robustness/README.md) | incident investigations, corner cases, OOD detection, adversarial attacks | 4 |
| [03 · Functional Safety (ISO 26262)](03_Functional_Safety_ISO26262/README.md) | lifecycle, HARA, FMEA/FMEDA, fault tree analysis, V&V | 5 |
| [04 · SOTIF (ISO 21448)](04_SOTIF_ISO21448/README.md) | triggering conditions, scenarios, OOD monitoring, simulation, RSS | 5 |
| [05 · Cybersecurity (ISO/SAE 21434)](05_Cybersecurity_ISO21434/README.md) | framework, TARA, attack surfaces, CAN intrusion detection | 4 |
| [06 · AI Safety (ISO/PAS 8800)](06_AI_Safety_ISO_PAS_8800/README.md) | uncertainty, ensembles, calibration, conformal prediction, XAI, statistical validation | 7 |
| [07 · Runtime Assurance and Operations](07_Runtime_Assurance_and_Operations/README.md) | runtime ODD monitoring, V2X, deployment landscape | 3 |
| [08 · Standards, Regulation and Safety Case](08_Standards_Regulation_and_Safety_Case/README.md) | standards integration, type approval, gaps, GSN safety cases | 4 |

Expand a module to open any notebook directly in Colab:

<!-- COURSE-TABLE:START -->
<!-- COURSE-TABLE:END -->

## Learning paths

| Goal | Path |
|---|---|
| **Complete course** (~40 h) | 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 |
| **Safety engineer** (~18 h) | 03 → 04 → 05 → 08 |
| **ML / perception engineer** (~20 h) | 01 → 02 → 06 → 04-03 → 07-01 |
| **Security engineer** (~10 h) | 05 → 02-04 → 07-02 → 08-01 |
| **Manager / regulator** (~6 h) | 01-01 → 02-01 → 03-01 → 04-01 → 05-01 → 06-01 → 08-02 → 08-04 |
| **One-hour taster** | 01-01 → 03-02 → the [interactive tools](#interactive-tools) |

## Interactive tools

Browser calculators that work on a phone and offline, using exactly the same tables as the toolkit (CI checks that
they agree):

| Tool | What it does |
|---|---|
| [ASIL calculator](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/asil.html) | Severity × exposure × controllability → ASIL, with decomposition options (ISO 26262-3, -9) |
| [TARA risk calculator](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/tara.html) | Attack potential, attack vector or CVSS v3.1 → feasibility → risk value and CAL (ISO/SAE 21434) |
| [RSS safe distance](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/rss.html) | Responsibility-Sensitive Safety minimum gap, TTC, headway and DRAC |
| [How many miles?](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/miles.html) | Failure-free distance needed to demonstrate a target rate (Kalra & Paddock, 2016) |

## The avsafety toolkit

The normative tables and formulas used across the course, as a small pip-installable package with unit tests
pinned to the standards and published references:

```bash
pip install "git+https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git"
```

```python
from avsafety import iso26262, iso21434, sotif, validation

iso26262.determine_asil("S3", "E4", "C2")                       # 'C'
iso21434.cvss31_base_score("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")  # 9.8
sotif.rss_safe_longitudinal_distance(v_rear=25.0, v_front=20.0)  # metres
validation.miles_to_demonstrate(1.09e-8, confidence=0.95)        # ≈ 275 million miles
```

See [avsafety/README.md](avsafety/README.md) for all modules: ISO 26262 (ASIL, decomposition, SPFM/LFM/PMHF),
ISO/SAE 21434 (attack potential, risk, CAL, CVSS), SOTIF metrics and RSS, statistical validation, uncertainty
(calibration, temperature scaling, conformal prediction) and scenario coverage.

## Templates

Professional, editable templates with worked examples that match the notebooks:
[HARA (ISO 26262)](templates/HARA_Template.md) ·
[SOTIF analysis (ISO 21448)](templates/SOTIF_Analysis_Template.md) ·
[TARA (ISO/SAE 21434)](templates/TARA_Template.md)

## Getting started

**Google Colab (recommended):** click any *Open in Colab* badge. Nothing to install.

**Locally:**

```bash
git clone https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git
cd Autonomous-Driving_AI-Safety-and-Security
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

The notebooks need Python 3.9 or later and run on a CPU. For local GPU acceleration, install PyTorch following the
[official instructions](https://pytorch.org/get-started/locally/).

## Research behind the course

The course draws on the author's research on SOTIF, uncertainty and assurance of ML-based perception at
Hochschule Kempten, for example:

- Patel, M., & Jung, R. (2026). Integrating cybersecurity into the AI safety assurance argument: A GSN pattern for AI-based perception components. *LNCS*, Springer. [doi:10.1007/978-3-032-35506-5_55](https://doi.org/10.1007/978-3-032-35506-5_55)
- Patel, M., & Jung, R. (2026). Uncertainty evaluation to support SOTIF analysis for identifying performance insufficiencies in ML-based LiDAR object detection. *VEHITS 2026*. [doi:10.5220/0014967200004030](https://doi.org/10.5220/0014967200004030)
- Patel, M., Jung, R., & Khatun, M. (2025). A systematic literature review on safety of the intended functionality for automated driving systems. *SAE Technical Paper* 2025-01-5030. [doi:10.4271/2025-01-5030](https://doi.org/10.4271/2025-01-5030)

More on the [About page](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/about).

## Contributing

Corrections, new topics and translations are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and the
[roadmap](ROADMAP.md) for ideas.

## Citation

```bibtex
@misc{patel_av_safety_security,
  author    = {Patel, Milin},
  title     = {Autonomous Driving: AI Safety and Security -- an open course},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security}
}
```

## Licence and disclaimer

[MIT Licence](LICENSE) © 2025–2026 Milin Patel. The material is for education: it explains standards and
regulations but does not reproduce or replace them, and it is not legal or certification advice.
