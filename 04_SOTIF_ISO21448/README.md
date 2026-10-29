# Module 04 · SOTIF (ISO 21448)

Hazards without a fault: functional insufficiencies, triggering conditions and reasonably foreseeable misuse. Triggering conditions measured on real data, scenario spaces, OOD monitoring as a safety measure, simulation-based validation, criticality metrics and RSS, and an open SOTIF benchmark that evaluates any detector against a declared requirement.

**6 notebooks** · each runs in Google Colab on CPU; real-data notebooks download the frames and records they need on demand.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ISO 21448: Safety of the Intended Functionality (SOTIF)](01_sotif_fundamentals.ipynb) | Intermediate | ISO 21448:2022, ISO 26262:2018 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| 02 | [Triggering Conditions and Scenario-Based Evaluation](02_triggering_conditions_and_scenarios.ipynb) | Intermediate | ISO 21448:2022, ISO 34502:2022, ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb) |
| 03 | [OOD Monitoring as a SOTIF Safety Measure](03_ood_monitoring_as_safety_measure.ipynb) | Intermediate | ISO 21448:2022, ISO/PAS 8800:2024, UN R157 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb) |
| 04 | [Simulation-Based SOTIF Validation](04_simulation_based_validation.ipynb) | Advanced | ISO 21448:2022, ISO 26262-8:2018, Regulation (EU) 2022/1426 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/04_simulation_based_validation.ipynb) |
| 05 | [Criticality Metrics and Responsibility-Sensitive Safety (RSS)](05_criticality_metrics_and_rss.ipynb) | Intermediate | ISO 21448:2022, IEEE 2846-2022, UL 4600 (3rd ed., 2023), ISO 34502:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb) |
| 06 | [An Open SOTIF Perception Benchmark](06_sotif_benchmark.ipynb) | Advanced | ISO 21448:2022, ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/06_sotif_benchmark.ipynb) |

## What you will learn

### 01 · ISO 21448: Safety of the Intended Functionality (SOTIF)

- State what ISO 21448:2022 covers and what it explicitly leaves to ISO 26262 and ISO/SAE 21434
- Distinguish **triggering conditions** (in the scenario) from **functional insufficiencies** (specification and performance insufficiencies, in the system)
- Use the four scenario **Areas 1–4** correctly and explain which areas SOTIF must evaluate
- Walk through the ISO 21448:2022 activity flow from specification to the operation phase
- Turn a quantitative **acceptance criterion** into a **validation target** (required exposure)
- Explain why the 'coverage of unknown scenarios' cannot be computed, and what can be estimated instead

### 02 · Triggering Conditions and Scenario-Based Evaluation

- Build a triggering-condition catalogue structured by the PEGASUS **6-layer model** and keep out-of-scope causes apart
- Link triggering conditions to **functional insufficiencies** (specification vs performance)
- **Measure** a performance insufficiency of a real camera detector on real KITTI frames under physically based fog,
- Turn the measurement into an industry-style **triggering-condition table** with measures and an **ODD restriction**
- Use the scenario abstraction levels **functional → logical → concrete** and distinguish a scenario from the **ODD** (ISO 34503:2023)
- Describe the **ISO 34502:2022** scenario-based safety evaluation framework and the role of **ASAM OpenSCENARIO / OpenODD**
- Generate a scenario space, measure **n-wise coverage** and build a **pairwise test set** in Python
- Explain what coverage of a discretised space does — and does not — say about residual risk

### 03 · OOD Monitoring as a SOTIF Safety Measure

- Place an out-of-distribution (OOD) monitor correctly in the ISO 21448 causal chain and activity flow
- Extract runtime monitor signals from a **real detector** (scores, entropy, low-confidence boxes, energy, backbone
- Set a monitor threshold **from a safety requirement** instead of an arbitrary percentile, and check it on held-out frames
- Convert a false-positive rate into **false alarms per hour**, state what a small clean sample can and cannot show,
- Treat the TPR/FPR trade-off as a **safety vs availability** decision and document it
- Choose a fallback that fits the **level of automation** (L2 warning, L3 transition demand, L4 minimal risk manoeuvre)
- State the limits: OOD is not the same as hazardous, and the monitor needs its own validation

### 04 · Simulation-Based SOTIF Validation

- Explain the role of simulation in the evaluation of known and unknown scenarios (ISO 21448 clauses 10–11)
- Structure a simulation campaign over weather and time of day, following the author's CARLA-based SOTIF use case
- Trace perception metrics to vehicle-level acceptance criteria instead of treating AP thresholds as 'ISO criteria'
- Assess **simulation credibility**: sim-to-real gap, tool confidence (ISO 26262-8), credibility assessment of virtual toolchains
- Estimate a rare failure probability with **importance sampling** and compare it with naive Monte Carlo
- Distinguish **coverage-oriented** from **distribution-oriented** scenario sampling

### 05 · Criticality Metrics and Responsibility-Sensitive Safety (RSS)

- Define and compute the surrogate safety (criticality) metrics **TTC, THW, DRAC, required deceleration and PET**, and state the assumptions behind each.
- Recognise the **failure modes** of these metrics (e.g. TTC is infinite when the vehicles are not closing; longitudinal metrics are blind to lateral conflicts).
- **Derive** the RSS minimum safe longitudinal distance from its worst-case assumptions and implement it exactly as in the paper.
- Explain RSS's notions of **dangerous situation, proper response and responsibility**, including the lateral case.
- Quantify the **sensitivity** of the RSS envelope to its parameters and the resulting **safety–usefulness trade-off**.
- Simulate a **cut-in** and compare an RSS-compliant controller with a naive one using metrics over time.
- Position such safety envelopes in **ISO 21448**, **IEEE 2846-2022** and **UL 4600** arguments, and state their limitations.

### 06 · An Open SOTIF Perception Benchmark

- Evaluate **any** camera detector against a fixed, versioned SOTIF benchmark in one call, and read the resulting
- Explain each design choice of the benchmark — frame rule, population, matching, conditions, threshold policy —
- Turn the report into a **verdict against a declared requirement**, a **supported speed per condition** (ODD
- Compare detectors fairly and recognise when a difference is inside the statistical noise
- State what a benchmark of synthetic conditions on real images can and cannot claim, and how a company would run
- Describe how the LiDAR track on SOTIF-PCOD adds weather and illumination conditions for LiDAR detectors

---

← [Module 03 · Functional Safety (ISO 26262)](../03_Functional_Safety_ISO26262/README.md) · [Course home](../README.md) · [Module 05 · Cybersecurity (ISO/SAE 21434)](../05_Cybersecurity_ISO21434/README.md) →
