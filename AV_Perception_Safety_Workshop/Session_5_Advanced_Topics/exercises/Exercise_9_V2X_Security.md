# Exercise 9: V2X Security Analysis

**Session 5: Advanced Topics in AV Safety**
**Estimated Time**: 60 minutes

---

## Learning Objectives

- Apply TARA (Threat Analysis and Risk Assessment) methodology to V2X systems
- Identify attack vectors for V2X communication
- Assess attack feasibility and impact
- Define cybersecurity goals and requirements
- Design countermeasures for V2X threats

---

## Scenario: Smart Intersection with V2X Communication

You are designing a smart intersection system that uses V2X communication to improve safety:

### System Components

1. **Roadside Unit (RSU)**:
   - Broadcasts Signal Phase and Timing (SPaT) messages
   - Receives and forwards Vehicle-to-Infrastructure (V2I) messages
   - Connected to traffic signal controller

2. **Vehicles**:
   - Equipped with C-V2X or DSRC communication
   - Receive SPaT, MAP, and emergency vehicle alerts
   - Broadcast Basic Safety Messages (BSM) with position, speed, heading

3. **Backend Server**:
   - Aggregates traffic data from RSUs
   - Optimizes signal timing
   - Detects incidents

### Communication Messages

- **SPaT** (Signal Phase and Timing): Traffic light status, countdown
- **MAP**: Intersection geometry, lane configuration
- **BSM** (Basic Safety Message): Vehicle position, speed, heading, size
- **EVA** (Emergency Vehicle Alert): Emergency vehicle approaching

---

## Part 1: Threat Identification (20 minutes)

### Task 1.1: Identify Attack Vectors

For each component, identify potential attack vectors:

**Template**:

| Component | Attack Vector | Attack Method | Potential Impact |
|-----------|---------------|---------------|------------------|
| RSU | Example: Message injection | Attacker sends false SPaT | Vehicles accelerate into red light |
| ... | ... | ... | ... |

Identify at least **10 different attack vectors** across all components.

### Task 1.2: Attack Scenarios

Describe **3 detailed attack scenarios**:

1. **Sybil Attack**:
   - How could an attacker create multiple fake vehicle identities?
   - What impact would this have on traffic flow?
   - How could it affect safety?

2. **Message Spoofing**:
   - How could an attacker spoof SPaT messages?
   - What happens if false "green light" messages are sent?
   - Impact on autonomous vehicles vs. human drivers?

3. **Denial of Service (DoS)**:
   - How could an attacker flood the V2X channel?
   - What's the impact on intersection safety?
   - Can emergency vehicles still communicate?

---

## Part 2: Risk Assessment (15 minutes)

### Task 2.1: Attack Feasibility Analysis

For each attack vector from Part 1, assess feasibility using ISO/SAE 21434 criteria:

**Feasibility Factors**:
- **Elapsed Time**: How long does attack take? (<1 day, <1 month, >1 month)
- **Specialist Expertise**: Required knowledge (Laymen, Proficient, Expert, Multiple Experts)
- **Knowledge of System**: Required understanding (Public, Restricted, Confidential, Strictly Confidential)
- **Window of Opportunity**: Access needed (Unlimited, Easy, Moderate, Difficult, None)
- **Equipment**: Tools required (Standard, Specialized, Bespoke, Multiple Bespoke)

**Feasibility Rating**:
- **Very High**: All factors "easy"
- **High**: Mix of easy and moderate
- **Medium**: Mix of moderate and difficult
- **Low**: Mostly difficult
- **Very Low**: All factors difficult or impossible

**Template**:

| Attack Vector | Elapsed Time | Expertise | Knowledge | Opportunity | Equipment | Feasibility Rating |
|---------------|--------------|-----------|-----------|-------------|-----------|-------------------|
| Example: RSU message injection | < 1 month | Proficient | Public | Moderate | Specialized | High |
| ... | ... | ... | ... | ... | ... | ... |

### Task 2.2: Impact Assessment

Assess the safety impact of each attack:

**Impact Categories**:
- **Severe**: Potential for fatalities
- **Major**: Serious injuries likely
- **Moderate**: Minor injuries possible
- **Negligible**: Property damage only

**Template**:

| Attack Vector | Impact Category | Justification |
|---------------|-----------------|---------------|
| Example: False green light SPaT | Severe | Could cause T-bone collision at high speed |
| ... | ... | ... |

