# Cybersecurity

**Module 05: ISO/SAE 21434 Implementation for Automotive Cybersecurity**

---

## Overview

Automotive cybersecurity is critical for protecting autonomous vehicles from malicious attacks that can compromise safety, privacy, and functionality. This module provides comprehensive coverage of ISO/SAE 21434, the international standard for automotive cybersecurity engineering. Students learn to conduct Threat Analysis and Risk Assessment (TARA), identify attack vectors, implement secure development practices, and integrate cybersecurity with functional safety.

### Module Objectives

Upon completing this module, you will:

1. **Master ISO/SAE 21434 Framework**: Understand cybersecurity engineering lifecycle from concept to decommissioning
2. **Conduct TARA**: Perform systematic Threat Analysis and Risk Assessment for autonomous systems
3. **Identify Attack Vectors**: Recognize physical, wireless, and supply chain attack surfaces
4. **Analyze Sensor Attacks**: Understand spoofing, jamming, and adversarial attacks on perception
5. **Implement Secure Development**: Apply Security Development Lifecycle (SDL) practices
6. **Design Defense Mechanisms**: Implement intrusion detection, authentication, and encryption
7. **Integrate with Safety**: Understand safety-security co-analysis and ISO 26262 interaction
8. **Address V2X Security**: Protect vehicle-to-everything communication channels

---

## Why Cybersecurity Matters

### Critical Challenges in Automotive Cybersecurity

**1. Attack Surface Expansion**
- **Wireless interfaces**: Cellular (4G/5G), Wi-Fi, Bluetooth, V2X (DSRC, C-V2X)
- **Physical interfaces**: OBD-II port, USB, charging stations
- **Sensor interfaces**: Camera, LiDAR, Radar, GPS, IMU
- **Backend connections**: Cloud services, OTA updates, fleet management
- **Supply chain**: Compromised components, malicious software updates
- Each interface is a potential entry point for attackers

**2. Safety-Security Interaction**
- **Cybersecurity attacks can cause safety hazards**:
  - GPS spoofing → incorrect localization → path planning errors
  - Sensor jamming → perception failure → collision risk
  - ECU compromise → unintended acceleration/braking
- **ISO 26262 + ISO/SAE 21434**: Combined safety-security analysis required
- **ASIL + CAL (Cybersecurity Assurance Level)**: Integrated risk assessment
- Security vulnerabilities can invalidate safety arguments

**3. Known Attack Demonstrations**
- **Jeep Cherokee (2015)**: Remote exploitation via UConnect system, control of steering/braking
- **Tesla Model S**: Compromised via browser vulnerability, later patched
- **CAN bus attacks**: Injecting malicious messages to control vehicle functions
- **GPS spoofing**: Misleading navigation and ADAS systems
- **LiDAR spoofing**: Injecting fake objects into point clouds
- These are not theoretical - real attacks have been demonstrated

**4. Sensor Spoofing Attacks**
- **Camera**: Adversarial patches on traffic signs, projected patterns, lens blinding
- **LiDAR**: Laser injection attacks, replay attacks, jamming
- **Radar**: False target injection, range/velocity manipulation
- **GPS**: Signal spoofing, jamming (widely available equipment)
- **Ultrasonic**: Inaudible commands, jamming
- Multi-modal fusion provides defense but also multiplies attack vectors

**5. V2X Communication Vulnerabilities**
- **Message injection**: False emergency vehicle warnings, phantom obstacles
- **Replay attacks**: Recording and retransmitting messages
- **Sybil attacks**: Single malicious entity pretending to be multiple vehicles
- **Man-in-the-middle**: Intercepting and modifying V2V/V2I communications
- **Privacy concerns**: Vehicle tracking via broadcast messages
- PKI (Public Key Infrastructure) required but introduces latency

**6. Over-the-Air (OTA) Update Risks**
- **Malicious updates**: Compromised backend or man-in-the-middle attacks
- **Rollback attacks**: Forcing vehicle to use older, vulnerable software
- **Denial of service**: Bricking vehicles with corrupted updates
- **Update integrity**: Code signing and secure boot chains required
- **Validation before deployment**: Testing on shadow fleet
- **Regulatory requirements**: UNECE WP.29 mandates secure OTA

---

## Module Structure

### 📓 Notebooks

1. **[01_automotive_cybersecurity.ipynb](notebooks/01_automotive_cybersecurity.ipynb)**
   - Automotive threat landscape evolution
   - ISO/SAE 21434 structure and scope
   - Cybersecurity engineering lifecycle
   - Cybersecurity Assurance Levels (CAL 1-4)
   - Security by design principles
   - UNECE WP.29 regulations (R155, R156)
   - Relationship to ISO 26262 and safety-security co-analysis

2. **[02_threat_analysis_risk_assessment.ipynb](notebooks/02_threat_analysis_risk_assessment.ipynb)**
   - TARA methodology: Asset identification, threat scenario identification
   - Attack feasibility assessment: Elapsed time, specialist expertise, equipment, knowledge of item
   - Impact rating: Safety, financial, operational, privacy
   - Cybersecurity goals and claims
   - Attack trees and attack paths
   - STRIDE threat modeling (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege)
   - Case study: TARA for autonomous emergency braking system

3. **[03_attack_vectors.ipynb](notebooks/03_attack_vectors.ipynb)**
   - Sensor spoofing: Camera (adversarial patches), LiDAR (laser injection), Radar (false targets), GPS (signal spoofing)
   - CAN bus attacks: Message injection, eavesdropping, DoS
   - V2X attacks: Message injection, Sybil, replay, jamming
   - ECU compromise: Exploiting software vulnerabilities, buffer overflows
   - Physical access: OBD-II, USB, debugging interfaces
   - Supply chain: Compromised components, malicious firmware
   - Cloud backend: API vulnerabilities, credential theft

