# Operational Design Domain (ODD) Definition Template

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Standard Reference:** ISO 34503:2023 - Road vehicles — Test scenarios for automated driving systems — Scenario based safety evaluation framework

---

## Document Information

| Field | Value |
|-------|-------|
| **System Name** | [Enter system name] |
| **SAE Automation Level** | [L0 / L1 / L2 / L3 / L4 / L5] |
| **Version** | [e.g., 1.0] |
| **Date** | [YYYY-MM-DD] |
| **Prepared By** | [Name] |
| **Reviewed By** | [Name] |
| **Approved By** | [Name] |

---

## 1. ODD Overview

### 1.1 System Description
Brief description of the automated driving system and its intended functionality:

[Enter description]

### 1.2 ODD Scope
Define the boundaries within which the system is designed to operate safely:

[Enter scope]

### 1.3 Use Cases
Primary use cases supported by this ODD:

1. [Use case 1]
2. [Use case 2]
3. [Use case 3]

---

## 2. Geographic and Roadway Attributes

### 2.1 Geographic Location

| Attribute | Specification | Rationale |
|-----------|---------------|-----------|
| **Countries/Regions** | [e.g., United States, Germany] | |
| **Urban/Rural** | [ ] Urban Only<br>[ ] Suburban<br>[ ] Rural<br>[ ] All | |
| **Altitude Range** | [e.g., -100m to 2000m above sea level] | |
| **Latitude Range** | [e.g., 30°N to 50°N] | Affects sun angle, daylight hours |

### 2.2 Road Types

Select all applicable road types:

- [ ] **Highways** (Limited access, high-speed)
- [ ] **Arterial Roads** (Multi-lane, signalized intersections)
- [ ] **Collector Roads** (Moderate traffic, lower speeds)
- [ ] **Local Streets** (Residential, low-speed)
- [ ] **Parking Lots** (Structured parking facilities)

### 2.3 Road Features

| Feature | Included? | Constraints |
|---------|-----------|-------------|
| **Lane Markings** | [ ] Yes [ ] No | [e.g., Visible, white/yellow, continuous] |
| **Road Surface** | [ ] Paved [ ] Unpaved | [e.g., Asphalt, concrete only] |
| **Number of Lanes** | Min: ___ Max: ___ | [e.g., 2-6 lanes per direction] |
| **Lane Width** | Min: ___ Max: ___ | [e.g., 3.0m - 3.7m] |
| **Shoulder Width** | Min: ___ Max: ___ | [e.g., 0.5m - 3m] |
| **Curvature** | Max radius: ___ | [e.g., Radius > 50m] |
| **Grade** | Max: ___ % | [e.g., < 10% gradient] |
| **Tunnels** | [ ] Yes [ ] No | [Constraints] |
| **Bridges** | [ ] Yes [ ] No | [Constraints] |
| **Construction Zones** | [ ] Yes [ ] No | [Constraints] |

---

## 3. Environmental Conditions

### 3.1 Weather Conditions

| Condition | Supported? | Constraints |
|-----------|------------|-------------|
| **Clear Weather** | [ ] Yes [ ] No | |
| **Light Rain** | [ ] Yes [ ] No | [e.g., < 2.5 mm/hr] |
| **Heavy Rain** | [ ] Yes [ ] No | [e.g., < 10 mm/hr] |
| **Snow** | [ ] Yes [ ] No | [Constraints] |
| **Fog** | [ ] Yes [ ] No | [e.g., Visibility > 200m] |
| **Hail** | [ ] Yes [ ] No | [Constraints] |
| **Strong Wind** | [ ] Yes [ ] No | [e.g., < 15 m/s] |

### 3.2 Lighting and Visibility

| Condition | Supported? | Constraints |
|-----------|------------|-------------|
| **Daytime** | [ ] Yes [ ] No | [e.g., Sun elevation > 10°] |
| **Dawn/Dusk** | [ ] Yes [ ] No | [e.g., Sun elevation -6° to 10°] |
| **Nighttime** | [ ] Yes [ ] No | [e.g., With street lighting only] |
| **Direct Sunlight (Glare)** | [ ] Yes [ ] No | [Constraints] |

### 3.3 Temperature Range

- **Minimum Operating Temperature:** [e.g., -10°C]
- **Maximum Operating Temperature:** [e.g., +45°C]

---

## 4. Traffic and Dynamic Objects

### 4.1 Traffic Density

