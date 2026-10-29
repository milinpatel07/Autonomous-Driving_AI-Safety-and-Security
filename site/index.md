---
title: "Autonomous Driving: AI Safety and Security"
short_title: Home
---

```{image} ../assets/banner.svg
:alt: Course map from perception to safety case
:width: 100%
```

## An open course from perception to the safety case

Fifty notebooks cover how an automated vehicle perceives and predicts its environment and how its safety and
security are argued before deployment: perception and prediction, failure analysis, ISO 26262, ISO 21448 (SOTIF),
ISO/SAE 21434, ISO/PAS 8800, runtime assurance, regulation and safety cases.

Each notebook runs on a CPU in Google Colab; 24 also [run in the browser](run-in-browser.md) without an account.
The perception, prediction, intrusion-detection and field-monitoring notebooks use public datasets (KITTI camera
images and LiDAR scans, NGSIM trajectories, ROAD CAN-bus logs and NHTSA crash reports), downloaded on demand.

```{figure} ../assets/real-data-kitti.jpg
:alt: A KITTI frame with LiDAR points projected onto the camera image and 3D boxes around pedestrians, cyclists and cars, with the bird's-eye view of the same scan below
:width: 100%
A KITTI frame as used in the course: LiDAR points projected onto the camera image (coloured by distance) and
annotated 3D boxes for pedestrians (yellow), cyclists (teal) and cars (white); below, the same scan from above.
Data: KITTI, CC BY-NC-SA 3.0.
```

::::{grid} 1 2 2 3
:::{card} Course
:link: learning-paths
Eight modules and 50 notebooks, each with learning objectives, exercises and an *In industry* section.
:::
:::{card} Industry work products
:link: industry
HARA, FMEDA, FTA, STPA, SOTIF analysis, TARA and safety case, each mapped to the notebooks that practise it.
:::
:::{card} Teaching guide
:link: teaching
Semester and industry-training plans, assessable learning outcomes, checked exercises and a capstone rubric.
:::
:::{card} Safety case as code
:link: safety-case
The capstone's safety argument with each claim linked to its evidence and re-evaluated in CI on every change.
:::
:::{card} SOTIF perception benchmark
:link: benchmark
Detector recall on KITTI under modelled fog, low light and lens dirt, with a release verdict against a requirement.
:::
:::{card} Field-safety statistics
:link: observatory
NHTSA crash reports for ADS and Level 2 ADAS and California DMV data, refreshed monthly, with reading caveats.
:::
:::{card} Datasets and licences
:link: datasets
KITTI, NGSIM, NHTSA and ROAD, and the simulated VeReMi V2X benchmark, with their licences.
:::
:::{card} Browser edition
:link: run-in-browser
24 notebooks that run in the browser without an account or installation.
:::
:::{card} Calculators
:link: interactive-tools
ASIL, TARA, RSS and validation-mileage calculators, checked against the toolkit.
:::
:::{card} Templates
:link: ../templates/HARA_Template.md
HARA, SOTIF and TARA templates with worked examples.
:::
:::{card} Python toolkit
:link: toolkit
`avsafety`: normative tables, formulas, data loaders, benchmark and safety case as a tested package.
:::
::::

## The modules

| # | Module | You will be able to |
|---|---|---|
| 01 | [Perception and Prediction](../01_Perception/README.md) | evaluate real camera, LiDAR, fusion and tracking pipelines, and predict real trajectories with calibrated uncertainty |
| 02 | [Failures and Robustness](../02_Failures_and_Robustness/README.md) | analyse real incidents, corner cases, distribution shift and adversarial attacks |
| 03 | [Functional Safety (ISO 26262)](../03_Functional_Safety_ISO26262/README.md) | perform a HARA, FMEA/FMEDA, FTA and STPA, and plan verification |
| 04 | [SOTIF (ISO 21448)](../04_SOTIF_ISO21448/README.md) | measure triggering conditions on real data, build scenario spaces and set validation targets |
| 05 | [Cybersecurity (ISO/SAE 21434)](../05_Cybersecurity_ISO21434/README.md) | run a TARA end to end and detect attacks on real CAN-bus logs and V2X misbehaviour |
| 06 | [AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) | quantify and calibrate the uncertainty of real detectors, build conformal prediction sets, and assess end-to-end and foundation-model driving |
| 07 | [Runtime Assurance and Operations](../07_Runtime_Assurance_and_Operations/README.md) | monitor the ODD, plan safely with fallbacks, design for the human driver, and monitor the field with real crash data |
| 08 | [Standards, Regulation and Safety Case](../08_Standards_Regulation_and_Safety_Case/README.md) | connect the standards, navigate type approval, build a GSN safety case and make a release decision |

:::{tip} New here?
Start with the [learning paths](learning-paths.md), see [how the course maps to industry work](industry.md), or
open the capstone: [pedestrian AEB from requirement to release](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb).
:::
