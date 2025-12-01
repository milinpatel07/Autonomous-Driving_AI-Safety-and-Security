# Exercise 11: Multi-Standard Integration - Autonomous Parking System

**Session 5: Standards Integration and Deployment**
**Estimated Time**: 90 minutes

---

## Learning Objectives

- Apply ISO 26262, ISO 21448, and ISO/SAE 21434 to the same system
- Perform integrated HARA + SOTIF + TARA analysis
- Resolve conflicts between standards
- Create unified safety and security argumentation
- Understand how standards complement each other

---

## Scenario: Automated Valet Parking (AVP) System

You are designing an Automated Valet Parking system for a shopping mall:

### System Description

**Operational Concept**:
1. Driver arrives at designated drop-off zone
2. Driver activates AVP via smartphone app
3. Vehicle autonomously navigates to parking spot
4. When driver returns, summons vehicle via app
5. Vehicle drives to pick-up zone

**System Components**:
- **Perception**: 4 surround-view cameras, 12 ultrasonic sensors, HD map
- **Localization**: GPS + HD map matching + visual odometry
- **Planning**: Path planning, trajectory generation
- **Control**: Low-speed control (max 10 km/h)
- **Connectivity**: 4G/5G for cloud communication, V2I for parking guidance
- **HMI**: Smartphone app for user commands

**ODD**:
- Geofenced parking garage
- Paved surface, marked spaces
- Dry weather only (garage is covered)
- Max speed: 10 km/h
- No human driver supervision

**ASIL Target**: ASIL B (moderate speed, limited ODD)

---

## Part 1: Integrated Hazard Identification (25 minutes)

### Task 1.1: Identify Hazards Requiring Multiple Standards

For each hazard, determine which standards apply:

**Template**:

| Hazard ID | Hazard Description | ISO 26262? | ISO 21448? | ISO/SAE 21434? | Rationale |
|-----------|-------------------|------------|------------|----------------|-----------|
| H-01 | Example: Collision with pedestrian in parking garage | ✓ | ✓ | ✗ | 26262: Sensor HW fault; 21448: Poor lighting limits detection; Not 21434: No cyber attack |
| ... | ... | ... | ... | ... | ... |

**Your Task**: Identify **at least 8 hazards**, covering:
- At least 3 requiring ISO 26262 only
- At least 3 requiring ISO 21448
- At least 2 requiring ISO/SAE 21434
- At least 2 requiring MULTIPLE standards

**Hint**: Think about:
- Hardware faults (26262)
- AI perception limitations (21448)
- Connectivity vulnerabilities (21434)
- Combined scenarios (e.g., cyberattack exploits AI weakness)

---

## Part 2: ISO 26262 - Functional Safety Analysis (20 minutes)

### Task 2.1: HARA (Hazard Analysis and Risk Assessment)

Select **3 hazards** from Part 1 that require ISO 26262 analysis.

**HARA Template**:

| Hazard | Operational Situation | Severity (S) | Exposure (E) | Controllability (C) | ASIL |
|--------|----------------------|--------------|--------------|---------------------|------|
| H-01: Collision with pedestrian | Vehicle moving in garage, pedestrian crossing | S3 (life-threatening) | E4 (high probability) | C2 (normally controllable) | ASIL C |
| ... | ... | ... | ... | ... | ... |

**Severity (S)**:
- S0: No injuries
- S1: Light/moderate injuries
- S2: Severe/fatal injuries (one person)
- S3: Life-threatening/fatal injuries (several persons)

**Exposure (E)**:
- E0: Incredible (<0.001%)
- E1: Very low (0.001-0.1%)
- E2: Low (0.1-1%)
- E3: Medium (1-10%)
- E4: High (>10%)

**Controllability (C)**:
- C0: Controllable in general
- C1: Simply controllable
- C2: Normally controllable
- C3: Difficult/uncontrollable

**ASIL Determination** (use ISO 26262-3 table):
- QM (no ASIL): Low risk
- ASIL A: Lowest
- ASIL B: Low-medium
- ASIL C: Medium-high
- ASIL D: Highest

