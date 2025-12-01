# Session 5: Standards Integration and Deployment - Resources

**Author:** Milin Patel
**Institution:** Hochschule Kempten

This document contains curated links and resources for Session 5 covering V2X communication, explainability (XAI), standards integration, ODD definition, and deployment challenges.

---

## 📡 V2X Communication and Cooperative Perception

### Standards and Specifications

1. **SAE J2735 - Dedicated Short Range Communications (DSRC) Message Set Dictionary**
   - Link: https://www.sae.org/standards/content/j2735_202007/
   - Description: Message format standards for V2V and V2I communication
   - Coverage: Basic Safety Message (BSM), Signal Phase and Timing (SPaT)

2. **IEEE 802.11p - Wireless Access in Vehicular Environments (WAVE)**
   - Link: https://standards.ieee.org/ieee/802.11p/4247/
   - Description: Physical layer standard for V2X
   - Note: Being superseded by C-V2X

3. **3GPP C-V2X Standards**
   - Link: https://www.3gpp.org/technologies/c-v2x
   - Description: Cellular V2X specifications (LTE-V2X and 5G-NR-V2X)
   - Features: Higher bandwidth, better latency than DSRC

4. **ETSI ITS Standards**
   - Link: https://www.etsi.org/technologies/intelligent-transport
   - Description: European V2X standards (CAM, DENM messages)
   - Use: European V2X deployment reference

### Interactive Demos and Visualizations

5. **5GAA - C-V2X Demos and Use Cases**
   - Link: https://5gaa.org/5g-technologies/c-v2x/
   - Description: Industry consortium demonstrations of C-V2X
   - Content: Real-world deployment examples

6. **CARLA Simulator - V2X Plugin**
   - Link: https://github.com/carla-simulator/carla
   - Description: Open-source simulator with V2X communication support
   - Use: Testing cooperative perception algorithms

### Research Papers

7. **"Cooperative Perception for Autonomous Vehicles"** (Chen et al., 2019)
   - Link: arXiv:1905.05265
   - Content: Survey of cooperative perception techniques

8. **"V2X Communication for Connected and Automated Driving"** (Naik et al., 2019)
   - Link: IEEE Communications Surveys & Tutorials
   - Content: Comprehensive V2X technology review

---

## 🔍 Explainability (XAI) for Safety Certification

### XAI Tools and Frameworks

9. **LIME (Local Interpretable Model-agnostic Explanations)**
   - GitHub: https://github.com/marcotcr/lime
   - Paper: https://arxiv.org/abs/1602.04938
   - Use: Explaining individual predictions

10. **SHAP (SHapley Additive exPlanations)**
    - GitHub: https://github.com/slundberg/shap
    - Paper: https://arxiv.org/abs/1705.07874
    - Website: https://shap.readthedocs.io/
    - Use: Unified framework for model interpretation

11. **Grad-CAM (Gradient-weighted Class Activation Mapping)**
    - Paper: https://arxiv.org/abs/1610.02391
    - Demo: https://gradcam.cloudcv.org/
    - Use: Visualizing CNN attention for perception models

12. **Captum (PyTorch XAI Library)**
    - Website: https://captum.ai/
    - GitHub: https://github.com/pytorch/captum
    - Features: Integrated gradients, layer activation, neuron visualization

### XAI for Safety Standards

13. **ISO/IEC TR 5469:2024 - Functional Safety and AI Systems**
    - Link: https://www.iso.org/standard/81283.html
    - Content: Guidance on AI transparency and explainability

14. **EU AI Act - Transparency Requirements**
    - Link: https://artificialintelligenceact.eu/
    - Content: Regulatory requirements for high-risk AI systems
    - Relevance: Explainability mandates for autonomous vehicles

### Research Papers

15. **"Explainable AI for Autonomous Vehicles"** (Atakishiyev et al., 2021)
    - Link: arXiv:2112.11561
    - Content: Survey of XAI techniques for AVs

16. **"Interpretable Machine Learning for Safety-Critical Systems"** (Rudin, 2019)
    - Link: Nature Machine Intelligence
    - Content: Case for inherently interpretable models

