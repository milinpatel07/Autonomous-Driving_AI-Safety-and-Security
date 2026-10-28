# Module 07 · Runtime Assurance and Operations

Safety after start of production: monitoring the ODD at runtime and falling back to a minimal risk condition, cooperative driving with V2X, and how automated driving is being deployed today.

**3 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [ODD Specification and Runtime Monitoring](01_odd_and_runtime_monitoring.ipynb) | Intermediate | ISO 34503:2023, SAE J3016 (2021), UN R157, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 02 | [V2X and Cooperative Driving](02_v2x_cooperative_driving.ipynb) | Intermediate | SAE J2735, ETSI EN 302 637-2/-3, ETSI TS 103 324, IEEE 1609.2, ETSI TS 103 097, 3GPP TS 22.185/22.186 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/02_v2x_cooperative_driving.ipynb) |
| 03 | [Industry Deployment: Status, Evidence and Operations](03_industry_deployment.ipynb) | Intermediate | NHTSA SGO 2021-01 (3rd amendment), UN R157, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/07_Runtime_Assurance_and_Operations/03_industry_deployment.ipynb) |

## What you will learn

### 01 · ODD Specification and Runtime Monitoring

- define an Operational Design Domain (ODD) with SAE J3016 terminology and structure it with the ISO 34503:2023 taxonomy;
- explain who performs the DDT fallback at each automation level, and distinguish a *minimal risk condition* (MRC) from a *minimum risk manoeuvre* (MRM);
- implement a runtime ODD monitor with hysteresis, dwell and confirmation times, driving a NOMINAL → DEGRADED → MRM → MRC state machine;
- reproduce the UN R157 transition-demand timings for a Level 3 ALKS;
- define leading and lagging *safety performance indicators* (SPIs) in the sense of UL 4600 and evaluate them with confidence intervals.

### 02 · V2X and Cooperative Driving

- distinguish V2V, V2I, V2P and V2N, and the radio technologies ITS-G5/DSRC, LTE-V2X and NR-V2X (PC5 sidelink vs. Uu);
- name the main message sets in the US (SAE J2735: BSM, SPaT, MAP, PSM, SDSM) and in Europe (ETSI CAM, DENM, SPATEM/MAPEM, CPM);
- quote the 3GPP latency and reliability requirements correctly, and explain why "V2X range" is not a single number;
- simulate packet delivery versus distance and channel load and its effect on a cooperative braking warning;
- describe V2X security (IEEE 1609.2 / ETSI TS 103 097, SCMS / EU CCMS, pseudonym certificates, misbehaviour detection);
- argue where V2X belongs in a safety case: as a non-safety-critical *additional* input, or as an input that then carries safety requirements.

### 03 · Industry Deployment: Status, Evidence and Operations

- describe the state of automated-driving deployment as of October 2026, with dated and sourced facts;
- distinguish the deployment models robotaxi, driverless trucking, consumer Level 3 and supervised Level 2, and who carries the fallback and the liability in each;
- interpret published safety-impact data (Waymo) statistically, and explain why injury outcomes can be demonstrated long before fatality outcomes;
- separate remote assistance from remote driving and treat remote-operations staffing as a safety parameter;
- explain what the NHTSA Standing General Order requires and what crash-report data can and cannot show.

---

← [Module 06 · AI Safety (ISO/PAS 8800)](../06_AI_Safety_ISO_PAS_8800/README.md) · [Course home](../README.md) · [Module 08 · Standards, Regulation and Safety Case](../08_Standards_Regulation_and_Safety_Case/README.md) →
