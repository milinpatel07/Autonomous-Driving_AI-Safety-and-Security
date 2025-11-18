# Exercise 6: Threat Analysis and Risk Assessment (TARA) for V2X Communication

**Estimated Time:** 45 minutes
**Difficulty:** Intermediate to Advanced
**Prerequisites:** Completed Notebook 14 (ISO/SAE 21434)

---

## Learning Objectives

By completing this exercise, you will:
- ✓ Apply TARA methodology to a vehicle communication system
- ✓ Identify cybersecurity assets and their properties
- ✓ Analyze threat scenarios and attack vectors
- ✓ Assess attack feasibility using the 5-factor model
- ✓ Determine CAL (Cybersecurity Assurance Level)
- ✓ Derive cybersecurity requirements

---

## System Description

### Item Definition

**System Name:** Vehicle-to-Everything (V2X) Communication System for Cooperative Perception

**Function:** Enable vehicles to share and receive real-time information about road conditions, hazards, and nearby vehicles/pedestrians to enhance autonomous driving perception.

**System Components:**
1. **V2X Communication Module** (DSRC/C-V2X radio)
2. **Security Module** (PKI certificates, encryption)
3. **Message Processing Unit** (validate and integrate V2X messages)
4. **Integration with Perception System** (fuses V2X data with sensor data)
5. **Cloud Backend** (certificate management, revocation lists)

**Communication Types:**
- **V2V (Vehicle-to-Vehicle):** Position, speed, trajectory sharing
- **V2I (Vehicle-to-Infrastructure):** Traffic signals, roadwork warnings
- **V2P (Vehicle-to-Pedestrian):** Pedestrian location warnings
- **V2N (Vehicle-to-Network):** Cloud-based services, map updates

**Message Types:**
- Basic Safety Message (BSM): Position, speed, heading (10 Hz)
- Cooperative Awareness Message (CAM): Vehicle status
- Decentralized Environmental Notification (DENM): Hazard warnings
- Signal Phase and Timing (SPaT): Traffic signal status
- Pedestrian Safety Message (PSM): Pedestrian location

---

## Part 1: Asset Identification (10 minutes)

Identify assets that require protection and their cybersecurity properties.

### Task 1.1: Identify Assets

Complete the asset table:

| Asset ID | Asset Name | Asset Type | Cybersecurity Property | Value | Justification |
|----------|------------|------------|----------------------|-------|---------------|
| A-001 | V2V position data | Data | **I** (Integrity) | Critical | False position data could cause collision |
| A-002 | [Your answer] | [Data/SW/HW/Function] | [C/I/A] | [Critical/High/Medium/Low] | [Justification] |
| A-003 | [Your answer] | | | | |
| A-004 | [Your answer] | | | | |
| A-005 | [Your answer] | | | | |
| A-006 | [Your answer] | | | | |

**Cybersecurity Properties:**
- **C (Confidentiality):** Prevent unauthorized disclosure
- **I (Integrity):** Prevent unauthorized modification
- **A (Availability):** Ensure authorized access when needed

**Hints:** Consider:
- Message data (BSM, CAM, DENM, SPaT, PSM)
- Cryptographic keys and certificates
- Software/firmware
- Communication channels
- Vehicle location/trajectory privacy
- Certificate revocation lists

### Task 1.2: Critical Asset Analysis

**Question 1:** Which asset(s) are most critical to safety?
- Answer: ___________________
- Why: ___________________

**Question 2:** Which asset(s) are most critical to privacy?
- Answer: ___________________
- Why: ___________________

**Question 3:** Can any assets have multiple cybersecurity properties? Give an example.
- Answer: ___________________

---

## Part 2: Threat Actor and Attack Goal Identification (5 minutes)

Identify relevant threat actors and their potential goals.

### Task 2.1: Threat Actors

Which threat actors are relevant for V2X systems? (Check all that apply)

- [ ] Script kiddie (curiosity, pranks)
- [ ] Skilled individual (demonstration, fame)
- [ ] Organized crime (financial gain, ransomware)
- [ ] Competitor (industrial espionage)
- [ ] Terrorist (cause harm, disruption)
- [ ] Nation state (strategic advantage, espionage)
- [ ] Malicious insider (revenge, financial gain)
- [ ] Privacy activist (expose surveillance)

