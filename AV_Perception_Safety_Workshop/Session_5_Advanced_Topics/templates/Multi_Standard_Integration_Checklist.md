# Multi-Standard Integration Checklist
## ISO 26262 + ISO 21448 + ISO/SAE 21434

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Applicable Standards:** ISO 26262:2018, ISO 21448:2022, ISO/SAE 21434:2021

---

## Document Information

| Field | Value |
|-------|-------|
| **System/Component Name** | [Enter name] |
| **System Description** | [Brief description] |
| **ASIL** | [QM / A / B / C / D] |
| **CAL (Cybersecurity Assurance Level)** | [CAL 1 / CAL 2 / CAL 3 / CAL 4] |
| **Version** | [e.g., 1.0] |
| **Date** | [YYYY-MM-DD] |
| **Prepared By** | [Name] |
| **Reviewed By** | [Name] |

---

## Purpose

This checklist ensures comprehensive integration of:
1. **ISO 26262** - Functional safety (random HW failures, systematic SW faults)
2. **ISO 21448** - Safety of the intended functionality (performance limitations, triggering conditions)
3. **ISO/SAE 21434** - Cybersecurity (intentional malicious attacks)

Use this checklist for **autonomous vehicle perception systems** or other safety-critical AI/ML components.

---

## Section 1: Concept Phase Integration

### 1.1 Item Definition (ISO 26262-3)

- [ ] **System boundaries defined** (inputs, outputs, interfaces)
- [ ] **Intended functionality documented**
- [ ] **Operational Design Domain (ODD) specified** (per ISO 34503)
- [ ] **Legal and regulatory requirements identified**
- [ ] **Assumptions documented** (environmental, operational, user behavior)

### 1.2 Hazard Analysis and Risk Assessment - HARA (ISO 26262-3)

- [ ] **Hazards identified** for malfunctioning behavior
- [ ] **Exposure, Severity, Controllability assessed** (E, S, C)
- [ ] **ASIL determined** for each safety goal (QM, A, B, C, D)
- [ ] **Safety goals defined** (top-level safety requirements)
- [ ] **Safe state(s) defined** for each safety goal

### 1.3 SOTIF Analysis (ISO 21448)

- [ ] **Known safe scenarios identified**
- [ ] **Known unsafe scenarios identified** (performance limitations + triggering conditions)
- [ ] **Unknown scenarios documented** (potential unknown unsafe scenarios)
- [ ] **Triggering conditions analyzed** (weather, lighting, rare objects, sensor degradation)
- [ ] **Performance limitations assessed** (algorithm accuracy, sensor range, latency)
- [ ] **Mitigation strategies defined** for known unsafe scenarios

### 1.4 Threat Analysis and Risk Assessment - TARA (ISO/SAE 21434)

- [ ] **Assets identified** (data, functions, components requiring protection)
- [ ] **Threat scenarios enumerated** (spoofing, tampering, DoS, elevation of privilege, information disclosure, repudiation)
- [ ] **Attack paths analyzed** (entry points, attack vectors)
- [ ] **Attack feasibility rated** (elapsed time, specialist expertise, knowledge of target, window of opportunity, equipment)
- [ ] **Impact on safety assessed** (impact on ISO 26262 safety goals)
- [ ] **Cybersecurity goals defined** (confidentiality, integrity, availability)
- [ ] **CAL (Cybersecurity Assurance Level) determined**

### 1.5 Combined Analysis (SAHARA Method)

- [ ] **Safety-Security interactions identified** (e.g., security failure leading to safety hazard)
- [ ] **Conflicting requirements resolved** (e.g., fail-safe vs fail-secure)
- [ ] **Combined risk assessment performed**
- [ ] **Integrated safety and security requirements derived**

---

## Section 2: System Design Phase

### 2.1 Functional Safety Concept (ISO 26262-3)

- [ ] **Functional safety requirements derived** from safety goals
- [ ] **ASIL decomposition applied** (if needed)
- [ ] **Fault detection, handling, and fallback strategies defined**
- [ ] **Redundancy and fail-operational design** (if ASIL D)
- [ ] **Hardware-Software Interface (HSI) specified**

### 2.2 SOTIF Design Measures (ISO 21448)

