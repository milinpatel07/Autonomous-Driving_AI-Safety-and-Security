---
title: "Autonomous Driving: AI Safety and Security"
short_title: Home
---

```{image} ../assets/banner.svg
:alt: Course map from perception to safety case
:width: 100%
```

## An open course from sensors to safety cases

Fifty runnable notebooks take you from **how an automated vehicle perceives and predicts the world** to
**how you argue that it is safe and secure enough to deploy**: perception and prediction, failure analysis,
ISO 26262, ISO 21448 (SOTIF), ISO/SAE 21434, ISO/PAS 8800, runtime assurance, regulation and safety cases.

Every notebook runs in Google Colab with one click and needs no GPU, and 24 of them [run in your browser](run-in-browser.md)
with no account. Perception, prediction, security and field-safety notebooks use **real public data** — KITTI camera
images and LiDAR scans, NGSIM highway trajectories, real CAN-bus attack logs and NHTSA crash reports — downloaded on
demand, a few files at a time.

```{figure} ../assets/real-data-kitti.jpg
:alt: A real KITTI frame with LiDAR points projected onto the camera image and 3D boxes around pedestrians, cyclists and cars, with the bird's-eye view of the same scan below
:width: 100%
A real KITTI frame as used in the course: LiDAR points projected onto the camera image (coloured by distance) and
annotated 3D boxes for pedestrians (yellow), cyclists (teal) and cars (white); below, the same scan from above.
Data: KITTI, CC BY-NC-SA 3.0.
```

::::{grid} 1 2 2 3
:::{card} 50 notebooks
:link: learning-paths
Eight modules, beginner to advanced, each with learning objectives, exercises and an *In industry* section.
:::
:::{card} A safety case that updates itself
:link: safety-case
The capstone's safety argument as code: every claim linked to its evidence and re-checked by CI on each change.
:::
:::{card} Open SOTIF benchmark
:link: benchmark
Rate any detector under fog, low light and lens dirt on real KITTI frames, with a release verdict.
:::
:::{card} Field safety observatory
:link: observatory
Monthly NHTSA crash reports for ADS and Level 2 ADAS, California disengagements and published exposure, with caveats.
:::
:::{card} Run in your browser
:link: run-in-browser
No login, no installation, nothing leaves your device; works where Colab is blocked.
:::
:::{card} For instructors
:link: teaching
Semester and industry-training plans, assessable outcomes, auto-checked exercises and a capstone rubric.
:::
:::{card} Real data
:link: datasets
KITTI, NGSIM, NHTSA and ROAD CAN data, plus the simulated VeReMi V2X benchmark, loaded by the course toolkit with licences stated.
:::
:::{card} For industry
:link: industry
Every work product — HARA, FMEDA, FTA, STPA, SOTIF analysis, TARA, safety case — mapped to notebooks.
:::
:::{card} Interactive tools
:link: interactive-tools
ASIL, TARA, RSS and validation-mileage calculators that run on your phone.
:::
:::{card} Professional templates
:link: ../templates/HARA_Template.md
HARA, SOTIF and TARA templates with worked examples.
:::
:::{card} Tested toolkit
:link: toolkit
`avsafety`: normative tables, formulas and real-data loaders as a pip-installable, unit-tested package.
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
| 06 | [AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) | quantify, calibrate and guarantee uncertainty of real detectors, and judge end-to-end and foundation-model driving |
| 07 | [Runtime Assurance and Operations](../07_Runtime_Assurance_and_Operations/README.md) | monitor the ODD, plan safely with fallbacks, design for the human driver, and monitor the field with real crash data |
| 08 | [Standards, Regulation and Safety Case](../08_Standards_Regulation_and_Safety_Case/README.md) | connect the standards, navigate type approval, build a GSN safety case and make a release decision |

:::{tip} New here?
Start with the [learning paths](learning-paths.md), see [how the course maps to industry work](industry.md), or
open the capstone: [pedestrian AEB from requirement to release](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb).
:::