4. **[04_secure_development.ipynb](notebooks/04_secure_development.ipynb)**
   - Security Development Lifecycle (SDL) integration
   - Secure coding practices: Input validation, bounds checking, least privilege
   - Cryptography: Symmetric (AES), asymmetric (RSA, ECC), hashing (SHA-256)
   - Secure communication: TLS/SSL, message authentication codes (MAC)
   - Intrusion Detection Systems (IDS): Anomaly detection, signature-based
   - Hardware Security Modules (HSM): Secure key storage
   - Penetration testing and vulnerability assessment
   - Incident response planning

---

## Prerequisites

### Knowledge
- Understanding of automotive systems and networks (CAN, FlexRay, Ethernet)
- Familiarity with ISO 26262 functional safety (Module 03)
- Basic networking and cryptography concepts
- Programming fundamentals

### Software
- Python 3.8+
- Libraries: Scapy (packet manipulation), PyCryptodome (cryptography)
- Optional: CANoe/CANalyzer for CAN bus analysis
- Wireshark for network protocol analysis

---

## Cybersecurity Tools and Frameworks

- **Scapy**: Python packet manipulation library
- **Wireshark**: Network protocol analyzer
- **CANoe/CANalyzer**: CAN bus development and analysis
- **AUTOSAR SecOC**: Secure Onboard Communication
- **HSM (Hardware Security Module)**: Secure cryptographic operations
- **PKI (Public Key Infrastructure)**: Certificate management for V2X

---

## Learning Path

### Beginner Path
1. Start with **01_automotive_cybersecurity** to understand threat landscape
2. Proceed to **02_threat_analysis_risk_assessment** for TARA methodology
3. Learn **03_attack_vectors** for specific vulnerability analysis

### Advanced Path
4. Master **04_secure_development** for implementation and defense

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Conduct TARA for adaptive cruise control (ACC) system
2. **Exercise 2**: Implement CAN bus message authentication using HMAC
3. **Exercise 3**: Demonstrate GPS spoofing attack and implement detection
4. **Exercise 4**: Develop intrusion detection system for automotive Ethernet
5. **Exercise 5**: Create secure OTA update verification system

---

## Code Examples

Located in `code/`:
- `tara_framework.py`: Threat analysis and risk assessment automation
- `can_ids.py`: CAN bus intrusion detection system
- `message_authentication.py`: Secure communication with MAC
- `sensor_anomaly_detector.py`: Statistical anomaly detection for sensors
- `secure_bootloader.py`: Verified boot chain implementation

---

## Industry Standards and References

### Standards
- **ISO/SAE 21434 (2021)**: Road Vehicles - Cybersecurity Engineering
- **UNECE WP.29 R155**: Cybersecurity and Cybersecurity Management System
- **UNECE WP.29 R156**: Software Update and Software Update Management System
- **ISO 26262**: Functional Safety - Safety-security co-analysis
- **SAE J3061**: Cybersecurity Guidebook for Cyber-Physical Vehicle Systems
- **AUTOSAR SecOC**: Secure Onboard Communication specification
- **IEEE 1609**: Wireless Access in Vehicular Environments (WAVE) security

### Key Papers
- Checkoway et al. (2011): "Comprehensive Experimental Analyses of Automotive Attack Surfaces"
- Miller & Valasek (2015): "Remote Exploitation of an Unaltered Passenger Vehicle"
- Petit et al. (2015): "Remote Attacks on Automated Vehicles Sensors"
- Parkinson et al. (2017): "Cyber Threats Facing Autonomous and Connected Vehicles"
- Steger et al. (2017): "Secure Automotive On-Board Protocols"

### Resources
- [ISO/SAE 21434 Official Standard](https://www.iso.org/standard/70918.html)
- [UNECE WP.29 Regulations](https://unece.org/transport/vehicle-regulations)
- [Auto-ISAC (Information Sharing and Analysis Center)](https://automotiveisac.com/)
- [NHTSA Cybersecurity Best Practices](https://www.nhtsa.gov/vehicle-manufacturers/cybersecurity)

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Explain ISO/SAE 21434 cybersecurity engineering lifecycle
✓ Conduct Threat Analysis and Risk Assessment (TARA)
✓ Identify attack vectors for sensors, networks, and backend systems
✓ Analyze sensor spoofing attacks (camera, LiDAR, radar, GPS)
✓ Implement secure communication protocols and authentication
✓ Design intrusion detection systems for automotive networks
✓ Apply secure development lifecycle (SDL) practices
✓ Integrate cybersecurity with functional safety (ISO 26262)
✓ Understand V2X security requirements and PKI

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding attack targets
- **Module 03**: Functional Safety - Safety-security interaction

### Related Modules
- **Module 02**: Failure Analysis - Adversarial attacks as security threats
- **Module 04**: SOTIF - Security vulnerabilities as triggering conditions
- **Module 06**: AI Safety - Adversarial robustness for perception

### Follow-up Modules
- **Module 07**: Validation & Verification - Penetration testing and security validation
- **Module 08**: Advanced Topics - V2X security and deployment

---

## Next Steps

After completing this module:
- **Module 06**: AI Safety - Adversarial robustness and uncertainty quantification
- **Module 07**: Validation & Verification - Security testing and penetration testing
- **Module 08**: Advanced Topics - V2X communication security

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
