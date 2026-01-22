# Module 03: Functional Safety - ISO 26262

How do we systematically ensure safety in autonomous vehicles?

This module introduces ISO 26262, the international standard for functional safety in automotive systems.

---

## What's in This Module

**2 notebooks covering:**
- ISO 26262 fundamentals and structure
- V-Model development lifecycle
- ASIL (Automotive Safety Integrity Levels)
- Hazard Analysis and Risk Assessment (HARA)
- Safety lifecycle and management

---

## Notebooks

### 01. ISO 26262 Fundamentals
**[01_iso_26262_fundamentals.ipynb](notebooks/01_iso_26262_fundamentals.ipynb)**

Learn the basics of ISO 26262:
- Standard structure (Parts 1-12)
- V-Model development lifecycle
- ASIL levels (A, B, C, D, QM)
- Safety goals and requirements

### 02. HARA Methodology
**[02_hara_methodology.ipynb](notebooks/02_hara_methodology.ipynb)**

Detailed Hazard Analysis and Risk Assessment:
- HARA process step-by-step
- Severity, Exposure, Controllability classification
- ASIL determination from S, E, C
- Safety goal derivation
- Practical examples for perception systems
- Interactive HARA worksheet tool

---

## Why This Matters

**ISO 26262 is mandatory for automotive safety:**
- Defines how to systematically manage safety throughout development
- ASIL-D (highest level) required for critical functions like pedestrian detection
- V-Model ensures verification at every development stage
- Required for regulatory approval and certification

**Key concepts:**
- Severity, Exposure, Controllability → ASIL level
- Safety goals translate hazards into requirements
- Functional safety complements SOTIF (ISO 21448)

---

## Prerequisites

**Required:**
- Basic automotive systems knowledge
- Understanding of perception systems (Module 01)
- Systems engineering basics

**Helpful:**
- Probability and statistics
- Risk analysis concepts

---

## After This Module

Continue to:
- **Module 04 (SOTIF)** - Handle performance limitations and unknown scenarios
- **Module 05 (Cybersecurity)** - Integrate safety and security (ISO/SAE 21434)
- **Module 06 (AI Safety)** - Apply safety concepts to AI/ML systems

---

## Note on Content

This module provides foundational coverage of ISO 26262. Advanced topics (detailed HARA, ASIL decomposition, safety case development) will be added in future releases.

For now, focus on understanding:
- Why functional safety matters
- How ASIL levels are determined
- How ISO 26262 integrates with perception systems

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
