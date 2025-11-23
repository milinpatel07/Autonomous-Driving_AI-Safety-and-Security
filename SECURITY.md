<!--
Copyright (c) 2025 Milin Patel
Hochschule Kempten - University of Applied Sciences

Autonomous Driving: AI Safety and Security Workshop
This project is licensed under the MIT License.
-->

# Automotive Cybersecurity: ISO/SAE 21434

**Cybersecurity Engineering for Autonomous Vehicles**

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Standard:** ISO/SAE 21434:2021 - Road vehicles — Cybersecurity engineering

---

## Table of Contents

1. [Introduction](#introduction)
2. [ISO/SAE 21434 Overview](#isosae-21434-overview)
3. [Threat Analysis and Risk Assessment (TARA)](#threat-analysis-and-risk-assessment-tara)
4. [Attack Vectors for Autonomous Vehicles](#attack-vectors-for-autonomous-vehicles)
5. [Cybersecurity Requirements](#cybersecurity-requirements)
6. [Secure Development Lifecycle](#secure-development-lifecycle)
7. [Validation and Testing](#validation-and-testing)
8. [Incident Response](#incident-response)
9. [Case Studies](#case-studies)
10. [Practical Guidelines](#practical-guidelines)
11. [References](#references)

---

## Introduction

**ISO/SAE 21434** provides a comprehensive framework for cybersecurity engineering in road vehicles, addressing the entire lifecycle from concept to decommissioning. For autonomous vehicles, cybersecurity is critical as successful attacks can directly impact vehicle safety, passenger privacy, and public trust.

### Why Cybersecurity Matters for Autonomous Vehicles

1. **Safety Impact**: Cyberattacks can directly compromise vehicle control and passenger safety
2. **Attack Surface**: AVs have extensive connectivity (V2X, OTA updates, cloud services, sensors)
3. **Data Privacy**: AVs collect and process sensitive location, behavior, and biometric data
4. **Economic Impact**: Vehicle theft, ransomware, fleet manipulation
5. **Regulatory Compliance**: UNECE WP.29 R155 mandates cybersecurity management systems

### Integration with Functional Safety

**ISO/SAE 21434** complements **ISO 26262**:
- ISO 26262 addresses random hardware failures and systematic faults
- ISO/SAE 21434 addresses intentional malicious attacks
- Combined safety and security analysis required (SAHARA method)

---

## ISO/SAE 21434 Overview

### Standard Structure

ISO/SAE 21434:2021 consists of:
- **Clauses 1-4**: Scope, normative references, terms and definitions
- **Clause 5**: Organizational cybersecurity management
- **Clauses 6-8**: Project-dependent cybersecurity management
- **Clauses 9-15**: Distributed cybersecurity activities (concept, development, validation, operations)

### Cybersecurity Lifecycle Phases

```
Concept Phase
    ↓
Development Phase (Product, System, Hardware, Software)
    ↓
Production Phase
    ↓
Operations and Maintenance
    ↓
Decommissioning
```

### Key Principles

1. **Security by Design**: Integrate cybersecurity from earliest concept phase
2. **Defense in Depth**: Multiple layers of security controls
3. **Risk-Based Approach**: Prioritize based on threat severity and feasibility
4. **Continuous Monitoring**: Threat landscape evolves, ongoing vigilance required
5. **Coordinated Disclosure**: Responsible vulnerability reporting and patching

---

## Threat Analysis and Risk Assessment (TARA)

### TARA Process Overview

TARA systematically identifies assets, threats, attack paths, and determines risk levels to derive cybersecurity goals.

### Step 1: Asset Identification

**Definition**: Assets are elements with value requiring protection.

**Asset Categories for Autonomous Vehicles:**

| Asset Type | Examples | Value |
|------------|----------|-------|
| **Safety-Critical Functions** | Steering, braking, acceleration control | Life-critical |
| **Perception Data** | Camera, LiDAR, radar sensor feeds | Safety & privacy |
| **Localization** | GNSS, HD maps, IMU data | Safety & navigation |
| **Communication** | V2X messages, cloud connectivity | Safety & data |
| **Software/Firmware** | ECU firmware, perception algorithms, OTA packages | Integrity & availability |
| **Cryptographic Keys** | TLS certificates, signing keys | Confidentiality & trust |
| **Personal Data** | Passenger identity, location history | Privacy |
| **Diagnostic Data** | CAN logs, error codes | Confidentiality |

### Step 2: Threat Scenario Identification

**Damage Scenarios**: Potential harms resulting from cybersecurity compromises

**AV-Specific Damage Scenarios:**
1. **Loss of Vehicle Control**: Unauthorized steering, braking, acceleration
2. **Collision Inducement**: Manipulated perception causing collision
3. **Privacy Breach**: Exfiltration of location, identity, behavior data
4. **Denial of Service**: Vehicle rendered inoperable
5. **Data Manipulation**: Falsified sensor data, corrupted maps
6. **Fleet-Wide Attack**: Simultaneous compromise of multiple vehicles

### Step 3: Threat Analysis

**Threat Modeling Methodologies:**
- **STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- **Attack Trees**: Hierarchical representation of attack paths
- **EVITA**: E-safety Vehicle Intrusion Protected Applications

**Example Threat: Sensor Spoofing**

```
Asset: LiDAR Perception System
Threat Agent: Remote attacker with moderate expertise
Attack Method: Laser-based LiDAR spoofing (phantom objects)
Entry Point: Wireless, line-of-sight to sensor
Impact: False positive detection → emergency braking → rear-end collision
```

### Step 4: Impact Rating

**Impact Categories (ISO/SAE 21434 Clause 15.2):**

| Impact Level | Safety | Financial | Operational | Privacy |
|--------------|--------|-----------|-------------|---------|
| **Severe** | Multiple fatalities | >€10M | Fleet recall | Large-scale PII leak |
| **Major** | Injury or fatality | €1M-10M | Regional disruption | PII leak (hundreds) |
| **Moderate** | Possible injury | €100K-1M | Local disruption | PII leak (dozens) |
| **Negligible** | No injury | <€100K | Minor inconvenience | Isolated PII leak |

### Step 5: Attack Feasibility Rating

**Attack Feasibility Factors:**

| Factor | Low | Medium | High | Very High |
|--------|-----|--------|------|-----------|
| **Elapsed Time** | >6 months | 3-6 months | 1-3 months | <1 month |
| **Specialist Expertise** | Expert (nation-state) | Professional | Proficient | Layman |
| **Knowledge of Item** | Confidential info | Restricted info | Public info | Public info |
| **Window of Opportunity** | <10 min | <1 hr | <1 day | Unlimited |
| **Equipment** | Bespoke | Specialized | Standard | Standard |

**Attack Feasibility Levels:**
- **Very Low**: Infeasible for most attackers (requires nation-state resources)
- **Low**: Requires significant resources and expertise
- **Medium**: Achievable by skilled attackers with moderate resources
- **High**: Script-kiddie level, readily available tools

### Step 6: Risk Determination

**Risk Matrix:**

|  | **Very Low Feasibility** | **Low** | **Medium** | **High** |
|---|---|---|---|---|
| **Severe Impact** | Medium | High | Very High | Critical |
| **Major Impact** | Low | Medium | High | Very High |
| **Moderate Impact** | Very Low | Low | Medium | High |
| **Negligible Impact** | Very Low | Very Low | Low | Medium |

### Step 7: Risk Treatment

**Risk Treatment Options:**
1. **Avoid**: Remove functionality or asset
2. **Reduce**: Implement cybersecurity controls (most common)
3. **Share**: Transfer risk through insurance, contracts
4. **Retain**: Accept residual risk (requires management approval)

---

## Attack Vectors for Autonomous Vehicles

### 1. Sensor Attacks

#### 1.1 Camera Attacks

**Attack Types:**
- **Blinding**: High-intensity light (laser, LED) to saturate sensor
- **Adversarial Stickers**: Physical perturbations causing misclassification
- **Phantom Images**: Projecting false images onto surfaces
- **Lens Contamination**: Dirt, graffiti obscuring view

**Example: Adversarial Stop Sign**
- Researchers added small stickers to stop sign
- Neural network misclassifies as "Speed Limit 45 mph"
- Vehicle fails to stop at intersection

**Mitigations:**
- Multi-sensor fusion (camera + LiDAR + radar)
- Anomaly detection on perception outputs
- Physical tamper detection (camera cleaning status)
- Adversarial training and certified robustness

#### 1.2 LiDAR Attacks

**Attack Types:**
- **Spoofing**: Inject false laser returns (phantom objects)
- **Jamming**: Saturate sensor with noise to deny service
- **Relay Attack**: Capture and replay LiDAR data

**Technical Details:**
- Attacker uses ~905nm laser synchronized with victim LiDAR
- Can create phantom vehicles causing emergency braking
- Demonstrated at ranges up to 100 meters

**Mitigations:**
- Authentication of LiDAR returns (emerging research area)
- Cross-modal consistency checks (camera-LiDAR agreement)
- Return signal analysis (intensity, pulse shape)
- Frequency hopping and randomized scanning patterns

#### 1.3 GNSS Jamming and Spoofing

**Attack Types:**
- **Jamming**: Broadcast noise on GNSS frequencies (1.2-1.6 GHz)
- **Spoofing**: Transmit counterfeit GNSS signals

**Impact:**
- Localization failure → cannot determine position
- False position → vehicle navigates to wrong location
- Timing attacks on V2X synchronization

**Mitigations:**
- Multi-GNSS (GPS + Galileo + GLONASS + BeiDou)
- Inertial navigation fusion (GNSS + IMU + odometry)
- GNSS signal authentication (Galileo OSNMA, GPS Chimera)
- Antenna diversity and interference detection

### 2. V2X (Vehicle-to-Everything) Attacks

#### 2.1 Message Injection

**Attack**: Attacker broadcasts false V2X messages

**Scenarios:**
- False emergency vehicle approaching → unnecessary lane change
- False hazard warning → sudden braking
- False traffic light state → red light violation

**Standards:** ETSI ITS, IEEE 1609.2, SAE J2945

**Mitigations:**
- PKI-based message authentication (IEEE 1609.2)
- Misbehavior detection systems
- Plausibility checks (sensor fusion validation)
- Geographic and temporal consistency verification

#### 2.2 Sybil Attack

**Attack**: Single attacker creates multiple fake vehicle identities

**Impact:**
- Fake congestion → route manipulation
- Overwhelm V2X network (DoS)
- Influence cooperative perception

**Mitigations:**
- Pseudonym management with rate limiting
- Position verification using RF fingerprinting
- Radar-based vehicle validation

### 3. Backend and Cloud Attacks

#### 3.1 OTA (Over-the-Air) Update Attacks

**Attack Vectors:**
- Man-in-the-middle (MITM) during update download
- Compromised update server
- Rollback to vulnerable firmware version

**Mitigations:**
- Code signing with hardware root of trust (HSM)
- Secure boot chain (UEFI Secure Boot)
- TLS 1.3 with certificate pinning
- Rollback protection (version monotonicity)
- A/B partition redundancy

#### 3.2 Cloud Infrastructure Compromise

**Assets at Risk:**
- HD maps and route planning services
- Fleet management dashboards
- Telemetry and diagnostics databases
- Machine learning model training pipelines

**Mitigations:**
- Zero-trust architecture
- Network segmentation and micro-segmentation
- Container security (Kubernetes RBAC)
- Secrets management (HashiCorp Vault, AWS KMS)
- Continuous vulnerability scanning

### 4. In-Vehicle Network Attacks

#### 4.1 CAN Bus Injection

**Attack**: Attacker gains access to CAN bus (via OBD-II, compromised ECU, or physical access)

**Impact:**
- Inject malicious CAN frames (steering, braking, acceleration)
- Denial of service (bus flooding)
- Replay attacks

**Mitigations:**
- CAN authentication (CANAuth, AUTOSAR SecOC)
- Intrusion detection systems (IDS) monitoring CAN traffic
- Gateway firewalls between network domains
- Physical security of diagnostic ports

#### 4.2 ECU Exploitation

**Attack Paths:**
- Buffer overflows in ECU software
- Exploitation of diagnostics protocols (UDS, XCP)
- Supply chain compromise (backdoored ECUs)

**Mitigations:**
- Secure coding practices (CERT C, MISRA C)
- Static analysis (Coverity, Polyspace)
- Fuzzing (AFL, LibFuzzer)
- Hardware-based isolation (ARM TrustZone, Intel SGX)

### 5. Physical Access Attacks

#### 5.1 JTAG/Debug Interface Exploitation

**Attack**: Physical access to debug ports extracts firmware or modifies ECU

**Mitigations:**
- Disable debug interfaces in production vehicles
- Debug port authentication
- Tamper-evident seals
- Secure chip packaging (anti-probing)

#### 5.2 Supply Chain Attacks

**Attack**: Compromise during manufacturing, shipping, or maintenance

**Examples:**
- Backdoored hardware components
- Malware in third-party software libraries
- Unauthorized firmware modifications during servicing

**Mitigations:**
- Supplier security assessments (ISO/SAE 21434 Clause 6)
- Component authentication (PUF-based)
- Integrity verification (measured boot)
- Secure supply chain logistics

---

## Cybersecurity Requirements

### Cybersecurity Goals

**Definition**: High-level cybersecurity objectives derived from TARA

**Example Cybersecurity Goals for AV Perception:**

| ID | Asset | Threat | Cybersecurity Goal | CAL |
|----|-------|--------|-------------------|-----|
| CG-1 | Steering ECU | Unauthorized CAN messages | Ensure authenticity of steering commands | CAL-3 |
| CG-2 | LiDAR sensor | Spoofing attack | Detect and reject false LiDAR returns | CAL-2 |
| CG-3 | OTA update | Malicious firmware | Verify integrity and authenticity of firmware | CAL-4 |
| CG-4 | V2X communication | Message injection | Authenticate V2X messages | CAL-3 |
| CG-5 | Passenger data | Unauthorized access | Protect confidentiality of personal data | CAL-2 |

### Cybersecurity Assurance Level (CAL)

**CAL Levels** (similar to ASIL in ISO 26262):

| CAL | Attack Feasibility Threshold | Security Measures Required |
|-----|------------------------------|---------------------------|
| **CAL-4** | Very Low feasibility attacks must be prevented | Extensive security controls, formal verification |
| **CAL-3** | Low feasibility attacks must be prevented | Strong security controls, penetration testing |
| **CAL-2** | Medium feasibility attacks must be prevented | Moderate security controls |
| **CAL-1** | High feasibility attacks must be prevented | Basic security controls |

### Cybersecurity Requirements Decomposition

**Hierarchy**: Cybersecurity Goals → Cybersecurity Requirements → Cybersecurity Specifications

**Example: OTA Update Security (CG-3)**

```
Cybersecurity Goal (CG-3): Verify integrity and authenticity of firmware

  → Requirement 1: Firmware shall be signed using asymmetric cryptography
      → Spec 1.1: Use ECDSA P-256 or RSA-3072 for signing
      → Spec 1.2: Private keys stored in HSM (FIPS 140-2 Level 3)

  → Requirement 2: ECU shall verify signature before applying update
      → Spec 2.1: Implement secure boot with signature verification
      → Spec 2.2: Rollback protection using version counters

  → Requirement 3: Update communication shall be encrypted
      → Spec 3.1: Use TLS 1.3 with mutual authentication
      → Spec 3.2: Certificate pinning to prevent MITM
```

---

## Secure Development Lifecycle

### Security in Requirements Phase

**Activities:**
- Cybersecurity claims definition
- Misuse case analysis
- Abuse case testing plans

### Security in Design Phase

**Architecture Patterns:**
1. **Network Segmentation**: Separate safety-critical and infotainment domains
2. **Gateway Filtering**: Stateful firewall between network segments
3. **Secure Enclave**: Isolated execution environment for cryptographic operations
4. **Least Privilege**: ECUs only access necessary resources

**Example AV Network Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│  Sensor Domain (CAL-3)                                      │
│  - Camera, LiDAR, Radar ECUs                                │
│  - Local sensor fusion                                      │
└────────────────┬────────────────────────────────────────────┘
                 │
          ┌──────▼──────┐
          │   Gateway   │  ← Firewall, IDS, SecOC
          │   (CAL-4)   │
          └──────┬──────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│  Vehicle Control Domain (CAL-4)                             │
│  - Planning, Control, ADAS ECUs                             │
│  - Steering, Braking, Powertrain                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Infotainment Domain (CAL-1)                                │
│  - Head unit, Media, Apps                                   │
│  - No direct access to vehicle control                      │
└─────────────────────────────────────────────────────────────┘
```

### Security in Implementation Phase

**Secure Coding Guidelines:**
- **CERT C Coding Standard**: Memory safety, input validation
- **MISRA C:2012**: Safety and security coding rules
- **CWE Top 25**: Avoid common weaknesses (buffer overflow, SQL injection, etc.)

**Cryptographic Libraries:**
- OpenSSL, mbedTLS, wolfSSL (use established, audited libraries)
- Avoid custom cryptography implementations

**Key Management:**
- Hardware Security Module (HSM) for key storage
- Key derivation using HKDF (HMAC-based KDF)
- Key rotation policies

### Security in Verification Phase

**Verification Methods:**

| Method | Description | Tool Examples |
|--------|-------------|---------------|
| **Static Analysis** | Source code analysis without execution | Coverity, Polyspace, CodeSonar |
| **Fuzzing** | Automated input generation to find crashes | AFL, LibFuzzer, Peach Fuzzer |
| **Penetration Testing** | Simulated attacks by security experts | Metasploit, Burp Suite, CAN tools |
| **Vulnerability Scanning** | Automated scanning for known vulnerabilities | Nessus, OpenVAS, Nmap |
| **Code Review** | Manual inspection by security experts | N/A (human process) |

---

## Validation and Testing

### Cybersecurity Validation

**Objective**: Demonstrate that cybersecurity goals are achieved in representative conditions

### Penetration Testing for AVs

**Test Scope:**
1. **External Interfaces**: V2X, cellular, WiFi, Bluetooth
2. **Physical Interfaces**: OBD-II, USB, diagnostic ports
3. **Wireless Sensors**: Camera, LiDAR, radar, GNSS
4. **Update Mechanisms**: OTA firmware updates
5. **Backend Services**: Cloud APIs, fleet management

**Example Test Cases:**

| Test ID | Attack Scenario | Expected Outcome |
|---------|----------------|------------------|
| PT-01 | CAN bus flooding via OBD-II | Gateway rate-limits messages, critical ECUs unaffected |
| PT-02 | Fuzzing V2X BSM messages | No crash or undefined behavior |
| PT-03 | LiDAR spoofing with laser | Cross-sensor validation detects inconsistency |
| PT-04 | MITM attack on OTA update | TLS connection fails, update rejected |
| PT-05 | Exploit ECU with CVE-2023-XXXX | Patch applied, exploit unsuccessful |

### Red Team / Blue Team Exercises

**Red Team**: Offensive security team attempting to compromise vehicle
**Blue Team**: Defensive team monitoring, detecting, and responding to attacks

**Objectives:**
- Test incident response procedures
- Validate intrusion detection systems
- Identify gaps in security controls

---

## Incident Response

### Cybersecurity Incident Response Process

**Phases:**

1. **Preparation**
   - Incident response team roles and contacts
   - Forensics tools and procedures
   - Communication templates

2. **Detection and Analysis**
   - Intrusion detection system (IDS) alerts
   - Anomaly detection in telemetry
   - Vulnerability disclosures (coordinated or public)

3. **Containment**
   - Isolate affected vehicles or ECUs
   - Disable compromised features
   - Deploy emergency patches

4. **Eradication**
   - Remove malware or unauthorized access
   - Patch vulnerabilities
   - Update cryptographic keys if compromised

5. **Recovery**
   - Restore normal operations
   - Validate system integrity
   - Monitor for recurrence

6. **Post-Incident Activity**
   - Root cause analysis
   - Update threat models
   - Improve detection and response

### Coordinated Vulnerability Disclosure

**Process:**
1. Security researcher discovers vulnerability
2. Responsible disclosure to OEM (not public disclosure)
3. OEM validates and develops patch
4. Coordinated public disclosure after patch deployment
5. CVE assignment and publication

**Timelines:**
- **Critical vulnerabilities**: 30-day disclosure timeline
- **High severity**: 90-day disclosure timeline

---

## Case Studies

### Case Study 1: Jeep Cherokee Remote Hack (2015)

**Incident:**
- Researchers Charlie Miller and Chris Valasek remotely hacked a Jeep Cherokee
- Exploited vulnerability in Uconnect infotainment system
- Gained access to CAN bus, controlled steering, braking, transmission

**Attack Chain:**
1. Exploited Sprint cellular network vulnerability
2. Compromised infotainment head unit (QNX-based)
3. Bridged from infotainment to CAN bus (insufficient isolation)
4. Sent malicious CAN messages to ECUs

**Impact:**
- 1.4 million vehicle recall
- Public demonstration eroded consumer trust

**Lessons Learned:**
- Network segmentation critical (infotainment ≠ vehicle control)
- Regular security updates for connectivity modules
- Intrusion detection on CAN bus

### Case Study 2: Tesla Model S Key Fob Relay Attack (2018)

**Incident:**
- Researchers demonstrated relay attack on Tesla Model S key fob
- Extended range of key fob signal using relay devices
- Unlocked and started vehicle without owner's key

**Attack Mechanism:**
- Passive keyless entry (PKE) systems assume proximity = authorization
- Relay devices capture and forward signals between key and car
- No cryptographic protection against relay

**Mitigations:**
- Ultra-wideband (UWB) ranging for precise distance measurement
- Time-of-flight verification (Bluetooth LE 5.1)
- Owner awareness and Faraday pouches for keys

### Case Study 3: C-V2X Security Architecture (2020+)

**Background:**
- Cellular V2X (C-V2X) enables vehicle-to-vehicle and vehicle-to-infrastructure communication
- Standardized by 3GPP and SAE

**Security Measures:**
1. **Message Authentication**: IEEE 1609.2 PKI with digital signatures
2. **Privacy**: Pseudonymous certificates (short-lived, rotated frequently)
3. **Misbehavior Detection**: Detect and revoke malicious vehicles
4. **Certificate Authority**: SCMS (Security Credential Management System)

**Challenges:**
- Scalability: Millions of vehicles, billions of messages/day
- Latency: Signature verification must complete within milliseconds
- Privacy: Balance authentication with driver anonymity

---

## Practical Guidelines

### For AV Developers

1. **Adopt ISO/SAE 21434 from Project Start**
   - Integrate TARA into early concept phase
   - Allocate cybersecurity resources (team, tools, budget)

2. **Implement Defense in Depth**
   - Don't rely on single security control
   - Layered security: network, system, application, data

3. **Use Established Cryptography**
   - TLS 1.3 for communication security
   - X.509 certificates with PKI
   - AES-256 for data encryption
   - ECDSA P-256 or RSA-3072 for signatures

4. **Secure the Supply Chain**
   - Vet suppliers for cybersecurity practices
   - Software Bill of Materials (SBOM) for dependency tracking
   - Component authentication and integrity verification

5. **Plan for Incidents**
   - 24/7 security operations center (SOC)
   - Incident response playbooks
   - OTA update infrastructure for rapid patching

### For Security Researchers

1. **Responsible Disclosure**
   - Report vulnerabilities privately to OEMs
   - Allow reasonable time for patching (30-90 days)
   - Coordinate public disclosure

2. **Document and Publish**
   - Academic publications advance the field
   - Reproducible research helps OEMs validate and fix issues

3. **Collaborate with Industry**
   - Attend conferences (Black Hat, DEF CON, ESCAR)
   - Join automotive security working groups (SAE, AUTOSAR)

---

## References

### Standards and Regulations

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
- **SAE J3061:2016** - Cybersecurity Guidebook for Cyber-Physical Vehicle Systems
- **UNECE WP.29 R155** - Uniform provisions concerning the approval of vehicles with regards to cybersecurity
- **UNECE WP.29 R156** - Uniform provisions concerning the approval of vehicles with regards to software update
- **AUTOSAR SecOC** - Secure Onboard Communication specification
- **IEEE 1609.2** - Security Services for Applications and Management Messages
- **NIST Cybersecurity Framework** - Framework for Improving Critical Infrastructure Cybersecurity

### Academic Papers

- Miller & Valasek (2015): "Remote Exploitation of an Unaltered Passenger Vehicle"
- Checkoway et al. (2011): "Comprehensive Experimental Analyses of Automotive Attack Surfaces"
- Petit et al. (2015): "Remote Attacks on Automated Vehicles Sensors: Experiments on Camera and LiDAR"
- Yan et al. (2016): "Can You Trust Autonomous Vehicles: Contactless Attacks against Sensors of Self-driving Vehicle"

### Books and Guidelines

- **"Car Hacker's Handbook"** by Craig Smith (2016)
- **"The Automotive Security Best Practices"** by Upstream Security
- **"Cybersecurity for Connected Vehicles"** by Wiley

### Online Resources

- [Automotive Security Research Group](https://www.autosec.org/)
- [OWASP Automotive Security](https://owasp.org/www-project-automotive-security/)
- [NIST Automotive Cybersecurity Guidance](https://www.nist.gov/)
- [ENISA Good Practices for Automotive Cybersecurity](https://www.enisa.europa.eu/)

---

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this repository or related materials, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email details to: [Create private security advisory on GitHub]
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested mitigation (optional)

We will acknowledge receipt within 48 hours and provide updates on remediation timeline.

---

**Document Version:** 1.0
**Last Updated:** 2025-01-18
**Author:** Milin Patel
**License:** MIT

---

*This document is part of the comprehensive Autonomous Driving: AI, Safety, and Security Workshop. For functional safety, see [SAFETY.md](SAFETY.md). For AI-specific safety considerations, see [AI_SAFETY.md](AI_SAFETY.md).*
