# TARA Template: Threat Analysis and Risk Assessment (ISO/SAE 21434)

## Document Information

| Field | Value |
|-------|-------|
| **System/Item Name** | [Enter system name] |
| **Version** | [Version number] |
| **Date** | [Date] |
| **Prepared by** | [Name/Team] |
| **Reviewed by** | [Name/Team] |
| **Security Classification** | [Confidential/Restricted/Internal] |
| **Status** | Draft / In Review / Approved |

---

## 1. Item Definition

### 1.1 System Description

**Item Name:** [System or component being analyzed]

**Purpose:** [Brief description of functionality]

**Connectivity:**
- External interfaces: [List all external connections]
- Communication protocols: [List protocols: CAN, Ethernet, V2X, etc.]
- Update mechanisms: [OTA, diagnostic port, etc.]

**Example:**
```
Item Name: Pedestrian Detection and AEB System
Purpose: Detect pedestrians and automatically brake to prevent collisions
Connectivity:
  - External interfaces: Camera, LIDAR, V2X module, cloud backend
  - Protocols: CAN-FD, Ethernet, DSRC/C-V2X, HTTPS
  - Updates: OTA updates for ML models and firmware
```

### 1.2 System Architecture

[Insert architecture diagram showing data flows and attack surfaces]

**Key Components:**
1. [Component]: [Description and security relevance]
2. [Component]: [Description and security relevance]

---

## 2. Asset Identification

Identify assets that require protection:

| Asset ID | Asset Name | Asset Type | Cybersecurity Property | Value/Criticality | Justification |
|----------|------------|------------|----------------------|-------------------|---------------|
| A-001 | [Name] | [Data/SW/HW/Function] | C / I / A | High/Medium/Low | [Why important] |
| A-002 | | | | | |

**Cybersecurity Properties:**
- **C (Confidentiality)**: Prevent unauthorized disclosure
- **I (Integrity)**: Prevent unauthorized modification
- **A (Availability)**: Ensure authorized access when needed

**Example:**
| Asset ID | Asset Name | Asset Type | Cybersecurity Property | Value/Criticality | Justification |
|----------|------------|------------|----------------------|-------------------|---------------|
| A-001 | Camera sensor data | Data | **I** | Critical | False data → collision |
| A-002 | ML model weights | Software | **I** | Critical | Poisoned model → failures |
| A-003 | ECU firmware | Software | **I** | Critical | Malicious code → arbitrary behavior |
| A-004 | V2X communication | Function | **I, A** | High | False messages → wrong decisions |
| A-005 | OTA update channel | Function | **I** | Critical | Compromised updates → fleet-wide impact |
| A-006 | User privacy data | Data | **C** | High | Regulatory compliance (GDPR) |

---

## 3. Threat Scenario Identification

### 3.1 Threat Actors

Identify potential attackers:

| Actor Type | Motivation | Capability Level | Examples |
|------------|------------|------------------|----------|
| Script kiddie | Curiosity, fame | Low | Hobbyist using public exploits |
| Skilled individual | Financial gain, revenge | Medium | Experienced hacker |
| Organized crime | Financial gain | High | Ransomware groups |
| Competitor | Corporate espionage | High | Industrial espionage |
| Nation state | Strategic advantage | Very High | APT groups |
| Insider threat | Various | Varies | Malicious employee/contractor |

**Relevant actors for this system:** [List applicable threat actors]

### 3.2 Attack Goals

What might attackers want to achieve?

- [ ] Cause safety hazard (injury/death)
- [ ] Steal sensitive data (privacy breach)
- [ ] Disable system (availability attack)
- [ ] Take control of vehicle
- [ ] Financial fraud
- [ ] Reputation damage
- [ ] Espionage (steal IP)
- [ ] Other: [Specify]

---

## 4. Threat Scenarios

For each asset, identify threat scenarios:

| Threat ID | Asset ID | Threat Scenario | Attack Vector | Threat Actor | Attack Goal |
|-----------|----------|-----------------|---------------|--------------|-------------|
| T-001 | A-001 | [What attack] | [How executed] | [Who] | [Why] |
| T-002 | | | | | |

**Example:**
| Threat ID | Asset ID | Threat Scenario | Attack Vector | Threat Actor | Attack Goal |
|-----------|----------|-----------------|---------------|--------------|-------------|
| T-001 | A-001 | Camera feed spoofing via adversarial patch | Physical placement of patch in environment | Skilled individual | Cause collision |
| T-002 | A-002 | Model poisoning via compromised OTA update | Network MITM attack or backend compromise | Organized crime | Fleet-wide disruption |
| T-003 | A-003 | Firmware tampering via diagnostic port | Physical access to OBD-II port | Skilled individual | Vehicle theft enabler |
| T-004 | A-004 | V2X message injection | Wireless attack, rogue V2X transmitter | Skilled individual | Cause wrong maneuvers |
| T-005 | A-001 | Sensor blinding via laser attack | Directed energy weapon | Skilled individual | Disable detection |

