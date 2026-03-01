# HARA Template: Hazard Analysis and Risk Assessment (ISO 26262)

## Document Information

| Field | Value |
|-------|-------|
| **System/Item Name** | [Enter system name] |
| **Version** | [Version number] |
| **Date** | [Date] |
| **Prepared by** | [Name/Team] |
| **Reviewed by** | [Name/Team] |
| **Status** | Draft / In Review / Approved |

---

## 1. Item Definition

### 1.1 System Description

**Item Name:** [System or function being analyzed]

**Purpose:** [Brief description of intended functionality]

**System Boundaries:**
- Input interfaces: [List all inputs]
- Output interfaces: [List all outputs]
- Dependencies: [Other systems this item depends on]
- Operational Design Domain (ODD): [Where/when the system operates]

**Example:**
```
Item Name: Pedestrian Detection and Emergency Braking System
Purpose: Detect pedestrians in the vehicle path and automatically apply brakes to avoid collision
System Boundaries:
  - Inputs: Camera images, LIDAR point cloud, vehicle speed, brake status
  - Outputs: Brake command, driver warning
  - Dependencies: Brake-by-wire system, sensor systems
  - ODD: Urban/suburban roads, speeds 0-60 km/h, daylight and twilight
```

### 1.2 System Architecture

[Insert or describe system architecture diagram]

**Key Components:**
1. [Component 1]: [Description]
2. [Component 2]: [Description]
3. [Component 3]: [Description]

---

## 2. Operational Situations

List all relevant operational situations where the system functions:

| ID | Operational Situation | Description | Environmental Conditions | Speed Range |
|----|----------------------|-------------|-------------------------|-------------|
| OS-01 | [Situation name] | [Description] | [Weather, lighting, road] | [Speed range] |
| OS-02 | | | | |
| OS-03 | | | | |

**Example:**
| ID | Operational Situation | Description | Environmental Conditions | Speed Range |
|----|----------------------|-------------|-------------------------|-------------|
| OS-01 | Urban crosswalk | Pedestrian crossing at marked crosswalk | Clear weather, daylight | 30-50 km/h |
| OS-02 | Highway exit | Pedestrian near highway exit ramp | Clear weather, day/night | 60-80 km/h |
| OS-03 | School zone | Children crossing near school | Various weather | 20-40 km/h |

---

## 3. Hazard Identification

For each operational situation, identify potential hazardous events:

| Hazard ID | Operational Situation | Malfunction/Triggering Event | Hazardous Event | Potential Harm |
|-----------|----------------------|------------------------------|-----------------|----------------|
| H-001 | [OS ID] | [What goes wrong] | [Resulting hazardous condition] | [Potential consequences] |
| H-002 | | | | |
| H-003 | | | | |

**Example:**
| Hazard ID | Operational Situation | Malfunction/Triggering Event | Hazardous Event | Potential Harm |
|-----------|----------------------|------------------------------|-----------------|----------------|
| H-001 | OS-01 | Camera fails to detect pedestrian | Vehicle does not brake, collision with pedestrian | Severe/fatal pedestrian injury |
| H-002 | OS-02 | Late detection due to processing delay | Insufficient time to brake | Severe injury |
| H-003 | OS-03 | False positive detection | Unnecessary emergency braking | Rear-end collision |

---

## 4. Hazard Classification

### 4.1 Severity (S) Rating

Rate the potential harm severity:

| Rating | Category | Description | Examples |
|--------|----------|-------------|----------|
| **S0** | No injuries | No harm to persons | Property damage only |
| **S1** | Light/moderate injuries | Recoverable injuries | Bruises, minor cuts |
| **S2** | Severe/life-threatening (survival probable) | Significant injuries | Broken bones, internal injuries |
| **S3** | Life-threatening/fatal (survival uncertain) | Critical or fatal injuries | Fatal collision |

### 4.2 Exposure (E) Rating

Rate the probability of the operational situation occurring:

| Rating | Category | Probability | Description |
|--------|----------|-------------|-------------|
| **E0** | Incredible | < 0.1% of operating time | Extremely unlikely scenario |
| **E1** | Very low probability | < 1% of operating time | Rare occurrence |
| **E2** | Low probability | < 10% of operating time | Occasional occurrence |
| **E3** | Medium probability | < 50% of operating time | Frequent occurrence |
| **E4** | High probability | ≥ 50% of operating time | Very common |

### 4.3 Controllability (C) Rating

Rate the ability of driver/other road users to avoid harm:

| Rating | Category | Description |
|--------|----------|-------------|
| **C0** | Controllable in general | > 99% of drivers can avoid harm |
| **C1** | Simply controllable | > 90% of drivers can avoid harm with simple actions |
| **C2** | Normally controllable | > 80% of drivers can avoid harm with normal complexity |
| **C3** | Difficult/uncontrollable | < 80% of drivers can avoid harm OR uncontrollable |

---

## 5. HARA Table

Complete HARA analysis for each identified hazard:

| Hazard ID | Operational Situation | Severity (S) | Exposure (E) | Controllability (C) | ASIL | Safety Goal |
|-----------|----------------------|--------------|--------------|---------------------|------|-------------|
| H-001 | [OS ID] | S[0-3] | E[0-4] | C[0-3] | [QM/A/B/C/D] | [Safety goal] |
| H-002 | | | | | | |
| H-003 | | | | | | |