- [ ] **Sensor fusion strategy** to reduce performance limitations
- [ ] **Uncertainty quantification implemented** (aleatoric, epistemic)
- [ ] **OOD (Out-of-Distribution) detection** for unknown scenarios
- [ ] **Graceful degradation strategy** when approaching ODD boundaries
- [ ] **Minimal Risk Condition (MRC) defined** for SOTIF violations
- [ ] **Runtime monitoring of triggering conditions** (weather, lighting, occlusion)

### 2.3 Cybersecurity Concept (ISO/SAE 21434)

- [ ] **Cybersecurity requirements derived** from cybersecurity goals
- [ ] **Secure communication protocols** (authentication, encryption, integrity)
- [ ] **Access control mechanisms** (least privilege, role-based access)
- [ ] **Secure boot and software integrity verification**
- [ ] **Intrusion detection and prevention**
- [ ] **Cybersecurity monitoring and logging**

### 2.4 AI/ML-Specific Considerations

- [ ] **Training data quality assured** (representative, diverse, bias-free)
- [ ] **Model validation performed** (test set performance, cross-validation)
- [ ] **Adversarial robustness evaluated** (FGSM, PGD attacks)
- [ ] **Explainability methods integrated** (LIME, SHAP, Grad-CAM for certification)
- [ ] **Model update and retraining strategy** (continuous learning, version control)

---

## Section 3: Development Phase

### 3.1 ISO 26262 Software Development (Part 6)

- [ ] **Software architecture designed** per ASIL requirements
- [ ] **Coding guidelines followed** (MISRA C, CERT C, etc.)
- [ ] **Software unit testing** with coverage per ASIL (statement, branch, MC/DC)
- [ ] **Static analysis performed** (no critical warnings)
- [ ] **Software integration testing** completed
- [ ] **Verification of software safety requirements** (traceability)

### 3.2 ISO 21448 Verification Activities

- [ ] **Scenario-based testing** for known unsafe scenarios
- [ ] **Boundary value testing** for ODD limits
- [ ] **Stress testing** (corner cases, edge cases, rare events)
- [ ] **Simulation-based validation** (million+ km in virtual environment)
- [ ] **Dataset coverage analysis** (geographic, weather, time of day diversity)

### 3.3 ISO/SAE 21434 Secure Development

- [ ] **Secure coding practices** (input validation, buffer overflow protection, etc.)
- [ ] **Vulnerability scanning** (SAST, DAST tools)
- [ ] **Cryptographic library usage** (approved algorithms, key management)
- [ ] **Third-party component security assessment** (SBOM, CVE checks)
- [ ] **Penetration testing** for attack vectors identified in TARA

---

## Section 4: Validation and Testing Phase

### 4.1 ISO 26262 Validation (Part 4)

- [ ] **System integration testing** in target environment
- [ ] **Fault injection testing** (HW faults, SW faults)
- [ ] **Fail-safe behavior validation** (transitions to safe state)
- [ ] **Field testing** with representative use cases
- [ ] **Validation of safety goals** (all safety goals verified)
- [ ] **Functional Safety Assessment** by independent assessor

### 4.2 ISO 21448 Validation

- [ ] **Known safe scenarios validated** (95% coverage target per ISO 21448)
- [ ] **Test drive distance sufficient** to demonstrate SOTIF (Kalra & Paddock analysis)
- [ ] **Evaluation of unknown scenarios** through extensive testing
- [ ] **Residual risk evaluation** (acceptable level achieved)
- [ ] **Field monitoring plan established** for continuous SOTIF validation

### 4.3 ISO/SAE 21434 Validation

- [ ] **Vulnerability testing** for all identified attack vectors
- [ ] **Penetration testing** by independent security experts
- [ ] **Security compliance testing** (encryption strength, authentication mechanisms)
- [ ] **Incident response plan validated** (tabletop exercise or simulation)
- [ ] **Cybersecurity validation report** completed

### 4.4 Integrated Validation

- [ ] **Combined safety-security test cases** executed
- [ ] **Cross-functional validation** (safety + SOTIF + cybersecurity)
- [ ] **End-to-end system validation** in real-world conditions
- [ ] **Acceptance criteria met** for all three standards

