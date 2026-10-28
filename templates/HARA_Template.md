# HARA Template: Hazard Analysis and Risk Assessment (ISO 26262-3:2018)

A working template for the hazard analysis and risk assessment of an item according to ISO 26262-3:2018, clauses 5 (item definition) and 6 (HARA). Each section has an empty table to fill in, followed by a short worked example: an automated emergency braking (AEB) function (a driver-assistance / active safety function), consistent with [Module 03, Notebook 02](../03_Functional_Safety_ISO26262/02_hara.ipynb).

> **Before you start**
> - The HARA analyses the **item at vehicle level**. Hazards are vehicle behaviours (e.g. "unintended deceleration"), not component outputs (e.g. "false positive of the detector").
> - The HARA is carried out **without considering the safety mechanisms** of the item under analysis. Their effect is credited later, in the functional and technical safety concepts.
> - Every S, E and C rating needs a **written rationale**. Rate the **worst credible** operational situation, not the worst imaginable one.
> - The HARA does not ask for the cause of a malfunction. Causes are analysed later: E/E faults under ISO 26262, functional insufficiencies and triggering conditions under ISO 21448:2022, and ML-specific insufficiencies under ISO/PAS 8800:2024.
>
> The example ratings in this template are illustrative teaching values, not the result of a HARA for a real product.

---

## 0. Document information

| Field | Value |
|---|---|
| Item | |
| Document ID / version | |
| Date | |
| Author(s) | |
| HARA team (roles) | e.g. functional-safety engineer, system engineer, vehicle-dynamics expert, driver-behaviour / HMI expert |
| Reviewed by (verification review) | |
| Confirmation review (ISO 26262-2, independence level) | |
| Status | Draft / In review / Released |
| Related documents | Item definition, ODD description, SOTIF analysis, TARA |

---

## 1. Item definition (ISO 26262-3:2018, clause 5)

| Attribute | Content |
|---|---|
| Item name | |
| Functional description (vehicle level) | |
| Level of driving automation (SAE J3016) | |
| Boundary: included elements | |
| Boundary: excluded elements / neighbouring items | |
| Inputs (signal, source) | |
| Outputs (signal, receiver) | |
| Operating modes | |
| Operating conditions / ODD | Speed range, road types, environment |
| Legal requirements, standards, known hazards from similar items | |
| Assumptions on the driver and other items | |

**Example (AEB, driver-assistance / active safety function):**

| Attribute | Content |
|---|---|
| Item name | Automated emergency braking (AEB) function |
| Functional description | Detects vehicles, pedestrians and cyclists in the vehicle path; if a collision is imminent and the driver does not react, requests automatic deceleration up to full braking (about 10 m/s²) |
| Level of automation | Driver-assistance / active safety function (momentary intervention; not driving automation per SAE J3016:2021, so outside Levels 1–5); the driver remains responsible for monitoring and braking |
| Included | Front camera and radar, perception and fusion, threat assessment and decision logic, deceleration request, driver-warning request |
| Excluded | Brake system / ESC hydraulics (separate item), instrument-cluster HMI hardware |
| Inputs | Camera images, radar targets, vehicle speed, yaw rate, brake-pedal and steering activity |
| Outputs | Deceleration request (to brake system), warning request (to HMI), AEB status |
| Operating modes | Active (10–130 km/h), standby, unavailable (fault detected) |
| Operating conditions | Public roads (urban, rural, motorway); day and night; dry and wet roads |
| Assumptions | The brake system executes a valid deceleration request; the driver can override by pressing the accelerator |

---

## 2. Operational situation catalogue

Exposure (E) belongs to the operational situation. State whether it is rated by **duration** or by **frequency**:

| Class | Description | Duration (share of average operating time) | Frequency |
|---|---|---|---|
| E0 | Incredible | – | – (no ASIL assigned) |
| E1 | Very low probability | Not specified | Less often than once a year for the great majority of drivers |
| E2 | Low probability | < 1 % | A few times a year for the great majority of drivers |
| E3 | Medium probability | 1 % to 10 % | Once a month or more often for an average driver |
| E4 | High probability | > 10 % | All or almost every drive on average |

Use **duration** for hazards that can strike at any time while the situation lasts (e.g. unintended braking), and **frequency** for hazards that only matter when the situation occurs (e.g. omission of a required intervention).

| OS ID | Road type | Speed range | Traffic participants | Environment | Driver state / manoeuvre | E | Basis (duration / frequency) | Rationale and data source |
|---|---|---|---|---|---|---|---|---|
| OS-01 | | | | | | | | |
| OS-02 | | | | | | | | |

**Example:**

