# TARA Template: Threat Analysis and Risk Assessment (ISO/SAE 21434:2021)

This template follows the TARA methods of ISO/SAE 21434:2021 **clause 15** (steps 15.3–15.9). It also covers the concept-phase outputs of **clause 9** (cybersecurity goals, claims, concept) and the interface to the ISO 26262 HARA.
The rating tables are the **informative examples** of Annexes E (CAL), F (impact), G (attack feasibility) and H (risk matrix). If your organisation uses its own tables, replace them and record the change in Section 0.

The worked examples (*Example:* rows) come from the AEB TARA in
[`05_Cybersecurity_ISO21434/02_tara.ipynb`](../05_Cybersecurity_ISO21434/02_tara.ipynb). They are illustrative and synthetic, and are not the result of a real assessment.

Delete the example rows when you fill in the template.

---

## Document information

| Field | Value |
|-------|-------|
| **Item name** | [Enter item name] |
| **Item definition reference** | [Document ID/version, shared with the HARA] |
| **HARA reference** | [Document ID/version] |
| **TARA version** | [Version number] |
| **Date** | [YYYY-MM-DD] |
| **Prepared by** | [Name/role] |
| **Reviewed by** | [Name/role, independence level] |
| **Information classification** | [Confidential/Restricted/Internal] |
| **Status** | Draft / In review / Released |

---

## 0. Method description

Record the methods so that a reviewer, or an auditor following ISO/SAE PAS 5112, can reproduce every rating.

| Aspect | Choice used in this TARA |
|---|---|
| Impact rating | Annex F categories Safety, Financial, Operational, Privacy (SFOP), road-user perspective; optional additional stakeholder categories: [list] |
| Feasibility method | Attack-potential (Annex G.2) / CVSS exploitability (G.3) / attack vector (G.4) — **select one primary method** |
| Attack path aggregation | e.g. AND = factor-wise maximum over steps; OR = most feasible path (minimum attack potential) |
| Attack vector convention | e.g. OBD-II diagnostic access = Local; physical-environment sensor attacks = Physical |
| Risk matrix | Annex H example (Section 7) / organisation-specific: [reference] |
| Risk treatment policy | e.g. risk ≥ 3 → Reduce; risk 2 with Severe safety impact → Reduce; otherwise Retain with claim |
| Residual risk acceptance | e.g. residual risk ≤ 2 acceptable; higher values need documented acceptance by [role] |
| CAL determination | Annex E example (impact × attack vector) / not used |

---

## 1. Item definition (clause 9.3)

The item definition should be **the same** as the one used for the ISO 26262 HARA.

| Attribute | Content |
|---|---|
| Item / function | [Description] |
| Boundary (included elements) | [ECUs, sensors, software, data] |
| Interfaces (outside the boundary) | [Gateway, backend, other ECUs] |
| External connectivity | [Cellular, Wi-Fi, Bluetooth, V2X, USB, OBD-II] |
| Update mechanisms | [OTA, workshop reprogramming] |
| Operating modes | [Active, degraded, diagnostic] |
| Operational environment and assumptions | [e.g. gateway filters diagnostic traffic; backend operated under ISO/IEC 27001] |

*Example:* Pedestrian AEB function. Inside the boundary: front camera, front radar, perception ECU (DNN detector, fusion, AEB logic), its software, model weights and calibration data, and the CAN-FD link to the brake ECU. Interfaces: brake ECU, central gateway (diagnostics, OTA client), telematics unit, OEM backend.

### 1.1 Safety interface (from the HARA)

| Safety goal | Description | ASIL | FTTI | Safe state |
|---|---|---|---|---|
| SG-xx | [from HARA] | [QM/A–D] | [ms] | [from HARA] |

*Example (illustrative S/E/C, ASIL per ISO 26262-3:2018 Table 4):*

| Safety goal | Description | S/E/C | ASIL | FTTI |
|---|---|---|---|---|
| SG-01 | Avoid unintended emergency braking | S2/E4/C2 | B | 200 ms |
| SG-02 | Avoid omission of emergency braking for a pedestrian in the path | S3/E3/C3 | C | 300 ms |

---

