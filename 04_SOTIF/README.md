# SOTIF - Safety of the Intended Functionality

**Module 04: ISO 21448 Implementation for Performance Limitations and Unknown Scenarios**

---

## Overview

While ISO 26262 addresses random hardware failures and systematic software faults, ISO 21448 (Safety of the Intended Functionality - SOTIF) focuses on hazards caused by performance limitations and triggering conditions even when the system functions as intended. This module provides comprehensive coverage of SOTIF methodology, particularly critical for AI-based perception systems where complete specification is impossible and unknown unsafe scenarios exist.

### Module Objectives

Upon completing this module, you will:

1. **Understand SOTIF Framework**: Master the four SOTIF quadrants (known safe/unsafe, unknown safe/unsafe scenarios)
2. **Identify Triggering Conditions**: Recognize environmental, operational, and system conditions that expose performance limitations
3. **Analyze Performance Limitations**: Systematically identify sensor, algorithm, and architectural limitations
4. **Apply Scenario-Based Validation**: Design validation strategies to discover unknown unsafe scenarios
5. **Implement Field Monitoring**: Deploy continuous validation and fleet learning approaches
6. **Integrate with ISO 26262**: Understand complementary relationship between functional safety and SOTIF
7. **Apply to AI Systems**: Address unique SOTIF challenges for machine learning-based perception
8. **Achieve SOTIF Acceptance**: Demonstrate that residual risk from unknown unsafe scenarios is acceptably low

---

## Why SOTIF Matters

### Critical Challenges in Intended Functionality Safety

**1. The Four SOTIF Quadrants**
- **Known Safe**: Scenarios validated through testing - safe operation confirmed
- **Known Unsafe**: Identified hazardous scenarios - mitigations implemented or ODD restricted
- **Unknown Safe**: Undiscovered scenarios that would be safe (benign unknowns)
- **Unknown Unsafe**: Undiscovered hazardous scenarios - the primary SOTIF challenge
- Goal: Minimize unknown unsafe quadrant through systematic validation

**2. Performance Limitations vs. Malfunctions**
- **ISO 26262**: Addresses malfunctions (system not working as intended)
- **SOTIF**: Addresses insufficiencies (system working as designed but design is inadequate)
- Examples:
  - Pedestrian detection fails in low light (performance limitation, not malfunction)
  - LiDAR range limited to 200m - vehicle at 250m not detected (by design)
  - Object classifier confused by unusual vehicle (training data limitation)
- AI systems have inherent performance limitations that cannot be fully eliminated

**3. Triggering Conditions**
- **Environmental**: Weather (rain, fog, snow), lighting (glare, darkness), road conditions
- **Operational**: High-speed highway, dense urban traffic, construction zones, unmarked roads
- **System State**: Sensor degradation (dirt, damage), multiple simultaneous objects, computational load
- **Human Factors**: Unusual pedestrian behavior, unexpected driver actions
- Combinations create exponential scenario space

**4. Verification vs. Validation Challenge**
- **Verification**: "Are we building the system right?" (ISO 26262 focus)
- **Validation**: "Are we building the right system?" (SOTIF focus)
- Cannot verify completeness of AI training - validation required
- Insufficient functional requirements for AI-based systems
- Testing cannot prove absence of unknown unsafe scenarios - only reduce probability

**5. The Billion Miles Problem**
- NHTSA study: Human drivers have ~1 fatality per 100 million miles
- Proving autonomous systems are safer requires statistically significant data
- 8.8 billion miles needed for 95% confidence (RAND study, Kalra & Paddock 2016)
- Physical testing alone is infeasible - combination of simulation, proving grounds, and public roads required
- SOTIF validation strategy addresses this through layered evidence

**6. Operational Design Domain (ODD) Definition**
- ODD specifies where/when system is designed to operate safely
- Examples: "Highways only, daylight, <65 mph, no heavy rain"
- Tighter ODD → easier SOTIF validation but reduced utility
- ODD must be monitorable at runtime (ISO 34503)
- Exiting ODD requires Minimum Risk Condition (MRC) transition

---

## Module Structure

### 📓 Notebooks

1. **[01_sotif_fundamentals.ipynb](notebooks/01_sotif_fundamentals.ipynb)**
   - ISO 21448 structure and scope
   - SOTIF four-quadrant model (known/unknown × safe/unsafe)
   - Performance limitations: Sensor, algorithm, architectural
   - Triggering conditions taxonomy
   - Relationship to ISO 26262 and ISO/PAS 8800
   - SOTIF lifecycle: Specification → Design → Verification → Validation
   - SOTIF acceptance criteria and argumentation

2. **[02_triggering_conditions.ipynb](notebooks/02_triggering_conditions.ipynb)**
   - Environmental triggering conditions: Weather, lighting, road surface
   - Sensor-specific triggers: Camera (glare, darkness), LiDAR (rain, fog), Radar (clutter)
   - Scenario-based triggers: Dense traffic, construction zones, unmarked roads
   - Temporal factors: Dawn/dusk transitions, sudden weather changes
   - Combined triggering conditions: Multi-factor scenario generation
   - Empirical data from field testing and disengagement analysis
   - Trigger coverage metrics and gap analysis

3. **[03_scenario_based_validation.ipynb](notebooks/03_scenario_based_validation.ipynb)**
   - Concrete scenarios: Specific test cases with exact parameters
   - Logical scenarios: Parameterized scenario families
   - Functional scenarios: Abstract behavior descriptions
   - PEGASUS 6-layer scenario model
   - Scenario generation methods: Combinatorial, Monte Carlo, adversarial
   - Simulation platforms: CARLA, SUMO, PreScan
   - Proving ground testing: Controlled environment validation
   - Field operational tests (FOT): Naturalistic driving studies
   - Coverage assessment: Measuring unknown unsafe scenario reduction

