# Module 04: SOTIF - ISO 21448

How do we handle performance limitations and unknown scenarios?

SOTIF (Safety of the Intended Functionality) addresses safety risks from performance limitations and unknown scenarios - especially critical for AI-based systems.

---

## What's in This Module

**1 notebook covering:**
- SOTIF fundamentals and motivation
- Known/unknown safe/unsafe scenarios
- Performance limitation analysis
- Validation strategies for AI systems

---

## Notebook

### SOTIF Fundamentals
**[01_sotif_fundamentals.ipynb](notebooks/01_sotif_fundamentals.ipynb)**

Learn ISO 21448 (SOTIF):
- Why SOTIF complements ISO 26262
- The 4-quadrant model: Known/Unknown × Safe/Unsafe scenarios
- Triggering conditions and performance limitations
- Systematic scenario identification
- Validation approaches for AI perception
- Integration with functional safety

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