### Task 2.2: Safety Goals and FSC

For your **highest ASIL hazard** (likely ASIL B or C):

**Safety Goal**:
```
SG-[number]: [Description]

Associated Hazard: H-[number]
ASIL: [A/B/C/D]
Safe State: [What is safe state?]

Goal: The system shall [prevent/detect/mitigate] [hazard]
      to ensure [safety outcome]
```

**Functional Safety Concept (FSC)**:

Derive 2-3 functional safety requirements:

```
FSR-[number]: [Description]

Derived from: SG-[number]
ASIL: [Inherited from safety goal]

Requirement: The [component] shall [specific function]

Rationale: [How this prevents the hazard]

Verification: [How to test]
```

**Example**:

```
Safety Goal SG-01: Prevent Collision with Pedestrians

Associated Hazard: H-01
ASIL: C
Safe State: Vehicle stopped

Goal: The AVP system shall detect pedestrians in vehicle path
      and stop before collision to prevent pedestrian injuries.

---

FSR-01-1: Pedestrian Detection

Derived from: SG-01
ASIL: C

Requirement: The perception system shall detect pedestrians
within 10 meters with ≥99.9% probability (ASIL C).

Rationale: Early detection allows sufficient braking distance
at 10 km/h.

Verification: Test on 10,000 pedestrian scenarios from garage dataset.

---

FSR-01-2: Emergency Braking

Derived from: SG-01
ASIL: C

Requirement: The control system shall initiate emergency braking
within 100ms of pedestrian detection.

Rationale: At 10 km/h, 100ms reaction + 2m braking distance =
safe stop within 10m.

Verification: HIL (Hardware-in-Loop) testing with injected pedestrian detections.
```

---

## Part 3: ISO 21448 (SOTIF) Analysis (20 minutes)

### Task 3.1: Identify Performance Limitations and Triggering Conditions

Select **2 hazards** from Part 1 that involve AI/perception limitations (ISO 21448).

**SOTIF Analysis Template**:

```markdown
## SOTIF Analysis: [Hazard Description]

### Performance Limitation
**Component**: [e.g., Camera-based pedestrian detection]
**Limitation**: [What is the fundamental limitation?]
**Root Cause**: [Why does this limitation exist?]

### Triggering Conditions
List conditions that trigger the limitation:
1. [Environmental: Lighting, weather, etc.]
2. [Scenario: Unusual pedestrian behavior, occlusion, etc.]
3. [System state: Speed, sensor degradation, etc.]

### Known Safe vs. Known Unsafe vs. Unknown
- **Known Safe**: [Scenarios validated to be safe]
- **Known Unsafe**: [Scenarios known to fail - need mitigation]
- **Unknown**: [Scenarios not yet tested - residual risk]

### Mitigation Strategies
1. **Design**: [How to reduce triggering conditions?]
2. **Verification**: [How to discover unknown unsafe scenarios?]
3. **Runtime**: [How to detect if operating in unsafe scenario?]

### Residual Risk Assessment
- After mitigation, what residual risk remains?
- Is this acceptable for ASIL B system?
- How to argue safety despite residual risk?
```

**Example**:

```markdown
## SOTIF Analysis: Pedestrian Detection in Low Light

### Performance Limitation
**Component**: RGB camera-based pedestrian detection
**Limitation**: Reduced accuracy in low-light areas of garage
**Root Cause**: Cameras rely on visible light; some garage areas poorly lit

### Triggering Conditions
1. Environmental: Shadows, dark corners, burnt-out lights
2. Scenario: Pedestrian wearing dark clothing
3. System state: Camera auto-exposure hasn't adapted yet

### Known Safe vs. Known Unsafe vs. Unknown
- **Known Safe**: Well-lit areas, pedestrians in bright clothing (validated on 5,000 scenarios)
- **Known Unsafe**: Dark corners + dark clothing (27 failure cases identified)
- **Unknown**: Unusual clothing (reflective vests?), children, wheelchairs

### Mitigation Strategies
1. **Design**:
   - Add infrared cameras for low-light
   - Reduce speed to 5 km/h in known dark areas
   - Illuminate area with vehicle lights
2. **Verification**:
   - Test in all garage lighting conditions
   - Synthetic data augmentation (darkened images)
3. **Runtime**:
   - Detect low-light via camera exposure settings
   - Trigger graceful degradation (slow down)

### Residual Risk Assessment
After mitigation: Estimated residual risk = 1 failure per 10 million km
For ASIL B: Acceptable (comparable to human driver)
Safety argument: Multi-layered mitigation reduces risk to ALARP
```