4. **[04_field_monitoring.ipynb](notebooks/04_field_monitoring.ipynb)**
   - Continuous validation requirements (ISO 34503)
   - Runtime monitoring: ODD compliance, performance metrics, anomaly detection
   - Disengagement analysis: Root cause categorization
   - Fleet learning: Aggregating experiences across vehicle fleet
   - Shadow mode testing: Running new algorithms alongside production system
   - Minimum Risk Condition (MRC): Transition strategies when leaving ODD
   - Over-the-air (OTA) updates: Validation requirements for deployment
   - Data-driven safety case evolution

---

## Prerequisites

### Knowledge
- Understanding of autonomous vehicle perception (Module 01)
- Familiarity with ISO 26262 functional safety (Module 03)
- Failure mode analysis (Module 02)
- Basic statistics and probability theory

### Software
- Python 3.8+
- CARLA Simulator (0.9.13+) for scenario testing
- Libraries: NumPy, Pandas, Matplotlib, SciPy
- Optional: SUMO for traffic simulation

---

## SOTIF Analysis Tools

- **CARLA Scenario Runner**: Scenario-based testing framework
- **OpenSCENARIO**: Standard scenario description format
- **ASAM OpenX Standards**: OpenDRIVE (road networks), OpenCRG (road surfaces)
- **PreScan**: Physics-based sensor simulation
- **VTD (Virtual Test Drive)**: Commercial AV simulation platform

---

## Learning Path

### Beginner Path
1. Start with **01_sotif_fundamentals** to understand the SOTIF framework
2. Proceed to **02_triggering_conditions** for systematic limitation identification
3. Learn **03_scenario_based_validation** for testing strategies

### Advanced Path
4. Master **04_field_monitoring** for continuous validation and deployment

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Map autonomous emergency braking (AEB) system to SOTIF four quadrants
2. **Exercise 2**: Identify triggering conditions for pedestrian detection in urban environment
3. **Exercise 3**: Generate 50 logical scenarios for highway lane change validation
4. **Exercise 4**: Analyze 100 disengagement reports and categorize by SOTIF root cause
5. **Exercise 5**: Develop SOTIF acceptance argument for limited ODD autonomous shuttle

---

## Code Examples

Located in `code/`:
- `sotif_quadrant_mapper.py`: Classify scenarios into SOTIF quadrants
- `trigger_analyzer.py`: Extract triggering conditions from test data
- `scenario_coverage.py`: Measure scenario space coverage
- `odd_monitor.py`: Runtime ODD compliance checker
- `fleet_aggregator.py`: Aggregate disengagement data across fleet

---

## Industry Standards and References

### Standards
- **ISO 21448 (2022)**: Road Vehicles - Safety of the Intended Functionality (SOTIF)
- **ISO 26262**: Functional Safety - Complementary to SOTIF
- **ISO 34503**: Road Vehicles - Test Scenarios for Automated Driving Systems
- **ISO/PAS 8800**: Safety and Artificial Intelligence - Addresses AI-specific SOTIF challenges
- **UL 4600**: Standard for Safety for the Evaluation of Autonomous Products
- **UNECE WP.29**: Automated Lane Keeping Systems (ALKS) regulation

### Key Papers
- Reschka (2016): "Safety Concept for Autonomous Vehicles" - SOTIF foundations
- Koopman & Wagner (2017): "Autonomous Vehicle Safety: An Interdisciplinary Challenge"
-Kalra & Paddock (2016): "Driving to Safety: How Many Miles of Driving Would It Take?"
- Czarnecki (2018): "Operational Design Domain for Automated Driving Systems"
- Jiang et al. (2021): "SOTIF Validation for Automated Driving Systems"

### Resources
- [ISO 21448 Official Standard](https://www.iso.org/standard/77490.html)
- [PEGASUS Project](https://www.pegasusprojekt.de/en/) - German research on scenario-based validation
- [ENABLE-S3 Project](https://enable-s3.eu/) - European SOTIF validation research
- [OpenSCENARIO Standard](https://www.asam.net/standards/detail/openscenario/)

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Explain ISO 21448 SOTIF framework and four-quadrant model
✓ Identify performance limitations of sensors and algorithms
✓ Analyze triggering conditions that expose insufficiencies
✓ Design scenario-based validation strategies
✓ Develop Operational Design Domain (ODD) specifications
✓ Implement runtime monitoring for ODD compliance
✓ Apply field monitoring and fleet learning approaches
✓ Create SOTIF acceptance arguments
✓ Understand relationship between ISO 26262 and ISO 21448

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding system capabilities
- **Module 03**: Functional Safety - ISO 26262 foundation

### Related Modules
- **Module 02**: Failure Analysis - Edge cases as triggering conditions
- **Module 06**: AI Safety - Uncertainty quantification for SOTIF validation
- **Module 07**: Validation & Verification - Scenario-based testing implementation

### Follow-up Modules
- **Module 08**: Advanced Topics - ODD monitoring and MRC strategies
- **Module 09**: LiDAR Technology - Sensor-specific performance limitations

---

## Next Steps

After completing this module:
- **Module 07**: Validation & Verification - Implement scenario-based testing strategies
- **Module 08**: Advanced Topics - Runtime ODD monitoring and standards integration
- **Module 06**: AI Safety - Apply uncertainty quantification for SOTIF validation

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