---

## Section 5: Production and Operations Phase

### 5.1 ISO 26262 Production

- [ ] **Production control plan** established
- [ ] **HW component traceability** (batch numbers, test reports)
- [ ] **Software version control** and release management
- [ ] **End-of-line testing** for safety mechanisms

### 5.2 ISO 21448 Field Monitoring

- [ ] **Fleet data collection** for SOTIF performance monitoring
- [ ] **Disengagement tracking** (rates, root causes)
- [ ] **ODD violation detection** and analysis
- [ ] **Triggering condition monitoring** (correlation with failures)
- [ ] **Continuous improvement process** for SOTIF

### 5.3 ISO/SAE 21434 Operations

- [ ] **Security Operations Center (SOC)** or monitoring in place
- [ ] **Vulnerability management process** (CVE monitoring, patching)
- [ ] **Secure OTA update mechanism** (signed updates, rollback capability)
- [ ] **Incident detection and response** capabilities operational
- [ ] **Security logging and auditing** active

### 5.4 Continuous Monitoring

- [ ] **Safety performance indicators tracked** (failure rates, MTBF)
- [ ] **SOTIF metrics monitored** (known unsafe scenario frequency)
- [ ] **Cybersecurity metrics tracked** (intrusion attempts, vulnerabilities found)
- [ ] **Integrated dashboard** for safety + SOTIF + security monitoring

---

## Section 6: Decommissioning Phase

### 6.1 ISO 26262 Decommissioning

- [ ] **Safe deactivation procedure** documented
- [ ] **Disposal of safety-critical components** per regulations

### 6.2 ISO/SAE 21434 Decommissioning

- [ ] **Secure data deletion** (cryptographic erasure)
- [ ] **Key revocation** and certificate invalidation
- [ ] **Decommissioning logged** for traceability

---

## Section 7: Documentation and Traceability

### 7.1 Required Documentation

- [ ] **Safety Plan** (ISO 26262-2)
- [ ] **SOTIF Validation Plan** (ISO 21448)
- [ ] **Cybersecurity Plan** (ISO/SAE 21434)
- [ ] **Combined Safety and Security Case** (argumentation)
- [ ] **Verification and Validation Reports** (all three standards)
- [ ] **Functional Safety Assessment Report**
- [ ] **Cybersecurity Assessment Report**

### 7.2 Traceability

- [ ] **Hazards → Safety Goals → Safety Requirements** (ISO 26262)
- [ ] **Triggering Conditions → Mitigation Strategies → Test Cases** (ISO 21448)
- [ ] **Threats → Cybersecurity Goals → Security Requirements** (ISO/SAE 21434)
- [ ] **Integrated Requirements Traceability Matrix** maintained

---

## Section 8: Roles and Responsibilities

### 8.1 ISO 26262 Roles

- [ ] **Safety Manager** assigned
- [ ] **Functional Safety Assessor** (independent) assigned
- [ ] **Safety Engineers** responsible for each safety goal

### 8.2 ISO 21448 Roles

- [ ] **SOTIF Engineer** or responsible person assigned
- [ ] **Validation Engineer** for extensive testing

### 8.3 ISO/SAE 21434 Roles

- [ ] **Cybersecurity Manager** assigned
- [ ] **Cybersecurity Assessor** (independent) assigned
- [ ] **Security Operations Team** for monitoring

### 8.4 Integration

- [ ] **Cross-functional Safety & Security Committee** established
- [ ] **Regular coordination meetings** scheduled
- [ ] **Escalation path defined** for conflicts or issues

---

## Section 9: Tools and Methods

### 9.1 Safety Tools

- [ ] **FMEA (Failure Modes and Effects Analysis)** tool
- [ ] **FTA (Fault Tree Analysis)** tool
- [ ] **Requirements management** tool (DOORS, Jama, etc.)
- [ ] **Static analysis** tool (Polyspace, Coverity, etc.)

### 9.2 SOTIF Tools

- [ ] **Scenario generation** tool (Pegasus, SCENIC, etc.)
- [ ] **Simulation platform** (CARLA, SUMO, IPG CarMaker, etc.)
- [ ] **Data analysis** tool for fleet data

