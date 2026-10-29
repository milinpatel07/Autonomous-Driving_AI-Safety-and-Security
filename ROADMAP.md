# Roadmap

## Delivered in version 4.0 (October 2026)

- A safety case kept as code: the capstone's argument with every claim linked to the notebook and metric that
  produce its evidence, re-evaluated by CI on every change (`avsafety.assurance`, `safety_case/`, notebook 08-06)
- An open SOTIF perception benchmark on real KITTI frames under physically modelled fog, low light and lens dirt,
  with a release verdict against a declared requirement and an optional SOTIF-PCOD LiDAR track (notebook 04-06)
- Field-safety statistics rebuilt monthly from NHTSA crash reports, California DMV data and published exposure
- Real CAN-bus attack logs (ROAD) in 05-04 and V2X misbehaviour detection on VeReMi Extension (new 05-05)
- A registry of every normative reference with its source, a consistency checker, monthly watches of the cited
  regulations and datasets, and a monthly re-run of the whole course against the live sources
- 24 notebooks run in the browser without an account (JupyterLite)
- Auto-checked exercises, a teaching guide with semester and industry-training plans, an autograded assignment
  template, and a paper draft for the Journal of Open Source Education
- A German edition of the core notebooks

## Delivered in version 3.0 (October 2026)

- Real public data across the course through `avsafety.data`: KITTI camera images, LiDAR scans, labels and
  tracking sequences (read frame by frame from the official archives), NGSIM highway trajectories and NHTSA
  Standing General Order crash reports
- Perception, fusion, tracking, VRU and dataset notebooks evaluated on real KITTI data against ground truth
- SOTIF triggering conditions measured on real images with a real detector (distance, occlusion, darkness,
  physically modelled fog)
- Calibration, conformal prediction and explainability applied to a real detector
- Seven new notebooks: trajectory prediction (NGSIM), STPA, end-to-end and foundation-model driving, safe motion
  planning and fallback, human factors and takeover, field safety monitoring (NHTSA), and a capstone from
  requirement to release decision
- An *In industry* section in every notebook and an industry map of work products and roles
- Optional support for the SOTIF-PCOD dataset (IEEE DataPort)

## Delivered in version 2.0 (October 2026)

- Expert review of every notebook against the standards and primary sources; factual, normative and code errors corrected
- Repaired 93 code cells that had stopped running; every notebook executes top to bottom on CPU in CI
- Eight modules with flat, descriptive paths and generated module READMEs
- Six new notebooks: multi-object tracking, fault tree analysis, criticality metrics and RSS, CAN-bus intrusion detection, conformal prediction, safety cases with GSN
- `avsafety` toolkit with unit tests pinned to the standards and published references
- Interactive browser tools (ASIL, TARA, RSS, validation mileage), tested against the toolkit
- Website (Jupyter Book 2) with learning paths, standards map and glossary

## Next candidates

Contributions are welcome; open an issue to claim a topic.

**Perception and prediction**
- Bird's-eye-view and occupancy networks on real data
- Learned 3D LiDAR detection (e.g. PointPillars) as a benchmark baseline on KITTI and SOTIF-PCOD under weather variants

**Safety analysis and assurance**
- Dependent-failure analysis and freedom from interference in a mixed-criticality software stack

**AI safety**
- Formal verification of small neural networks (interval bound propagation)
- Data-quality metrics in the spirit of ISO/PAS 8800 and ISO/IEC 5259 applied to KITTI

**Security**
- Secure over-the-air updates (UN R156, ISO 24089) and software bills of materials
- GNSS spoofing detection and localisation integrity

**Tools**
- More benchmark baselines (stronger detectors run on GPU) and a camera–LiDAR fusion track
- Safety cases as code for a second item (e.g. ALKS lane keeping)
- Interactive SOTIF scenario-space explorer and n-wise coverage tool in the browser
- HARA and TARA worksheet export (CSV/Excel) from the toolkit
- Further translations, and the German edition extended beyond the core notebooks
