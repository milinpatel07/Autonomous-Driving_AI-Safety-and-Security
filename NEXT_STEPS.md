# What to Code Next

A practical, implementation-first roadmap to evolve this repository from a learning resource into a stronger **hands-on engineering toolkit**.

## Priority 1 — Add executable safety/security utilities (high impact)

### 1) `tools/risk_matrix.py`
Build a CLI utility that converts HARA/TARA inputs into a normalized risk matrix.

- **Why next:** It connects directly to existing templates and helps users practice repeatable risk scoring.
- **Definition of done:**
  - Accept CSV/JSON inputs for severity, exposure, controllability (HARA) and impact/attack feasibility (TARA).
  - Output risk class + markdown summary table.
  - Include unit tests for score boundaries.

### 2) `tools/scenario_coverage.py`
Create a scenario coverage analyzer for SOTIF-style datasets.

- **Why next:** Scenario completeness is a recurring theme across modules; this makes it tangible.
- **Definition of done:**
  - Ingest scenario metadata (weather, time, road type, actor density, sensor quality).
  - Compute coverage heatmaps and list underrepresented bins.
  - Export an action-oriented gap report.

## Priority 2 — Add verification notebooks with reusable code cells

### 3) New notebook: `03_Functional_Safety/notebooks/05_safety_case_argumentation.ipynb`
Introduce Goal Structuring Notation (GSN)-style safety argument skeletons.

- **Why next:** Bridges analysis outputs (HARA/FMEA/V&V) into assurance evidence.
- **Definition of done:**
  - Provide reusable safety claim templates.
  - Map each claim to evidence artifacts from repository outputs.
  - Include an example argument for pedestrian emergency braking.

### 4) New notebook: `05_Cybersecurity/notebooks/04_v2x_threat_simulation.ipynb`
Simulate basic V2X threat scenarios and mitigations.

- **Why next:** Extends attack-surface theory into lightweight experimentation.
- **Definition of done:**
  - Model replay/spoofing/jamming at conceptual simulation level.
  - Quantify simple risk changes before/after mitigations.
  - Tie controls to ISO/SAE 21434 work products.

## Priority 3 — Improve project usability for contributors

### 5) Add a lightweight test harness (`tests/`)
Start with data-validation and utility tests.

- **Why next:** Makes future additions safer and reviewable.
- **Definition of done:**
  - `pytest` setup and CI-ready command.
  - Tests for risk matrix mapping and scenario coverage math.
  - Notebook smoke-check script (e.g., metadata + broken link checks).

### 6) Add `examples/` with sample datasets
Provide minimal synthetic CSV files that exercise tools and notebooks.

- **Why next:** Users can run everything quickly without external data wrangling.
- **Definition of done:**
  - HARA/TARA example inputs.
  - Scenario metadata sample for SOTIF coverage.
  - Expected output snapshots for regression checks.

## Suggested implementation order (2-week sprint)

1. Build `tools/risk_matrix.py` + tests.
2. Build `tools/scenario_coverage.py` + tests.
3. Add synthetic data in `examples/`.
4. Add safety case notebook.
5. Add V2X threat simulation notebook.
6. Add CI-style test script in README/CONTRIBUTING.

## Suggested success metrics

- **Adoption:** Number of notebook/tool runs from clean setup.
- **Quality:** Test pass rate and reduced regression bugs.
- **Coverage:** Increase in scenario-bin coverage across key ODD dimensions.
- **Traceability:** Fraction of claims linked to explicit evidence artifacts.
