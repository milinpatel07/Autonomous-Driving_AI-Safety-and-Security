# Module 05 · Cybersecurity (ISO/SAE 21434)

Protecting the vehicle over its lifecycle: the ISO/SAE 21434 framework, threat analysis and risk assessment (TARA), attack surfaces, intrusion detection on real CAN-bus attack logs and misbehaviour detection on V2X benchmark data.

**5 notebooks** · each runs in Google Colab on CPU; real-data notebooks download the frames and records they need on demand.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ISO/SAE 21434: Automotive Cybersecurity Engineering](01_iso21434_fundamentals.ipynb) | Beginner | ISO/SAE 21434:2021, UN R155, UN R156 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 02 | [Threat Analysis and Risk Assessment (TARA)](02_tara.ipynb) | Intermediate | ISO/SAE 21434:2021 (cl. 9, 15; Annexes E–H), ISO 26262-3:2018 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/02_tara.ipynb) |
| 03 | [Attack Surface Analysis for Autonomous Vehicles](03_attack_surface_analysis.ipynb) | Intermediate | ISO/SAE 21434:2021 (cl. 15.6, Annex G), CVSS v3.1, ISO 14229-1:2020, IEEE 1609.2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| 04 | [CAN Bus Security and Intrusion Detection](04_can_bus_intrusion_detection.ipynb) | Advanced | ISO/SAE 21434:2021, UN R155, ISO 11898-1:2024, AUTOSAR SecOC | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb) |
| 05 | [V2X Misbehaviour Detection](05_v2x_misbehaviour_detection.ipynb) | Advanced | ISO/SAE 21434:2021, UN R155, ETSI TS 103 759, ETSI TR 103 460, ETSI TS 103 097, IEEE 1609.2-2022, ETSI EN 302 637-2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) |

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
- Load and inspect **real in-vehicle CAN traffic with physically verified attacks** (the ROAD dataset of Oak Ridge National Laboratory) and reconstruct frame-level ground truth from the published metadata.
- Implement and tune four intrusion detectors — **per-identifier frequency**, **identifier entropy**, **signal-level payload plausibility** and a **learned window classifier** — on benign training traffic only, or with an honest capture-level split.
- Evaluate them per attack type (fuzzing, targeted injection, masquerade) the way a vehicle programme must: **detection rate, detection delay and false alarms per hour**, including a confidence bound when no false alarm is observed.
- Quantify the cost of prevention with AUTOSAR SecOC on the real bus, and answer the questions an ISO/SAE 21434 / UN R155 reviewer asks about an intrusion-detection claim.

### 05 · V2X Misbehaviour Detection

- Explain why a correctly **signed** V2X message can still be **false**, and how falsified position or speed reaches cooperative perception and an AEB function.
- Load the **VeReMi Extension** benchmark (simulated, with labelled attacks), and state what simulation-based benchmark data can and cannot show.
- Implement the classic local plausibility checks — acceptance range (ART), sudden appearance (SAW), speed plausibility, position–speed consistency, beacon frequency and a **Kalman-filter** consistency test — and a **learned** detector built on them.
- Evaluate detectors per attack type with a **time-separated** split: detection per attacker, false-positive rate per genuine sender, detection latency and compute cost.
- Show what **on-board sensor cross-checks** add for attacks that are internally consistent, and place local detection in the ETSI misbehaviour-reporting chain and in the TARA of [notebook 2](02_tara.ipynb).

---

← [Module 04 · SOTIF (ISO 21448)](../04_SOTIF_ISO21448/README.md) · [Course home](../README.md) · [Module 06 · AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) →