---

## 5. Impact Rating

Rate the impact of successful attacks on four dimensions (Scale: 1-4):

### 5.1 Impact Categories

| Rating | Safety | Financial | Operational | Privacy |
|--------|--------|-----------|-------------|---------|
| **4 - Severe** | Fatalities probable | > $10M loss | Complete system failure | Massive data breach |
| **3 - Major** | Serious injuries | $1M - $10M | Major degradation | Significant breach |
| **2 - Moderate** | Minor injuries | $100K - $1M | Partial degradation | Limited breach |
| **1 - Negligible** | No injuries | < $100K | Minor impact | No privacy impact |

### 5.2 Impact Assessment

| Threat ID | Safety Impact | Financial Impact | Operational Impact | Privacy Impact | Overall Impact |
|-----------|--------------|------------------|-------------------|----------------|----------------|
| T-001 | [1-4] | [1-4] | [1-4] | [1-4] | [Max of all] |
| T-002 | | | | | |

**Example:**
| Threat ID | Safety Impact | Financial Impact | Operational Impact | Privacy Impact | Overall Impact |
|-----------|--------------|------------------|-------------------|----------------|----------------|
| T-001 | 4 | 2 | 3 | 1 | **4** |
| T-002 | 4 | 4 | 4 | 2 | **4** |
| T-003 | 4 | 3 | 4 | 2 | **4** |
| T-004 | 3 | 2 | 3 | 1 | **3** |
| T-005 | 4 | 1 | 3 | 1 | **4** |

---

## 6. Attack Feasibility Assessment

Rate feasibility based on five factors:

### 6.1 Feasibility Factors

| Factor | Very Low (0) | Low (1) | Medium (4) | High (7) | Very High (10) |
|--------|--------------|---------|------------|----------|----------------|
| **Elapsed Time** | > 1 year | 6-12 months | 3-6 months | 1-3 months | < 1 month |
| **Specialist Expertise** | Layman | Proficient | Expert | Multiple experts | Nation state |
| **Knowledge of Item** | Public info | Restricted | Confidential | Strictly confidential | Top secret |
| **Window of Opportunity** | Unlimited | Easy access | Moderate access | Difficult access | Very difficult |
| **Equipment** | Standard | Specialized | Bespoke | Multiple bespoke | State-level resources |

### 6.2 Attack Feasibility Rating

Sum the scores and determine overall feasibility:

| Total Score | Feasibility Rating |
|-------------|--------------------|
| 0-9 | Very Low |
| 10-17 | Low |
| 18-24 | Medium |
| 25-33 | High |
| 34+ | Very High |

### 6.3 Feasibility Analysis

| Threat ID | Time | Expertise | Knowledge | Opportunity | Equipment | Total Score | Feasibility |
|-----------|------|-----------|-----------|-------------|-----------|-------------|-------------|
| T-001 | [0-10] | [0-10] | [0-10] | [0-10] | [0-10] | [Sum] | [Rating] |
| T-002 | | | | | | | |

**Example:**
| Threat ID | Time | Expertise | Knowledge | Opportunity | Equipment | Total Score | Feasibility |
|-----------|------|-----------|-----------|-------------|-----------|-------------|-------------|
| T-001 | 4 (Medium) | 4 (Expert) | 1 (Public) | 0 (Unlimited) | 1 (Specialized patch) | **10** | **Low** |
| T-002 | 7 (High) | 7 (Multiple experts) | 7 (Strictly confidential) | 7 (Difficult) | 7 (Multiple bespoke) | **35** | **Very High** |
| T-003 | 4 (Medium) | 4 (Expert) | 4 (Confidential) | 4 (Moderate) | 4 (Bespoke tools) | **20** | **Medium** |
| T-004 | 4 (Medium) | 4 (Expert) | 1 (Public) | 0 (Unlimited) | 4 (Bespoke radio) | **13** | **Low** |
| T-005 | 1 (Low) | 4 (Expert) | 1 (Public) | 4 (Moderate) | 7 (Laser equipment) | **17** | **Low** |

---

## 7. Risk Determination

Combine impact and feasibility to determine risk level:

### 7.1 Risk Matrix

