# Module 05: Cybersecurity - ISO/SAE 21434

How do we protect autonomous vehicles from malicious actors?

This module introduces ISO/SAE 21434, the automotive cybersecurity standard, and explores threats specific to autonomous driving systems.

---

## What's in This Module

**1 notebook covering:**
- Automotive cybersecurity landscape
- ISO/SAE 21434 fundamentals
- Threat Analysis and Risk Assessment (TARA)
- Attack vectors for autonomous vehicles

---

## Notebook

### Automotive Cybersecurity
**[01_automotive_cybersecurity.ipynb](notebooks/01_automotive_cybersecurity.ipynb)**

Learn ISO/SAE 21434 basics:
- Why cybersecurity matters for safety
- Threat landscape: V2X attacks, sensor spoofing, GPS spoofing
- TARA (Threat Analysis and Risk Assessment) methodology
- Attack vectors specific to perception systems
- LiDAR jamming and camera dazzling
- Secure development lifecycle
- Integration with ISO 26262 (safety-security co-analysis)

---

## Why This Matters

**Cyberattacks can cause safety hazards:**
- Adversarial patches can fool object detection
- GPS spoofing can cause localization errors
- V2X message injection can trigger false emergency braking
- Sensor jamming (LiDAR, radar) creates blind spots
- Remote attacks via OTA updates or connected services

**ISO/SAE 21434 requirements:**
- Systematic threat modeling
- Risk assessment and mitigation
- Secure development processes
- Cybersecurity validation and testing

---

## Prerequisites

**Required:**
- Perception systems (Module 01)
- Basic cybersecurity concepts
- Understanding of adversarial attacks (Module 02)

**Helpful:**
- Network security basics
- Cryptography fundamentals

---

## After This Module

Continue to:
- **Module 02 (Failure Analysis)** - Deep dive into adversarial attacks on perception
- **Module 08 (Advanced Topics)** - V2X communication security
- **Module 06 (AI Safety)** - Adversarial robustness for AI systems

---

## Note on Content

This module provides foundational cybersecurity coverage. Advanced topics (detailed TARA, cryptographic implementations, secure OTA updates) will be added in future releases.

For now, focus on understanding:
- Cybersecurity threats to autonomous vehicles
- How attacks can compromise safety
- TARA methodology basics

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
