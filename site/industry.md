---
title: For industry
---

The course is built so that engineers can use it at work, not only in a lecture: every notebook ends with an
**In industry** section that names the work product it feeds, who usually owns it and what reviewers and
assessors look for. This page is the index.

:::{note} What this course is and is not
It explains the methods behind the work products and lets you practise them on real data. It does not replace the
standards, a qualified safety or cybersecurity process, or an independent assessment.
:::

## Work products and where to practise them

| Work product | Standard | Notebooks | Template / tool |
|---|---|---|---|
| Item definition, operational situations | ISO 26262-3 (clause 5) | [03-02 HARA](../03_Functional_Safety_ISO26262/02_hara.ipynb) | [HARA template](../templates/HARA_Template.md) |
| Hazard analysis and risk assessment, safety goals (ASIL, FTTI) | ISO 26262-3 (clause 6) | [03-02 HARA](../03_Functional_Safety_ISO26262/02_hara.ipynb), [08-05 Capstone](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) | [ASIL calculator](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/asil.html), `avsafety.iso26262` |
| Safety analyses: FMEA, FTA, dependent failures, ASIL decomposition | ISO 26262-9 (clauses 5, 7, 8) | [03-03 FMEA/FMEDA](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04 FTA](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05 STPA](../03_Functional_Safety_ISO26262/05_stpa.ipynb) | `avsafety.iso26262` |
| Hardware architectural metrics (SPFM, LFM) and PMHF | ISO 26262-5 | [03-03 FMEA/FMEDA](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) | `avsafety.iso26262.hardware_metrics` |
| Software verification, safety validation | ISO 26262-6, ISO 26262-4 | [03-06 V&V](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) | |
| Functional insufficiencies and triggering conditions | ISO 21448 (clause 7) | [04-02 Triggering conditions](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb) (measured on real KITTI data), [02-02 Corner cases](../02_Failures_and_Robustness/02_corner_cases.ipynb) | [SOTIF template](../templates/SOTIF_Analysis_Template.md) |
| Acceptance criteria, validation targets, known and unknown scenarios | ISO 21448 (clauses 6, 9–12) | [04-01 SOTIF](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-04 Simulation](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [06-08 Statistical validation](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb) | [How many miles?](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/miles.html), `avsafety.validation`, `avsafety.coverage` |
| Perception performance evidence (KPIs by condition, distance, occlusion) | ISO 21448, ISO/PAS 8800 | [04-06 SOTIF benchmark](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb) (any detector, release verdict), [01-04 Detection](../01_Perception/04_object_detection.ipynb), [01-05 VRU](../01_Perception/05_vulnerable_road_user_detection.ipynb), [01-03 LiDAR](../01_Perception/03_lidar_point_clouds.ipynb), [01-06 Fusion](../01_Perception/06_sensor_fusion.ipynb) | `avsafety.data`, `avsafety.bench` |
| Dataset specification and analysis | ISO/PAS 8800 | [01-08 Datasets](../01_Perception/08_driving_datasets.ipynb) | `avsafety.data.kitti_object_labels_all` |
| Uncertainty, calibration and runtime monitoring of AI components | ISO/PAS 8800, ISO 21448 | [06-02 – 06-05](../06_AI_Safety_ISO_PAS_8800/README.md), [04-03 OOD monitoring](../04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb) | `avsafety.uq` |
| Threat analysis and risk assessment, cybersecurity goals, CAL | ISO/SAE 21434 (clause 15) | [05-02 TARA](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03 Attack surface](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) | [TARA template](../templates/TARA_Template.md), [TARA calculator](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/tara.html), `avsafety.iso21434` |
| In-vehicle network intrusion detection, security monitoring | ISO/SAE 21434, UN R155 | [05-04 CAN IDS](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb) (real ROAD attack logs) | |
| V2X misbehaviour detection and reporting | ISO/SAE 21434, UN R155, ETSI TS 103 759 | [05-05 V2X misbehaviour detection](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) | |
| Safety envelope, fallback and minimal risk manoeuvre | ISO 21448, UN R157, ISO/TS 5083 | [04-05 RSS](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb), [07-02 Safe planning](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [07-01 ODD monitoring](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) | [RSS tool](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/tools/rss.html), `avsafety.sotif` |
| Human–machine interaction, takeover, foreseeable misuse | ISO 21448, UN R157 | [07-03 Human factors](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [03-05 STPA](../03_Functional_Safety_ISO26262/05_stpa.ipynb) | |
| Field monitoring, safety performance indicators, incident reporting | UL 4600, ISO/TS 5083, NHTSA SGO | [07-05 Field monitoring](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb) (real NHTSA reports) | `avsafety.data.nhtsa_sgo`, [field-safety observatory](observatory.md) |
| Safety case maintenance, evidence traceability, continuous assurance | UL 4600, ISO/TS 5083, ISO 21448 (clause 13) | [08-06 Continuous assurance](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb) | `avsafety.assurance`, [safety case status](safety-case.md) |
| Safety case and release argument | ISO 26262-2, UL 4600, ISO/TS 5083, ISO/PAS 8800 | [08-04 GSN](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05 Capstone](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) | |
| Type approval and regulatory compliance (CSMS, SUMS, ALKS, ADS) | UN R155, R156, R157, EU 2022/1426 | [08-02 Regulation](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) | |

## By role

::::{grid} 1 1 2 2
:::{card} Functional safety engineer
HARA, safety goals, FMEA/FMEDA, FTA, STPA, ASIL decomposition, V&V planning, safety case.
**Start:** 03-02 → 03-04 → 03-05 → 08-05.
:::
:::{card} SOTIF / perception safety engineer
Triggering conditions measured on real data, perception KPIs, acceptance criteria and validation targets.
**Start:** 01-04 → 04-02 → 04-03 → 04-06 → 06-08.
:::
:::{card} ML / perception engineer
Real detection, fusion and tracking evaluation; calibration, conformal prediction and monitoring; what an assessor needs from ML.
**Start:** 01-04 → 01-06 → 06-04 → 06-05 → 06-07.
:::
:::{card} Cybersecurity engineer
TARA end to end, attack surfaces, CAN intrusion detection, safety–security co-engineering.
**Start:** 05-02 → 05-03 → 05-04 → 05-05 → 02-04.
:::
:::{card} Validation and test engineer
Scenario spaces and coverage, simulation credibility, statistical arguments, field data.
**Start:** 04-02 → 04-04 → 06-08 → 07-05.
:::
:::{card} Safety manager, assessor, regulator
How the standards fit together, regulation, gaps, safety cases and release decisions.
**Start:** 08-01 → 08-02 → 08-04 → 08-05 → 08-06.
:::
::::

## Using the toolkit in your own work

`avsafety` (MIT licence) is a small, dependency-light package with unit tests pinned to the standards. Typical uses:
cross-checking an ASIL or TARA table in a review, computing hardware metrics from an FMEDA export, sizing a
validation target, or evaluating detector calibration. Install with
`pip install "avsafety[data] @ git+https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security.git"`.

:::{warning} Data licences
The course uses public datasets for teaching. **KITTI is licensed CC BY-NC-SA 3.0 (non-commercial)**: use it to
learn the methods, then apply them to your organisation's own data. NHTSA and NGSIM data are public. See
[Data and licences](datasets.md).
:::
