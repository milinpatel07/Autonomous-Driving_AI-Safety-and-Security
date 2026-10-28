# Module 03 · Functional Safety (ISO 26262)

Hazards caused by malfunctioning E/E systems: the ISO 26262 lifecycle, hazard analysis and risk assessment (HARA), FMEA/FMEDA and hardware metrics, fault tree analysis, system-theoretic process analysis (STPA), and verification and validation.

**6 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ISO 26262: Functional Safety for Road Vehicles](01_iso26262_fundamentals.ipynb) | Beginner | ISO 26262:2018 (Parts 1–6, 9) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb) |
| 02 | [Hazard Analysis and Risk Assessment (HARA)](02_hara.ipynb) | Intermediate | ISO 26262-3:2018, ISO 26262-9:2018 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/02_hara.ipynb) |
| 03 | [FMEA and FMEDA for Perception Hardware and Software](03_fmea_and_fmeda.ipynb) | Intermediate | ISO 26262-5:2018, ISO 26262-9:2018, AIAG & VDA FMEA Handbook (2019) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) |
| 04 | [Fault Tree Analysis (FTA) and Dependent Failures](04_fault_tree_analysis.ipynb) | Intermediate | ISO 26262-9:2018, ISO 26262-5:2018, IEC 61025:2006 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb) |
| 05 | [STPA: System-Theoretic Process Analysis](05_stpa.ipynb) | Intermediate | ISO 26262:2018, ISO 21448:2022, SAE J3187 (2023), UN R157 (01 series) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 06 | [Verification and Validation for Functional Safety](06_verification_and_validation.ipynb) | Intermediate | ISO 26262-4:2018, ISO 26262-6:2018, ISO 26262-2:2018 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |

## What you will learn

### 01 · ISO 26262: Functional Safety for Road Vehicles

- Describe the structure and key concepts of ISO 26262:2018
- Outline the V-model and where each safety activity sits in it
- Classify hazardous events by Severity, Exposure and Controllability and determine the ASIL with ISO 26262-3 Table 4
- Explain what a HARA rates (vehicle-level malfunctioning behaviour) and what it does not (causes, safety mechanisms)
- Separate ISO 26262 from ISO 21448 (SOTIF) and ISO/PAS 8800 for an AI-based perception function
- Distinguish verification, safety validation and confirmation measures

### 02 · Hazard Analysis and Risk Assessment (HARA)

- Carry out the HARA steps of ISO 26262-3 (clause 6) for an automated emergency braking (AEB) function
- Write an item definition at vehicle level and build an operational-situation catalogue with exposure rationale
- Formulate hazards as vehicle-level malfunctioning behaviours, independent of their cause
- Classify S, E and C with the wording of the standard and a written rationale, and determine the ASIL
- Derive vehicle-level safety goals with safe states and FTTI, and check a mechanism's FDTI + FRTI against the FTTI
- Apply ASIL decomposition (D → B(D) + B(D)) and state the independence it requires

### 03 · FMEA and FMEDA for Perception Hardware and Software

- Place FMEA and FMEDA within ISO 26262 (inductive safety analysis; hardware metrics)
- Build a design FMEA for a camera perception channel and trace failure effects to the HARA safety goals
- Explain the pitfalls of the Risk Priority Number and apply the AIAG-VDA Action Priority (AP) lookup
- Compute SPFM, LFM and a first-order PMHF estimate from an FMEDA, including latent-fault coverage
- Recognise which perception 'failure modes' are really SOTIF / ISO/PAS 8800 insufficiencies

### 04 · Fault Tree Analysis (FTA) and Dependent Failures

- Distinguish **deductive** (top-down, FTA) from **inductive** (bottom-up, FMEA) safety analyses and place both within ISO 26262-9:2018 clause 8.
- Read and draw the standard **fault tree symbols** and manipulate fault trees with **Boolean algebra**.
- Build a fault tree for the AEB top event *"unintended full braking"* and compute its **minimal cut sets** with the MOCUS algorithm.
- Quantify the top event **exactly**, with the **rare-event approximation**, and with a **Monte Carlo** check, starting from failure rates in FIT.
- Rank basic events with **Birnbaum** and **Fussell–Vesely** importance measures.
- Explain why **ASIL decomposition** (e.g. D → B(D) + B(D)) only works with **independence**, and quantify how **common-cause failures** (beta-factor model) erode redundancy.
- Recognise where FTA reaches its limits for **machine-learning components**, whose performance insufficiencies have no meaningful failure rate.

### 05 · STPA: System-Theoretic Process Analysis

- Explain why accidents with automated vehicles often involve **unsafe interactions** between components that have not failed, and why this calls for a control-theoretic analysis in addition to FMEA, FTA and HARA.
- Carry out the four steps of STPA (Leveson & Thomas, 2018): losses, hazards and system-level constraints; control structure; unsafe control actions (UCAs) of the four types; loss scenarios.
- Model the control structure of a **Level 3 motorway chauffeur** (ALKS-like, UN R157) with driver, ADS, HMI, vehicle and the AEB item as a graph, and check it for missing feedback.
- Generate a UCA table **systematically**, with an explicit decision for every combination of control action, UCA type and context, and derive controller constraints.
- Derive loss scenarios, including **mode confusion** and **takeover** failures, and turn them into requirements.
- State what STPA finds that HARA and FTA do not (and the reverse), extend the analysis to security with **STPA-Sec**, and place STPA relative to ISO 26262, ISO 21448 and SAE J3187.

### 06 · Verification and Validation for Functional Safety

- Distinguish verification, safety validation and confirmation measures in ISO 26262
- Select software unit verification methods and structural-coverage metrics per ASIL (ISO 26262-6:2018 Tables 7 and 9)
- Build a requirements-to-test traceability matrix and detect tests that are weaker than their requirement
- Separate ISO 26262 safety requirements from SOTIF / ISO/PAS 8800 acceptance criteria for ML components
- Quantify a recall claim statistically (zero-failure bound) and interpret fault-injection findings against the FTTI

---

← [Module 02 · Failures and Robustness](../02_Failures_and_Robustness/README.md) · [Course home](../README.md) · [Module 04 · SOTIF (ISO 21448)](../04_SOTIF_ISO21448/README.md) →
