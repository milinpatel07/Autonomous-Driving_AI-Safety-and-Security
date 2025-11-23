<!--
Copyright (c) 2025 Milin Patel
Hochschule Kempten - University of Applied Sciences

Autonomous Driving: AI Safety and Security Workshop
This project is licensed under the MIT License.
-->

# Session 5: Advanced Topics in AV Safety and Deployment

**Author:** Milin Patel
**Institution:** Hochschule Kempten

## Overview

This session covers advanced topics critical for real-world autonomous vehicle deployment:
- V2X communication and cooperative perception
- Explainability (XAI) for safety certification
- How safety standards integrate in practice
- Industry deployment challenges and barriers
- Operational Design Domain (ODD) specification
- Open problems and future research directions

## Prerequisites

- Completion of Sessions 1-4
- Understanding of ISO 26262, ISO 21448, and ISO/SAE 21434
- Familiarity with AI/ML perception systems

## Learning Objectives

After completing this session, you will understand:

1. **V2X Communication**: How vehicles communicate with infrastructure and each other for safety
2. **Cooperative Perception**: Using V2X data to improve perception beyond line-of-sight
3. **Explainability (XAI)**: How to explain AI decisions to regulators and certify black-box models
4. **Standards Integration**: Practical workflow for applying ISO 26262 + SOTIF + 21434 together
5. **Industry Reality**: What actually prevents Level 4/5 deployment today
6. **ODD Specification**: How to define and monitor operational boundaries
7. **Open Problems**: What research questions remain unsolved

## Session Structure

### Notebook 19: V2X Communication and Cooperative Perception

**Topics:**
- V2V (Vehicle-to-Vehicle), V2I (Vehicle-to-Infrastructure), V2P (Vehicle-to-Pedestrian)
- C-V2X vs DSRC standards comparison
- Cooperative perception: sharing sensor data
- V2X security (message authentication, Sybil attacks)
- ISO/SAE 21434 application to V2X
- Practical challenges: latency, reliability, coverage

**Standards:** SAE J2735, SAE J2945, IEEE 802.11p, 3GPP C-V2X

### Notebook 20: Explainability (XAI) for Safety Certification

**Topics:**
- Why explainability matters for certification
- XAI methods: LIME, SHAP, GradCAM, attention visualization
- Saliency maps for perception models
- Counterfactual explanations
- XAI requirements in ISO/IEC TR 5469
- How to document AI decisions for regulators
- Trade-offs: accuracy vs interpretability

**Standards:** ISO/IEC TR 5469, EU AI Act requirements

### Notebook 21: Standards Integration - Practical Workflow

**Topics:**
- How ISO 26262, ISO 21448, and ISO/SAE 21434 work together
- Which standard applies to which hazard?
- Conflict resolution between standards
- Combined HARA + SOTIF + TARA analysis
- Documentation and traceability requirements
- Tool chain for multi-standard compliance
- Real example: AEB system full analysis

**Key Insight:** Standards are complementary, not redundant

### Notebook 22: Industry Deployment Challenges

**Topics:**
- Why Level 4/5 AVs are not deployed widely
- Regulatory barriers (US, EU, China)
- Liability and insurance issues
- Cost of safety validation (billions of miles)
- Public acceptance and trust
- Infrastructure requirements
- Economic viability
- What's actually working: robotaxis in geofenced areas

**Real Data:** Waymo One, Cruise (before shutdown), Baidu Apollo Go

### Notebook 23: ODD Definition and Runtime Monitoring

**Topics:**
- What is Operational Design Domain (ODD)?
- How to define ODD boundaries (ISO 34503)
- ODD attributes: weather, road types, speed, lighting
- Runtime ODD monitoring
- Graceful degradation when leaving ODD
- Minimal Risk Condition (MRC)
- Driver handover protocols (SAE J3016 Level 3)

**Standards:** ISO 34503, SAE J3016

### Notebook 24: Standards Gaps and Open Problems

**Topics:**
- What ISO 26262 cannot handle for AI/ML
- SOTIF limitations: unknown unknowns
- Unresolved research questions
- Emerging issues not yet standardized
- Future standards in development
- Industry feedback on current standards
- Areas needing more research

**Critical Thinking:** Where do we need better solutions?

## Exercises

### Exercise 9: V2X Security Analysis
Apply TARA methodology to a V2X intersection safety scenario.

### Exercise 10: XAI for Certification
Generate and document explainability evidence for a perception model.

### Exercise 11: Multi-Standard Integration
Perform combined HARA + SOTIF + TARA for an autonomous parking system.

## Key Takeaways

1. **V2X is the future** but deployment is slow due to infrastructure costs
2. **XAI is mandatory** for certification, not optional
3. **Standards must be used together** - no single standard is enough
4. **Deployment is hard** - technical challenges are solved, but regulatory/economic barriers remain
5. **ODD is critical** - every AV must know its limits
6. **Many problems remain open** - this is an active research field

## Resources

- [3GPP C-V2X Specifications](https://www.3gpp.org/)
- [NHTSA AV Policy](https://www.nhtsa.gov/technology-innovation/automated-vehicles-safety)
- [EU Type Approval for Automated Driving](https://ec.europa.eu/growth/sectors/automotive/automated-mobility_en)
- [ISO 34503: Road vehicles — Test scenarios for automated driving systems](https://www.iso.org/standard/78952.html)

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
