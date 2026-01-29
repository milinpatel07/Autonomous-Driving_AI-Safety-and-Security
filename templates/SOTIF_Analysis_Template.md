# SOTIF Analysis Template: Safety of the Intended Functionality (ISO 21448)

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

## 1. Item Definition and Intended Functionality

### 1.1 System Description

**Item Name:** [System or function being analyzed]

**Intended Functionality:** [Clear description of what the system is supposed to do]

**Performance Specifications:**
- Detection range: [Specify]
- Detection accuracy: [Specify]
- Response time: [Specify]
- Operating conditions: [Specify]

**Example:**
```
Item Name: Pedestrian Detection and AEB System
Intended Functionality: Detect pedestrians in vehicle path and apply emergency braking
Performance Specifications:
  - Detection range: 0-100m
  - Detection accuracy: ≥95% true positive rate
  - Response time: <200ms from detection to brake actuation
  - Operating conditions: Urban roads, 0-60 km/h
```

---

## 2. Operational Design Domain (ODD)

Define the operational boundaries within which the system is designed to function:

### 2.1 Geographic Conditions
- [ ] Urban roads
- [ ] Suburban roads
- [ ] Highways
- [ ] Rural roads
- [ ] Specific regions: [List]

### 2.2 Environmental Conditions
- **Weather:**
  - [ ] Clear
  - [ ] Light rain
  - [ ] Heavy rain
  - [ ] Fog/Mist
  - [ ] Snow/Ice
  - [ ] Excluded: [List]

- **Lighting:**
  - [ ] Daylight
  - [ ] Twilight (dawn/dusk)
  - [ ] Night with street lights
  - [ ] Night without street lights
  - [ ] Excluded: [List]

- **Temperature range:** [Min to Max °C]

### 2.3 Road Conditions
- **Road surface:**
  - [ ] Dry asphalt
  - [ ] Wet asphalt
  - [ ] Snow/ice covered
  - [ ] Gravel
  - [ ] Excluded: [List]

- **Road markings:**
  - [ ] Well-marked lanes
  - [ ] Faded markings
  - [ ] No markings
  - [ ] Excluded: [List]

- **Road geometry:**
  - [ ] Straight roads
  - [ ] Curves (radius > X m)
  - [ ] Intersections
  - [ ] Roundabouts
  - [ ] Excluded: [List]

### 2.4 Speed Range
- Minimum speed: [X km/h]
- Maximum speed: [Y km/h]
- Optimal speed: [Z km/h]

### 2.5 Traffic Conditions
- [ ] Light traffic
- [ ] Moderate traffic
- [ ] Heavy traffic
- [ ] Excluded: [List]

### 2.6 User Responsibilities
[Describe what the driver/user is expected to do]

**Example:**
```
- Driver must remain attentive and ready to take control
- Driver must keep hands on steering wheel
- Driver must not use system outside defined ODD
- Driver must respond to takeover requests within 5 seconds
```

---

## 3. Triggering Conditions Identification

Identify circumstances that could lead to insufficient performance:

| TC ID | Category | Triggering Condition | Description | Impact on Performance |
|-------|----------|---------------------|-------------|----------------------|
| TC-001 | [Sensor/Algorithm/Environment/Human] | [Condition name] | [Detailed description] | [Performance degradation] |
| TC-002 | | | | |

**Categories:**
- **Sensor Limitations**: Range, resolution, environmental sensitivity
- **Algorithm Limitations**: Edge cases, out-of-distribution data
- **Environmental Factors**: Weather, lighting, unexpected scenarios
- **Human Factors**: Misuse, overreliance, distraction

**Example:**
| TC ID | Category | Triggering Condition | Description | Impact on Performance |
|-------|----------|---------------------|-------------|----------------------|
| TC-001 | Environmental | Heavy rain | Camera image quality degraded by rain on lens | Detection rate drops to 75% |
| TC-002 | Sensor | Low-light conditions | Camera sensitivity insufficient at night | Miss rate increases to 10% |
| TC-003 | Algorithm | Unusual pedestrian pose | Person carrying large object, unusual clothing | Misclassification as non-pedestrian |
| TC-004 | Environmental | Dense fog | Visibility < 50m, sensor range limited | Detection range reduced to 30m |

---

## 4. Scenario Categorization

Categorize scenarios into the four SOTIF spaces:

### 4.1 Known Safe (S1)

Scenarios where the system performs acceptably:

| Scenario ID | Description | Validation Evidence | Notes |
|-------------|-------------|---------------------|-------|
| S1-001 | [Scenario description] | [Test results, field data] | [Comments] |
| S1-002 | | | |

**Example:**
| Scenario ID | Description | Validation Evidence | Notes |
|-------------|-------------|---------------------|-------|
| S1-001 | Adult pedestrian crossing at marked crosswalk, daylight, clear weather, 40 km/h | 10,000+ test cases, 99.5% detection rate | Well within ODD |
| S1-002 | Pedestrian on sidewalk, suburban area, overcast, 30 km/h | 5,000+ test cases, 98.8% detection rate | Standard scenario |

