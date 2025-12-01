<!--
Copyright (c) 2025 Milin Patel
Hochschule Kempten - University of Applied Sciences

Autonomous Driving: AI Safety and Security Workshop
This project is licensed under the MIT License.
-->

# Functional Safety for Autonomous Vehicles

**ISO 26262 and ISO 21448 (SOTIF) Implementation Guide**

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Standards:** ISO 26262:2018 (Functional Safety) & ISO 21448:2022 (SOTIF)

---

> **📖 Quick Start:** For workshop overview and getting started, see [README.md](README.md)
>
> **Purpose:** This document provides detailed technical reference for functional safety standards. It complements the main README with in-depth ISO 26262 and ISO 21448 (SOTIF) implementation guidance.

---

## Table of Contents

1. [Introduction](#introduction)
2. [ISO 26262: Functional Safety](#iso-26262-functional-safety)
3. [ISO 21448: Safety of the Intended Functionality (SOTIF)](#iso-21448-safety-of-the-intended-functionality-sotif)
4. [Integration of ISO 26262 and ISO 21448](#integration-of-iso-26262-and-iso-21448)
5. [Safety Case Development](#safety-case-development)
6. [Verification and Validation](#verification-and-validation)
7. [Practical Examples](#practical-examples)
8. [References](#references)

---

## Introduction

Functional safety is critical for autonomous vehicles, where system failures can directly result in injury or fatality. This document provides comprehensive guidance on applying **ISO 26262** (Functional Safety) and **ISO 21448** (SOTIF - Safety of the Intended Functionality) to autonomous driving systems.

### Why Two Standards?

**ISO 26262** addresses:
- Random hardware failures (e.g., sensor malfunction due to manufacturing defect)
- Systematic software faults (e.g., coding errors, specification mistakes)
- **Malfunctioning behavior** of E/E systems

**ISO 21448 (SOTIF)** addresses:
- Performance limitations of sensors and algorithms (e.g., radar cannot detect stationary objects)
- Triggering conditions that activate limitations (e.g., heavy rain reduces LiDAR range)
- **Intended but insufficient functionality** (system works as designed but design is inadequate)

### Complementary Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                    Total Vehicle Safety                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────┐         ┌───────────────────┐      │
│  │   ISO 26262       │         │   ISO 21448       │      │
│  │                   │         │   (SOTIF)         │      │
│  │ Random HW faults  │         │ Performance       │      │
│  │ Systematic faults │         │   limitations     │      │
│  │ Malfunctioning    │         │ Triggering        │      │
│  │   behavior        │         │   conditions      │      │
│  └───────────────────┘         └───────────────────┘      │
│           │                             │                  │
│           └──────────┬──────────────────┘                  │
│                      │                                     │
│              Combined Safety                                │
│            Argumentation                                    │
│                                                             │
│  ┌─────────────────────────────────────────────┐          │
│  │        ISO/SAE 21434                        │          │
│  │        (Cybersecurity)                      │          │
│  │  Protects both from malicious attacks      │          │
│  └─────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## ISO 26262: Functional Safety

### Overview

**ISO 26262:2018** (Second Edition) - Road vehicles — Functional safety
- **12 Parts** covering entire safety lifecycle
- **ASIL (Automotive Safety Integrity Level)** risk classification: QM, A, B, C, D
- **V-Model** development process

### V-Model Safety Lifecycle

```
Concept Phase          │          Validation Phase
                       │
Item Definition   ─────┼─────>  Vehicle Integration
                       │          and Testing
     │                 │               │
     ▼                 │               │
Hazard Analysis   ─────┼─────>  System Validation
  and Risk             │
  Assessment           │               │
  (HARA)               │               │
     │                 │               │
     ▼                 │               │
Safety Goals      ─────┼─────>  Safety Validation
                       │
     │                 │               │
System Level           │          HW/SW Integration
                       │
Safety Concept    ─────┼─────>  Safety Requirements
                       │          Verification
     │                 │               │
     ▼                 │               │
Technical         ─────┼─────>  Technical Safety
Safety Concept         │          Verification
     │                 │               │
     ▼                 │               │
HW/SW Safety      ─────┼─────>  HW/SW Safety
Requirements           │          Verification
     │                 │               │
     ▼                 │               │
Implementation    ─────┼─────>  Unit Testing
```

### 1. Item Definition (ISO 26262-3 Clause 5)

**Purpose:** Define the item (system or function) and its interfaces

**For AV Perception System Example:**

**Item:** Object Detection and Classification System
**Function:** Detect and classify road users (vehicles, pedestrians, cyclists) and static objects
**Components:**
- Front camera (8MP, 120° FOV)
- Side cameras (2 × 2MP, 190° FOV)
- LiDAR (64-layer, 200m range, 10 Hz)
- Radar (4 × long-range, 77 GHz)
- Perception ECU (NVIDIA Drive AGX, 8-core ARM + GPU)

**Interfaces:**
- **Input:** Raw sensor data (camera images, LiDAR point clouds, radar detections)
- **Output:** Object list (position, velocity, class, confidence) at 10 Hz
- **Communication:** CAN FD to planning ECU, Ethernet to logging system

**Assumptions:**
- Sensors calibrated and synchronized
- HD map available for localization
- Operating temperature: -40°C to 85°C
- Operational Design Domain (ODD): Highway, 0-130 km/h, day/night, clear/rain

### 2. Hazard Analysis and Risk Assessment (HARA) (ISO 26262-3 Clause 6-7)

**Purpose:** Identify hazards, analyze risks, derive safety goals

#### HARA Process

**Step 1: Identify Hazardous Events**

Hazardous Event = Hazard + Operational Situation

**Example Hazards:**

| Hazard ID | Hazard | Operational Situation | Hazardous Event |
|-----------|--------|----------------------|-----------------|
| H-001 | False negative (missed pedestrian) | Urban intersection, 50 km/h, ego vehicle turning left | Vehicle strikes undetected pedestrian in crosswalk |
| H-002 | False positive (phantom object) | Highway, 120 km/h, dense traffic | Emergency braking causes rear-end collision |
| H-003 | Incorrect object classification (pedestrian as static) | Urban street, 30 km/h, pedestrian entering roadway | Vehicle fails to yield, strikes pedestrian |
| H-004 | Position error (3m lateral offset) | Highway lane change, 100 km/h, adjacent vehicle | Sideswipe collision during lane change |
| H-005 | Loss of perception (black screen) | Any situation | Vehicle continues with outdated environment model |

**Step 2: ASIL Determination**

ASIL = f(Severity, Exposure, Controllability)

**Severity (S):**
- **S0**: No injuries
- **S1**: Light to moderate injuries
- **S2**: Severe to life-threatening injuries (survival probable)
- **S3**: Life-threatening to fatal injuries (survival uncertain)

**Exposure (E):**
- **E0**: Incredibly unlikely (<0.001% of operating time)
- **E1**: Very low probability (0.001% to 0.1%)
- **E2**: Low probability (0.1% to 1%)
- **E3**: Medium probability (1% to 10%)
- **E4**: High probability (>10%)

**Controllability (C):**
- **C0**: Controllable in general (>99% of drivers)
- **C1**: Simply controllable (>90%)
- **C2**: Normally controllable (>50%)
- **C3**: Difficult to control or uncontrollable (<50%)

**ASIL Determination Table:**

| S | E | C0 | C1 | C2 | C3 |
|---|---|----|----|----|----|
| S0 | E1-E4 | QM | QM | QM | QM |
| S1 | E1 | QM | QM | QM | A |
| S1 | E2 | QM | QM | A | B |
| S1 | E3 | QM | A | B | C |
| S1 | E4 | QM | A | B | C |
| S2 | E1 | QM | QM | A | B |
| S2 | E2 | QM | A | B | C |
| S2 | E3 | A | B | C | D |
| S2 | E4 | A | B | C | D |
| S3 | E1 | QM | A | B | C |
| S3 | E2 | A | B | C | D |
| S3 | E3 | B | C | D | D |
| S3 | E4 | B | C | D | D |

**Example: H-001 (Missed Pedestrian)**
- Severity: **S3** (fatal injury)
- Exposure: **E4** (pedestrians frequent in urban areas)
- Controllability: **C3** (driver cannot react in time at 50 km/h)
- **ASIL: D**

### 3. Safety Goals (ISO 26262-3 Clause 8)

**Definition:** Top-level safety requirements to avoid or mitigate hazardous events

**Example Safety Goals:**

| SG ID | Safety Goal | Related Hazard | ASIL | Safe State |
|-------|-------------|----------------|------|------------|
| SG-001 | The system shall detect pedestrians with >99.9% recall | H-001 | D | Minimal Risk Condition (MRC) - emergency stop |
| SG-002 | The system shall limit false positive rate to <0.01 per km | H-002 | C | Degrade gracefully, no emergency braking |
| SG-003 | Object classification accuracy shall exceed 98% | H-003 | C | Conservative assumption (treat ambiguous as hazardous) |
| SG-004 | Lateral position error shall not exceed ±0.3m (3σ) | H-004 | D | Abort lane change, return to original lane |
| SG-005 | Loss of perception shall be detected within 100ms | H-005 | D | MRC - emergency stop with hazard lights |

### 4. Functional Safety Concept (ISO 26262-3 Clause 8)

**Purpose:** Derive functional safety requirements from safety goals

**Example for SG-001 (Pedestrian Detection):**

**FSR-001.1**: Camera-based pedestrian detection with minimum 95% recall (ASIL D)
**FSR-001.2**: LiDAR-based pedestrian detection with minimum 95% recall (ASIL D)
**FSR-001.3**: Sensor fusion combining camera and LiDAR detections (ASIL D)
**FSR-001.4**: Diversity in neural network architectures (2 independent models) (ASIL D)
**FSR-001.5**: Runtime monitoring detecting degraded performance (ASIL D)
**FSR-001.6**: Transition to MRC if pedestrian detection confidence drops (ASIL D)

**Safety Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                     Perception System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐              ┌──────────────┐           │
│  │   Camera     │              │   LiDAR      │           │
│  │  (ASIL D)    │              │  (ASIL D)    │           │
│  └──────┬───────┘              └──────┬───────┘           │
│         │                             │                   │
│         │  ┌──────────────┐           │                   │
│         └─>│  CNN Model A │           │                   │
│            │  (YOLOv8)    │           │                   │
│            └──────┬───────┘           │                   │
│                   │                   │                   │
│         ┌─────────▼───────┐  ┌────────▼────────┐         │
│         │  CNN Model B    │  │ PointNet++ 3D  │         │
│         │  (Faster R-CNN) │  │ Detection       │         │
│         └─────────┬───────┘  └────────┬────────┘         │
│                   │                   │                   │
│                   └────────┬──────────┘                   │
│                            │                              │
│                   ┌────────▼────────┐                     │
│                   │  Sensor Fusion  │                     │
│                   │   (Kalman)      │                     │
│                   └────────┬────────┘                     │
│                            │                              │
│                   ┌────────▼────────┐                     │
│                   │ Safety Monitor  │                     │
│                   │ (Plausibility)  │                     │
│                   └────────┬────────┘                     │
│                            │                              │
│                   ┌────────▼────────┐                     │
│                   │ Object List     │ ──> To Planning    │
│                   │ Output (ASIL D) │                     │
│                   └─────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5. ASIL Decomposition (ISO 26262-9)

**Purpose:** Reduce ASIL requirement by combining redundant elements

**Example:** ASIL D can be decomposed to ASIL B(D) + ASIL B(D)

```
SG-001 (ASIL D): Detect pedestrians with >99.9% recall

Decompose to:
├─> Camera detection path (ASIL B decomposed from D)
│   - Requires 95% recall
│   - Independent failure mode from LiDAR
│
└─> LiDAR detection path (ASIL B decomposed from D)
    - Requires 95% recall
    - Independent failure mode from camera

Combined: 1 - (1 - 0.95)² = 99.75% recall ≈ 99.9% ✓
```

**Justification for Independence:**
- Different sensing principles (optics vs. laser ranging)
- Different environmental failure modes (camera: darkness, glare; LiDAR: rain, fog)
- Different hardware (camera ISP vs. LiDAR APD)
- Different software stacks

### 6. Hardware and Software Safety Requirements

**Hardware-Software Interface (HSI) Considerations for AI Accelerators:**

| Component | Function | ASIL | Safety Mechanism |
|-----------|----------|------|------------------|
| GPU/TPU | Neural network inference | D | ECC memory, redundant execution |
| DMA Engine | Sensor data transfer | D | CRC checks, timeout monitoring |
| System RAM | Model weights, activations | D | ECC, memory scrubbing |
| Flash Storage | Model storage | D | Checksum verification, A/B partitioning |

### 7. Safety Mechanisms (ISO 26262-5, 6, 9)

**Purpose:** Detect and mitigate faults

**Examples for Perception:**

| Mechanism ID | Mechanism | Fault Detected | FMEDA Coverage |
|--------------|-----------|----------------|----------------|
| SM-001 | Sensor self-test (BIST) | Sensor hardware failure | 95% |
| SM-002 | Temporal redundancy (dual execution) | Transient faults | 90% |
| SM-003 | Cross-sensor plausibility checks | Systematic sensor error | 85% |
| SM-004 | Watchdog timer | Software hang | 99% |
| SM-005 | CRC on data communication | Data corruption | 99.9% |
| SM-006 | Model output range checking | Software fault | 80% |
| SM-007 | Diversity in neural networks | Systematic ML error | 70% |

---

## ISO 21448: Safety of the Intended Functionality (SOTIF)

### Overview

**ISO 21448:2022** addresses risks from performance limitations and triggering conditions, particularly relevant for AI/ML-based systems.

### Key Terminology

**Performance Limitation:** Insufficiency in the system's functionality due to:
- Sensor limitations (e.g., radar cannot detect stationary objects)
- Algorithm limitations (e.g., neural network fails on rare edge cases)

**Triggering Condition:** Specific operational situation that activates a performance limitation:
- Environmental (e.g., heavy rain reduces LiDAR range by 50%)
- System state (e.g., sensor contamination by mud)
- Road infrastructure (e.g., missing lane markings)

**SOTIF Scenario Classification:**

```
                     Known Scenarios    │    Unknown Scenarios
                                        │
    ─────────────────────────────────────┼──────────────────────────────
                                        │
    SAFE      │  Known Safe             │    Unknown Safe
    Scenarios │  (Validated)            │    (Presumed safe, not yet
              │                         │     validated)
    ──────────┼─────────────────────────┼──────────────────────────────
                                        │
    UNSAFE    │  Known Unsafe           │    Unknown Unsafe
    Scenarios │  (Identified hazards,   │    (Residual risk,
              │   mitigated)            │     goal is to minimize)
```

**SOTIF Goal:** Move scenarios from "unknown" to "known" through extensive testing, and ensure "known unsafe" scenarios are mitigated.

### SOTIF Process

#### Phase 1: Design and Architecture

**Activities:**
1. Define Operational Design Domain (ODD)
2. Identify known performance limitations
3. Analyze triggering conditions
4. Design mitigation strategies

**Example ODD Definition:**

| Parameter | Specification |
|-----------|---------------|
| **Road Type** | Highways and major roads with clear lane markings |
| **Speed Range** | 0 - 130 km/h |
| **Weather** | Clear, light rain (visibility >200m), no snow/ice |
| **Time of Day** | Day and night (with functional street lighting) |
| **Traffic Density** | All levels (stop-and-go to free-flow) |
| **Geography** | Mapped regions with HD maps available |

**Known Limitations for Camera-based Lane Detection:**

| Limitation | Triggering Condition | Consequence | Mitigation |
|------------|---------------------|-------------|------------|
| Cannot detect faded markings | Poorly maintained roads | Incorrect lane position | Use HD map as backup |
| Glare saturation | Direct sunlight at sunrise/sunset | Lane not detected | LiDAR-based lane detection |
| Shadows misclassified | Trees creating shadows on road | False lane detection | Temporal consistency checking |
| Occlusion by leading vehicle | Large truck in front | Loss of lane visibility | Increase following distance |

#### Phase 2: Verification

**Purpose:** Test known scenarios systematically

**Test Categories:**

1. **Nominal Performance Testing**
   - Standard scenarios within ODD
   - Objective: Ensure system meets performance targets

2. **Boundary Testing**
   - Edge of ODD (e.g., 199m visibility, 129 km/h speed)
   - Objective: Verify graceful degradation

3. **Stress Testing**
   - Challenging but known scenarios (e.g., heavy rain, night)
   - Objective: Verify robustness

4. **Negative Testing**
   - Outside ODD (e.g., snow, unpaved roads)
   - Objective: Verify safe degradation or refusal to operate

**Example Test Matrix for Pedestrian Detection:**

| Weather | Lighting | Occlusion | Pedestrian Type | Test Cases |
|---------|----------|-----------|----------------|------------|
| Clear | Day | None | Adult | 100 |
| Clear | Day | Partial (50%) | Adult | 50 |
| Clear | Day | None | Child | 50 |
| Clear | Night | None | Adult | 100 |
| Light Rain | Day | None | Adult | 50 |
| Light Rain | Night | None | Adult | 50 |
| ... | ... | ... | ... | ... |
| **Total** | | | | **5000+** |

#### Phase 3: Validation

**Purpose:** Discover unknown unsafe scenarios

**Methods:**

1. **Scenario Mining from Naturalistic Driving Data**
   - Analyze millions of km of real-world driving
   - Identify rare events and edge cases
   - Tools: Scenario databases (PEGASUS, OpenSCENARIO)

2. **Simulation-based Exploration**
   - Generate synthetic scenarios with parameter variation
   - Use genetic algorithms, reinforcement learning to find failures
   - Simulators: CARLA, LGSVL, Metadrive

3. **Expert Knowledge and Brainstorming**
   - Safety workshops with domain experts
   - Systematic use of HAZOP (Hazard and Operability Study)

4. **Field Testing**
   - Controlled test tracks with safety drivers
   - Progressive rollout: R&D fleet → pilot fleet → public deployment
   - Disengagement reporting and analysis

**Corner Case Examples:**

1. **Ambiguous Object:** Cardboard box on highway - is it empty (ignore) or full (avoid)?
2. **Rare Vehicle Type:** Oversized load truck, animal-drawn cart, funeral procession
3. **Unusual Pedestrian:** Person in wheelchair, child chasing ball, costumed character
4. **Infrastructure Anomaly:** Missing traffic sign, construction zone without proper marking
5. **Sensor Edge Case:** Sun reflected in puddle causes LiDAR false positive

#### Phase 4: Field Monitoring

**Purpose:** Continuous learning from deployed vehicles

**Data Collection:**
- Disengagements (safety driver takeover)
- Near-misses (hazard detected, maneuver avoided collision)
- Anomaly detections (out-of-distribution scenarios)
- Performance metrics (detection recall, precision)

**Feedback Loop:**
1. Fleet identifies new triggering condition
2. Scenario reproduced in simulation
3. Performance verified as acceptable or mitigation developed
4. Update deployed via OTA if needed
5. Updated scenario added to validation test suite

**Statistical Evidence:**

SOTIF validation requires demonstrating sufficiently low residual risk. Example calculation:

- Target: <10⁻⁹ per hour (1 critical failure per billion hours)
- Testing: 100 million km without critical failures
- Assumes: 50 km/h average speed → 2 million hours
- Confidence: Statistical upper bound with confidence level

*Note: This is illustrative; actual SOTIF targets depend on ODD and risk acceptance.*

---

## Integration of ISO 26262 and ISO 21448

### Combined Safety Argumentation

**Safety Claim:** The AV perception system is acceptably safe for deployment

**Structured Argument (GSN - Goal Structuring Notation):**

```
┌─────────────────────────────────────────────────────────────┐
│ G1: Perception system is acceptably safe                   │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
┌────────▼──────────┐    ┌────────▼──────────┐
│ G2: Systematic     │    │ G3: Insufficient  │
│ faults addressed   │    │ performance       │
│ (ISO 26262)        │    │ addressed         │
│                    │    │ (ISO 21448)       │
└────────┬───────────┘    └────────┬──────────┘
         │                         │
    ┌────┴────┐               ┌────┴────┐
    │         │               │         │
┌───▼───┐ ┌──▼───┐      ┌────▼────┐ ┌─▼─────┐
│ ASIL D│ │Safety│      │Known    │ │Unknown│
│compliant│ │mech. │      │scenarios│ │scenarios│
│ process│ │99%   │      │mitigated│ │minimized│
│        │ │coverage│     │         │ │         │
└────────┘ └──────┘      └─────────┘ └────────┘
```

### Complementary Verification

| Aspect | ISO 26262 | ISO 21448 |
|--------|-----------|-----------|
| **Fault Type** | Random HW faults, systematic SW faults | Performance limitations |
| **Testing Focus** | Fault injection, safety mechanism validation | Scenario-based testing, edge cases |
| **Metrics** | PMHF, SPFM, LFM | Residual risk, scenario coverage |
| **Confidence** | Statistical (FIT rates) | Operational (km driven) |
| **Validation** | Formal verification, testing | Extensive simulation and field testing |

**Example Integration for Pedestrian Detection:**

1. **ISO 26262 Verification:**
   - Sensor self-test detects camera malfunction within 100ms
   - Dual neural network execution with comparison
   - Safety mechanism coverage: 95%

2. **ISO 21448 Verification:**
   - Tested on 5000+ pedestrian scenarios
   - Recall >99% in known scenarios (day, clear weather)
   - Identified 20 challenging scenarios (backlighting, occlusion)

3. **Combined Confidence:**
   - System meets ASIL D requirements for systematic faults
   - Residual SOTIF risk <10⁻⁹ per hour (based on test evidence)
   - Safe for ODD: urban/highway, day/night, clear/light rain

---

## Safety Case Development

### Safety Case Structure (ISO 26262-2 Clause 6)

**Components:**
1. **Claims:** What is being asserted (e.g., "System is ASIL D compliant")
2. **Arguments:** Logical reasoning supporting claims
3. **Evidence:** Test results, analysis outputs, design documents

**Example Safety Case Fragment:**

**Claim C1:** Pedestrian detection system achieves ASIL D integrity

**Argument A1:** ASIL D achieved through:
- Sub-claim C1.1: Hardware meets ASIL D requirements
- Sub-claim C1.2: Software meets ASIL D requirements
- Sub-claim C1.3: Safety mechanisms provide sufficient coverage

**Evidence for C1.2 (Software):**
- E1: Software architecture document (compliant with ISO 26262-6)
- E2: Unit test results (100% statement coverage, 95% branch coverage)
- E3: Integration test results (all functional safety requirements verified)
- E4: Static analysis report (MISRA C compliance, zero critical defects)
- E5: Diversity analysis (camera vs. LiDAR, YOLOv8 vs. Faster R-CNN)

---

## Verification and Validation

### Verification Methods (ISO 26262-8)

**Requirements-based Testing:**
- Each safety requirement has corresponding test case
- Traceability matrix: Requirement → Test → Result

**Back-to-back Testing:**
- Compare ML model output with reference implementation
- Useful for regression testing after model updates

**Fault Injection:**
- Inject hardware faults (bit flips, sensor failures)
- Verify safety mechanisms trigger correctly

### Validation Methods (ISO 26262-4)

**Validation Goals:**
- Demonstrate safety goals are sufficient (complete, correct)
- Verify safety goals are achieved in vehicle

**Techniques:**
- Test drives on proving grounds
- HIL (Hardware-in-the-Loop) with representative sensor inputs
- Subjective evaluation by safety experts

---

## Practical Examples

### Example 1: Hazard Analysis for Lane Keeping Assist (ASIL B)

**Item:** Lane Keeping Assist System (LKAS)
**Function:** Keep vehicle centered in lane on highways

**Hazards:**
- H1: Unintended lane departure
- H2: False intervention (steering into adjacent lane)

**HARA for H1:**
- Severity: S2 (collision with adjacent vehicle or barrier)
- Exposure: E3 (driver inattentive ~5% of highway driving)
- Controllability: C1 (driver can easily override)
- **ASIL: B**

**Safety Goal:** Prevent unintended lane departure due to LKAS malfunction

**Functional Safety Requirements:**
- FSR-1: Lane markings detected with >95% recall
- FSR-2: Steering intervention limited to <2° per second
- FSR-3: Driver override (torque >5 Nm) immediately disables LKAS
- FSR-4: System degraded if lane confidence <80%

### Example 2: SOTIF Analysis for Adaptive Cruise Control (ACC)

**Known Performance Limitations:**

| ID | Limitation | Triggering Condition | Mitigation |
|----|-----------|---------------------|------------|
| L1 | Radar cannot detect stationary objects at >60 km/h | Highway with stopped vehicle ahead | Camera-based detection as backup |
| L2 | Reduced range in heavy rain (-30%) | Rainfall >50mm/h | Increase minimum following distance |
| L3 | False detection from overhead signs | Gantry signs over roadway | Angle-of-arrival filtering |

**Validation Scenarios:**
1. **Cut-in scenario**: Vehicle merges into ego lane from adjacent lane
   - Test cases: 100 (varying speeds, distances, vehicle types)
   - Acceptance: Zero collisions, <5 hard braking events

2. **Stationary target**: Stopped vehicle ahead on highway
   - Test cases: 50 (varying visibility, distance)
   - Acceptance: Camera detects target, ACC disengages gracefully

3. **Weather degradation**: Heavy rain, fog
   - Test cases: 30 (varying rainfall, fog density)
   - Acceptance: System increases following distance or alerts driver

---

## References

### Standards

- **ISO 26262:2018** - Road vehicles — Functional safety (Parts 1-12)
- **ISO 21448:2022** - Road vehicles — Safety of the intended functionality (SOTIF)
- **ISO/PAS 21448:2019** - Preliminary version of SOTIF
- **SAE J3016:2021** - Taxonomy and Definitions for Terms Related to Driving Automation Systems

### Academic Papers

- Burton et al. (2023): "Safety of the Intended Functionality: Engineering the System"
- Koopman & Wagner (2017): "Autonomous Vehicle Safety: An Interdisciplinary Challenge"
- Riedmaier et al. (2020): "Survey on Scenario-Based Safety Assessment of Automated Vehicles"

### Books

- **"ISO 26262 - A Practical Guide"** by Schmittner et al. (2022)
- **"Automated Driving: Safer and More Efficient Future Driving"** by Watzenig & Horn (2016)
- **"Functional Safety for Road Vehicles"** by Hillenbrand et al. (2021)

### Industry Guidelines

- [UNECE WP.29 Guidelines on Automated Vehicles](https://unece.org/transport/vehicle-regulations)
- [SAE Standards for Automated Driving](https://www.sae.org/standards/)
- [ASAM OpenSCENARIO](https://www.asam.net/standards/detail/openscenario/) - Scenario description format

---

**Document Version:** 1.0
**Last Updated:** 2025-01-18
**Author:** Milin Patel
**License:** MIT

---

*This document is part of the comprehensive Autonomous Driving: AI, Safety, and Security Workshop. For cybersecurity, see [SECURITY.md](SECURITY.md). For AI-specific safety considerations, see [AI_SAFETY.md](AI_SAFETY.md).*