---

## Part 4: ISO/SAE 21434 (Cybersecurity) Analysis (15 minutes)

### Task 4.1: TARA (Threat Analysis and Risk Assessment)

Select **2 hazards** from Part 1 involving cybersecurity threats.

**TARA Template**:

```markdown
## TARA: [Threat Scenario]

### Asset
**Asset**: [What needs protection?]
**Damage Scenario**: [What happens if asset compromised?]
**Safety Impact**: [How does this relate to ISO 26262 hazards?]

### Threat Scenario
**Attacker**: [Who? Motivation?]
**Attack Method**: [How is attack executed?]
**Attack Path**: [Step-by-step attack sequence]

### Attack Feasibility
- **Elapsed Time**: [<1 day, <1 month, >1 month]
- **Specialist Expertise**: [Laymen, Proficient, Expert, Multiple Experts]
- **Knowledge of System**: [Public, Restricted, Confidential, Strictly Confidential]
- **Window of Opportunity**: [Unlimited, Easy, Moderate, Difficult, None]
- **Equipment**: [Standard, Specialized, Bespoke, Multiple Bespoke]
- **Feasibility Rating**: [Very High, High, Medium, Low, Very Low]

### Impact Rating
- **Safety**: [Severe, Major, Moderate, Negligible]
- **Financial**: [Severe, Major, Moderate, Negligible]
- **Operational**: [Severe, Major, Moderate, Negligible]
- **Privacy**: [Severe, Major, Moderate, Negligible]

### CAL (Cybersecurity Assurance Level)
Based on feasibility + impact: [CAL 1-4]

### Cybersecurity Goal
**CG-[number]**: The system shall [protect/detect/respond] to [threat]
to prevent [impact].

### Cybersecurity Requirements
1. **CR-[number]**: [Specific security control]
2. **CR-[number]**: [Specific security control]
```

**Example**:

```markdown
## TARA: Malicious App Command Injection

### Asset
**Asset**: Smartphone app command interface
**Damage Scenario**: Attacker sends false "summon vehicle" commands
**Safety Impact**: Vehicle moves unexpectedly, potential collision (relates to H-01)

### Threat Scenario
**Attacker**: Malicious individual in parking garage
**Attack Method**: Intercept and replay app commands
**Attack Path**:
1. Attacker captures legitimate app command (man-in-the-middle)
2. Replays command when victim's vehicle is parked
3. Vehicle starts moving unexpectedly
4. Potential collision with pedestrians or other vehicles

### Attack Feasibility
- **Elapsed Time**: < 1 day
- **Specialist Expertise**: Proficient (basic RF knowledge)
- **Knowledge of System**: Public (app protocol may be reverse-engineered)
- **Window of Opportunity**: Easy (garage is public space)
- **Equipment**: Specialized (SDR - Software Defined Radio)
- **Feasibility Rating**: High

### Impact Rating
- **Safety**: Major (potential injury)
- **Financial**: Moderate (vehicle damage)
- **Operational**: Major (service disruption)
- **Privacy**: Negligible

### CAL (Cybersecurity Assurance Level)
Feasibility: High + Impact: Major → **CAL 3**

### Cybersecurity Goal
**CG-02**: The system shall authenticate all app commands to prevent
unauthorized vehicle control, thereby preventing unintended vehicle motion.

### Cybersecurity Requirements
1. **CR-02-1**: App commands shall be encrypted using TLS 1.3 with mutual authentication
2. **CR-02-2**: Each command shall include timestamp and sequence number to prevent replay attacks
3. **CR-02-3**: Vehicle shall verify command originated from authorized user device (device fingerprinting)
```