## 2. Asset identification and damage scenarios (15.3)

### 2.1 Assets

| Asset ID | Asset | Category | Cybersecurity properties | Rationale |
|---|---|---|---|---|
| A-xx | [Name] | Data / Software / Communication / Function / Hardware | C / I / A (+ authenticity, authorisation, non-repudiation if used) | [Why relevant] |

*Example:*

| Asset ID | Asset | Category | Properties |
|---|---|---|---|
| A-01 | Camera video stream (camera → perception ECU) | Data | I, A |
| A-02 | Perception DNN weights and configuration | Software | I |
| A-03 | Object list / brake request on CAN-FD | Communication | I, A |
| A-04 | Perception-ECU firmware | Software | I |
| A-05 | Camera calibration parameters | Data | I |
| A-06 | Recorded AEB event clips (camera images) | Data | C |

### 2.2 Damage scenarios

Describe the adverse consequence **for the road user** (driver, passengers, pedestrians, other traffic participants). Link it to a safety goal if it violates one.

| DS ID | Damage scenario | Safety | Financial | Operational | Privacy | Impact (max) | Safety goal | Rationale |
|---|---|---|---|---|---|---|---|---|
| DS-xx | [Description] | [S/M/Mo/N] | | | | | [SG-xx / –] | [Why] |

*Example:*

| DS ID | Damage scenario | S | F | O | P | Impact | SG |
|---|---|---|---|---|---|---|---|
| DS-01 | Unintended emergency braking in following traffic → rear-end collision | Major | Moderate | Moderate | Negligible | Major | SG-01 |
| DS-02 | No/late emergency braking for a pedestrian in the path → fatal collision | Severe | Major | Major | Negligible | Severe | SG-02 |
| DS-03 | AEB unavailable (degraded mode, driver warned) | Negligible | Negligible | Major | Negligible | Major | – |
| DS-04 | Recorded images of identifiable people disclosed | Negligible | Moderate | Negligible | Major | Major | – |

---

## 3. Threat scenario identification (15.4)

A threat scenario states the **asset**, the compromised **cybersecurity property** and the **cause**, and links to damage scenarios.
STRIDE may be used as a brainstorming heuristic. Threat actors and motivation are optional context; they do not replace the feasibility rating.

| TS ID | Asset | Property | Cause (how) | STRIDE | Damage scenario(s) |
|---|---|---|---|---|---|
| TS-xx | A-xx | [I/C/A] | [Cause] | [S/T/R/I/D/E] | DS-xx |

*Example:*

| TS ID | Asset | Property | Cause | Damage scenario(s) |
|---|---|---|---|---|
| TS-01 | A-03 | Integrity | Forged object-list/brake-request frames injected on CAN-FD | DS-01 |
| TS-02 | A-02 | Integrity | Manipulated DNN weights installed through a malicious software update | DS-02 |
| TS-03 | A-03 | Integrity | Physical adversarial patch suppresses pedestrian detections | DS-02 |
| TS-04 | A-01 | Availability | Dazzling of the camera with a high-power light source | DS-02, DS-03 |
| TS-05 | A-05 | Integrity | Calibration parameters rewritten via diagnostic services | DS-02 |
| TS-06 | A-06 | Confidentiality | Event clips read out via diagnostic services | DS-04 |
| TS-07 | A-03 | Availability | Flooding of the CAN-FD segment with high-priority frames | DS-03 |

Note: physical-world sensor attacks (TS-03, TS-04) must also be analysed under ISO 21448 (SOTIF) and ISO/PAS 8800.

---

## 4. Impact rating (15.5)

Rate each damage scenario in each category. The impact of a threat scenario is the worst impact of its linked damage scenarios.
Impact is rated **without** the controls that this TARA will define.

| Rating | Safety (ISO 26262 S-class) | Financial (road user) | Operational | Privacy |
|---|---|---|---|---|
| **Severe** | S3: life-threatening or fatal injuries | Catastrophic consequences the road user might not overcome | Loss or impairment of a core vehicle function | Significant harm; highly sensitive, easily linkable data |
| **Major** | S2: severe injuries, survival probable | Substantial consequences the road user can overcome | Loss or impairment of an important vehicle function | Serious harm |
| **Moderate** | S1: light and moderate injuries | Inconvenient consequences, overcome with limited resources | Partial degradation of a vehicle function | Moderate harm |
| **Negligible** | S0: no injuries | No or negligible consequences | No perceived impairment | No or negligible harm |