---

## 📋 Standards Integration

### Multi-Standard Implementation Guides

17. **ISO 26262:2018 + ISO 21448:2022 Integration White Paper**
    - Source: TÜV SÜD
    - Link: https://www.tuvsud.com/en/themes/automotive/iso-26262-and-sotif
    - Content: Combined safety argumentation approach

18. **SAHARA Method (Combined Safety and Security Analysis)**
    - Paper: "SAHARA: A Security-Aware Hazard and Risk Analysis Method"
    - Link: IEEE Conference on Design, Automation and Test in Europe
    - Use: Integrating ISO 26262 and ISO/SAE 21434

19. **Automotive SPICE + ISO 26262 Mapping**
    - Link: http://www.automotivespice.com/
    - Content: Process assessment model for automotive software
    - Use: Development process compliance

### Standards Organizations

20. **ISO Standards Catalogue**
    - Link: https://www.iso.org/standards.html
    - Standards: ISO 26262, 21448, 21434, 34503

21. **SAE International Standards**
    - Link: https://www.sae.org/standards/
    - Standards: SAE J3016, J2735, J3061

22. **UNECE WP.29 Vehicle Regulations**
    - Link: https://unece.org/transport/vehicle-regulations
    - Content: UN regulations on cybersecurity (R155) and software updates (R156)

---

## 🗺️ ODD Definition and Runtime Monitoring

### ODD Specification Standards

23. **ISO 34503 - Operational Design Domain (ODD) Taxonomy**
    - Link: https://www.iso.org/standard/78951.html
    - Published: 2023
    - Content: Standardized ODD attributes and description framework

24. **SAE J3016 - Levels of Driving Automation**
    - Link: https://www.sae.org/standards/content/j3016_202104/
    - Content: ODD requirements for each automation level

### Runtime Monitoring Tools

25. **Runtime Verification for Autonomous Systems**
    - Paper: "Runtime Verification of Autonomous Driving Systems" (Desai et al., 2017)
    - Content: Formal methods for runtime monitoring

26. **Minimal Risk Condition (MRC) Strategies**
    - Source: ISO 21448 Clause 8
    - Content: Graceful degradation and safe stop strategies

### Research

27. **"Defining Operational Design Domains for Automated Driving"** (Czarnecki, 2018)
    - Link: University of Waterloo Technical Report
    - Content: ODD formalization approaches

28. **"Runtime Monitoring of Autonomous Systems"** (Pnueli & Zaks, 2006)
    - Content: Temporal logic for runtime verification

---

## 🏭 Industry Deployment Challenges

### Case Studies and Reports

29. **Waymo Safety Report**
    - Link: https://waymo.com/safety/
    - Content: Detailed safety methodology and operational data

30. **Cruise Safety Report**
    - Link: https://www.getcruise.com/safety/
    - Content: Safety validation approach and metrics

31. **NTSB Crash Investigation Reports**
    - Link: https://www.ntsb.gov/investigations/
    - Filter: Highway accidents involving automation
    - Use: Learning from real-world failures

32. **California DMV Autonomous Vehicle Disengagement Reports**
    - Link: https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/autonomous-vehicle-collision-reports/
    - Content: Annual disengagement statistics from all AV operators
    - Use: Benchmarking AV performance

### Economic and Regulatory Analysis

33. **RAND Corporation - Autonomous Vehicle Testing Requirements**
    - Link: https://www.rand.org/pubs/research_reports/RR1478.html
    - Paper: "Driving to Safety" (Kalra & Paddock, 2016)
    - Content: Statistical analysis of validation requirements

34. **McKinsey - Autonomous Vehicles Economic Impact**
    - Link: https://www.mckinsey.com/industries/automotive-and-assembly/our-insights
    - Content: Market analysis and deployment barriers

35. **European Commission - Mobility and Transport**
    - Link: https://transport.ec.europa.eu/transport-modes/road/connected-and-automated-mobility_en
    - Content: European regulatory framework for AVs

---