**Most Relevant Actors for This System:**
1. ___________________
2. ___________________
3. ___________________

### Task 2.2: Attack Goals

What might attackers want to achieve? (Check all that apply and add your own)

- [ ] Cause vehicle collision (safety impact)
- [ ] Track vehicle movements (privacy breach)
- [ ] Disrupt traffic flow (availability attack)
- [ ] Steal vehicle/fleet data
- [ ] Demonstrate vulnerability (researcher, activist)
- [ ] Create traffic chaos (terrorist)
- [ ] [Your goal]: ___________________
- [ ] [Your goal]: ___________________

---

## Part 3: Threat Scenario Development (15 minutes)

Develop threat scenarios for identified assets.

### Task 3.1: Define Threat Scenarios

Complete the threat scenario table (at least 6 threats):

| Threat ID | Asset ID | Threat Scenario | Attack Vector | Threat Actor | Attack Goal |
|-----------|----------|-----------------|---------------|--------------|-------------|
| T-001 | A-001 | Injection of false V2V position messages | Rogue V2X transmitter broadcasting fake BSMs | Skilled individual | Cause collision or dangerous maneuver |
| T-002 | [Your answer] | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| T-003 | [Your answer] | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| T-004 | [Your answer] | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| T-005 | [Your answer] | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| T-006 | [Your answer] | [Your answer] | [Your answer] | [Your answer] | [Your answer] |

**Example Threat Scenarios to Consider:**
- Message injection (false data)
- Message replay (replay old messages)
- Jamming attack (denial of service)
- Privacy tracking (monitor vehicle movements)
- Certificate theft or compromise
- Sybil attack (create multiple fake identities)
- Man-in-the-middle attack on backend communication
- Firmware/software compromise

### Task 3.2: Attack Vector Details

For each threat, describe the technical attack vector in detail:

**T-001 Attack Vector Detail:**
Attacker uses a software-defined radio (SDR) or modified V2X module to broadcast BSM messages with false position coordinates (e.g., claiming to be at an intersection when not present). Receiver vehicle processes the false message and may brake unnecessarily or make wrong maneuver decisions.

**T-002 Attack Vector Detail:**
___________________

**T-003 Attack Vector Detail:**
___________________

(Continue for all threats)

---

## Part 4: Impact Assessment (5 minutes)

Rate the impact of successful attacks on four dimensions.

### Task 4.1: Impact Rating

Rate each threat's impact (1-4):

| Threat ID | Safety Impact | Financial Impact | Operational Impact | Privacy Impact | Overall Impact |
|-----------|--------------|------------------|-------------------|----------------|----------------|
| T-001 | 4 | 2 | 3 | 1 | **4** |
| T-002 | | | | | |
| T-003 | | | | | |
| T-004 | | | | | |
| T-005 | | | | | |
| T-006 | | | | | |

**Impact Scale:**
- **4 - Severe:** Fatalities probable / >$10M / Complete system failure / Massive breach
- **3 - Major:** Serious injuries / $1M-$10M / Major degradation / Significant breach
- **2 - Moderate:** Minor injuries / $100K-$1M / Partial degradation / Limited breach
- **1 - Negligible:** No injuries / <$100K / Minor impact / No privacy impact

### Task 4.2: Impact Justification

Provide justification for your impact ratings:

**T-001 Justification:**
- Safety: 4 (False position data could cause emergency braking or collision at highway speeds)
- Financial: 2 (Moderate damage from single incident, but potential liability)
- Operational: 3 (V2X system effectiveness degraded, may need to disable)
- Privacy: 1 (No privacy impact from this specific attack)

**T-002 Justification:**
___________________

(Continue for all threats)

---

## Part 5: Attack Feasibility Assessment (10 minutes)

Assess attack feasibility using the 5-factor model.

### Feasibility Factors

Rate each factor 0-10 based on these criteria:

