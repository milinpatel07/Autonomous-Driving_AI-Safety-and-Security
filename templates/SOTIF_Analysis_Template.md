# SOTIF Analysis Template (ISO 21448:2022)

A working template for the safety of the intended functionality (SOTIF) of a driver-assistance or automated-driving
function. The sections follow the activity flow of **ISO 21448:2022** (clauses 5–13). Example rows use a camera-based
**pedestrian AEB** and match the teaching notebooks in [`04_SOTIF_ISO21448/`](../04_SOTIF_ISO21448/).

> **How to use:** replace every `[...]` field; delete the example rows (marked *Example*) before release.
> **All example numbers are illustrative teaching values, not recommended targets or measurements.**
> Clause numbers refer to ISO 21448:2022; titles are paraphrased — check against the standard.

**Scope reminder.** ISO 21448 covers hazards caused by **functional insufficiencies** (insufficiencies of specification
and performance insufficiencies) activated by **triggering conditions**, including **reasonably foreseeable misuse**.
It does **not** cover E/E malfunctions (→ ISO 26262:2018) or cybersecurity threats (→ ISO/SAE 21434:2021).
ML-specific insufficiencies are elaborated in ISO/PAS 8800:2024.

---

## 0. Document information

| Field | Value |
|---|---|
| Function / item | [name] |
| Level of driving automation (SAE J3016:2021) | [none (active safety) / L1 / L2 / L3 / L4] |
| Document version | [x.y] |
| Date | [YYYY-MM-DD] |
| Prepared by | [name, role] |
| Reviewed by | [name, role] |
| Status | ☐ Draft ☐ In review ☐ Approved |
| Related work products | HARA [ref], TARA [ref], safety case [ref] |

---

## 1. Specification and design (clause 5)

### 1.1 Intended functionality

| Item | Description |
|---|---|
| Intended functionality | [what the function does, for whom, in which situations] |
| Driver / user role | [supervises continuously (L2) / fallback-ready user (L3) / passenger only (L4)] |
| System elements | Sensors: [...] · Perception/algorithms: [...] · Actuators: [...] · HMI: [...] |
| Performance specification | Detection range, accuracy, latency, availability: [...] |
| Known limitations at design time | [...] |
| Fallback / minimal risk manoeuvre | [description] |

*Example:* Pedestrian AEB — detects pedestrians in the vehicle path and brakes automatically; driver remains
responsible (momentary-intervention active safety system, outside the SAE J3016 levels 1–5); front camera + radar; system latency ≤ [x] ms; known limitation: reduced recall in
heavy rain and darkness.

### 1.2 Operational design domain (structured per ISO 34503:2023)

| Top-level attribute | Included | Excluded (ODD exit) | How exit is detected |
|---|---|---|---|
| **Scenery** (road types, geometry, junctions, markings, signs, structures) | [...] | [...] | [...] |
| **Environmental conditions** (weather, particulates, illumination, connectivity) | [...] | [...] | [...] |
| **Dynamic elements** (traffic participants, density, subject-vehicle speed) | [...] | [...] | [...] |

*Example:* Environmental conditions — included: daylight, dusk, dry or wet road, light rain; excluded: dense fog
(visibility < [x] m); detection: camera contrast estimate + rain sensor → function degraded with driver message.

### 1.3 User responsibilities and transitions

| Item | Specification | Justification |
|---|---|---|
| User responsibilities | [...] | [...] |
| Takeover / transition time budget (L3) | [specify] | [justify, e.g. against UN R157: minimal risk manoeuvre at the earliest 10 s after the transition demand starts] |
| Driver monitoring | [...] | [...] |

---

## 2. Hazard identification and risk evaluation (clause 6)

Use **one vehicle-level hazard list** shared with the ISO 26262 HARA. A hazard can have E/E-fault causes (ISO 26262)
and SOTIF causes (this document).

| H-ID | Hazardous behaviour | Relevant scenario(s) | Severity / controllability notes | Cross-ref. HARA (ISO 26262) |
|---|---|---|---|---|
| H-[nn] | [...] | [...] | [...] | [HZ-ID, ASIL] |
| *Example* H-01 | No or late braking for a crossing pedestrian | Urban, pedestrian crossing, ≤ 60 km/h | Severe injury possible; driver may not react in time | HZ-03 |
| *Example* H-02 | Unintended emergency braking | Any traffic with following vehicle | Rear-end collision; following driver may not react | HZ-05 |