| Density Level | Supported? | Definition |
|---------------|------------|------------|
| **Light Traffic** | [ ] Yes [ ] No | [e.g., < 10 vehicles visible] |
| **Moderate Traffic** | [ ] Yes [ ] No | [e.g., 10-30 vehicles visible] |
| **Heavy Traffic** | [ ] Yes [ ] No | [e.g., > 30 vehicles visible] |
| **Stop-and-Go Traffic** | [ ] Yes [ ] No | [e.g., < 10 km/h average speed] |

### 4.2 Traffic Participants

Select all object types the system must handle:

- [ ] **Passenger Vehicles** (Cars, SUVs, minivans)
- [ ] **Motorcycles**
- [ ] **Bicycles**
- [ ] **Pedestrians**
- [ ] **Heavy Trucks** (Semi-trailers, delivery trucks)
- [ ] **Buses**
- [ ] **Emergency Vehicles** (Police, ambulance, fire)
- [ ] **Construction Vehicles**
- [ ] **Animals** (Specify: _______________)

### 4.3 Speed Range

- **Minimum Speed:** [e.g., 0 km/h (full stop capability)]
- **Maximum Speed:** [e.g., 120 km/h]

### 4.4 Traffic Regulations

| Regulation | Supported? | Notes |
|------------|------------|-------|
| **Traffic Signals** | [ ] Yes [ ] No | [e.g., Standard red/yellow/green] |
| **Stop Signs** | [ ] Yes [ ] No | |
| **Yield Signs** | [ ] Yes [ ] No | |
| **Speed Limit Signs** | [ ] Yes [ ] No | |
| **Lane Markings** | [ ] Yes [ ] No | [e.g., Solid, dashed, double] |
| **Crosswalks** | [ ] Yes [ ] No | |
| **Roundabouts** | [ ] Yes [ ] No | |
| **Railroad Crossings** | [ ] Yes [ ] No | |

---

## 5. Connectivity and Communication

### 5.1 V2X Communication

| Feature | Required? | Standard |
|---------|-----------|----------|
| **V2V (Vehicle-to-Vehicle)** | [ ] Required [ ] Optional [ ] Not Used | [e.g., C-V2X, DSRC] |
| **V2I (Vehicle-to-Infrastructure)** | [ ] Required [ ] Optional [ ] Not Used | [Standard] |
| **V2P (Vehicle-to-Pedestrian)** | [ ] Required [ ] Optional [ ] Not Used | [Standard] |
| **V2N (Vehicle-to-Network)** | [ ] Required [ ] Optional [ ] Not Used | [e.g., 4G/5G] |

### 5.2 Positioning Services

| Service | Required? | Accuracy |
|---------|-----------|----------|
| **GNSS (GPS/Galileo/GLONASS)** | [ ] Required [ ] Optional | [e.g., ±2m] |
| **HD Maps** | [ ] Required [ ] Optional | [e.g., Lane-level accuracy] |
| **Real-time Map Updates** | [ ] Required [ ] Optional | [Update frequency] |

---

## 6. Operational Constraints

### 6.1 Time-Based Constraints

- **Time of Day:** [e.g., 6:00 AM - 10:00 PM only]
- **Day of Week:** [e.g., Monday - Friday only]
- **Holidays:** [e.g., No operation on public holidays]

### 6.2 Maintenance and Calibration

- **Sensor Cleaning:** [e.g., Required every 100 km or as needed]
- **Calibration Check:** [e.g., Before each trip]
- **Software Version:** [e.g., Minimum version X.Y.Z]

### 6.3 Passenger Requirements

- **Driver Availability:** [e.g., Alert driver required (SAE L3) or No driver needed (SAE L4)]
- **Passenger Restrictions:** [e.g., Maximum 4 passengers]

---

## 7. Exclusions and Boundaries

### 7.1 Explicitly Excluded Scenarios

List scenarios that are **outside** the ODD:

1. [e.g., Driving in heavy snow (> 5 cm accumulation)]
2. [e.g., Unpaved roads]
3. [e.g., Visibility < 100m]
4. [e.g., Emergency vehicle operations]
5. [Add more as needed]

### 7.2 Edge Cases and Boundary Conditions

Scenarios at the boundary of the ODD that require special attention:

| Scenario | Criticality | Mitigation |
|----------|-------------|------------|
| [e.g., Transition from day to night] | High | [e.g., Gradual transition with sensor validation] |
| [e.g., Light rain turning to heavy rain] | High | [e.g., Real-time weather monitoring, MRC activation] |
| [Add more as needed] | | |

---

## 8. Transition to Minimal Risk Condition (MRC)

### 8.1 MRC Trigger Conditions

List conditions that will trigger transition to Minimal Risk Condition:

