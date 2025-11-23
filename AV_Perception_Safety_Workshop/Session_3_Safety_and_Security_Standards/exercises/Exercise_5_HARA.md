# Exercise 5: Hazard Analysis and Risk Assessment (HARA) for Automated Emergency Braking

**Difficulty:** Intermediate
**Prerequisites:** Completed Notebook 11 (ISO 26262)

---

## Learning Objectives

By completing this exercise, you will:
- ✓ Apply the complete HARA methodology to a real system
- ✓ Practice severity, exposure, and controllability assessment
- ✓ Determine ASIL levels systematically
- ✓ Derive safety goals from hazards
- ✓ Create functional safety requirements

---

## System Description

### Item Definition

**System Name:** Automated Emergency Braking (AEB) System with Pedestrian Detection

**Function:** Detect pedestrians in the vehicle's path and automatically apply emergency braking to avoid or mitigate collisions.

**System Components:**
1. **Front-facing camera** (1920×1080, 30 fps)
2. **Short-range radar** (77 GHz, range 0-80m)
3. **Perception ECU** (runs deep learning pedestrian detection)
4. **Brake control interface** (to brake-by-wire system)
5. **Driver warning interface** (visual + auditory alerts)

**System Boundaries:**
- **Inputs:**
  - Camera images
  - Radar point cloud
  - Vehicle speed (from vehicle network)
  - Steering angle
  - Brake pedal position
  - System enable/disable state

- **Outputs:**
  - Brake pressure command
  - Driver warning signals
  - System status

**Operational Design Domain (ODD):**
- **Speed range:** 5-80 km/h
- **Environment:** Urban and suburban roads
- **Weather:** Clear, light rain (heavy rain excluded)
- **Lighting:** Daytime and well-lit nighttime
- **Road type:** Paved roads with clear visibility

---

## Part 1: Operational Situation Analysis

Identify at least **5 operational situations** where the AEB system operates.

### Task 1.1: Define Operational Situations

Complete the table below:

| ID | Operational Situation | Description | Speed | Environment | Road Users |
|----|----------------------|-------------|-------|-------------|------------|
| OS-01 | Urban crosswalk | Pedestrian crossing at marked crosswalk in city | 30-50 km/h | Urban, clear weather, daylight | Pedestrian, other vehicles |
| OS-02 | [Your answer] | | | | |
| OS-03 | [Your answer] | | | | |
| OS-04 | [Your answer] | | | | |
| OS-05 | [Your answer] | | | | |

**Hints:**
- Consider different locations (urban, suburban, highway exit)
- Consider different pedestrian types (adult, child, cyclist)
- Consider different traffic situations (heavy traffic, isolated road)
- Consider time of day and weather variations

---

## Part 2: Hazard Identification

For each operational situation, identify hazardous events that could occur.

### Task 2.1: Identify Malfunctions

What could go wrong with the AEB system?

Potential malfunctions (check all that apply and add your own):
- [ ] Camera fails to detect pedestrian (false negative)
- [ ] Late detection of pedestrian
- [ ] Misclassification (pedestrian as non-pedestrian)
- [ ] False positive detection (phantom braking)
- [ ] Insufficient braking force applied
- [ ] Brake applied too late
- [ ] System fails to activate (stuck OFF)
- [ ] System activates unnecessarily (stuck ON)
- [ ] [Your malfunction]: ___________________
- [ ] [Your malfunction]: ___________________

### Task 2.2: Define Hazardous Events

Complete the HARA table (at least 6 hazards):

| Hazard ID | Operational Situation | Malfunction | Hazardous Event | Potential Harm |
|-----------|----------------------|-------------|-----------------|----------------|
| H-001 | OS-01 | Camera fails to detect pedestrian | Vehicle does not brake, collides with pedestrian | Severe/fatal pedestrian injury |
| H-002 | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| H-003 | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| H-004 | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| H-005 | [Your answer] | [Your answer] | [Your answer] | [Your answer] |
| H-006 | [Your answer] | [Your answer] | [Your answer] | [Your answer] |

**Hint:** Consider both "failure to brake" and "unwanted braking" scenarios.

---

## Part 3: Hazard Classification

For each hazard, determine Severity (S), Exposure (E), and Controllability (C).