### 9.3 Cybersecurity Tools

- [ ] **Threat modeling** tool (Microsoft Threat Modeling Tool, etc.)
- [ ] **Vulnerability scanner** (Nessus, Qualys, etc.)
- [ ] **SIEM (Security Information and Event Management)** system

### 9.4 Integrated Tools

- [ ] **Combined safety-security analysis** tool (Medini Analyze, PREEvision, etc.)
- [ ] **Traceability tool** linking all three standards

---

## Section 10: Standards Compliance Summary

### 10.1 ISO 26262 Compliance

| ISO 26262 Requirement | Status | Evidence |
|----------------------|--------|----------|
| Item Definition (Part 3, Clause 5) | [ ] Complete | [Document reference] |
| HARA (Part 3, Clause 7) | [ ] Complete | [Document reference] |
| Functional Safety Concept (Part 3, Clause 8) | [ ] Complete | [Document reference] |
| System Design (Part 4) | [ ] Complete | [Document reference] |
| Software Development (Part 6) | [ ] Complete | [Document reference] |
| Validation (Part 4, Clause 8) | [ ] Complete | [Document reference] |
| Functional Safety Assessment (Part 2, Clause 6) | [ ] Complete | [Document reference] |

### 10.2 ISO 21448 Compliance

| ISO 21448 Requirement | Status | Evidence |
|-----------------------|--------|----------|
| Known Scenarios (Clause 7) | [ ] Complete | [Document reference] |
| Verification (Clause 8) | [ ] Complete | [Document reference] |
| Validation (Clause 9) | [ ] Complete | [Document reference] |
| Field Monitoring (Clause 10) | [ ] Complete | [Document reference] |

### 10.3 ISO/SAE 21434 Compliance

| ISO/SAE 21434 Requirement | Status | Evidence |
|---------------------------|--------|----------|
| TARA (Clause 9) | [ ] Complete | [Document reference] |
| Cybersecurity Concept (Clause 10) | [ ] Complete | [Document reference] |
| Cybersecurity Validation (Clause 14) | [ ] Complete | [Document reference] |
| Operations and Maintenance (Clause 15) | [ ] Complete | [Document reference] |

---

## Section 11: Open Issues and Risks

| Issue ID | Description | Impact (Safety/SOTIF/Security) | Owner | Due Date | Status |
|----------|-------------|--------------------------------|-------|----------|--------|
| | | | | | |
| | | | | | |

---

## Section 12: Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Safety Manager** | | | |
| **SOTIF Engineer** | | | |
| **Cybersecurity Manager** | | | |
| **Program Manager** | | | |
| **Functional Safety Assessor** | | | |
| **Cybersecurity Assessor** | | | |

---

## References

1. ISO 26262:2018 - Road vehicles — Functional safety
2. ISO 21448:2022 - Road vehicles — Safety of the intended functionality
3. ISO/SAE 21434:2021 - Road vehicles — Cybersecurity engineering
4. ISO 34503:2023 - Road vehicles — Test scenarios for automated driving systems
5. ISO/IEC TR 5469:2024 - Functional safety and AI systems
6. SAHARA Method: "Security-Aware Hazard and Risk Analysis Method" (Macher et al., 2015)

---

**Template Version:** 1.0
**Developed By:** Milin Patel, Hochschule Kempten
**Copyright © 2025 Milin Patel. All Rights Reserved.**
**License:** MIT License

---

## Notes for Users

This checklist integrates three complementary standards:
- **ISO 26262** prevents malfunctions (random HW, systematic SW faults)
- **ISO 21448** addresses insufficient design (performance limitations, rare scenarios)
- **ISO/SAE 21434** protects against malicious attacks (intentional harm)

**Combined approach is essential** because:
1. A cyberattack can cause a malfunction (security → safety)
2. A performance limitation can create a security vulnerability (SOTIF → security)
3. Safety measures can introduce security weaknesses (e.g., diagnostic ports)

**Recommended Usage:**
1. Complete Sections 1-4 sequentially during development
2. Review Sections 5-6 for operations planning
3. Maintain Section 7 (documentation) throughout the lifecycle
4. Use Section 10 as final compliance checklist before release