---

## 3. Acceptance criteria and validation targets (clauses 6 and 9)

Acceptance criteria concern the **residual risk of hazardous behaviour at vehicle level**. Give the rationale (e.g.
regulations, performance of comparable functions, careful human drivers, traffic statistics for the target market).
Derive the **validation target** as the exposure needed to show the criterion with a stated confidence.

For $k$ hazardous events in exposure $n$ (Poisson model, confidence $C$):
$n \ge \chi^2_{C}(2(k+1)) / (2\lambda_{AC})$; for $k = 0$: $n \ge -\ln(1-C)/\lambda_{AC} \approx 3/\lambda_{AC}$ at $C = 95\,\%$
(`avsafety.validation.miles_to_demonstrate`).

| AC-ID | Hazard | Acceptance criterion | Rationale / source | Confidence | Validation target | Exposure unit and relevant subset |
|---|---|---|---|---|---|---|
| AC-[nn] | H-[nn] | ≤ [λ] events per [h / km / encounter] | [...] | [%] | [n] with ≤ [k] events | [...] |
| *Example* AC-02 | H-02 | ≤ 1 × 10⁻⁵ unintended emergency brakings per hour | [rationale] | 95 % | 3.0 × 10⁵ h with 0 events | Operating hours in the ODD |

Derived component requirements (e.g. perception recall) must be traced to an AC-ID; they are not acceptance criteria
themselves.

| Derived requirement | Traced to | Argument (architecture, fusion, braking strategy) |
|---|---|---|
| [e.g. pedestrian recall ≥ [x] % within [y] m] | AC-[nn] | [...] |

---

## 4. Functional insufficiencies and triggering conditions (clause 7)

### 4.1 Triggering conditions — conditions of the **scenario**

Structure by the 6-layer model (L1 road network, L2 roadside structures, L3 temporary modifications, L4 dynamic
objects, L5 environment, L6 digital information) plus *sensor exposure* and *driver behaviour / misuse*.

| TC-ID | Group / layer | Triggering condition | Inside ODD? | Source (analysis, simulation, test, field) |
|---|---|---|---|---|
| TC-[nn] | [...] | [...] | Y / N / boundary | [...] |
| *Example* TC-01 | L5 Environment | Low sun in camera field of view | Y | Analysis |
| *Example* TC-02 | L4 Dynamic objects | Child stepping out between parked cars | Y | Expert review |
| *Example* TC-03 | Sensor exposure | Water film on windscreen in heavy rain | Boundary | Simulation |

### 4.2 Functional insufficiencies — properties of the **system**

| FI-ID | Type | Element | Description | Activated by (TC-IDs) | Output insufficiency | Hazard (H-ID) |
|---|---|---|---|---|---|---|
| FI-[nn] | Specification / Performance | [...] | [...] | [...] | [...] | [...] |
| *Example* FI-01 | Performance | Camera | Limited dynamic range | TC-01 | Missed detection | H-01 |
| *Example* FI-02 | Specification | Function specification | No requirement for pedestrians emerging at short time-to-collision | TC-02 | Braking starts too late | H-01 |
| *Example* FI-03 | Performance | Detector (training-data coverage) | Low recall in rain-blurred images | TC-03 | Missed detection | H-01 |

### 4.3 Combinations of triggering conditions

| Combination | Why relevant | How evaluated (e.g. n-wise test set, targeted search) |
|---|---|---|
| [TC-xx × TC-yy (× ...)] | [...] | [...] |
| *Example* TC-02 × running pedestrian | Physically unavoidable at ≥ 30 km/h | Specification change: speed limit next to parked cars |

### 4.4 Reasonably foreseeable misuse

| MU-ID | Misuse (direct / indirect) | Consequence | Measure | Verification |
|---|---|---|---|---|
| MU-[nn] | [...] | [...] | [...] | [...] |
| *Example* MU-01 | Driver relies on AEB and stops watching the road (indirect) | No intervention when AEB is insufficient | HMI wording, driver monitoring, warnings | User study / simulator test |

### 4.5 Causes handled outside this analysis

| Cause | Handled by | Reference |
|---|---|---|
| E/E faults (random hardware, systematic HW/SW) | ISO 26262:2018 | [FMEA / FTA ref] |
| Attacks (adversarial patterns, spoofing) | ISO/SAE 21434:2021 | [TARA ref] |

---

## 5. Functional modifications (clause 8)