| OS ID | Road type | Speed range | Traffic participants | Environment | Driver state / manoeuvre | E | Basis | Rationale |
|---|---|---|---|---|---|---|---|---|
| OS-01 | Urban | 30–50 km/h | Pedestrian steps into path, collision imminent | Any | Driver inattentive | E2 | Frequency | Emergency conflicts with pedestrians: a few times a year at most |
| OS-02 | Urban | 30–50 km/h | Following vehicle close behind | Any | Normal driving | E4 | Duration | Urban driving with a follower: well above 10 % of operating time |
| OS-03 | Motorway | 100–130 km/h | Following vehicle at about 1 s headway | Any | Normal driving | E4 | Duration | Assumed > 10 % for the target market; confirm with field data |
| OS-04 | Motorway / rural | 80–130 km/h | Stationary end of a traffic jam ahead | Any | Approaching the queue | E3 | Frequency | About once a month or more for an average driver |

---

## 3. Malfunctioning behaviours (vehicle level)

Derive them systematically with guide words: *no / unintended / too early / too late / too much / too little / too long*.

| MB ID | Item function | Guide word | Malfunctioning behaviour (vehicle level) | Resulting hazard |
|---|---|---|---|---|
| MB-01 | | | | |

**Example:**

| MB ID | Item function | Guide word | Malfunctioning behaviour | Resulting hazard |
|---|---|---|---|---|
| MB-01 | Emergency deceleration | no / too little / too late | No or insufficient AEB deceleration when a collision is imminent | Collision that AEB should have mitigated |
| MB-02 | Emergency deceleration | unintended | Unintended AEB deceleration (up to full braking) without a collision threat | Rear-end collision by following traffic; loss of stability |
| MB-03 | Emergency deceleration | too much / too long | Deceleration stronger or longer than required | Rear-end collision after the threat has passed |

---

## 4. Classification scales (ISO 26262-3:2018, Annex B)

**Severity (S)**: extent of harm to each person potentially affected.

| Class | Description | Informative AIS guidance |
|---|---|---|
| S0 | No injuries | AIS 0, or < 10 % probability of AIS 1–6 |
| S1 | Light and moderate injuries | > 10 % probability of AIS 1–6 (and not S2 or S3) |
| S2 | Severe and life-threatening injuries (survival probable) | > 10 % probability of AIS 3–6 (and not S3) |
| S3 | Life-threatening injuries (survival uncertain), fatal injuries | > 10 % probability of AIS 5–6 |

**Exposure (E)**: see section 2.

**Controllability (C)**: ability of the **driver or other persons at risk** (e.g. following drivers, pedestrians) to avoid the specific harm.

| Class | Description | Guidance |
|---|---|---|
| C0 | Controllable in general | No percentage (no ASIL assigned) |
| C1 | Simply controllable | 99 % or more of drivers or other traffic participants are usually able to avoid harm |
| C2 | Normally controllable | 90 % or more are usually able to avoid harm |
| C3 | Difficult to control or uncontrollable | Less than 90 % are usually able, or barely able, to avoid harm |

**ASIL determination (ISO 26262-3:2018 Table 4).** Rows: exposure; columns: controllability. S0, E0 or C0 → no ASIL (QM).

| S1 | C1 | C2 | C3 |
|---|---|---|---|
| E1 | QM | QM | QM |
| E2 | QM | QM | QM |
| E3 | QM | QM | A |
| E4 | QM | A | B |

| S2 | C1 | C2 | C3 |
|---|---|---|---|
| E1 | QM | QM | QM |
| E2 | QM | QM | A |
| E3 | QM | A | B |
| E4 | A | B | C |

| S3 | C1 | C2 | C3 |
|---|---|---|---|
| E1 | QM | QM | A |
| E2 | QM | A | B |
| E3 | A | B | C |
| E4 | B | C | D |

Quick check: with S, E and C as numbers, S + E + C = 10 → D, 9 → C, 8 → B, 7 → A, ≤ 6 → QM. The same table is implemented and tested in [`avsafety/iso26262.py`](../avsafety/iso26262.py) (`determine_asil`).

---

## 5. Hazardous events and ASIL determination

A hazardous event = malfunctioning behaviour × operational situation.

| HE ID | MB | OS | Operating mode | Hazardous event (description) | S | S rationale | E | E rationale (from OS) | C | C rationale (who controls, how) | ASIL | Safety goal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HE-01 | | | | | | | | | | | | |

**Example:**

