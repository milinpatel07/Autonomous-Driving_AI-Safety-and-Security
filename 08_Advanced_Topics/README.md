# Module 08: Advanced Topics

How do we deploy safe autonomous systems in the real world?

This module integrates everything - V2X security, explainability, multi-standard compliance, runtime monitoring, and real deployment challenges.

---

## What's in This Module

**6 notebooks covering:**
- V2X communication security
- Explainability (LIME, SHAP, Grad-CAM)
- Multi-standard integration
- ODD runtime monitoring
- Industry deployment challenges
- Standards gaps and open problems

---

## Notebooks

### 1. V2X Communication
**[19_V2X_Communication.ipynb](notebooks/19_V2X_Communication.ipynb)**

Vehicle-to-everything communication:
- V2V, V2I, V2P, V2N architectures
- C-V2X vs DSRC technology comparison
- Message types (CAM, DENM, BSM)
- Security challenges: Authentication, privacy, Sybil attacks
- Standards: IEEE 1609, ETSI ITS-G5

### 2. Explainability (XAI)
**[20_Explainability_XAI.ipynb](notebooks/20_Explainability_XAI.ipynb)**

Making AI decisions interpretable:
- Why explainability matters for certification
- LIME: Local model-agnostic explanations
- SHAP: SHapley Additive exPlanations
- Grad-CAM: Gradient-weighted activation mapping
- Attention visualization for transformers
- Trade-offs: Explainability vs performance

### 3. Standards Integration
**[21_Standards_Integration.ipynb](notebooks/21_Standards_Integration.ipynb)**

Harmonizing multiple standards:
- ISO 26262 (functional safety)
- ISO 21448 (SOTIF)
- ISO/SAE 21434 (cybersecurity)
- ISO/PAS 8800 (AI safety)
- Overlaps, gaps, and conflicts
- Unified safety case development

### 4. ODD Runtime Monitoring
**[23_ODD_Runtime_Monitoring.ipynb](notebooks/23_ODD_Runtime_Monitoring.ipynb)**

Continuous ODD compliance:
- Defining monitorable ODD parameters
- Runtime checks: Weather, road type, sensor health, traffic
- Minimum Risk Condition (MRC) strategies
- Transition time and FTTI (Fault Tolerant Time Interval)
- ISO 34503 requirements

### 5. Industry Deployment Challenges
**[22_Industry_Deployment_Challenges.ipynb](notebooks/22_Industry_Deployment_Challenges.ipynb)**

Real-world barriers:
- Economic: Development cost, sensor pricing, ROI uncertainty
- Regulatory: Fragmentation across countries/states
- Liability: Who's responsible for crashes?
- Public acceptance and trust
- Insurance models
- Business models: Robotaxis, trucking, delivery

### 6. Standards Gaps and Open Problems
**[24_Standards_Gaps_Open_Problems.ipynb](notebooks/24_Standards_Gaps_Open_Problems.ipynb)**

Current limitations and research frontiers:
- What current standards don't cover
- AI-specific challenges (distribution shift, adversarial attacks)
- V2X security scalability
- Mixed autonomy traffic (humans + AVs)
- Ethical decision-making frameworks
- Open research questions

---

## Why This Matters

**Deployment is harder than development:**
- Standards developed independently - integration not fully specified
- ODD monitoring is critical but challenging to implement
- V2X security requires infrastructure that doesn't exist yet
- Explainability needed for certification but hurts performance
- Economic and regulatory barriers slow deployment

**This module brings it all together:**
- Shows how all 7 modules connect in real deployment
- Addresses practical challenges not covered in standards
- Prepares you for actual autonomous vehicle engineering

---

## Prerequisites

**Required:**
- All previous modules (01-06)
- Understanding of safety, SOTIF, and cybersecurity standards

**Recommended:**
- Systems integration experience
- Real-world engineering perspective

---

## After This Module

You'll understand:
- How to integrate multiple standards in one system
- Real deployment challenges beyond technical specifications
- Where current standards fall short
- What open research problems remain

**Next steps:**
- Apply this knowledge to real AV projects
- Contribute to standards development
- Research open problems in AV safety and security

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten
**Last Updated:** 2025-12-28
