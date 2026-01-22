# Module 04: SOTIF - ISO 21448

How do we handle performance limitations and unknown scenarios?

SOTIF (Safety of the Intended Functionality) addresses safety risks from performance limitations and unknown scenarios - especially critical for AI-based systems.

---

## What's in This Module

**3 notebooks covering:**
- SOTIF fundamentals and motivation
- Known/unknown safe/unsafe scenarios (4-quadrant model)
- Triggering conditions and scenario analysis
- Out-of-Distribution detection for SOTIF
- Validation strategies for AI systems

---

## Notebooks

### 01. SOTIF Fundamentals
**[01_sotif_fundamentals.ipynb](notebooks/01_sotif_fundamentals.ipynb)**

Introduction to ISO 21448:
- Why SOTIF complements ISO 26262
- The 4-quadrant model
- Basic triggering conditions
- Integration with functional safety

### 02. Scenario Analysis and Triggering Conditions
**[02_scenario_analysis.ipynb](notebooks/02_scenario_analysis.ipynb)**

Detailed scenario-based SOTIF analysis:
- Systematic triggering condition identification
- Functional insufficiencies for perception
- Scenario generation methodologies
- Scenario classification into quadrants
- Validation pyramid approach

### 03. OOD Detection for SOTIF
**[03_ood_detection_sotif.ipynb](notebooks/03_ood_detection_sotif.ipynb)**

Out-of-Distribution detection as SOTIF support:
- OOD detection role in safety lifecycle
- Mahalanobis distance method
- k-NN based detection
- Energy-based detection
- Runtime monitoring implementation
- Based on Patel et al. (2023) REFSQ paper

---

## Why This Matters

**ISO 26262 isn't enough for AI systems:**
- ISO 26262 handles random/systematic failures (broken sensor, software bug)
- SOTIF handles performance limitations (fog, unusual object, edge case)
- AI perception has inherent limitations - can't handle all scenarios
- Need systematic approach to find unknown unsafe scenarios

**Key concepts:**
- Known safe: System performs correctly, validated
- Known unsafe: Identified limitations, mitigated or restricted (ODD)
- Unknown unsafe: The dangerous unknown - what SOTIF aims to discover
- Goal: Move unknown unsafe → known unsafe → known safe

---

## Prerequisites

**Required:**
- Perception systems (Module 01)
- Failure analysis concepts (Module 02)
- ISO 26262 basics (Module 03)

**Helpful:**
- Scenario-based testing concepts
- Statistics and probability

---

## After This Module

Continue to:
- **Module 06 (AI Safety)** - Uncertainty quantification for unknown scenario detection
- **Module 08 (Advanced Topics)** - Runtime ODD monitoring and fallback strategies
- **Module 02 (Failure Analysis)** - OOD detection as SOTIF implementation

---

## Note on Content

This module provides foundational SOTIF coverage. Advanced topics (detailed scenario catalogs, quantitative SOTIF metrics, field monitoring strategies) will be added in future releases.

For now, focus on understanding:
- Why SOTIF is essential for AI systems
- The 4-quadrant scenario model
- How SOTIF complements ISO 26262

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
