---
title: Learning paths
---

Pick the route that matches your goal. Each path is an order of notebooks, not a schedule: go as deep as your
work needs. Notebook numbers are module-notebook, e.g. 03-02 is the HARA notebook in Module 03.

::::{grid} 1 1 2 2

:::{card} Complete course
All eight modules in order, 01 → 08, ending with the capstone 08-05. For students and for engineers new to AV safety.
:::

:::{card} Functional safety engineer
03-01 → 03-02 HARA → 03-03 FMEA/FMEDA → 03-04 FTA → 03-05 STPA → 03-06 V&V → 08-04 Safety case → 08-05 Capstone.
:::

:::{card} SOTIF / perception safety engineer
01-04 Detection → 01-05 VRU → 04-01 SOTIF → 04-02 Triggering conditions (real data) → 04-03 OOD monitoring →
04-05 RSS → 06-08 Statistical validation.
:::

:::{card} ML / perception engineer
01-02 → 01-03 LiDAR → 01-04 Detection → 01-06 Fusion → 01-07 Tracking → 01-09 Prediction → 06-02 – 06-05
Uncertainty, calibration, conformal → 06-07 End-to-end and foundation models.
:::

:::{card} Security engineer
05-01 → 05-02 TARA → 05-03 Attack surface → 05-04 CAN intrusion detection → 02-04 Adversarial attacks →
07-04 V2X → 08-01 Standards integration.
:::

:::{card} Validation and operations
04-02 → 04-04 Simulation → 06-08 Statistical validation → 07-01 ODD monitoring → 07-02 Safe planning and fallback →
07-03 Human factors → 07-05 Field monitoring (NHTSA data).
:::

:::{card} Manager, assessor, regulator
01-01 SAE levels and ODD → 02-01 Incident case studies → 08-01 Standards integration → 08-02 Regulation →
07-05 Field monitoring → 08-04 Safety case → 08-05 Capstone.
:::

:::{card} Short introduction
01-01 SAE levels and ODD → 03-02 HARA → 08-05 Capstone, plus the [interactive tools](interactive-tools.md).
:::
::::

## Prerequisites

- Python basics (NumPy, pandas, Matplotlib). Every notebook explains its code.
- No GPU and no local install: use the **Open in Colab** badge at the top of each notebook. Real-data notebooks
  install the course toolkit and download the frames they need automatically.
- Standards are paywalled; the notebooks explain their concepts and cite clause numbers so that you can follow up
  with the official texts. See also the [industry map](industry.md).