| Factor | 0 (Very Low) | 1 (Low) | 4 (Medium) | 7 (High) | 10 (Very High) |
|--------|-------------|---------|------------|----------|----------------|
| **Elapsed Time** | > 1 year | 6-12 months | 3-6 months | 1-3 months | < 1 month |
| **Specialist Expertise** | Layman | Proficient | Expert | Multiple experts | Nation state |
| **Knowledge of Item** | Public | Restricted | Confidential | Strictly confidential | Top secret |
| **Window of Opportunity** | Unlimited | Easy | Moderate | Difficult | Very difficult |
| **Equipment** | Standard | Specialized | Bespoke | Multiple bespoke | State-level |

### Task 5.1: Feasibility Assessment

| Threat ID | Time | Expertise | Knowledge | Opportunity | Equipment | Total | Feasibility Rating |
|-----------|------|-----------|-----------|-------------|-----------|-------|-------------------|
| T-001 | 1 | 4 | 1 | 0 | 4 | **10** | **Low** |
| T-002 | | | | | | | |
| T-003 | | | | | | | |
| T-004 | | | | | | | |
| T-005 | | | | | | | |
| T-006 | | | | | | | |

**Feasibility Rating Scale:**
- 0-9: Very Low
- 10-17: Low
- 18-24: Medium
- 25-33: High
- 34+: Very High

### Task 5.2: Feasibility Justification

**T-001 Justification:**
- Time: 1 (SDR tools and V2X protocol specs readily available, < 1 week to implement)
- Expertise: 4 (Requires expert knowledge of V2X protocols and SDR programming)
- Knowledge: 1 (V2X message formats are public standards)
- Opportunity: 0 (Can attack from roadside, unlimited access in public areas)
- Equipment: 4 (Requires SDR or modified V2X module, bespoke but obtainable ~$5K)

**T-002 Justification:**
___________________

(Continue for all threats)

---

## Part 6: Risk Determination (5 minutes)

Combine impact and feasibility to determine risk level.

### Risk Matrix

|                | Very Low Feasibility | Low Feasibility | Medium Feasibility | High Feasibility | Very High Feasibility |
|----------------|---------------------|-----------------|-------------------|------------------|-----------------------|
| **Impact 4**   | Medium | High | High | Critical | Critical |
| **Impact 3**   | Low | Medium | High | High | Critical |
| **Impact 2**   | Low | Low | Medium | Medium | High |
| **Impact 1**   | Negligible | Low | Low | Medium | Medium |

### Task 6.1: Risk Assessment

| Threat ID | Impact | Feasibility | Risk Level | Treatment Decision | Priority |
|-----------|--------|-------------|------------|-------------------|----------|
| T-001 | 4 | Low | **High** | **Reduce** | High |
| T-002 | | | | | |
| T-003 | | | | | |
| T-004 | | | | | |
| T-005 | | | | | |
| T-006 | | | | | |

**Treatment Options:**
- **Avoid:** Remove functionality
- **Reduce:** Implement mitigations
- **Share:** Transfer risk (insurance, third party)
- **Retain:** Accept risk (if acceptable)

### Task 6.2: CAL Determination

Based on risk level, determine CAL:

| Risk Level | CAL |
|------------|-----|
| Negligible | No CAL |
| Low | CAL 1 |
| Medium | CAL 2 |
| High | CAL 3 |
| Critical | CAL 4 |

| Threat ID | Risk Level | CAL |
|-----------|------------|-----|
| T-001 | High | **3** |
| T-002 | | |
| T-003 | | |
| T-004 | | |
| T-005 | | |
| T-006 | | |

---

## Part 7: Cybersecurity Goals and Requirements (5 minutes)

Derive cybersecurity goals and requirements from threats.

### Task 7.1: Cybersecurity Goals

Define high-level cybersecurity goals:

| CG ID | Related Threat(s) | CAL | Cybersecurity Goal |
|-------|-------------------|-----|-------------------|
| CG-001 | T-001 | 3 | Ensure authenticity and integrity of V2V messages |
| CG-002 | [Your answer] | | [Your answer] |
| CG-003 | [Your answer] | | [Your answer] |
| CG-004 | [Your answer] | | [Your answer] |

### Task 7.2: Cybersecurity Requirements

For CG-001, derive at least **4 detailed cybersecurity requirements**:

