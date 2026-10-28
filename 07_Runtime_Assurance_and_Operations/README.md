# Module 07 · Runtime Assurance and Operations

Safety in operation: monitoring the ODD at runtime, safe motion planning and fallback, the human driver in supervision and takeover, cooperative driving with V2X, field safety monitoring with real NHTSA crash reports, and how automated driving is being deployed today.

**6 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ODD Specification and Runtime Monitoring](01_odd_and_runtime_monitoring.ipynb) | Intermediate | ISO 34503:2023, SAE J3016 (2021), UN R157, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 02 | [Safe Motion Planning and Fallback](02_safe_motion_planning_and_fallback.ipynb) | Advanced | ISO 21448:2022, ISO 26262:2018, UN R157 (01 series), ISO 23793-1:2024, IEEE 2846-2022, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb) |
| 03 | [Human Factors: Supervision, Takeover and Misuse](03_human_factors_and_takeover.ipynb) | Intermediate | SAE J3016 (2021), UN R157 (01 series), Reg. (EU) 2019/2144, ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 04 | [V2X and Cooperative Driving](04_v2x_cooperative_driving.ipynb) | Intermediate | SAE J2735, ETSI EN 302 637-2/-3, ETSI TS 103 324, IEEE 1609.2, ETSI TS 103 097, 3GPP TS 22.185/22.186 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb) |
| 05 | [Field Safety Monitoring with Real Crash Reports](05_field_safety_monitoring.ipynb) | Intermediate | NHTSA SGO 2021-01 (third amendment), UL 4600 (3rd ed., 2023), ISO/TS 5083:2025, UN R157, UN R155, Regulation (EU) 2022/1426 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb) |
| 06 | [Industry Deployment: Status, Evidence and Operations](06_industry_deployment.ipynb) | Intermediate | NHTSA SGO 2021-01 (3rd amendment), UN R157, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb) |

## What you will learn

### 01 · ODD Specification and Runtime Monitoring

- define an Operational Design Domain (ODD) with SAE J3016 terminology and structure it with the ISO 34503:2023 taxonomy;
- explain who performs the DDT fallback at each automation level, and distinguish a *minimal risk condition* (MRC) from a *minimum risk manoeuvre* (MRM);
- implement a runtime ODD monitor with hysteresis, dwell and confirmation times, driving a NOMINAL → DEGRADED → MRM → MRC state machine;
- reproduce the UN R157 transition-demand timings for a Level 3 ALKS;
- define leading and lagging *safety performance indicators* (SPIs) in the sense of UL 4600 and evaluate them with confidence intervals.

### 02 · Safe Motion Planning and Fallback

- Place **route, behaviour and motion planning** in an automated driving stack and state which safety properties each layer can and cannot provide.
- Implement a **sampling-based Frenet lattice planner** (quintic lateral and quartic longitudinal polynomials) from scratch, and separate **soft costs** from **hard safety constraints**.
- Quantify the error of a constant-velocity **prediction on real NGSIM trajectories** and use it as an **inflated occupancy** or a **chance constraint**, including the "freezing robot" failure of over-conservative constraints.
- Build an **RSS safety shield** (the same envelope as `avsafety.sotif`) in a **Simplex** arrangement over a nominal planner, and measure its effect on collisions, minimum TTC, jerk and progress in closed loop with **real US-101 traffic**.
- Design **minimal risk manoeuvres**, derive comfort limits from **real KITTI GPS/IMU data**, and quantify how an emergency stop shifts risk to following traffic, using real follower gaps.
- Distinguish **fail-safe** and **fail-operational** architectures and compare them in a fault-injection experiment.

### 03 · Human Factors: Supervision, Takeover and Misuse

- Distinguish the human roles of SAE J3016: the **Level 2 driver who supervises** and the **Level 3 fallback-ready user**, and state what each implies for system design.
- Explain **automation complacency**, **mode confusion** and the **out-of-the-loop** problem, and connect each to a design requirement.
- Use published take-over-time evidence correctly: what the meta-analysis of Zhang et al. (2019) shows, and why non-critical transitions take much longer (Eriksson & Stanton, 2017).
- Fit a take-over-time **distribution** to published summary statistics and compute the **lead time required for 95 % successful takeovers**, with its uncertainty.
- Simulate takeover outcomes against the **UN R157** transition demand and MRM timings, and size the transition demand for a planned event.
- State the driver-monitoring requirements of UN R157 and the **DDAW/ADDW** timeline of Regulation (EU) 2019/2144.
- Run a **foreseeable-misuse analysis** as an ISO 21448 work product, using the NHTSA Autopilot recall 23V-838 as a real case.

### 04 · V2X and Cooperative Driving

- distinguish V2V, V2I, V2P and V2N, and the radio technologies ITS-G5/DSRC, LTE-V2X and NR-V2X (PC5 sidelink vs. Uu);
- name the main message sets in the US (SAE J2735: BSM, SPaT, MAP, PSM, SDSM) and in Europe (ETSI CAM, DENM, SPATEM/MAPEM, CPM);
- quote the 3GPP latency and reliability requirements correctly, and explain why "V2X range" is not a single number;
- simulate packet delivery versus distance and channel load and its effect on a cooperative braking warning;
- describe V2X security (IEEE 1609.2 / ETSI TS 103 097, SCMS / EU CCMS, pseudonym certificates, misbehaviour detection);
- argue where V2X belongs in a safety case: as a non-safety-critical *additional* input, or as an input that then carries safety requirements.

### 05 · Field Safety Monitoring with Real Crash Reports

- state what the NHTSA Standing General Order (SGO) requires to be reported for ADS and for Level 2 ADAS under the third amendment, and why the two populations have different reporting thresholds;
- load the public SGO crash reports, resolve report versions and duplicate reports of the same crash, and handle redactions (CBI, PII);
- describe the ADS and ADAS crash populations by operator, state, roadway, crash partner, pre-crash movement, injury severity and time, and say what the two populations can and cannot be compared on;
- turn reports into rates using an operator's published, dated exposure (Waymo Safety Impact Data Hub), with exact Poisson confidence intervals, and show why a human benchmark must be matched by geography and outcome definition;
- build a small safety performance indicator (SPI) dashboard with leading and lagging indicators in the sense of UL 4600;
- extract simple themes from unredacted crash narratives, and name the main biases of field crash data;
- place field monitoring in the regulatory frame (UN R157, UN R155, EU 2022/1426, ISO/TS 5083) and in an incident escalation process.

### 06 · Industry Deployment: Status, Evidence and Operations

- describe the state of automated-driving deployment as of October 2026, with dated and sourced facts;
- distinguish the deployment models robotaxi, driverless trucking, consumer Level 3 and supervised Level 2, and who carries the fallback and the liability in each;
- interpret published safety-impact data (Waymo) statistically, and explain why injury outcomes can be demonstrated long before fatality outcomes;
- separate remote assistance from remote driving and treat remote-operations staffing as a safety parameter;
- explain what the NHTSA Standing General Order requires and what crash-report data can and cannot show.

---

← [Module 06 · AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) · [Course home](../README.md) · [Module 08 · Standards, Regulation and Safety Case](../08_Standards_Regulation_and_Safety_Case/README.md) →