### 4.2 Known Unsafe (S2)

Scenarios where performance is known to be insufficient:

| Scenario ID | Description | Performance Gap | Mitigation Strategy | ODD Restriction |
|-------------|-------------|----------------|---------------------|-----------------|
| S2-001 | [Scenario] | [Specific limitation] | [How to address] | [Yes/No, details] |
| S2-002 | | | | |

**Example:**
| Scenario ID | Description | Performance Gap | Mitigation Strategy | ODD Restriction |
|-------------|-------------|----------------|---------------------|-----------------|
| S2-001 | Heavy rain (>50mm/hr) | Detection rate 70% | Driver warning + speed limit to 30 km/h | Yes - exclude from ODD |
| S2-002 | Dense fog (visibility <30m) | Detection range 25m | Require driver takeover | Yes - system disengages |
| S2-003 | Dark clothing at night, no street lights | Miss rate 15% | Add infrared sensor OR restrict ODD | ODD restricted |

### 4.3 Unknown Safe (S3)

Scenarios not yet validated but likely to perform well:

| Scenario ID | Description | Why Likely Safe | Validation Plan |
|-------------|-------------|-----------------|-----------------|
| S3-001 | [Scenario] | [Reasoning] | [How to test] |
| S3-002 | | | |

**Example:**
| Scenario ID | Description | Why Likely Safe | Validation Plan |
|-------------|-------------|-----------------|-----------------|
| S3-001 | Pedestrian with mobility aid (cane, walker) | Similar visual characteristics to normal pedestrian | Add to test dataset, validate with 500+ cases |
| S3-002 | Light snow (visibility >200m) | Minor degradation expected, within margins | Test in controlled environment |

### 4.4 Unknown Unsafe (S4)

Scenarios not yet identified that may have insufficient performance:

| Potential Area | Why Unknown | Discovery Strategy | Priority |
|----------------|-------------|-------------------|----------|
| [Domain/condition] | [Reason not identified] | [How to discover] | High/Medium/Low |

**Example:**
| Potential Area | Why Unknown | Discovery Strategy | Priority |
|----------------|-------------|-------------------|----------|
| Adversarial scenarios | Intentional attacks not in training data | Research adversarial ML, add test cases | High |
| Rare weather combinations | Limited field data on combinations | Simulation-based testing, field monitoring | Medium |
| Novel pedestrian behaviors | Unexpected actions not in dataset | Continuous field monitoring, incident analysis | High |
| Unusual road geometry | Limited geographic diversity in training | Expand testing to diverse locations | Medium |

---

## 5. SOTIF Process Activities

### 5.1 Design Phase

| Activity | Status | Notes |
|----------|--------|-------|
| Define ODD | ☐ Not Started ☐ In Progress ☑ Complete | [Comments] |
| Identify triggering conditions | ☐ Not Started ☐ In Progress ☑ Complete | |
| Design mitigation measures | ☐ Not Started ☐ In Progress ☑ Complete | |
| Establish performance targets | ☐ Not Started ☐ In Progress ☑ Complete | |

### 5.2 Verification Activities

| Activity | Status | Coverage/Results | Notes |
|----------|--------|------------------|-------|
| Known safe scenarios tested | ☐ Not Started ☐ In Progress ☑ Complete | [X% coverage] | |
| Known unsafe scenarios identified | ☐ Not Started ☐ In Progress ☑ Complete | [Number found] | |
| Triggering conditions analyzed | ☐ Not Started ☐ In Progress ☑ Complete | [Analysis depth] | |
| Mitigation effectiveness verified | ☐ Not Started ☐ In Progress ☑ Complete | [Test results] | |

### 5.3 Validation Activities

| Activity | Status | Results | Notes |
|----------|--------|---------|-------|
| Scenario database established | ☐ Not Started ☐ In Progress ☑ Complete | [Number of scenarios] | |
| Unknown safe scenarios tested | ☐ Not Started ☐ In Progress ☑ Complete | [Number validated] | |
| Diverse environmental testing | ☐ Not Started ☐ In Progress ☑ Complete | [Conditions tested] | |
| Field testing conducted | ☐ Not Started ☐ In Progress ☑ Complete | [Miles/hours] | |

### 5.4 Field Monitoring

| Activity | Status | Plan/Results | Notes |
|----------|--------|--------------|-------|
| Monitoring system deployed | ☐ Not Started ☐ In Progress ☑ Complete | [Details] | |
| Performance metrics tracked | ☐ Not Started ☐ In Progress ☑ Complete | [Metrics list] | |
| Edge case collection | ☐ Not Started ☐ In Progress ☑ Complete | [Cases found] | |
| Incident investigation process | ☐ Not Started ☐ In Progress ☑ Complete | [Process defined] | |

---

## 6. Scenario Coverage Analysis