| CR ID | CG ID | CAL | Requirement | Verification Method |
|-------|-------|-----|-------------|---------------------|
| CR-001.1 | CG-001 | 3 | All V2V messages shall be signed using ECDSA-256 or equivalent | Code review + protocol testing |
| CR-001.2 | CG-001 | 3 | [Your requirement] | [Your method] |
| CR-001.3 | CG-001 | 3 | [Your requirement] | [Your method] |
| CR-001.4 | CG-001 | 3 | [Your requirement] | [Your method] |

**Hints for Requirements:**
- Message authentication (PKI, signatures)
- Message freshness checks (timestamps, nonces)
- Plausibility validation (cross-check with sensors)
- Rate limiting and anomaly detection
- Certificate management and revocation
- Secure key storage (HSM, TPM)
- Privacy protection (pseudonymity, certificate rotation)

---

## Bonus Challenge (Optional, +15 minutes)

### Challenge 1: Privacy vs. Security Trade-off

V2X systems have a tension between security and privacy:
- **Security:** Need to authenticate senders (traceability)
- **Privacy:** Don't want to track individual vehicles

**Questions:**
1. How can we achieve both? ___________________
2. What role do pseudonym certificates play? ___________________
3. How often should pseudonym certificates rotate? ___________________
4. What are the security risks of pseudonym rotation? ___________________

### Challenge 2: Integration with ISO 26262

For T-001 (false V2V message injection):

1. **What safety hazards (HARA) could this trigger?**
   - Hazard: ___________________
   - ASIL: ___________________

2. **Combined safety-security requirement:**
   - ___________________

3. **Should CAL match ASIL?**
   - Answer: ___________________
   - Justification: ___________________

### Challenge 3: Incident Response

Assume a successful attack is detected (false messages being received):

1. **Detection:** How would you detect this attack in real-time?
   - ___________________

2. **Response:** What should the vehicle do immediately?
   - ___________________

3. **Recovery:** How do you restore normal operation?
   - ___________________

4. **Reporting:** Who should be notified and when?
   - ___________________

---

## Submission Checklist

Before completing this exercise, ensure you have:

- [ ] Identified at least 6 assets with cybersecurity properties
- [ ] Defined at least 6 threat scenarios
- [ ] Assessed impact (Safety, Financial, Operational, Privacy) for all threats
- [ ] Rated attack feasibility using 5 factors for all threats
- [ ] Determined risk level and CAL for all threats
- [ ] Defined cybersecurity goals for main threats
- [ ] Created detailed cybersecurity requirements for CG-001
- [ ] Answered all analysis questions
- [ ] (Optional) Completed bonus challenges

---

## Self-Assessment Questions

1. **What's the difference between a threat and a vulnerability?**
   - Answer: ___________________

2. **Why is attack feasibility assessment important?**
   - Answer: ___________________

3. **How does TARA differ from HARA?**
   - Answer: ___________________

4. **Why is V2X security critical for autonomous driving safety?**
   - Answer: ___________________

5. **What is the biggest challenge in securing V2X communication?**
   - Answer: ___________________

---

## Solution Hints

**Asset Hints:**
- V2V/V2I/V2P message data (integrity)
- Private encryption keys (confidentiality)
- PKI certificates (integrity, availability)
- Certificate revocation list (integrity, availability)
- Vehicle location/trajectory data (confidentiality - privacy)
- V2X firmware (integrity)

**Threat Hints:**
- Message replay attack (replay old messages)
- Jamming/DoS attack (block V2X communication)
- Sybil attack (create multiple fake vehicles)
- Privacy tracking (correlate pseudonyms)
- Certificate theft from compromised vehicle
- Backend PKI compromise

**Typical CAL Distribution:**
- CAL 4: ~20% (critical threats to safety/fleet)
- CAL 3: ~30% (high impact threats)
- CAL 2: ~30% (medium impact)
- CAL 1: ~20% (low impact)

---

## Additional Resources

- ISO/SAE 21434:2021 (Cybersecurity Engineering)
- SAE J2735 (V2X Message Set Dictionary)
- IEEE 1609.2 (V2X Security Services)
- ETSI TS 103 097 (V2X Security Header and Certificate Formats)
- TARA_Template.md in templates folder
- Notebook 14: ISO/SAE 21434 Cybersecurity

---

**Previous Exercise:** Exercise 5 - HARA for AEB System

**Questions?** Refer to the workshop discussion forum or instructor.

---

© 2024 AV Perception Safety Workshop
