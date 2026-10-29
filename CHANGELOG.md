# Changelog

All notable changes to the course. Versions follow [semantic versioning](https://semver.org/) as described
in [MAINTAINING.md](MAINTAINING.md#releases-and-versions); the `avsafety` toolkit has its own version in
`pyproject.toml`.

## [Unreleased]

## [4.0.0] — 2026-10-29

Safety case as code, SOTIF perception benchmark, field-safety statistics, browser edition and German edition; 50 notebooks.

### Added
- A safety case kept as code (`avsafety.assurance`, `safety_case/`, `scripts/safety_case.py`): the capstone's
  pedestrian-AEB argument with every claim linked to the notebook and metric that produce its evidence;
  evidence from changed code is marked stale, and CI reports any claim whose status flips. New notebook
  08-06, *Continuous assurance*.
- An open SOTIF perception benchmark (`avsafety.bench`, `avsafety.perturb`, `benchmark/`): any camera detector
  on a versioned 120-frame KITTI split under physically modelled fog, low light and lens dirt, with recall
  intervals, a triggering-condition table, a supported speed and a release verdict; two CPU baselines, a
  leaderboard page and an optional SOTIF-PCOD LiDAR track. New notebook 04-06.
- A field-safety observatory (`scripts/observatory.py`, `site/observatory.md`) rebuilt monthly from NHTSA
  Standing General Order reports, California DMV data and Waymo's published data.
- Real CAN-bus attack logs (ROAD) in 05-04 and a new notebook 05-05 on V2X misbehaviour detection with the
  VeReMi Extension benchmark; loaders `can_ids`, `veremi`, `veremi_ground_truth`.
- An in-browser edition (JupyterLite): 24 notebooks run without an account (`scripts/build_lite.py`).
- Auto-checked exercises (`avsafety.exercises`), a teaching guide, an autograded assignment template
  (`classroom/`) and a paper draft for the Journal of Open Source Education (`paper/`).
- A German edition of six core notebooks (`de/`) with a glossary and a drift check.

- `references/normative.yaml`: a registry of every clause, paragraph, table, annex and article the course
  cites from ISO 26262, ISO 21448, ISO/SAE 21434, ISO/PAS 8800, UN R155 and R157, Regulations (EU)
  2024/1689, 2026/1744, 2022/1426, 2019/2144 and 2024/2847 and German traffic law — with what the course
  states, the edition, the source and how it was verified.
- `scripts/check_references.py`: finds the clause citations in notebooks, templates, site pages and the
  toolkit, maps them to the registry, reports unregistered citations and unverified entries, and fails
  when the same fact is cited with different paragraph numbers. It also writes the
  [normative references](site/references.md) page: which notebook cites what.
- Source watch (`scripts/watch_sources.py`, monthly workflow): detects new editions and amendments of the
  cited standards and regulations (ISO Open Data, EU Publications Office, UNECE amendment lists) and new
  releases of KITTI, NGSIM, the NHTSA crash-report files, ROAD and VeReMi, and opens one issue that names
  the affected notebooks.
- Canary (monthly workflow): runs every notebook with an empty data cache and the newest dependency
  versions, checks all external links (`scripts/check_links.py`), and opens one issue when something broke.
- `MAINTAINING.md` (monthly routine, watch and canary issues, references, releases, new notebooks) and this
  changelog.

### Changed
- `avsafety` 1.2.0; modules 04, 05 and 08 renumbered; 04-02 imports its perturbations from `avsafety.perturb`.
- AI Act passages quote Regulation (EU) 2026/1744 directly; three ambiguous clause references qualified.

### Fixed
- UN R157 MRM deceleration limit cited as §5.5.2 of the 01 series (it was §5.5.1 in the original text).
- 05-04 used an f-string that only Python 3.12+ accepts.

## [3.0.0] — 2026-10-28

Real public data throughout; 47 notebooks.

### Added
- `avsafety.data`: loaders for KITTI camera images, LiDAR scans, labels and tracking sequences (read frame by
  frame from the official archives), NGSIM highway trajectories and NHTSA Standing General Order crash
  reports, with licence attributions.
- Seven notebooks: trajectory prediction on NGSIM, STPA, end-to-end and foundation-model driving, safe motion
  planning and fallback, human factors and takeover, field safety monitoring with NHTSA data, and a capstone
  that takes the AEB example from requirement to release decision.
- An *In industry* section in every notebook (work product, owner, what assessors check) and an industry map
  of work products and roles.
- Optional loading of the SOTIF-PCOD dataset from a local copy.

### Changed
- Perception, fusion, tracking, VRU and dataset notebooks evaluated on real KITTI data against ground truth;
  SOTIF triggering conditions measured on real images with a real detector; calibration, conformal
  prediction and explainability applied to a real detector.
- Notebooks renumbered in modules 03, 06 and 07 to make room for the new ones.

## [2.0.0] — 2026-10-28

Verified rebuild; 40 notebooks.

### Added
- Six notebooks: multi-object tracking, fault tree analysis, criticality metrics and RSS, CAN-bus intrusion
  detection, conformal prediction, safety cases with GSN.
- The `avsafety` toolkit with unit tests pinned to the standards and published references.
- Interactive browser tools (ASIL, TARA, RSS, validation mileage), tested against the toolkit.
- Website with learning paths, standards map and glossary.
- Continuous integration that executes every notebook and checks links and Colab badges.

### Changed
- Every notebook reviewed against the standards and primary sources; factual, normative and code errors
  corrected.
- 93 code cells that had stopped running repaired; every notebook runs top to bottom on a CPU.
- Eight modules with flat, descriptive paths and generated module READMEs.

## [1.0.0]

The original workshop materials on perception safety and AI safety for automated driving: 34 notebooks in
workshop sessions.
