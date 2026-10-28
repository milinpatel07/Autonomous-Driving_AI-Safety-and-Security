# Module 05 · Cybersecurity (ISO/SAE 21434)

Protecting the vehicle over its lifecycle: the ISO/SAE 21434 framework, threat analysis and risk assessment (TARA), attack surfaces and hands-on intrusion detection on the CAN bus.

**4 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ISO/SAE 21434: Automotive Cybersecurity Engineering](01_iso21434_fundamentals.ipynb) | Beginner | ISO/SAE 21434:2021, UN R155, UN R156 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 02 | [Threat Analysis and Risk Assessment (TARA)](02_tara.ipynb) | Intermediate | ISO/SAE 21434:2021 (cl. 9, 15; Annexes E–H), ISO 26262-3:2018 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/02_tara.ipynb) |
| 03 | [Attack Surface Analysis for Autonomous Vehicles](03_attack_surface_analysis.ipynb) | Intermediate | ISO/SAE 21434:2021 (cl. 15.6, Annex G), CVSS v3.1, ISO 14229-1:2020, IEEE 1609.2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| 04 | [CAN Bus Security and Intrusion Detection](04_can_bus_intrusion_detection.ipynb) | Advanced | ISO/SAE 21434:2021, UN R155, ISO 11898-1:2024, AUTOSAR SecOC | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb) |

## What you will learn

### 01 · ISO/SAE 21434: Automotive Cybersecurity Engineering

- Explain the scope and lifecycle of ISO/SAE 21434:2021 and name its clause structure (clauses 5–15).
- List the seven TARA steps of clause 15 in the correct order.
- Apply the informative rating tables: impact (Severe/Major/Moderate/Negligible), attack feasibility (attack-potential and attack-vector based), the example risk matrix (risk value 1–5) and the example CAL table.
- Explain why a CAL is **not** a risk measure and **not** an ASIL equivalent.
- Place ISO/SAE 21434 next to UN R155/R156, ISO/SAE PAS 5112, ISO 24089 and the EU Cyber Resilience Act.

### 02 · Threat Analysis and Risk Assessment (TARA)

- perform all seven TARA steps of ISO/SAE 21434 clause 15 for a perception-based AEB function, in the order of the standard;
- formulate threat scenarios as *asset + cybersecurity property + cause* and link them to damage scenarios;
- build attack paths, aggregate them (AND/OR) and rate attack feasibility with the attack-potential approach;
- derive risk values, treatment decisions, cybersecurity goals/claims and CALs **programmatically**, so that every number is traceable;
- connect the TARA to the HARA of Module 03 (safety–security co-engineering), including timing of security controls against the FTTI.

### 03 · Attack Surface Analysis for Autonomous Vehicles

- Enumerate the attack surfaces of an automated vehicle and classify them by attack vector (Network, Adjacent, Local, Physical).
- Build an attack tree with AND/OR aggregation and find the most feasible attack path (ISO/SAE 21434 cl. 15.6 → 15.7).
- Apply defence in depth and map security controls to attack surfaces, distinguishing link integrity from physical-world sensor attacks.
- Compute real CVSS v3.1 base scores and map the exploitability sub-score to attack feasibility (Annex G.3).
- Understand the principle and limits of a timing-based CAN intrusion detector.

### 04 · CAN Bus Security and Intrusion Detection

- Explain the CAN 2.0 frame format, bitwise arbitration and the three properties that make the bus hard to defend: **broadcast**, **priority by identifier** and **no sender authentication**.
- Generate realistic synthetic CAN traffic (per-ECU clocks, jitter, event-driven frames, counters and checksums) so that a *known-ground-truth* stream is available for testing detectors.
- Implement three families of intrusion detection from first principles — **timing/frequency**, **payload/semantic plausibility** and **unsupervised ML** (Isolation Forest, identifier entropy) — plus a clock-skew fingerprint in the spirit of CIDS.
- Evaluate detectors the way a vehicle programme must: precision/recall/F1, ROC, **detection latency** and **false alarms per hour of driving**.
- Quantify the cost of prevention with AUTOSAR SecOC (truncated MAC, freshness value) on classic CAN versus CAN FD, and relate the analysis to an ISO/SAE 21434 TARA and the UN R155 Annex 5 threat list.

---

← [Module 04 · SOTIF (ISO 21448)](../04_SOTIF_ISO21448/README.md) · [Course home](../README.md) · [Module 06 · AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) →