| HE ID | MB | OS | Mode | Hazardous event | S | S rationale | E | C | C rationale | ASIL | SG |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HE-01 | MB-01 | OS-01 | Active | No AEB braking for a pedestrian at 30–50 km/h | S3 | Pedestrian struck at up to 50 km/h | E2 | C2 | Driver assistance: the driver remains responsible for braking; most attentive drivers brake themselves | A | SG-02 |
| HE-02 | MB-01 | OS-04 | Active | No AEB braking when approaching a stationary queue | S3 | High-speed impact into a stationary vehicle | E3 | C2 | Driver monitors the road and normally brakes | B | SG-02 |
| HE-03 | MB-02 | OS-03 | Active | Unintended full braking at 100–130 km/h with a close follower | S3 | Rear impact at a high speed difference, possibly by a heavy goods vehicle | E4 | C3 | Sudden full braking without warning at about 1 s headway: fewer than 90 % of following drivers avoid the impact | D | SG-01 |
| HE-04 | MB-02 | OS-02 | Active | Unintended full braking at 30–50 km/h with a close follower | S1 | Low-speed rear-end impact (whiplash) | E4 | C2 | Following drivers can normally brake in time | A | SG-01 |

Note on the example: some published AEB analyses argue that omission (MB-01) of a driver-assistance function is QM, because the vehicle then behaves like one without AEB. Whatever you decide, record the argument.

---

## 6. Safety goals

| SG ID | Safety goal (vehicle level) | ASIL (highest of covered HEs) | Covered HEs | Safe state (operating mode) | FTTI | Emergency operation (if needed) | Remarks |
|---|---|---|---|---|---|---|---|
| SG-01 | | | | | | | |

Definitions (ISO 26262-1:2018):

- **FTTI** (fault tolerant time interval): minimum time span from the occurrence of a fault in the item to a possible occurrence of a hazardous event, if the safety mechanisms are not activated.
- **FDTI** (fault detection time interval): time span from the occurrence of a fault to its detection.
- **FRTI** (fault reaction time interval): time span from the detection of a fault to reaching a safe state or emergency operation.
- Each safety mechanism must satisfy **FDTI + FRTI ≤ FTTI**.

A safe state is an **operating mode**, such as "function switched off, driver warned". An intervention such as "apply emergency braking" is not a safe state.

**Example:**

| SG ID | Safety goal | ASIL | Covered HEs | Safe state | FTTI (illustrative) | Remarks |
|---|---|---|---|---|---|---|
| SG-01 | Avoid unintended AEB deceleration (illustrative limit: > 3 m/s² for > 300 ms) | D | HE-03, HE-04 | AEB deceleration request inhibited, AEB-unavailable warning; driver keeps full control | ≈ 300 ms, to be derived from the deceleration ramp and confirmed by vehicle tests | Candidate for ASIL decomposition D → B(D) + B(D): decision channel and independent plausibility channel; requires a dependent failure analysis (ISO 26262-9, clause 7). Hardware metrics and PMHF stay at ASIL D. |
| SG-02 | Avoid omission of AEB deceleration when a collision with a pedestrian or a stationary vehicle is imminent | B | HE-01, HE-02 | AEB unavailable, driver warned; driver remains responsible for braking | ≈ 500 ms (illustrative) | The SG-01 safe state (AEB off) is acceptable for a driver-assistance function only because the driver is the fallback |

---

## 7. Outlook: first functional safety requirements (optional)

Functional safety requirements are specified in the functional safety concept (ISO 26262-3, clause 7). They are listed here only to show traceability.

| FSR ID | Safety goal | ASIL | Functional safety requirement | Allocated to |
|---|---|---|---|---|
| | | | | |

**Example:**

| FSR ID | SG | ASIL | Requirement | Allocated to |
|---|---|---|---|---|
| FSR-01.1 | SG-01 | B(D) | Issue a deceleration request only when the fused object list indicates an imminent collision | AEB decision channel |
| FSR-01.2 | SG-01 | B(D) | Forward a deceleration request only when an independent check confirms an imminent collision | Plausibility channel (brake ECU) |
| FSR-01.3 | SG-01 | D | Protect the deceleration request against corruption, repetition and loss (end-to-end protection) | Communication path |
| FSR-02.1 | SG-02 | B | Detect faults that prevent AEB braking and warn the driver within the fault-handling time | AEB ECU, HMI |

Note on FSR-01.2: the item definition excludes the brake system. The plausibility function on the brake ECU is either declared part of the AEB item (boundary updated accordingly) or specified as a requirement on the neighbouring brake item and agreed through a development interface agreement (DIA, ISO 26262-8:2018, clause 5). Either way, the B(D) requirement and the independence argument must hold across that interface.

Perception **performance targets** (e.g. pedestrian recall, false-positive rate per hour) are not ISO 26262 safety requirements and carry no ASIL. Record them as acceptance criteria in the SOTIF analysis ([`SOTIF_Analysis_Template.md`](SOTIF_Analysis_Template.md)) and, for ML components, under ISO/PAS 8800.