Optional: add organisation-defined categories for other stakeholders, e.g. OEM recall cost or reputation, in **separate** columns. Do not mix them into the road-user rating.

---

## 5. Attack path analysis (15.6)

List one or more attack paths per threat scenario (OR). Each path is a sequence of steps (AND). The entry step determines the attack vector.
Attack trees are a common notation.

| TS ID | Path ID | Step | Entry vector | Elapsed time | Expertise | Knowledge | Window | Equipment |
|---|---|---|---|---|---|---|---|---|
| TS-xx | AP-xx | 1. [Action] | [N/A/L/P] | | | | | |
| | | 2. [Action] | | | | | | |

*Example (TS-01; values are attack-potential points, Section 6):*

| Path | Step | Vector | ET | Ex | Kn | Win | Eq |
|---|---|---|---|---|---|---|---|
| AP-01a | 1. Remote code execution on the telematics unit | Network | 17 | 6 | 7 | 0 | 4 |
| | 2. Bypass gateway routing to the AEB segment | | 4 | 6 | 7 | 0 | 0 |
| | 3. Forge object-list frames | | 1 | 3 | 3 | 0 | 0 |
| | **Aggregated (factor-wise max)** | | **17** | **6** | **7** | **0** | **4** → **34** |
| AP-01b | 1. Splice a device into CAN-FD wiring at the radar connector | Physical | 1 | 3 | 3 | 4 | 4 |
| | 2. Forge object-list frames | | 1 | 3 | 3 | 0 | 0 |
| | **Aggregated** | | **1** | **3** | **3** | **4** | **4** → **15** |

---

## 6. Attack feasibility rating (15.7)

### 6.1 Attack-potential approach (Annex G.2; values from ISO/IEC 18045)

| Factor | Values |
|---|---|
| Elapsed time | ≤1 day **0** · ≤1 week **1** · ≤1 month **4** · ≤6 months **17** · >6 months **19** |
| Specialist expertise | Layman **0** · Proficient **3** · Expert **6** · Multiple experts **8** |
| Knowledge of the item | Public **0** · Restricted **3** · Confidential **7** · Strictly confidential **11** |
| Window of opportunity | Unlimited **0** · Easy **1** · Moderate **4** · Difficult **10** |
| Equipment | Standard **0** · Specialised **4** · Bespoke **7** · Multiple bespoke **9** |

| Attack potential (sum) | Attack feasibility |
|---|---|
| 0–13 | **High** |
| 14–19 | **Medium** |
| 20–24 | **Low** |
| ≥ 25 | **Very Low** |

A higher attack potential means a harder attack and a lower feasibility. There is no "Very High" class.

### 6.2 Alternative approaches

- **CVSS-based (G.3):** map the CVSS v3.1 *exploitability* sub-score: 2.96–3.89 High, 2.00–2.95 Medium, 1.06–1.99 Low, 0.12–1.05 Very Low.
- **Attack-vector-based (G.4):** Network → High, Adjacent → Medium, Local → Low, Physical → Very Low. This method is coarse. It underrates physical-world sensor attacks, which need no access to the vehicle.

### 6.3 Feasibility per threat scenario

| TS ID | Most feasible path | Attack potential | Feasibility | Vector (best path) | Most remote vector (for CAL) |
|---|---|---|---|---|---|
| TS-xx | AP-xx | | | | |

*Example:*

| TS | Path | AP | Feasibility | Vector (best) | Most remote vector |
|---|---|---|---|---|---|
| TS-01 | AP-01b | 15 | Medium | Physical | Network |
| TS-02 | AP-02b | 41 | Very Low | Local | Network |
| TS-03 | AP-03a | 14 | Medium | Physical | Physical |
| TS-04 | AP-04a | 7 | High | Physical | Physical |
| TS-05 | AP-05a | 21 | Low | Local | Local |
| TS-06 | AP-06a | 21 | Low | Local | Local |
| TS-07 | AP-07a | 11 | High | Physical | Physical |