**Example:**
| Hazard ID | Operational Situation | Severity (S) | Exposure (E) | Controllability (C) | ASIL | Safety Goal |
|-----------|----------------------|--------------|--------------|---------------------|------|-------------|
| H-001 | OS-01 | S3 | E4 | C3 | **D** | SG-001: Prevent collision with pedestrians due to non-detection |
| H-002 | OS-02 | S3 | E3 | C3 | **D** | SG-002: Ensure timely pedestrian detection |
| H-003 | OS-03 | S2 | E3 | C2 | **C** | SG-003: Prevent false positive detections causing unnecessary braking |

---

## 6. ASIL Determination Matrix

Use this matrix to determine ASIL based on S, E, C:

### For Severity S1:

|     | E1 | E2 | E3 | E4 |
|-----|----|----|----|----|
| C1  | QM | QM | QM | A  |
| C2  | QM | A  | A  | B  |
| C3  | A  | B  | B  | C  |

### For Severity S2:

|     | E1 | E2 | E3 | E4 |
|-----|----|----|----|----|
| C1  | QM | A  | A  | B  |
| C2  | A  | B  | B  | C  |
| C3  | B  | C  | C  | D  |

### For Severity S3:

|     | E1 | E2 | E3 | E4 |
|-----|----|----|----|----|
| C1  | A  | B  | B  | C  |
| C2  | B  | C  | C  | D  |
| C3  | C  | D  | D  | D  |

**Note:** S0 or E0 or C0 → QM (Quality Management only)

---

## 7. Safety Goals

Derive safety goals from ASIL-rated hazards:

| Safety Goal ID | Related Hazard(s) | ASIL | Safety Goal Statement | Safe State |
|----------------|-------------------|------|-----------------------|------------|
| SG-001 | H-001 | D | [Clear, measurable safety objective] | [Acceptable fallback condition] |
| SG-002 | | | | |

**Example:**
| Safety Goal ID | Related Hazard(s) | ASIL | Safety Goal Statement | Safe State |
|----------------|-------------------|------|-----------------------|------------|
| SG-001 | H-001, H-002 | D | Prevent collision with pedestrians due to detection failures | System warns driver and applies emergency braking OR transitions to safe stop |
| SG-002 | H-003 | C | Prevent false positive detections causing unnecessary hard braking | Degraded mode with driver warning, no automatic braking |

---

## 8. Functional Safety Requirements (High-level)

Derive functional safety requirements from safety goals:

| FSR ID | Safety Goal | ASIL | Functional Safety Requirement |
|--------|-------------|------|-------------------------------|
| FSR-001.1 | SG-001 | D | [Specific, verifiable requirement] |
| FSR-001.2 | SG-001 | D | |
| FSR-002.1 | SG-002 | C | |

**Example:**
| FSR ID | Safety Goal | ASIL | Functional Safety Requirement |
|--------|-------------|------|-------------------------------|
| FSR-001.1 | SG-001 | D | System shall detect pedestrians within 50m with ≥99.9% true positive rate |
| FSR-001.2 | SG-001 | D | System shall classify detected objects as pedestrian/non-pedestrian with ≥99.9% accuracy |
| FSR-001.3 | SG-001 | D | System shall activate emergency braking within 200ms of pedestrian detection |
| FSR-001.4 | SG-001 | D | System shall provide redundant detection using independent sensor modalities |

---

## 9. Verification and Validation Plan

| ASIL Level | V&V Requirements | Test Coverage | Methods |
|------------|------------------|---------------|---------|
| A | [Requirements] | ≥ 90% | [Test methods] |
| B | | ≥ 95% | |
| C | | ≥ 98% | |
| D | | ≥ 99.9% | |

**Example for ASIL D:**
- Requirements-based testing: 100% coverage
- Fault injection testing: All single-point faults
- Back-to-back comparison testing: Software vs model
- Resource usage testing: Worst-case scenarios
- Interface testing: All communication paths
- Independent safety assessment required

---

## 10. Review and Approval

### Assumptions and Limitations
[List any assumptions made during the analysis]

### Open Issues
| Issue ID | Description | Owner | Target Date |
|----------|-------------|-------|-------------|
| | | | |

### Review History
| Date | Reviewer | Comments | Status |
|------|----------|----------|--------|
| | | | |

### Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Safety Manager | | | |
| Chief Engineer | | | |
| Quality Manager | | | |

---

## Notes and Best Practices

### Tips for Conducting HARA:

1. **Be systematic**: Cover all operational situations
2. **Be specific**: Clearly define malfunctions and hazards
3. **Be conservative**: When in doubt, choose higher severity/exposure/lower controllability
4. **Involve experts**: Include domain experts from different disciplines
5. **Document assumptions**: Record all assumptions for traceability
6. **Update regularly**: HARA is a living document, update when design changes

### Common Mistakes to Avoid:

- ❌ Underestimating severity or exposure
- ❌ Assuming perfect controllability
- ❌ Missing edge cases and rare scenarios
- ❌ Not considering combinations of failures
- ❌ Insufficient documentation of rationale
- ❌ Not updating HARA when design evolves

### Integration with Other Analyses:

- **SOTIF**: Use HARA hazards as starting point for SOTIF triggering conditions
- **TARA**: Consider how cybersecurity threats could trigger safety hazards
- **FMEA**: Detailed failure mode analysis at component level
- **FTA**: Fault tree analysis for complex failure combinations

---

**Template Version:** 1.0
**Last Updated:** 2025
**Reference Standard:** ISO 26262:2018
