# Module 04 · SOTIF (ISO 21448)

Hazards without a fault: functional insufficiencies, triggering conditions and reasonably foreseeable misuse. Scenario spaces, OOD monitoring as a safety measure, simulation-based validation, criticality metrics and RSS.

**5 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Time | Open |
|---|---|---|---|---|
| 01 | [ISO 21448: Safety of the Intended Functionality (SOTIF)](01_sotif_fundamentals.ipynb) | Intermediate | ~60 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| 02 | [Triggering Conditions and Scenario-Based Evaluation](02_triggering_conditions_and_scenarios.ipynb) | Intermediate | ~75 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb) |
| 03 | [OOD Monitoring as a SOTIF Safety Measure](03_ood_monitoring_as_safety_measure.ipynb) | Intermediate | ~60 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb) |
| 04 | [Simulation-Based SOTIF Validation](04_simulation_based_validation.ipynb) | Advanced | ~75 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/04_simulation_based_validation.ipynb) |
| 05 | [Criticality Metrics and Responsibility-Sensitive Safety (RSS)](05_criticality_metrics_and_rss.ipynb) | Intermediate | ~75 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb) |

## What you will learn

### 01 · ISO 21448: Safety of the Intended Functionality (SOTIF)

*Standards:* ISO 21448:2022, ISO 26262:2018

- State what ISO 21448:2022 covers and what it explicitly leaves to ISO 26262 and ISO/SAE 21434
- Distinguish **triggering conditions** (in the scenario) from **functional insufficiencies** (specification and performance insufficiencies, in the system)
- Use the four scenario **Areas 1–4** correctly and explain which areas SOTIF must evaluate
- Walk through the ISO 21448:2022 activity flow from specification to the operation phase
- Turn a quantitative **acceptance criterion** into a **validation target** (required exposure)
- Explain why the 'coverage of unknown scenarios' cannot be computed, and what can be estimated instead

### 02 · Triggering Conditions and Scenario-Based Evaluation

*Standards:* ISO 21448:2022, ISO 34502:2022, ISO 34503:2023

- Build a triggering-condition catalogue structured by the PEGASUS **6-layer model** and keep out-of-scope causes apart
- Link triggering conditions to **functional insufficiencies** (specification vs performance)
- Use the scenario abstraction levels **functional → logical → concrete** and distinguish a scenario from the **ODD** (ISO 34503:2023)
- Describe the **ISO 34502:2022** scenario-based safety evaluation framework and the role of **ASAM OpenSCENARIO / OpenODD**
- Generate a scenario space, measure **n-wise coverage** and build a **pairwise test set** in Python
- Explain what coverage of a discretised space does — and does not — say about residual risk

### 03 · OOD Monitoring as a SOTIF Safety Measure

*Standards:* ISO 21448:2022, ISO/PAS 8800:2024, UN R157

- Place an out-of-distribution (OOD) monitor correctly in the ISO 21448 causal chain and activity flow
- Set a monitor threshold **from a safety requirement** instead of an arbitrary percentile
- Convert a false-positive rate into **false alarms per hour** and design a temporal filter
- Treat the TPR/FPR trade-off as a **safety vs availability** decision and document it
- Choose a fallback that fits the **level of automation** (L2 warning, L3 transition demand, L4 minimal risk manoeuvre)
- State the limits: OOD is not the same as hazardous, and the monitor needs its own validation

### 04 · Simulation-Based SOTIF Validation

*Standards:* ISO 21448:2022, ISO 26262-8:2018, Regulation (EU) 2022/1426

- Explain the role of simulation in the evaluation of known and unknown scenarios (ISO 21448 clauses 10–11)
- Structure a simulation campaign over weather and time of day, following the author's CARLA-based SOTIF use case
- Trace perception metrics to vehicle-level acceptance criteria instead of treating AP thresholds as 'ISO criteria'
- Assess **simulation credibility**: sim-to-real gap, tool confidence (ISO 26262-8), credibility assessment of virtual toolchains
- Estimate a rare failure probability with **importance sampling** and compare it with naive Monte Carlo
- Distinguish **coverage-oriented** from **distribution-oriented** scenario sampling

### 05 · Criticality Metrics and Responsibility-Sensitive Safety (RSS)

*Standards:* ISO 21448:2022, IEEE 2846-2022, UL 4600 (3rd ed., 2023), ISO 34502:2022

- Define and compute the surrogate safety (criticality) metrics **TTC, THW, DRAC, required deceleration and PET**, and state the assumptions behind each.
- Recognise the **failure modes** of these metrics (e.g. TTC is infinite when the vehicles are not closing; longitudinal metrics are blind to lateral conflicts).
- **Derive** the RSS minimum safe longitudinal distance from its worst-case assumptions and implement it exactly as in the paper.
- Explain RSS's notions of **dangerous situation, proper response and responsibility**, including the lateral case.
- Quantify the **sensitivity** of the RSS envelope to its parameters and the resulting **safety–usefulness trade-off**.
- Simulate a **cut-in** and compare an RSS-compliant controller with a naive one using metrics over time.
- Position such safety envelopes in **ISO 21448**, **IEEE 2846-2022** and **UL 4600** arguments, and state their limitations.

---

← [Module 03 · Functional Safety (ISO 26262)](../03_Functional_Safety_ISO26262/README.md) · [Course home](../README.md) · [Module 05 · Cybersecurity (ISO/SAE 21434)](../05_Cybersecurity_ISO21434/README.md) →