1. [e.g., ODD boundary violation detected]
2. [e.g., Sensor degradation beyond threshold]
3. [e.g., Weather conditions exceeding limits]
4. [e.g., V2X connectivity loss (if required)]
5. [Add more as needed]

### 8.2 MRC Strategy

Describe the system's behavior when MRC is triggered:

[e.g., "System will safely bring vehicle to a stop in the rightmost lane or shoulder, activate hazard lights, and notify remote operations center."]

### 8.3 Fallback Capabilities

| Fallback Level | Description | Conditions |
|----------------|-------------|------------|
| **Level 1: Graceful Degradation** | [e.g., Reduced speed operation] | [e.g., Light fog] |
| **Level 2: Controlled Stop** | [e.g., Stop in lane] | [e.g., Sensor failure] |
| **Level 3: Emergency Stop** | [e.g., Immediate stop] | [e.g., Critical system failure] |

---

## 9. Runtime Monitoring

### 9.1 ODD Compliance Monitoring

List parameters monitored in real-time to ensure ODD compliance:

| Parameter | Sensor/Source | Threshold | Action if Exceeded |
|-----------|---------------|-----------|---------------------|
| [e.g., Visibility] | [Camera, LiDAR] | [< 200m] | [Initiate MRC] |
| [e.g., Rain intensity] | [Rain sensor] | [> 10 mm/hr] | [Reduce speed, then MRC] |
| [e.g., Road curvature] | [HD Map, IMU] | [Radius < 50m] | [Alert, slow down] |
| [Add more as needed] | | | |

### 9.2 Sensor Health Monitoring

| Sensor | Health Check | Frequency | Failure Response |
|--------|--------------|-----------|------------------|
| [e.g., Front Camera] | [Calibration check, lens blockage] | [Every 1 second] | [Switch to redundant sensor, MRC] |
| [e.g., LiDAR] | [Point cloud density] | [Every 1 second] | [Reduce speed, MRC] |
| [Add more as needed] | | | |

---

## 10. Validation and Testing

### 10.1 ODD Validation Approach

Describe how the ODD will be validated:

- **Simulation Testing:** [e.g., 1 million km in CARLA simulator covering all ODD conditions]
- **Test Track:** [e.g., 10,000 km at proving grounds]
- **Public Road Testing:** [e.g., 100,000 km in defined ODD regions]

### 10.2 Test Scenarios

List key test scenarios covering ODD boundaries:

1. [Scenario 1]
2. [Scenario 2]
3. [Scenario 3]

### 10.3 Acceptance Criteria

Define metrics for ODD validation:

| Metric | Target | Method |
|--------|--------|--------|
| [e.g., Disengagement rate] | [< 0.1 per 1000 km] | [Real-world testing] |
| [e.g., MRC activation rate] | [< 0.01 per 1000 km] | [Real-world testing] |
| [e.g., ODD violation detection rate] | [> 99.9%] | [Simulation + testing] |

---

## 11. Safety Argumentation

### 11.1 Relationship to ISO Standards

| Standard | Relevance | Reference Section |
|----------|-----------|-------------------|
| **ISO 26262** | [e.g., ASIL decomposition for perception within ODD] | [Part 3, Clause X] |
| **ISO 21448 (SOTIF)** | [e.g., ODD defines known safe scenarios] | [Clause 8] |
| **ISO/SAE 21434** | [e.g., Cybersecurity for V2X within ODD] | [Clause 9] |

### 11.2 Assumptions

List key assumptions underlying this ODD:

1. [e.g., HD maps are updated at least weekly]
2. [e.g., Traffic participants follow traffic rules]
3. [e.g., Road infrastructure is maintained to standard]
4. [Add more as needed]

---

## 12. Updates and Maintenance

### 12.1 ODD Versioning

- **Current Version:** [e.g., 1.0]
- **Last Review Date:** [YYYY-MM-DD]
- **Next Review Date:** [YYYY-MM-DD]

### 12.2 Change Log

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| 1.0 | [YYYY-MM-DD] | Initial ODD definition | [Name] |
| | | | |

### 12.3 Continuous Improvement

Describe process for updating ODD based on field data:

[e.g., "ODD will be reviewed quarterly based on fleet disengagement data, incident reports, and new sensor capabilities. Expansion of ODD requires re-validation."]

---

## 13. Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **System Engineer** | | | |
| **Safety Manager** | | | |
| **Cybersecurity Manager** | | | |
| **Program Manager** | | | |

---

**Template Version:** 1.0
**Developed By:** Milin Patel, Hochschule Kempten
**Copyright © 2025 Milin Patel. All Rights Reserved.**
**License:** MIT License