---

## 7. Risk value determination (15.8)

Example risk matrix (Annex H). The risk value runs from 1 (lowest) to 5 (highest).

| Impact \ Feasibility | Very Low | Low | Medium | High |
|---|---|---|---|---|
| **Severe** | 2 | 3 | 4 | 5 |
| **Major** | 1 | 2 | 3 | 4 |
| **Moderate** | 1 | 2 | 2 | 3 |
| **Negligible** | 1 | 1 | 1 | 1 |

| TS ID | Impact | Feasibility | Risk value |
|---|---|---|---|
| TS-xx | | | |

*Example:* TS-01 Major × Medium = 3; TS-02 Severe × Very Low = 2; TS-03 Severe × Medium = 4; TS-04 Severe × High = 5; TS-05 Severe × Low = 3; TS-06 Major × Low = 2; TS-07 Major × High = 4.

---

## 8. Risk treatment decision (15.9)

**Every** threat scenario gets a decision with a rationale.

| Option | Meaning | Output |
|---|---|---|
| Avoid | Remove the activity or function that causes the risk | Design change |
| Reduce | Apply controls | Cybersecurity goal (Section 9) |
| Share | Transfer, e.g. by contract or insurance | Cybersecurity claim |
| Retain | Accept the risk | Cybersecurity claim |

| TS ID | Risk value | Decision | Rationale | Goal / claim ID |
|---|---|---|---|---|
| TS-xx | | | | |

*Example (policy from Section 0):*

| TS | Risk | Decision | Rationale | Goal/claim |
|---|---|---|---|---|
| TS-01 | 3 | Reduce | Risk ≥ 3 | CG-01 |
| TS-02 | 2 | Reduce | Risk 2 with Severe safety impact | CG-02 |
| TS-03 | 4 | Reduce | Risk ≥ 3 | CG-03 |
| TS-04 | 5 | Reduce | Risk ≥ 3 | CG-04 |
| TS-05 | 3 | Reduce | Risk ≥ 3 | CG-05 |
| TS-06 | 2 | Retain | Within threshold; no Severe safety impact | CC-06 |
| TS-07 | 4 | Reduce | Risk ≥ 3 | CG-07 |

---

## 9. Cybersecurity goals, claims and CAL (clause 9.4; Annex E)

A **cybersecurity goal** is a concept-level requirement to protect an asset's property against a threat scenario. Express it in terms of the property and the threat, not as a specific mechanism.
A **cybersecurity claim** documents why a retained or shared risk is acceptable.

A **CAL** may be assigned to each goal to scale the rigour of assurance activities. The Annex E example (informative) uses **impact × attack vector**:

| Impact \ Attack vector | Physical | Local | Adjacent | Network |
|---|---|---|---|---|
| **Severe** | CAL 2 | CAL 3 | CAL 4 | CAL 4 |
| **Major** | CAL 1 | CAL 2 | CAL 3 | CAL 4 |
| **Moderate** | CAL 1 | CAL 1 | CAL 2 | CAL 3 |
| **Negligible** | – | – | – | – |

A CAL is **not** a risk value and has **no** correspondence to an ASIL.

| ID | Type | TS | Statement | CAL |
|---|---|---|---|---|
| CG-xx / CC-xx | Goal / claim | TS-xx | [Statement] | [1–4 / n/a] |

*Example:*

| ID | Type | TS | Statement | CAL |
|---|---|---|---|---|
| CG-01 | Goal | TS-01 | The integrity of the object list / brake request on CAN-FD shall be protected against forged frames injected on CAN-FD | 4 (Major, Network) |
| CG-02 | Goal | TS-02 | The integrity of the perception DNN weights shall be protected against manipulated software updates | 4 (Severe, Network) |
| CG-03 | Goal | TS-03 | The integrity of the object list shall be protected against physical adversarial patches | 2 (Severe, Physical) |
| CG-04 | Goal | TS-04 | The availability of the camera video stream shall be protected against dazzling (detect and degrade) | 2 (Severe, Physical) |
| CG-05 | Goal | TS-05 | The integrity of the camera calibration parameters shall be protected against modification via diagnostic services | 3 (Severe, Local) |
| CC-06 | Claim | TS-06 | Risk value 2 retained; re-evaluated by cybersecurity monitoring (cl. 8) | n/a |
| CG-07 | Goal | TS-07 | The availability of the object list / brake request shall be protected against bus flooding | 1 (Major, Physical) |