|                | Very Low Feasibility | Low Feasibility | Medium Feasibility | High Feasibility | Very High Feasibility |
|----------------|---------------------|-----------------|-------------------|------------------|-----------------------|
| **Impact 4**   | Medium | High | High | Critical | Critical |
| **Impact 3**   | Low | Medium | High | High | Critical |
| **Impact 2**   | Low | Low | Medium | Medium | High |
| **Impact 1**   | Negligible | Low | Low | Medium | Medium |

### 7.2 Risk Assessment

| Threat ID | Impact | Feasibility | Risk Level | Treatment Decision |
|-----------|--------|-------------|------------|-------------------|
| T-001 | [1-4] | [Very Low - Very High] | [Risk] | [Avoid/Reduce/Share/Retain] |
| T-002 | | | | |

**Risk Treatment Options:**
- **Avoid**: Remove the functionality (eliminate risk)
- **Reduce**: Implement mitigations (reduce likelihood or impact)
- **Share**: Transfer risk (insurance, supplier responsibility)
- **Retain**: Accept the risk (if within acceptable threshold)

**Example:**
| Threat ID | Impact | Feasibility | Risk Level | Treatment Decision |
|-----------|--------|-------------|------------|-------------------|
| T-001 | 4 | Low | **High** | **Reduce** (implement detection + sensor fusion) |
| T-002 | 4 | Very High | **Critical** | **Reduce** (code signing + secure boot + HSM) |
| T-003 | 4 | Medium | **High** | **Reduce** (port authentication + logging) |
| T-004 | 3 | Low | **Medium** | **Reduce** (message authentication + plausibility checks) |
| T-005 | 4 | Low | **High** | **Reduce** (redundant sensors + health monitoring) |

---

## 8. CAL (Cybersecurity Assurance Level) Determination

Determine CAL based on risk level (simplified approach):

| Risk Level | CAL | Description |
|------------|-----|-------------|
| Negligible | No CAL required | Standard quality processes |
| Low | CAL 1 | Basic security measures |
| Medium | CAL 2 | Moderate security assurance |
| High | CAL 3 | High security assurance |
| Critical | CAL 4 | Highest security assurance |

### CAL Assignment

| Threat ID | Risk Level | CAL | Justification |
|-----------|------------|-----|---------------|
| T-001 | High | **3** | Safety-critical, high impact |
| T-002 | Critical | **4** | Fleet-wide safety impact |
| T-003 | High | **3** | Direct vehicle control |
| T-004 | Medium | **2** | Limited scope, detectable |
| T-005 | High | **3** | Safety-critical sensor |

---

## 9. Cybersecurity Goals and Requirements

### 9.1 Cybersecurity Goals

Derive high-level security goals from threat scenarios:

| CG ID | Related Threat(s) | CAL | Cybersecurity Goal |
|-------|-------------------|-----|-------------------|
| CG-001 | T-001 | 3 | Prevent unauthorized manipulation of camera sensor data |
| CG-002 | T-002 | 4 | Ensure integrity of ML model and firmware updates |
| CG-003 | T-003 | 3 | Protect ECU firmware from tampering |
| CG-004 | T-004 | 2 | Ensure authenticity and integrity of V2X messages |
| CG-005 | T-005 | 3 | Detect and respond to sensor attacks |

### 9.2 Cybersecurity Requirements

Derive detailed requirements from cybersecurity goals:

| CR ID | CG ID | CAL | Cybersecurity Requirement | Verification Method |
|-------|-------|-----|---------------------------|---------------------|
| CR-001.1 | CG-001 | 3 | System shall detect adversarial patterns in camera feed using anomaly detection | Penetration testing |
| CR-001.2 | CG-001 | 3 | System shall use sensor fusion (camera + LIDAR) for cross-validation | Integration testing |
| CR-001.3 | CG-001 | 3 | System shall monitor confidence scores and trigger alerts on anomalies | Runtime testing |
| CR-002.1 | CG-002 | 4 | All OTA packages shall be signed using RSA-4096 or equivalent | Code review + testing |
| CR-002.2 | CG-002 | 4 | ECU shall verify signature before installing updates | Negative testing |
| CR-002.3 | CG-002 | 4 | Private signing keys shall be stored in HSM | Audit |
| CR-002.4 | CG-002 | 4 | Secure boot shall verify firmware integrity on startup | Boot testing |
| CR-003.1 | CG-003 | 3 | Diagnostic port access shall require authentication | Penetration testing |
| CR-003.2 | CG-003 | 3 | All diagnostic activities shall be logged | Log review |
| CR-004.1 | CG-004 | 2 | V2X messages shall be authenticated using PKI | Protocol testing |
| CR-004.2 | CG-004 | 2 | System shall validate message plausibility using sensor data | Integration testing |
| CR-005.1 | CG-005 | 3 | System shall monitor sensor health (saturation, dropout) | Fault injection |
| CR-005.2 | CG-005 | 3 | Redundant sensors shall be used for critical detection | Failure mode testing |