| M-ID | Addresses (FI / TC / MU) | Type | Description | Verification of effectiveness |
|---|---|---|---|---|
| M-[nn] | [...] | Improve performance / Restrict ODD / Hand over to driver / Runtime monitor / Specification change | [...] | [...] |
| *Example* M-01 | FI-03, TC-03 | Improve performance | Radar–camera fusion for pedestrians in rain | Simulation + proving-ground tests |
| *Example* M-02 | TC-03 | Restrict ODD | Degrade function above rain intensity [x] | ODD-exit detection tests |
| *Example* M-03 | FI-01, FI-03 | Runtime monitor | OOD monitor; threshold from requirement (≥ [x] % detection of specified OOD conditions); false alarms ≤ [y] per hour | Validation set with confidence bound; correlated ID driving data |

---

## 6. Verification and validation strategy (clause 9)

| Method | Purpose | Scenario source | Measure of completeness / effort | Credibility evidence | Status |
|---|---|---|---|---|---|
| Analysis (STPA, FMEA-style SOTIF analysis) | Identify TCs and FIs | [...] | [...] | n/a | ☐ |
| Simulation (MiL/SiL/HiL) | Known scenarios; search for hazardous combinations; rare-event estimation | Logical scenarios (e.g. ASAM OpenSCENARIO) | n-wise coverage of the discretised space: [x] % (n = [ ]); runs: [ ] | Tool confidence (ISO 26262-8 cl. 11: TCL [ ]); model validation vs real data for [conditions] | ☐ |
| Proving ground | Physical confirmation; sim-to-real correlation | [...] | Scenario runs: [ ] | Measurement uncertainty | ☐ |
| Public road / FOT | Real exposure; discovery | ODD routes | Exposure: [h / km] vs validation target | Data logging plan | ☐ |

Rationale for the chosen methods and their combination: [...]

---

## 7. Evaluation of known scenarios (clause 10) — Area 2

| SC-ID | Scenario | TC / FI | Evaluation result (with uncertainty) | Measure | Outcome |
|---|---|---|---|---|---|
| SC-[nn] | [...] | [...] | [...] | M-[nn] | ☐ Area 1 after modification ☐ Accepted residual risk (rationale) ☐ Open |
| *Example* SC-04 | Dense fog at a crosswalk | TC: fog; FI: contrast below sensitivity | Recall [x] % (95 % CI [a, b]) | M-02 (ODD restriction) | ☐ Area 1 after modification ☐ Accepted ☐ Open |

---

## 8. Evaluation of unknown scenarios (clause 11) — Area 3

The share of unknown scenarios cannot be measured. Record **how** unknown hazardous scenarios are searched for and
**how** their residual risk is bounded.

### 8.1 Discovery plan

| Method | Scope | Planned effort | Findings so far |
|---|---|---|---|
| Randomised / adversarial simulation over the logical scenario space | [...] | [...] | [...] |
| Variation of known scenarios (e.g. twin-scenario generation) | [...] | [...] | [...] |
| Public-road driving with event logging (incl. OOD monitor events) | [...] | [...] | [...] |
| Unusual road users (costumes, mobility devices, animals) | [...] | [...] | [...] |

Trend of discovery: new triggering-condition classes per [10⁴ km]: [values over time]; probability that the next
encounter is a new class (Good–Turing $N_1/N$): [value].

### 8.2 Statistical argument

| AC-ID | Exposure achieved | Hazardous events observed | Upper bound at [C] % | Criterion | Met? |
|---|---|---|---|---|---|
| AC-[nn] | [h / km] | [k] | [λ_U] | [λ_AC] | ☐ Yes ☐ No |

---

## 9. Evaluation of SOTIF achievement (clause 12)

| Question | Evidence | Answer |
|---|---|---|
| Are all identified hazards evaluated and their causes analysed? | [refs] | ☐ Yes ☐ No |
| Is the residual risk from known scenarios (Area 2) acceptable? | Section 7 | ☐ Yes ☐ No |
| Is the residual risk from unknown scenarios (Area 3) acceptable with sufficient confidence? | Section 8 | ☐ Yes ☐ No |
| Are validation targets met (or deviations justified)? | Sections 3, 8.2 | ☐ Yes ☐ No |
| Is the operation-phase monitoring in place? | Section 10 | ☐ Yes ☐ No |

**Recommendation:** ☐ Release ☐ Release with conditions: [...] ☐ No release

**Residual-risk statement:** [...]

---