---

## 10. Cybersecurity concept, controls and residual risk (clause 9.5)

Refine each goal into cybersecurity requirements allocated to architecture elements. Then re-rate the feasibility (and the impact, if a control changes the damage scenario) to obtain the residual risk.

| Req ID | Goal | Requirement | Allocated to | Verification method (cl. 10) |
|---|---|---|---|---|
| CR-xx.y | CG-xx | [Requirement] | [Element] | [Test/analysis/review] |

| TS ID | Controls | Effect on feasibility/impact | Residual risk | Acceptable? / approved by |
|---|---|---|---|---|
| TS-xx | | | | |

*Example:*

| TS | Controls | Effect | Residual |
|---|---|---|---|
| TS-01 | AUTOSAR SecOC (truncated CMAC + freshness, keys in HSM); plausibility check in brake ECU | Knowledge → strictly confidential; AP 15 → 26 (Very Low) | 1 |
| TS-02 | Signed packages (ISO 24089 / UN R156 process), secure boot, HSM-protected signing keys | Already Very Low | 2 |
| TS-03 | AEB requires confirmation by the independent radar channel; perception plausibility monitor | AP 14 → 36 (Very Low) | 2 |
| TS-04 | Blinding detection → degraded mode with driver warning | Damage scenario DS-02 → DS-03 (impact Major); feasibility unchanged (High) | 4: needs documented acceptance or further measures |
| TS-05 | UDS Authentication 0x29 (ISO 14229-1:2020, certificate-based) replaces 0x27 seed/key | AP 21 → 29 (Very Low) | 2 |
| TS-07 | Dedicated AEB segment not reachable from bumper connectors; bus-load monitoring | Window → difficult; AP 11 → 17 (Medium) | 3: needs documented acceptance or further measures |

**Match controls to threats.** Link authentication (MAC or signature) protects data **in transit**. It does **not** detect physical-world manipulation of the scene, such as adversarial patches or dazzling. Those need diverse sensing, plausibility checks and robust or monitored ML.

---

## 11. Safety–security interface

| Item | Content |
|---|---|
| Damage scenarios violating safety goals | [DS-xx → SG-xx] |
| Threat scenarios with potential safety impact (to be communicated to the safety team) | [TS list per SG] |
| Security controls credited in the safety concept | [Control, ASIL, independence argument] |
| Safety mechanisms relied on by security | [e.g. none; note that E2E CRC/counters do not provide authenticity] |
| Timing of security controls vs FTTI | [Detection + reaction time ≤ FTTI?] |
| Interface agreement / communication channel | [Reference; ISO 26262-2:2018 Annex E, ISO/SAE 21434 cl. 5] |

*Example:* SG-02 can be violated by TS-02, TS-03, TS-04 and TS-05. Camera blinding detection (3 frames × 33 ms) plus transition to degraded mode (50 ms) takes 149 ms, within the 300 ms FTTI. A backend VSOC response (hours) is **not** a safety mechanism.

---

## 12. Verification (clause 10) and validation (clause 11)

| Activity | Purpose | Applied to |
|---|---|---|
| Requirements-based testing | Verify cybersecurity specifications | All CR |
| Interface testing / fuzzing | Robustness of external and internal interfaces | Interfaces in scope |
| Static analysis, code review | Detect implementation weaknesses | Software in scope |
| Vulnerability scanning | Known vulnerabilities in components (SBOM-based) | All software components |
| Penetration testing | Validate that the goals are achieved at vehicle level (cl. 11) | Item / vehicle |

How rigour can scale with CAL (illustrative; organisation-defined, following the idea of ISO/SAE 21434 Annex E, informative):