### 6.1 Coverage Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| S1 (Known Safe) scenarios | [Target number] | [Current] | ☑ / ☐ |
| S2 (Known Unsafe) identified and mitigated | 100% | [Current %] | ☑ / ☐ |
| S3 (Unknown Safe) validated | [Target number] | [Current] | ☑ / ☐ |
| S4 (Unknown Unsafe) minimized | < [Threshold] | [Estimate] | ☑ / ☐ |
| Overall scenario coverage | > 95% | [Current %] | ☑ / ☐ |

### 6.2 Coverage Gaps

| Gap ID | Description | Risk Level | Action Plan | Owner | Target Date |
|--------|-------------|------------|-------------|-------|-------------|
| GAP-001 | [Description] | High/Medium/Low | [Actions] | [Name] | [Date] |

**Example:**
| Gap ID | Description | Risk Level | Action Plan | Owner | Target Date |
|--------|-------------|------------|-------------|-------|-------------|
| GAP-001 | Limited testing in snow conditions | Medium | Conduct winter field tests in northern regions | Test Lead | Q1 2025 |
| GAP-002 | No data on pedestrians with wheelchairs | High | Add wheelchair scenarios to test suite | Dataset Team | Q4 2024 |

---

## 7. Integration with ISO 26262

### 7.1 Hazard-Triggering Condition Mapping

Map SOTIF triggering conditions to ISO 26262 hazards:

| Hazard ID (26262) | SOTIF Triggering Condition | Combined Analysis | Treatment |
|-------------------|---------------------------|-------------------|-----------|
| H-001 | TC-001 | [Joint analysis] | [Mitigation approach] |

**Example:**
| Hazard ID (26262) | SOTIF Triggering Condition | Combined Analysis | Treatment |
|-------------------|---------------------------|-------------------|-----------|
| H-001: Pedestrian not detected | TC-001: Heavy rain degradation | Rain causes sensor limitation (SOTIF) AND may hide system fault (26262) | Sensor fusion + driver warning + speed reduction |

### 7.2 Combined Requirements

| Requirement ID | Source | Combined Requirement | ASIL/SOC |
|----------------|--------|---------------------|----------|
| REQ-001 | 26262 + SOTIF | [Combined statement] | [Level] |

---

## 8. Validation Strategy

### 8.1 Test Methods

| Method | Purpose | Coverage Target | Status |
|--------|---------|----------------|--------|
| Track testing | Controlled environment validation | [Scenarios] | ☐ |
| Simulation | Rare/dangerous scenario testing | [Scenarios] | ☐ |
| Public road testing | Real-world validation | [Miles/hours] | ☐ |
| Closed-course testing | Edge case validation | [Scenarios] | ☐ |

### 8.2 Acceptance Criteria

Define criteria for acceptable performance:

| Criterion | Target | Measurement Method |
|-----------|--------|-------------------|
| Detection rate (S1 scenarios) | ≥ 99% | [Method] |
| False positive rate | ≤ 0.1% | [Method] |
| S2 scenarios identified | 100% | [Method] |
| S4 scenarios minimized | < 5% estimated | [Method] |

---

## 9. Continuous Improvement Plan

### 9.1 Update Triggers

System updates required when:
- [ ] New S2 (Known Unsafe) scenarios identified
- [ ] S4 (Unknown Unsafe) scenarios discovered in field
- [ ] Performance degradation detected
- [ ] ODD expanded or modified
- [ ] New software/model version deployed

### 9.2 Review Schedule

| Review Type | Frequency | Next Review Date |
|-------------|-----------|------------------|
| Scenario database update | [Quarterly/etc.] | [Date] |
| Performance monitoring review | [Monthly/etc.] | [Date] |
| ODD reassessment | [Annually/etc.] | [Date] |
| SOTIF analysis update | [Per update/etc.] | [Date] |

---

## 10. Approval and Sign-off

### Assumptions
[List key assumptions made in this analysis]

### Limitations
[List known limitations of the analysis]

### Review History
| Date | Reviewer | Comments | Status |
|------|----------|----------|--------|
| | | | |

### Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| SOTIF Lead | | | |
| Safety Manager | | | |
| Validation Lead | | | |

---

## Notes and Best Practices

### Tips for SOTIF Analysis:

1. **Start broad**: Cast a wide net for triggering conditions
2. **Be honest about limitations**: Don't hide Known Unsafe scenarios
3. **Use real data**: Field data is invaluable for discovery
4. **Iterate**: SOTIF is continuous, not one-time
5. **Integrate with safety**: Always consider ISO 26262 interplay
6. **Document everything**: Traceability is key

### Common Mistakes:

- ❌ Assuming all unknown scenarios are safe
- ❌ Insufficient scenario diversity in testing
- ❌ Not restricting ODD when limitations found
- ❌ Lack of field monitoring plan
- ❌ Treating SOTIF as separate from ISO 26262

### Tools and Resources:

- Scenario database management tools
- Simulation platforms (CARLA, SUMO, etc.)
- Field data collection and analysis systems
- Automated scenario generation tools

---

**Template Version:** 1.0
**Last Updated:** 2025
**Reference Standard:** ISO 21448:2022