---

## 10. Verification and Validation

### 10.1 Security Testing Plan

| Test Type | CAL 1 | CAL 2 | CAL 3 | CAL 4 |
|-----------|-------|-------|-------|-------|
| Vulnerability scan | ++ | ++ | ++ | ++ |
| Penetration testing | + | ++ | ++ | ++ |
| Fuzzing | + | + | ++ | ++ |
| Code review | + | ++ | ++ | ++ |
| Cryptographic validation | + | ++ | ++ | ++ |
| Independent assessment | - | + | ++ | ++ |

++ = Highly Recommended, + = Recommended, - = Optional

### 10.2 Test Results

| Test ID | Requirement(s) Tested | Test Method | Result | Issues Found |
|---------|----------------------|-------------|--------|--------------|
| TEST-001 | CR-001.1 | Penetration test with adversarial patches | [Pass/Fail] | [Issues] |
| TEST-002 | CR-002.1, CR-002.2 | Negative testing with unsigned packages | [Pass/Fail] | [Issues] |

---

## 11. Supply Chain Security

### 11.1 Supplier/Partner Security

| Supplier/Partner | Component/Service | Security Requirements | Verification |
|------------------|-------------------|----------------------|--------------|
| [Name] | [Component] | [Requirements] | [How verified] |

**Example:**
| Supplier/Partner | Component/Service | Security Requirements | Verification |
|------------------|-------------------|----------------------|--------------|
| Camera Vendor | Camera module | Secure firmware, tamper detection | Supplier audit |
| Cloud Provider | OTA backend | ISO 27001, SOC 2 Type II | Certification review |
| ML Model Provider | Pre-trained models | Provenance tracking, integrity checks | Contract + validation |

---

## 12. Incident Response Plan

### 12.1 Incident Detection

- [ ] Security monitoring system deployed
- [ ] Anomaly detection active
- [ ] Log aggregation and analysis
- [ ] Threat intelligence feeds integrated

### 12.2 Response Procedures

| Severity | Response Time | Actions |
|----------|--------------|---------|
| Critical | Immediate (< 1 hour) | [Specific actions] |
| High | < 4 hours | [Specific actions] |
| Medium | < 24 hours | [Specific actions] |
| Low | < 1 week | [Specific actions] |

### 12.3 Communication Plan

| Stakeholder | When to Notify | Method | Responsible Party |
|-------------|---------------|--------|-------------------|
| Internal security team | All incidents | [Email/SMS/etc.] | [Role] |
| Management | High/Critical | [Method] | [Role] |
| Customers | Safety impact | [Method] | [Role] |
| Regulators | As required by law | [Method] | [Role] |

---

## 13. Continuous Monitoring

### 13.1 Monitoring Metrics

| Metric | Target | Current | Alert Threshold |
|--------|--------|---------|-----------------|
| Failed authentication attempts | [Target] | [Current] | [Threshold] |
| Anomaly detection rate | [Target] | [Current] | [Threshold] |
| Patch deployment time | [Target] | [Current] | [Threshold] |
| Vulnerabilities open | [Target] | [Current] | [Threshold] |

### 13.2 Update Triggers

TARA shall be updated when:
- [ ] New threat intelligence available
- [ ] Vulnerability discovered
- [ ] System architecture changes
- [ ] New connectivity added
- [ ] Security incident occurs
- [ ] Annual review (minimum)

---

## 14. Approval and Sign-off

### Assumptions and Limitations
[List assumptions made during TARA]

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
| Cybersecurity Manager | | | |
| Chief Information Security Officer | | | |
| Product Security Lead | | | |

---

## Notes and Best Practices

### Tips for TARA:

1. **Think like an attacker**: Consider all possible attack vectors
2. **Don't underestimate feasibility**: Attacks get easier over time
3. **Consider supply chain**: Attacks often come through partners
4. **Defense in depth**: Multiple layers of security
5. **Update regularly**: Threat landscape evolves constantly
6. **Integration is key**: Link with ISO 26262 HARA

### Common Mistakes:

- ❌ Focusing only on network attacks (physical access matters!)
- ❌ Ignoring insider threats
- ❌ Underestimating nation-state capabilities
- ❌ Not considering attack combinations
- ❌ Weak cryptography choices
- ❌ Insufficient monitoring and logging

### Integration with ISO 26262:

- Security vulnerabilities can cause safety hazards
- TARA should reference HARA hazards
- CAL should align with ASIL where applicable
- Combined safety-security analysis recommended

---

**Template Version:** 1.0
**Last Updated:** November 2024
**Reference Standard:** ISO/SAE 21434:2021