| Activity | CAL 1 | CAL 2 | CAL 3 | CAL 4 |
|---|---|---|---|---|
| Penetration testing depth | Basic | Grey-box | Grey-box, extended | White-box, extended |
| Fuzzing | Optional | Recommended | Required | Required, coverage-guided |
| Independence of review/testing | Same team | Different person | Different team | Independent organisation |

| Test ID | Requirement(s) | Method | Result | Open findings |
|---|---|---|---|---|
| T-xx | CR-xx.y | [Method] | [Pass/Fail] | [IDs] |

**Release criterion:** base it on **open** (unremediated) findings, e.g. no open critical or high findings. Remaining findings each need a documented risk assessment (cl. 8.6).

---

## 13. Distributed cybersecurity activities (clause 7)

| Supplier / partner | Component or service | Responsibilities (cybersecurity interface agreement, Annex C) | Evidence |
|---|---|---|---|
| [Name] | [Component] | [Who performs TARA, testing, vulnerability management, incident response] | [Audit, work products] |

*Example:* camera supplier (secure firmware update, vulnerability reporting); ML model supplier (provenance and integrity of weights, training-data governance); OTA backend operator (key management, ISO/IEC 27001 certification).

---

## 14. Continual activities (clause 8) and operations (clause 13)

| Activity | Description | Owner |
|---|---|---|
| Cybersecurity monitoring (8.3) | Collect threat intelligence, vulnerability databases, field data (VSOC) | [Role] |
| Event evaluation (8.4) | Decide whether an event affects this item | [Role] |
| Vulnerability analysis (8.5) | Analyse weaknesses, e.g. with CVSS and attack paths | [Role] |
| Vulnerability management (8.6) | Remediate or document the risk | [Role] |
| Incident response (13.3) | Response plan, communication, remediation | [Role] |
| Updates (13.4) | Secure update per UN R156 / ISO 24089 | [Role] |

**TARA update triggers:**
- [ ] New or changed interface or connectivity
- [ ] Architecture or software change affecting assets
- [ ] New vulnerability or threat intelligence relevant to the item (cl. 8)
- [ ] Security incident in the field or at a comparable product
- [ ] Organisation-defined periodic review (interval: [ ]), e.g. to keep the UN R155 CSMS evidence current
- [ ] Change of end-of-support date (cl. 14)

---

## 15. Assumptions, open issues and approval

### Assumptions

| ID | Assumption | Validated by |
|---|---|---|
| AS-xx | [e.g. gateway blocks diagnostic write services while the vehicle is moving] | [Reference] |

### Open issues

| ID | Description | Owner | Target date |
|---|---|---|---|
| | | | |

### Review history

| Date | Reviewer | Comments | Status |
|---|---|---|---|
| | | | |

### Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Cybersecurity manager (item) | | | |
| Functional safety manager (interface review) | | | |
| Product owner / project manager | | | |

---

## Notes and common mistakes

1. **Follow the order of clause 15.** Damage scenarios come with the assets, and impact is rated *before* attack path analysis.
2. **Feasibility direction.** Layman, public information, standard equipment and an unlimited window mean **high** feasibility.
3. **Road-user perspective.** Do not rate impact by OEM financial loss.
4. **Every threat scenario gets a treatment decision**, including retained risks, which need a claim.
5. **CAL ≠ risk, CAL ≠ ASIL.** Do not derive a CAL from the risk value, and do not "align" it with the ASIL.
6. **Physical-world sensor attacks** are cheap and need no vehicle access. The attack-vector method and CVSS underrate them, so prefer the attack-potential method.
7. **E2E protection (CRC/counter) is not authentication.** Use a keyed MAC (e.g. SecOC) against forgery.
8. **V2X signatures are not encryption**, and a valid signature does not make the content true.
9. Keep normative statements traceable to the standard's clause numbers. Mark informative examples as such.

---

**Template version:** 2.0 (October 2026)
**Reference standards:** ISO/SAE 21434:2021; ISO 26262:2018; UN R155, UN R156; ISO 24089:2023; ISO/SAE PAS 5112:2022
**Companion notebook:** [`05_Cybersecurity_ISO21434/02_tara.ipynb`](../05_Cybersecurity_ISO21434/02_tara.ipynb)
**Author:** Milin Patel · Hochschule Kempten · MIT Licence