### Task 3.1: Rate Severity (S)

For each hazard, determine severity using these guidelines:

| Rating | Description | Examples |
|--------|-------------|----------|
| S0 | No injuries | Only property damage |
| S1 | Light/moderate injuries | Bruises, minor whiplash |
| S2 | Severe injuries (survival probable) | Broken bones, severe whiplash |
| S3 | Life-threatening/fatal (survival uncertain) | Fatal pedestrian collision |

### Task 3.2: Rate Exposure (E)

For each hazard, determine exposure probability:

| Rating | Description | Interpretation |
|--------|-------------|----------------|
| E0 | Incredibly unlikely | < 0.1% of driving time |
| E1 | Very low | < 1% of driving time |
| E2 | Low | < 10% of driving time |
| E3 | Medium | < 50% of driving time (e.g., daily urban driving) |
| E4 | High | ≥ 50% of driving time |

### Task 3.3: Rate Controllability (C)

For each hazard, determine controllability by driver:

| Rating | Description | Driver Ability |
|--------|-------------|----------------|
| C0 | Controllable in general | > 99% of drivers can avoid harm |
| C1 | Simply controllable | > 90% of drivers, simple reaction |
| C2 | Normally controllable | > 80% of drivers, normal complexity |
| C3 | Difficult/uncontrollable | < 80% of drivers OR uncontrollable |

### Task 3.4: Complete Classification

Fill in S, E, C ratings:

| Hazard ID | Operational Situation | Severity (S) | Exposure (E) | Controllability (C) |
|-----------|----------------------|--------------|--------------|---------------------|
| H-001 | OS-01 | S3 | E4 | C3 |
| H-002 | [Your OS] | [Your rating] | [Your rating] | [Your rating] |
| H-003 | [Your OS] | [Your rating] | [Your rating] | [Your rating] |
| H-004 | [Your OS] | [Your rating] | [Your rating] | [Your rating] |
| H-005 | [Your OS] | [Your rating] | [Your rating] | [Your rating] |
| H-006 | [Your OS] | [Your rating] | [Your rating] | [Your rating] |

**Justification Required:** For each rating, briefly explain your reasoning.

**Example for H-001:**
- **S3**: Pedestrian collision at 30-50 km/h is life-threatening/fatal
- **E4**: Urban driving with crosswalks is very common (>50% of operating time)
- **C3**: Driver unlikely to notice and react in time (< 0.5 seconds available)

Your justifications:
- **H-002:** _________________________________
- **H-003:** _________________________________
- **H-004:** _________________________________
- **H-005:** _________________________________
- **H-006:** _________________________________

---

## Part 4: ASIL Determination

Using the ASIL determination matrix, calculate ASIL for each hazard.

### ASIL Matrix Reference

For **Severity S3**:

|     | E1 | E2 | E3 | E4 |
|-----|----|----|----|----|
| C1  | A  | B  | B  | C  |
| C2  | B  | C  | C  | D  |
| C3  | C  | D  | D  | D  |

(Refer to Notebook 11 for complete matrices)

### Task 4.1: Determine ASIL

| Hazard ID | S | E | C | ASIL | Priority |
|-----------|---|---|---|------|----------|
| H-001 | S3 | E4 | C3 | **D** | Highest |
| H-002 | | | | | |
| H-003 | | | | | |
| H-004 | | | | | |
| H-005 | | | | | |
| H-006 | | | | | |

### Task 4.2: Analysis Questions

1. **Which hazards are ASIL D?** ___________________
2. **What percentage of your hazards are ASIL C or D?** ___________________
3. **Are there any QM (Quality Management only) hazards?** ___________________
4. **Which hazard has the highest risk if the ASIL is the same?** (Consider secondary factors) ___________________

---

## Part 5: Safety Goals and Requirements

Derive safety goals from ASIL-rated hazards.

### Task 5.1: Define Safety Goals

For each hazard with ASIL ≥ B, define a safety goal:

| Safety Goal ID | Related Hazard(s) | ASIL | Safety Goal | Safe State |
|----------------|-------------------|------|-------------|------------|
| SG-001 | H-001 | D | Prevent collision with pedestrians due to detection failure | Emergency braking applied with driver warning OR controlled deceleration with takeover request |
| SG-002 | [Your answer] | | [Your answer] | [Your answer] |
| SG-003 | [Your answer] | | [Your answer] | [Your answer] |
| SG-004 | [Your answer] | | [Your answer] | [Your answer] |

