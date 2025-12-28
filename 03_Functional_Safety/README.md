# Functional Safety

**Module 03: ISO 26262 Implementation for Autonomous Vehicle Systems**

---

## Overview

Functional safety is the cornerstone of automotive system development, ensuring that electronic systems behave correctly even in the presence of faults. This module provides comprehensive coverage of ISO 26262, the international standard for functional safety of electrical/electronic systems in road vehicles. Students learn to conduct Hazard Analysis and Risk Assessment (HARA), allocate Automotive Safety Integrity Levels (ASIL), and develop safety cases for autonomous driving systems.

### Module Objectives

Upon completing this module, you will:

1. **Master ISO 26262 Framework**: Understand the V-Model development lifecycle and safety management requirements
2. **Conduct HARA**: Perform systematic Hazard Analysis and Risk Assessment for autonomous systems
3. **Assign ASIL Levels**: Determine Automotive Safety Integrity Levels based on severity, exposure, and controllability
4. **Perform ASIL Decomposition**: Allocate safety requirements across redundant systems
5. **Develop Safety Goals**: Translate hazards into measurable, verifiable safety requirements
6. **Create Safety Cases**: Build evidence-based argumentation for system safety
7. **Apply to AI Systems**: Extend ISO 26262 to machine learning-based perception and decision-making
8. **Integrate with SOTIF**: Understand the complementary relationship between ISO 26262 and ISO 21448

---

## Why Functional Safety Matters

### Critical Challenges in Automotive Safety Engineering

**1. Complexity of Modern Vehicles**
- Modern vehicles contain 100+ Electronic Control Units (ECUs)
- 100+ million lines of software code
- Perception systems process gigabytes of sensor data per second
- Failures can propagate across multiple systems (perception → planning → control)
- Systematic approach required to manage complexity and ensure safety

**2. ASIL-D Requirements for Critical Functions**
- **ASIL-D**: Highest safety level, required for critical functions (pedestrian detection, emergency braking)
- Requirements:
  - <10^-8 failures per hour (less than 1 failure in 11,400 years of operation)
  - Redundancy and fault tolerance mechanisms
  - Comprehensive testing and validation
  - Independent safety assessment
- AI-based perception systems face challenges meeting ASIL-D due to inherent non-determinism

**3. V-Model Development Lifecycle**
- **Left side (Design)**: Concept → System → Hardware/Software → Component development
- **Right side (Verification)**: Unit testing → Integration testing → System testing → Vehicle testing
- Traceability required from hazard → safety goal → functional safety requirement → implementation → test
- ISO 26262 mandates specific methods and techniques at each stage

**4. Random Hardware Failures vs. Systematic Failures**
- **Random failures**: Aging, wear-out, environmental stress (addressed through redundancy, diagnostic coverage)
- **Systematic failures**: Design errors, specification faults, software bugs (addressed through rigorous development process)
- Machine learning introduces new systematic failure modes (training data bias, OOD inputs)
- ISO 26262 Part 11 (under development) addresses semiconductor-specific failures

**5. Safety Culture and Management**
- ISO 26262 Part 2: Management of functional safety
- Safety culture requirements: transparency, continuous improvement, blame-free reporting
- Competency management: Safety engineers require specific training and certification
- Supplier management: Safety requirements flow down to all tiers
- Configuration management: Traceability of all safety-relevant artifacts

**6. Integration with Other Standards**
- **ISO 21448 (SOTIF)**: Performance limitations and intended functionality
- **ISO/SAE 21434**: Cybersecurity integration (attacks can cause safety hazards)
- **ISO/PAS 8800**: AI-specific safety considerations
- **UNECE Regulations**: WP.29 regulations for automated driving systems
- Multiple standards must be satisfied simultaneously for certification

---

## Module Structure

### 📓 Notebooks

1. **[01_iso_26262_fundamentals.ipynb](notebooks/01_iso_26262_fundamentals.ipynb)**
   - ISO 26262 structure: Parts 1-12 overview
   - V-Model development lifecycle
   - Automotive Safety Integrity Levels (ASIL A, B, C, D, QM)
   - Safety lifecycle phases: Concept → Development → Production → Operation → Decommissioning
   - Confirmation measures and functional safety audit
   - Differences from IEC 61508 (generic functional safety standard)

2. **[02_hazard_analysis_risk_assessment.ipynb](notebooks/02_hazard_analysis_risk_assessment.ipynb)**
   - HARA methodology: Item definition, hazard identification, classification
   - Severity (S0-S3): No injuries → Life-threatening/fatal injuries
   - Exposure (E0-E4): Incredibly unlikely → High probability
   - Controllability (C0-C3): Controllable in general → Difficult/uncontrollable
   - ASIL determination matrix (S × E × C → ASIL)
   - Safety goal formulation with safe state and fault tolerant time interval (FTTI)
   - Case study: HARA for autonomous emergency braking (AEB)

3. **[03_asil_decomposition.ipynb](notebooks/03_asil_decomposition.ipynb)**
   - ASIL decomposition principles: ASIL D = ASIL B(D) + ASIL B(D)
   - Independence requirements between redundant elements
   - Freedom from interference: Temporal, spatial, communication
   - Architectural metrics: Single-Point Fault Metric (SPFM), Latent Fault Metric (LFM)
   - Sensor fusion redundancy: Camera + LiDAR for pedestrian detection
   - Practical limitations: Cost, complexity, diagnostic coverage