---

## Part 5: Integration and Conflict Resolution (10 minutes)

### Task 5.1: Unified Safety-Security Analysis

Now, identify scenarios where **safety and security interact**:

**Combined Scenario Template**:

```markdown
## Combined Analysis: [Scenario]

### Multi-Standard Applicability
- ISO 26262: [Which safety goal?]
- ISO 21448: [Which SOTIF limitation?]
- ISO/SAE 21434: [Which cybersecurity goal?]

### Interaction
[How do safety and security issues combine?]

### Example Combined Scenario:
**Scenario**: Cyberattack on perception system + AI limitation

1. **ISO 26262**: Camera hardware is functioning (no fault)
2. **ISO 21448**: Camera struggles in low light (performance limitation)
3. **ISO/SAE 21434**: Attacker injects false "all clear" sensor data

**Combined Risk**:
- Normally, low-light condition would trigger graceful degradation (slow down)
- But attacker's false data prevents detection of limitation
- System continues at normal speed despite degraded perception
- **Much higher risk than either issue alone**

### Integrated Mitigation
[How to address combined threat?]

**Example**:
1. **Sensor Fusion** (26262 + 21448): Don't rely on camera alone; use ultrasonic as backup
2. **Intrusion Detection** (21434): Detect anomalous sensor data patterns
3. **Runtime Monitoring** (21448): Independent check of lighting conditions
```

**Your Task**:

Create **1 combined analysis** showing how safety + security + SOTIF issues interact.

### Task 5.2: Resolve Conflicts Between Standards

**Potential Conflict Example**:

- **ISO 26262 says**: "Use redundant sensors for ASIL C"
- **ISO 21448 says**: "Redundant sensors of same type may have same limitation (e.g., all cameras fail in dark)"
- **ISO/SAE 21434 says**: "More sensors = larger attack surface"

**Your Task**:

Identify **1 conflict** between standards and propose resolution:

**Conflict Resolution Template**:

```markdown
## Conflict: [Brief description]

### ISO 26262 Requirement
[What does 26262 require?]

### ISO 21448 / ISO/SAE 21434 Concern
[What does other standard say that conflicts?]

### Analysis
[Why is this a conflict?]

### Resolution
[How to satisfy both standards?]

### Traceability
- 26262 requirement [ID]: Met by [solution]
- 21448/21434 requirement [ID]: Met by [solution]
```

---

## Deliverables

Submit a comprehensive report containing:

1. **Part 1**: Hazard identification table (8+ hazards)
2. **Part 2**: ISO 26262 HARA + 1 safety goal + 2-3 FSRs
3. **Part 3**: 2 SOTIF analyses with mitigations
4. **Part 4**: 2 TARA analyses with cybersecurity goals
5. **Part 5**:
   - 1 combined safety-security scenario analysis
   - 1 conflict resolution

**Bonus** (Optional, +20 points):
- Create integrated traceability matrix linking:
  - Hazards → Safety Goals → FSRs → SOTIF Mitigations → Cybersecurity Goals
- Visual diagram showing how standards overlap for your system
- Cost estimate for implementing all requirements

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Hazard Identification** | 15 | Complete, realistic hazards covering all standards |
| **ISO 26262 HARA** | 20 | Correct ASIL determination and safety goals |
| **ISO 21448 SOTIF** | 20 | Thorough limitation analysis and mitigation |
| **ISO/SAE 21434 TARA** | 20 | Realistic threat scenarios and CAL determination |
| **Integration** | 15 | Understanding of standard interactions |
| **Conflict Resolution** | 10 | Practical and compliant resolution |
| **Total** | 100 | |

---

## References

- **ISO 26262-3:2018** - Concept phase (HARA methodology)
- **ISO 21448:2022** - SOTIF (Performance limitation analysis)
- **ISO/SAE 21434:2021** - Cybersecurity (TARA methodology)
- **SAE J3061** - Cybersecurity guidebook for cyber-physical vehicle systems

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