## 10. Operation phase activities (clause 13)

| Activity | Data source | Trigger for action | Responsible |
|---|---|---|---|
| Field monitoring of hazardous behaviour and near misses | [...] | [...] | [...] |
| Analysis of logged OOD / ODD-exit events → candidate triggering conditions | [...] | [...] | [...] |
| Re-evaluation after ODD change or software/model update | [...] | Any change to ODD, sensors, models | [...] |
| Incident investigation | [...] | [...] | [...] |

---

## 11. Status tracking

| Activity (clause) | Status | Notes |
|---|---|---|
| Specification and ODD (5) | ☐ Not started ☐ In progress ☐ Complete | |
| Hazards and acceptance criteria (6) | ☐ Not started ☐ In progress ☐ Complete | |
| Insufficiencies, triggering conditions, misuse (7) | ☐ Not started ☐ In progress ☐ Complete | |
| Functional modifications (8) | ☐ Not started ☐ In progress ☐ Complete | |
| V&V strategy and validation targets (9) | ☐ Not started ☐ In progress ☐ Complete | |
| Known scenarios (10) | ☐ Not started ☐ In progress ☐ Complete | |
| Unknown scenarios (11) | ☐ Not started ☐ In progress ☐ Complete | |
| SOTIF achievement (12) | ☐ Not started ☐ In progress ☐ Complete | |
| Operation phase plan (13) | ☐ Not started ☐ In progress ☐ Complete | |

---

## 12. Assumptions, limitations, review and approval

**Assumptions:** [...]

**Limitations of this analysis:** [...]

| Date | Reviewer | Comments | Status |
|---|---|---|---|
| | | | |

| Role | Name | Signature | Date |
|---|---|---|---|
| SOTIF / safety lead | | | |
| Validation lead | | | |
| Functional safety manager (ISO 26262 interface) | | | |
| Cybersecurity manager (ISO/SAE 21434 interface) | | | |

---

## Appendix A — Reference definitions

**Scenario areas (ISO 21448:2022, clause 4.2.2)**

|  | Known | Unknown |
|---|---|---|
| **Not hazardous** | Area 1 | Area 4 — no SOTIF action needed |
| **Hazardous** | Area 2 — evaluate (clause 10) | Area 3 — discover and bound (clause 11) |

**Causal chain:** triggering condition → functional insufficiency → output insufficiency → hazardous behaviour →
(in a scenario without sufficient controllability) harm.

**Common mistakes**

- Listing sensor or algorithm limitations as triggering conditions (they are functional insufficiencies).
- Treating "tested" as "not hazardous"; a tested scenario can fail.
- Computing "coverage of unknown scenarios" — the denominator is unknowable; use coverage of a defined space plus a
  statistical bound.
- Calling AP or recall thresholds "ISO 21448 acceptance criteria".
- Including adversarial attacks or E/E faults in the SOTIF triggering-condition list.
- Pre-filling status boxes before the work is done.

## Appendix B — References

- ISO 21448:2022 *Road vehicles — Safety of the intended functionality* (replaces ISO/PAS 21448:2019).
- ISO 26262:2018 *Road vehicles — Functional safety*; Part 8, clause 11 (tool confidence).
- ISO/SAE 21434:2021 *Road vehicles — Cybersecurity engineering*.
- ISO/PAS 8800:2024 *Road vehicles — Safety and artificial intelligence*.
- ISO 34502:2022 (scenario-based safety evaluation framework); ISO 34503:2023 (ODD specification).
- SAE J3016 (2021) *Taxonomy and Definitions for Terms Related to Driving Automation Systems*.
- UN Regulation No. 157 (ALKS).
- Scholtes, M., et al. (2021). 6-Layer Model for a Structured Description and Categorization of Urban Traffic and Environment. *IEEE Access* 9. https://doi.org/10.1109/ACCESS.2021.3072739
- Kalra, N., Paddock, S. M. (2016). Driving to safety. *Transportation Research Part A* 94, 182–193. https://doi.org/10.1016/j.tra.2016.09.010
- Patel, M., Jung, R., Khatun, M. (2025). A Systematic Literature Review on Safety of the Intended Functionality for Automated Driving Systems. SAE Technical Paper 2025-01-5030. https://doi.org/10.4271/2025-01-5030

---

**Template version:** 2.0 · **Last updated:** October 2026 · **Reference standard:** ISO 21448:2022 ·
Author: Milin Patel · Hochschule Kempten · MIT Licence