**Safety Goal Guidelines:**
- Must be clear and measurable
- Must state what to prevent
- Must define acceptable safe state
- Should be technology-independent (high-level)

### Task 5.2: Functional Safety Requirements

For SG-001, derive at least **4 functional safety requirements**:

| FSR ID | Safety Goal | ASIL | Functional Safety Requirement | Verification Method |
|--------|-------------|------|-------------------------------|---------------------|
| FSR-001.1 | SG-001 | D | System shall detect pedestrians within 50m with ≥99.9% true positive rate | Scenario-based testing with 10,000+ cases |
| FSR-001.2 | SG-001 | D | [Your requirement] | [Your method] |
| FSR-001.3 | SG-001 | D | [Your requirement] | [Your method] |
| FSR-001.4 | SG-001 | D | [Your requirement] | [Your method] |

**Hints for requirements:**
- Detection performance (accuracy, range, latency)
- Classification accuracy
- Braking response time
- Sensor redundancy
- Fault detection and monitoring
- Driver warning mechanisms

---

## Bonus Challenge (Optional, +15 minutes)

### Challenge 1: Multi-Sensor Redundancy

Given that camera-only detection is insufficient for ASIL D, design a multi-sensor architecture:

1. **Which sensors would you use?** (Choose at least 2)
   - [ ] Camera
   - [ ] LIDAR
   - [ ] Radar
   - [ ] Ultrasonic
   - [ ] Infrared

2. **How would you combine them?**
   - Sensor fusion approach: ___________________
   - Voting/arbitration strategy: ___________________
   - Failure detection: ___________________

3. **Update FSR-001 requirements** to reflect multi-sensor architecture.

### Challenge 2: Integration with SOTIF

For H-001 (pedestrian detection failure):

1. **Identify triggering conditions** (performance limitations):
   - ___________________
   - ___________________
   - ___________________

2. **Categorize scenarios:**
   - S1 (Known Safe): ___________________
   - S2 (Known Unsafe): ___________________
   - S3/S4 (Unknown): ___________________

3. **How does SOTIF complement HARA for this hazard?**
   - ___________________

---

## Submission Checklist

Before completing this exercise, ensure you have:

- [ ] Identified at least 5 operational situations
- [ ] Defined at least 6 hazards
- [ ] Rated S, E, C for all hazards with justification
- [ ] Determined ASIL for all hazards
- [ ] Defined safety goals for all ASIL B+ hazards
- [ ] Created functional safety requirements for SG-001
- [ ] Answered all analysis questions
- [ ] (Optional) Completed bonus challenges

---

## Self-Assessment Questions

1. **What is the primary difference between a malfunction and a hazard?**
   - Answer: ___________________

2. **Why is pedestrian detection typically ASIL D?**
   - Answer: ___________________

3. **What's the difference between a Safety Goal and a Functional Safety Requirement?**
   - Answer: ___________________

4. **Why do we need SOTIF in addition to ISO 26262 for AEB systems?**
   - Answer: ___________________

5. **How would cybersecurity (ISO/SAE 21434) relate to this HARA?**
   - Answer: ___________________

---

## Solution Hints

**Hint for OS-02:** Consider suburban school zone with children

**Hint for H-002:** What if detection is late (but not absent)?

**Hint for H-003:** False positive on highway → rear-end collision

**Typical ASIL distribution:**
- ASIL D: 30-40% (critical safety scenarios)
- ASIL C: 20-30% (significant safety scenarios)
- ASIL B: 20-30% (moderate safety scenarios)
- ASIL A: 10-20% (minor safety scenarios)
- QM: 5-10% (no safety impact)

---

## Additional Resources

- ISO 26262-3:2018 (Concept Phase)
- ISO 26262-9:2018 (ASIL-oriented analysis)
- HARA_Template.md in templates folder
- Notebook 11: ISO 26262 Functional Safety

---

**Next Exercise:** Exercise 6 - TARA for V2X Communication

**Questions?** Refer to the workshop discussion forum or instructor.

---

© 2024 AV Perception Safety Workshop
