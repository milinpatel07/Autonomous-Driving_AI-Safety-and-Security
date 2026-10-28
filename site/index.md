---
title: "Autonomous Driving: AI Safety and Security"
short_title: Home
---

+++ {"kind": "split-image"}

## An open course from sensors to safety cases

Forty runnable notebooks that take you from **how an automated vehicle perceives the world** to **how you argue that it is safe and secure enough to deploy**: perception, failure analysis, ISO 26262, ISO 21448 (SOTIF), ISO/SAE 21434, ISO/PAS 8800, runtime assurance, regulation and safety cases.

Every notebook runs in Google Colab with one click, needs no GPU and no dataset download, and comes with exercises, self-assessment questions and verified references.

```{image} ../assets/banner.svg
:alt: Course map from perception to safety case
```

+++

::::{grid} 1 2 2 4
:::{card} 40 notebooks
:link: learning-paths
Eight modules, beginner to advanced, each with learning objectives and exercises.
:::
:::{card} Interactive tools
:link: tools
ASIL, TARA, RSS and validation-mileage calculators that run on your phone.
:::
:::{card} Professional templates
:link: ../templates/HARA_Template.md
HARA, SOTIF and TARA templates with worked examples.
:::
:::{card} Tested toolkit
:link: toolkit
`avsafety`: the normative tables and formulas as a pip-installable, unit-tested package.
:::
::::

## The modules

| # | Module | You will be able to |
|---|---|---|
| 01 | [Perception Systems](../01_Perception/README.md) | explain sensors, detection, fusion and tracking, and where perception can fail |
| 02 | [Failures and Robustness](../02_Failures_and_Robustness/README.md) | analyse real incidents, corner cases, distribution shift and adversarial attacks |
| 03 | [Functional Safety (ISO 26262)](../03_Functional_Safety_ISO26262/README.md) | perform a HARA, FMEA/FMEDA and FTA, and plan verification |
| 04 | [SOTIF (ISO 21448)](../04_SOTIF_ISO21448/README.md) | identify triggering conditions, build scenario spaces and set validation targets |
| 05 | [Cybersecurity (ISO/SAE 21434)](../05_Cybersecurity_ISO21434/README.md) | run a TARA end to end and detect attacks on the CAN bus |
| 06 | [AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) | quantify, calibrate and guarantee uncertainty, and validate ML statistically |
| 07 | [Runtime Assurance and Operations](../07_Runtime_Assurance_and_Operations/README.md) | monitor the ODD at runtime, use V2X safely and read the deployment landscape |
| 08 | [Standards, Regulation and Safety Case](../08_Standards_Regulation_and_Safety_Case/README.md) | connect the standards, navigate type approval and build a GSN safety case |

:::{tip} New here?
Start with the [learning paths](learning-paths.md), or open the very first notebook in Colab:
[SAE levels and the ODD](../01_Perception/01_sae_levels_and_odd.ipynb).
:::
