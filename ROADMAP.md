# Roadmap

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
- Learned 3D LiDAR detection (e.g. PointPillars) evaluated on KITTI and SOTIF-PCOD under weather variants

**Safety analysis and assurance**
- Dependent-failure analysis and freedom from interference in a mixed-criticality software stack
- Safety performance indicator dashboard across operators, updated automatically from NHTSA releases

**AI safety**
- Formal verification of small neural networks (interval bound propagation)
- Data-quality metrics in the spirit of ISO/PAS 8800 and ISO/IEC 5259 applied to KITTI

**Security**
- V2X misbehaviour detection with simulated position-falsification attacks
- Secure over-the-air updates (UN R156, ISO 24089) and software bills of materials
- GNSS spoofing detection and localisation integrity

**Tools**
- Interactive SOTIF scenario-space explorer and n-wise coverage tool in the browser
- HARA and TARA worksheet export (CSV/Excel) from the toolkit
- Translations of the core notebooks (German first)