4. **[04_safety_case_development.ipynb](notebooks/04_safety_case_development.ipynb)**
   - Goal Structuring Notation (GSN) for safety argumentation
   - Safety case elements: Claims, evidence, strategies, context
   - Evidence types: Test results, simulation data, field data, reviews
   - Confidence arguments: Why evidence is sufficient
   - Patterns for safety cases: Hazard avoidance, hazard mitigation, fault tolerance
   - ISO 26262 Part 8: Supporting processes (documentation, configuration management)
   - Independent safety assessment requirements

---

## Prerequisites

### Knowledge
- Basic understanding of automotive systems
- Familiarity with autonomous vehicle perception (Module 01)
- Systems engineering fundamentals
- Probability and statistics

### Software
- None required for core content
- Optional: Python for HARA automation and ASIL calculation
- Safety case tools: ASCE (Adelard Safety Case Editor), GSN tooling

---

## Safety Engineering Tools

- **Goal Structuring Notation (GSN)**: Safety argumentation visualization
- **ASCE (Adelard Safety Case Editor)**: Safety case development tool
- **Fault Tree Analysis (FTA)**: Top-down deductive failure analysis
- **Failure Mode and Effects Analysis (FMEA)**: Bottom-up inductive failure analysis
- **medini analyze**: ISO 26262 workflow and HARA tool

---

## Learning Path

### Beginner Path
1. Start with **01_iso_26262_fundamentals** to understand the standard structure
2. Proceed to **02_hazard_analysis_risk_assessment** for practical HARA
3. Learn **03_asil_decomposition** for architectural safety design

### Advanced Path
4. Master **04_safety_case_development** for certification-ready documentation

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Conduct HARA for lane keeping assist system
2. **Exercise 2**: Calculate ASIL levels for 10 autonomous driving hazards
3. **Exercise 3**: Design ASIL decomposition for redundant perception architecture
4. **Exercise 4**: Develop safety case for pedestrian detection system using GSN
5. **Exercise 5**: Perform gap analysis between existing system and ISO 26262 requirements

---

## Code Examples

Located in `code/`:
- `hara_calculator.py`: Automated ASIL determination from S, E, C values
- `safety_goal_generator.py`: Template-based safety goal formulation
- `asil_decomposition_validator.py`: Check decomposition independence requirements
- `fmea_template.py`: Structured FMEA worksheet generator
- `gsn_exporter.py`: Export safety arguments to GSN XML format

---

## Industry Standards and References

### Standards
- **ISO 26262 (2018)**: Road Vehicles - Functional Safety (Parts 1-12)
  - Part 1: Vocabulary
  - Part 2: Management of functional safety
  - Part 3: Concept phase
  - Part 4: Product development at system level
  - Part 5: Product development at hardware level
  - Part 6: Product development at software level
  - Part 8: Supporting processes
  - Part 9: ASIL-oriented and safety-oriented analyses
  - Part 11: Application to semiconductors
  - Part 12: Motorcycles
- **IEC 61508**: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems
- **ISO/PAS 21448 (SOTIF)**: Complementary standard for intended functionality
- **ISO/TR 4804**: Road Vehicles - Safety and Cybersecurity for Automated Driving Systems

### Key Papers
- Abdulkhaleq et al. (2018): "A Systematic Approach for Developing Safe Autonomous Driving Systems"
- Koopman & Wagner (2016): "Challenges in Autonomous Vehicle Testing and Validation"
- Burton et al. (2019): "Mind the Gaps: Assuring the Safety of Autonomous Systems from an Engineering, Ethical, and Legal Perspective"
- Salay et al. (2017): "An Analysis of ISO 26262: Machine Learning and Safety for Autonomous Vehicles"

### Resources
- [ISO 26262 Official Standard](https://www.iso.org/standard/68383.html)
- [SAE International - Functional Safety Resources](https://www.sae.org/standards/content/iso26262/)
- [Automotive Safety Council](https://autosafetycouncil.org/)
- [MISRA C:2012 Guidelines](https://www.misra.org.uk/) - Software coding standards

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Explain ISO 26262 V-Model and safety lifecycle
✓ Conduct Hazard Analysis and Risk Assessment (HARA)
✓ Determine ASIL levels from severity, exposure, and controllability
✓ Formulate safety goals with measurable criteria
✓ Perform ASIL decomposition for redundant architectures
✓ Develop safety cases using Goal Structuring Notation (GSN)
✓ Apply ISO 26262 to AI-based autonomous systems
✓ Understand integration with SOTIF (ISO 21448) and cybersecurity (ISO/SAE 21434)

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding what requires safety analysis

### Related Modules
- **Module 02**: Failure Analysis - FMEA and failure mode identification
- **Module 04**: SOTIF - Complementary to ISO 26262 for intended functionality
- **Module 05**: Cybersecurity - Safety-security co-analysis

### Follow-up Modules
- **Module 06**: AI Safety - Extending functional safety to machine learning
- **Module 07**: Validation & Verification - ISO 26262 V&V requirements
- **Module 08**: Advanced Topics - Standards integration and certification

---

## Next Steps

After completing this module:
- **Module 04**: SOTIF - Understand performance limitations and unknown unsafe scenarios
- **Module 05**: Cybersecurity - Learn ISO/SAE 21434 for integrated safety-security analysis
- **Module 07**: Validation & Verification - Apply ISO 26262 testing requirements

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