## 🔬 Standards Gaps and Open Problems

### Research Frontier

36. **ISO/IEC JTC 1/SC 42 - Artificial Intelligence**
    - Link: https://www.iso.org/committee/6794475.html
    - Content: Ongoing AI standardization work
    - Relevance: Future AI safety standards

37. **NIST AI Risk Management Framework (AI RMF)**
    - Link: https://www.nist.gov/itl/ai-risk-management-framework
    - Content: Comprehensive AI governance framework
    - Use: Filling gaps in automotive AI standards

38. **IEEE P2846 - Standard for Assumptions in Safety-Related Models**
    - Link: https://standards.ieee.org/ieee/2846/7365/
    - Status: Under development
    - Content: Formalizing assumptions for AI/ML models

### Academic Research

39. **"Open Problems in AI Safety for Autonomous Vehicles"** (Burton et al., 2020)
    - Content: Survey of unsolved safety challenges

40. **"Testing and Validation of AI in Safety-Critical Systems"** (Koopman, 2021)
    - Content: Current limitations and research directions

---

## 🎓 Online Courses and Tutorials

41. **Coursera - Self-Driving Cars Specialization (University of Toronto)**
    - Link: https://www.coursera.org/specializations/self-driving-cars
    - Coverage: V2V communication, safety standards

42. **Udacity - Self-Driving Car Engineer Nanodegree**
    - Link: https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd0013
    - Coverage: Advanced topics including V2X

43. **edX - Autonomous Mobile Robots (ETH Zurich)**
    - Link: https://www.edx.org/course/autonomous-mobile-robots
    - Coverage: Multi-robot coordination, cooperative perception

---

## 📚 Books and Technical Reports

44. **"Safety of the Intended Functionality: Engineering the System"** (Burton et al., 2023)
    - Publisher: Springer
    - Content: Comprehensive SOTIF implementation guide

45. **"Automotive Cybersecurity Engineering Handbook"** (Macher et al., 2020)
    - Publisher: SAE International
    - Content: Practical ISO/SAE 21434 implementation

46. **"Explainable AI: Interpreting, Explaining and Visualizing Deep Learning"** (Samek et al., 2019)
    - Publisher: Springer
    - Content: XAI methods and applications

---

## 🛠️ Open-Source Projects

47. **Autoware Foundation**
    - Link: https://github.com/autowarefoundation/autoware
    - Content: Open-source AV stack with V2X support

48. **Apollo Auto (Baidu)**
    - Link: https://github.com/ApolloAuto/apollo
    - Content: Production-grade AV platform

49. **CARLA Simulator**
    - Link: https://github.com/carla-simulator/carla
    - Content: Open-source simulator for AV research

50. **OpenPilot (comma.ai)**
    - Link: https://github.com/commaai/openpilot
    - Content: Open-source advanced driver assistance system

---

## 🔐 Security Resources

51. **OWASP Automotive Security Project**
    - Link: https://owasp.org/www-project-automotive-security/
    - Content: Security best practices for automotive systems

52. **CAPEC (Common Attack Pattern Enumeration and Classification)**
    - Link: https://capec.mitre.org/
    - Filter: Vehicle and V2X attacks
    - Use: Threat modeling for TARA

53. **CVE Database - Automotive**
    - Link: https://cve.mitre.org/
    - Search: "Automotive" OR "Vehicle" OR "V2X"
    - Use: Vulnerability tracking

---

## 📊 Datasets

54. **V2V Communication Datasets**
    - VeReMi (Vehicle Reference Misbehavior Dataset): https://veremi-dataset.github.io/
    - V2X-Sim: https://github.com/At-Num/V2X-Sim

55. **ODD-Related Datasets**
    - BDD100K (Diverse ODDs): https://www.bdd100k.com/
    - CADC (Canadian Adverse Driving Conditions): http://cadcd.uwaterloo.ca/

---

**Note:** All links verified as of December 2025. If a link is broken, search for the paper/standard title directly.

**Milin Patel**
Hochschule Kempten
Copyright © 2025 Milin Patel. All Rights Reserved.