---

## Part 3: Cybersecurity Requirements (15 minutes)

### Task 3.1: Define Cybersecurity Goals

For the **3 highest-risk** attack vectors (High feasibility + Severe/Major impact):

Define cybersecurity goals using the template:

**Template**:

```
Cybersecurity Goal CG-[number]: [Brief description]

Threat: [From Part 1]
Attack Vector: [From Part 1]
Asset: [What needs protection]
Impact: [From Part 2]

Goal: The system shall [protect/detect/respond to] [specific threat]
      to prevent [specific impact]

CAL (Cybersecurity Assurance Level): [1-4, based on impact and feasibility]
```

**Example**:

```
Cybersecurity Goal CG-01: Prevent False SPaT Message Injection

Threat: Attacker injects false SPaT messages
Attack Vector: Unauthorized message transmission to RSU
Asset: Signal Phase and Timing data integrity
Impact: Severe (collision risk)

Goal: The RSU shall authenticate all SPaT messages to prevent
      injection of false traffic light status, thereby preventing
      vehicles from receiving incorrect signal information.

CAL: 4 (High)
```

Create **at least 3 cybersecurity goals**.

### Task 3.2: Derive Cybersecurity Requirements

For each goal, derive **2-3 specific requirements**:

**Template**:

```
Cybersecurity Requirement CR-[number]: [Brief description]

Derived from: CG-[number]

Requirement: The [component] shall [specific security measure]

Rationale: [Why this requirement addresses the goal]

Verification: [How to test this requirement]
```

**Example**:

```
Cybersecurity Requirement CR-01-1: SPaT Message Authentication

Derived from: CG-01

Requirement: The RSU shall authenticate all SPaT messages using
ECDSA-256 digital signatures as specified in IEEE 1609.2.

Rationale: Digital signatures ensure messages originate from
authorized traffic signal controller and haven't been tampered with.

Verification:
- Unit test: Verify RSU rejects messages with invalid signatures
- Penetration test: Attempt to inject unsigned messages, confirm rejection
- Performance test: Verify <50ms signature verification latency
```

Create **at least 6 requirements** (2 per goal).

---

## Part 4: Countermeasure Design (10 minutes)

### Task 4.1: Select Countermeasures

For each cybersecurity requirement, select appropriate countermeasures:

**Common V2X Countermeasures**:
- **Message Authentication**: Digital signatures (ECDSA, EdDSA)
- **Certificate Management**: PKI (Public Key Infrastructure)
- **Misbehavior Detection**: Identify anomalous messages
- **Geofencing**: Verify message origin location
- **Rate Limiting**: Prevent message flooding
- **Encryption**: Protect confidentiality (if needed)
- **Intrusion Detection**: Monitor for attacks
- **Secure Boot**: Prevent firmware tampering
- **Hardware Security Module (HSM)**: Protect cryptographic keys

**Template**:

| Requirement | Countermeasure | Implementation Details | Limitations |
|-------------|----------------|------------------------|-------------|
| CR-01-1 | ECDSA-256 signatures | IEEE 1609.2 standard | Latency: ~10-50ms, Certificate management complexity |
| ... | ... | ... | ... |

---

## Deliverables

Submit a report containing:

1. **Part 1**: Threat identification table and 3 attack scenarios
2. **Part 2**: Feasibility and impact assessment tables
3. **Part 3**:
   - 3 cybersecurity goals
   - 6+ cybersecurity requirements
4. **Part 4**: Countermeasure selection table

**Bonus** (Optional, +10 points):
- Create a threat diagram showing attack paths
- Estimate cost of implementing countermeasures
- Compare C-V2X vs. DSRC security features

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Threat Identification** | 25 | Completeness and realism of attack vectors |
| **Risk Assessment** | 25 | Correct application of ISO/SAE 21434 criteria |
| **Cybersecurity Goals** | 20 | Clear, specific, and traceable goals |
| **Requirements** | 20 | Requirements are verifiable and address goals |
| **Countermeasures** | 10 | Appropriate selection and justification |
| **Total** | 100 | |

---

## References

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering (Section 9: Threat Analysis)
- **IEEE 1609.2** - Security Services for V2X Communications
- **SAE J2735** - Dedicated Short Range Communications (DSRC) Message Set Dictionary
- **NIST Cybersecurity Framework** - Risk assessment methodology

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