---

## 8. Assumptions log

| ID | Assumption | Affects (OS / HE / SG) | Source or justification | Owner | How and when validated | Status |
|---|---|---|---|---|---|---|
| A-01 | | | | | | Open |

**Example:**

| ID | Assumption | Affects | Justification | Validation | Status |
|---|---|---|---|---|---|
| A-01 | Motorway driving with a follower at ≤ 2 s headway exceeds 10 % of operating time | OS-03, HE-03 | Engineering judgement | Field data from the predecessor vehicle | Open |
| A-02 | Following drivers cannot avoid a rear-end impact after unexpected full braking at 1 s headway (C3) | HE-03 | Literature on brake reaction times | Controllability study (e.g. per the RESPONSE 3 Code of Practice for the Design and Evaluation of ADAS, 2009) | Open |
| A-03 | The brake system executes a valid deceleration request (neighbouring item) | All | Interface agreement | Development interface agreement (DIA) | Agreed |

---

## 9. Review checklist

| # | Check | Yes / No / N/A | Comment |
|---|---|---|---|
| 1 | The item is defined at vehicle level, including its actuator path and boundary | | |
| 2 | Operating modes (including degraded and fault modes) are considered | | |
| 3 | The situation catalogue covers road types, speeds, environment, other road users (also following traffic) and foreseeable misuse | | |
| 4 | Malfunctioning behaviours were derived systematically (e.g. guide words) for every item function | | |
| 5 | Hazards are vehicle-level behaviours, not component outputs or causes | | |
| 6 | No safety mechanism of the item was credited in S, E or C | | |
| 7 | Every S, E and C rating has a written rationale; the E basis (duration / frequency) is stated | | |
| 8 | C considers the driver **and** other persons at risk | | |
| 9 | ASILs were determined with ISO 26262-3 Table 4 (cross-checked, e.g. with `avsafety.iso26262.determine_asil`) | | |
| 10 | Every hazardous event with ASIL A–D is covered by a safety goal; each goal has the highest ASIL of its events | | |
| 11 | Safety goals are vehicle-level, verifiable and free of design solutions | | |
| 12 | Safe states are operating modes; FTTIs are stated (also for commission hazards) | | |
| 13 | Conflicting safety goals (e.g. "avoid unintended braking" vs "avoid omission") were identified and resolved | | |
| 14 | Performance insufficiencies are handed over to the SOTIF analysis and ML-specific issues to the ISO/PAS 8800 analysis | | |
| 15 | Cybersecurity-induced hazards are exchanged with the TARA (shared damage scenarios) | | |
| 16 | Assumptions are logged with owner and validation plan | | |
| 17 | Verification review and confirmation review (ISO 26262-2, Table 1) are planned or completed | | |

---

## 10. Open issues and review history

| Issue ID | Description | Owner | Target date | Status |
|---|---|---|---|---|
| | | | | |

| Version | Date | Reviewer / role | Findings | Status |
|---|---|---|---|---|
| | | | | |

| Role | Name | Date | Approval |
|---|---|---|---|
| Functional safety manager | | | |
| System / project lead | | | |

---

## Notes and common mistakes

- **Conservative rating** means choosing the higher S, E and C classes when the evidence is insufficient (C3 = least controllable), and recording the evidence that is missing.
- **Typical mistakes:** rating causes ("detector false negative") instead of vehicle behaviour; crediting safety mechanisms; writing safety goals as performance targets ("detect all pedestrians"); safe states that are interventions; "FTTI = N/A" for commission hazards; missing following traffic as persons at risk.
- **Interfaces to other analyses:** ISO 21448 (SOTIF) reuses the hazards and severities to judge the residual risk from functional insufficiencies; ISO/SAE 21434 (TARA) shares damage scenarios with safety impact; FMEA and FTA ([Notebooks 03 and 04](../03_Functional_Safety_ISO26262/)) analyse causes against the safety goals.

## References

- ISO 26262-1:2018, -3:2018 and -9:2018, *Road vehicles: Functional safety*. Geneva: ISO.
- ISO 21448:2022, *Road vehicles: Safety of the intended functionality*. Geneva: ISO.
- ISO/PAS 8800:2024, *Road vehicles: Safety and artificial intelligence*. Geneva: ISO.
- SAE J2980, *Considerations for ISO 26262 ASIL Hazard Classification*. SAE International.
- SAE J3016 (2021), *Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles*.

---

*Template version 2.0 · Milin Patel · Hochschule Kempten · MIT Licence*
