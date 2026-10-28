# Roadmap

## Delivered in version 2.0 (October 2026)

- Expert review of every notebook against the standards and primary sources; factual, normative and code errors corrected
- Repaired 93 code cells that had stopped running; every notebook executes top to bottom on CPU in CI
- New structure: eight modules with flat, descriptive paths and module READMEs
- Six new notebooks: multi-object tracking, fault tree analysis, criticality metrics and RSS, CAN-bus intrusion detection, conformal prediction, safety cases with GSN
- `avsafety` toolkit with unit tests pinned to the standards and published references
- Interactive browser tools (ASIL, TARA, RSS, validation mileage), tested against the toolkit
- Website (Jupyter Book 2) with learning paths, standards map and glossary
- The ideas formerly in `NEXT_STEPS.md`: risk-matrix utility (`avsafety.iso26262`, `avsafety.iso21434`), scenario coverage (`avsafety.coverage`), safety-case notebook, test harness and CI

## Next candidates

Contributions are welcome; open an issue to claim a topic.

**Perception and prediction**
- Bird's-eye-view and occupancy networks, hands-on with a tiny synthetic BEV dataset
- Trajectory prediction and its uncertainty (multi-modal forecasts, minADE/minFDE, calibration of forecasts)
- Sensor degradation models: rain, fog and dirt on LiDAR and camera, with SOTIF triggering-condition analysis

**Safety analysis and assurance**
- STPA and STPA-Sec for an automated driving function
- Safety performance indicators and field monitoring with real crash-report data (NHTSA Standing General Order)
- Human factors of Level 3 take-over: transition time distributions and HMI design
- Dependent-failure analysis and freedom from interference in a mixed-criticality software stack

**AI safety**
- Uncertainty for object detection (probabilistic boxes, calibration of detectors)
- Formal verification of small neural networks (interval bound propagation)
- Dataset specification and data-quality metrics in the spirit of ISO/PAS 8800 and ISO/IEC 5259
- Safety of end-to-end and foundation-model driving stacks: failure modes, monitoring and evidence

**Security**
- V2X misbehaviour detection with simulated position-falsification attacks
- Secure over-the-air updates (UN R156, ISO 24089) and software bills of materials
- GNSS spoofing detection and localisation integrity

**Tools**
- Interactive SOTIF scenario-space explorer and n-wise coverage tool in the browser
- HARA and TARA worksheet export (CSV/Excel) from the toolkit
- Translations of the core notebooks (German first)
