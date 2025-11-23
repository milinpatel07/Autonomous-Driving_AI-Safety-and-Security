# Exercise 10: XAI for Safety Certification

**Session 5: Advanced Topics in AV Safety**
**Estimated Time**: 75 minutes

---

## Learning Objectives

- Generate explainability evidence for AI-based perception models
- Apply XAI methods (LIME, SHAP, GradCAM) to autonomous driving scenarios
- Document AI decisions for regulatory compliance
- Evaluate trade-offs between accuracy and interpretability
- Create certification-ready XAI documentation

---

## Scenario: Pedestrian Detection System Certification

You are preparing a pedestrian detection system for safety certification. Regulators require explainability evidence demonstrating the system's decision-making process is trustworthy.

### System Specifications

- **Model**: YOLOv8-based pedestrian detector
- **Input**: 1280x720 RGB camera images
- **Output**: Bounding boxes with confidence scores
- **Performance**: 95.2% AP on KITTI pedestrian benchmark
- **ASIL**: ASIL B (ISO 26262)
- **ODD**: Urban streets, daylight, dry weather

### Regulatory Requirements (ISO/IEC TR 5469)

1. **Explainability**: System shall provide explanations for decisions
2. **Transparency**: Training data and model architecture shall be documented
3. **Auditability**: Decisions shall be logged and traceable
4. **Trustworthiness**: Explanations shall be validated against ground truth

---

## Part 1: XAI Method Application (25 minutes)

### Task 1.1: GradCAM Visualization

Apply Gradient-weighted Class Activation Mapping (GradCAM) to visualize what the model "sees."

**Scenario 1: Correct Detection**
- Image: Pedestrian crossing street in crosswalk
- Model output: Bounding box with 98% confidence

**Questions**:
1. If GradCAM highlights the pedestrian's body and clothing, what does this tell you about model behavior?
2. If GradCAM highlights the crosswalk markings instead of the person, is this a problem? Why or why not?
3. How would you document this for certification?

**Scenario 2: False Negative**
- Image: Pedestrian in dark clothing at dusk
- Model output: No detection (0% confidence)

**Questions**:
1. Use GradCAM: What regions is the model activating?
2. Why might the model fail to detect this pedestrian?
3. What changes to training data or model would fix this?
4. How do you document this failure mode in the safety case?

### Task 1.2: SHAP Analysis

Use SHAP (SHapley Additive exPlanations) to identify which input features contribute most to decisions.

**Scenario**: Pedestrian detected with 85% confidence

**Hypothetical SHAP Output**:
- Upper body visible: +0.35
- Legs visible: +0.25
- Skin tone (face/hands): +0.15
- Motion (compared to background): +0.10
- Context (near crosswalk): +0.05
- Base value: 0.10

**Questions**:
1. Is the model relying on appropriate features? Justify your answer.
2. The model uses "skin tone" as a feature. Is this acceptable? What are the ethical implications?
3. If "context (near crosswalk)" has high contribution, is the model overfitting to crosswalks? What if pedestrian is NOT at crosswalk?
4. How would you report this feature importance to regulators?

### Task 1.3: LIME (Local Interpretable Model-Agnostic Explanations)

Apply LIME to create locally faithful explanations.

**Scenario**: Pedestrian detected behind partially obstructing vehicle

**LIME Process**:
1. Generate perturbed versions of the image (blur regions, mask areas)
2. Get model predictions for perturbed images
3. Fit local linear model to approximate behavior

**Hypothetical LIME Output**:
- If head region removed: Confidence drops to 20%
- If legs region removed: Confidence drops to 45%
- If torso region removed: Confidence drops to 35%
- If background changed: Confidence unchanged

**Questions**:
1. What does this tell you about which features the model finds critical?
2. Is it safe that removing the head drops confidence so dramatically?
3. If background change doesn't affect detection, is this good or bad? (Hint: Think about domain shift)
4. Create a 1-paragraph explanation suitable for non-technical regulators.

---

## Part 2: Failure Mode Documentation (20 minutes)

### Task 2.1: Create Failure Mode Catalog

Document known failure modes with explanations.

**Template**:

```markdown
## Failure Mode FM-[number]: [Brief description]

### Triggering Conditions
- Lighting: [e.g., Low light, high contrast]
- Pedestrian characteristics: [e.g., Dark clothing, small stature]
- Environmental: [e.g., Occlusion, weather]

### Model Behavior
- Output: [What does model predict?]
- Confidence: [Typical confidence level]
- XAI Evidence: [What does GradCAM/SHAP show?]

### Root Cause Analysis
[Why does model fail in this scenario?]

### Safety Impact
- ASIL: [A, B, C, or D]
- Consequence: [What happens if undetected?]
- Mitigation: [How to prevent/detect this failure?]

### SOTIF Classification
- [ ] Known Safe
- [ ] Known Unsafe (Mitigated)
- [X] Known Unsafe (Residual Risk)
- [ ] Unknown

### Validation
- Test cases: [How many test cases cover this?]
- Success rate: [% of correct detections]
- Countermeasures: [Redundant sensors, conservative planning]
```

**Your Task**:

Create failure mode documentation for **3 scenarios**:

1. **FM-01: Pedestrian in dark clothing at dusk**
   - Use XAI evidence from Part 1, Task 1.1

2. **FM-02: Child partially occluded by parked car**
   - Hypothesize model behavior
   - What would GradCAM show?
   - Why is this safety-critical?

3. **FM-03: Pedestrian carrying large object (e.g., box, ladder)**
   - How might this confuse the model?
   - What unusual feature distributions occur?
   - Safety implications?

---

## Part 3: XAI Validation and Trustworthiness (15 minutes)

### Task 3.1: Validate Explanations Against Ground Truth

**Problem**: XAI methods can produce plausible but incorrect explanations.

**Scenario**: Model detects pedestrian, GradCAM highlights the correct person.

**Validation Questions**:

1. **Consistency Check**:
   - If you run GradCAM 10 times on the same image, do you get the same heatmap?
   - If not, how can you trust the explanation?

2. **Counterfactual Validation**:
   - Modify the image based on GradCAM (e.g., blur highlighted regions)
   - Does confidence drop as expected?
   - If confidence doesn't change, is the explanation trustworthy?

3. **Human Expert Agreement**:
   - Show GradCAM heatmaps to human annotators
   - Do they agree this is what a pedestrian looks like?
   - If model highlights unusual features (e.g., shadow), is this acceptable?

**Your Task**:

Design a **validation protocol** for XAI explanations:

**Template**:

```markdown
## XAI Validation Protocol

### Objective
Ensure XAI explanations are accurate, consistent, and trustworthy.

### Validation Tests

#### Test 1: Consistency
- Method: [How to test]
- Acceptance Criteria: [What is acceptable?]
- Frequency: [How often to run?]

#### Test 2: Counterfactual
- Method: [How to test]
- Acceptance Criteria: [What is acceptable?]
- Frequency: [How often to run?]

#### Test 3: Human Expert Review
- Method: [How to test]
- Acceptance Criteria: [What is acceptable?]
- Frequency: [How often to run?]

### Non-Conformance
If validation fails:
- [What actions to take?]
- [Who to notify?]
- [Can system still be deployed?]
```

---

## Part 4: Certification Documentation (15 minutes)

### Task 4.1: Create XAI Certification Package

Regulators need documentation proving your AI system is trustworthy.

**Required Documents**:

1. **XAI Methods Report**
   - Which XAI techniques are used?
   - Why were they selected?
   - What are their limitations?

2. **Failure Mode Analysis with XAI Evidence**
   - From Part 2: Catalog of failure modes
   - Include XAI visualizations
   - Show root cause analysis

3. **Validation Evidence**
   - From Part 3: XAI validation protocol
   - Test results
   - Expert review outcomes

4. **Safety Argumentation**
   - How does XAI support safety claims?
   - Traceability: XAI evidence → Safety requirements

**Your Task**:

Create a **1-page Executive Summary** for regulators:

**Template**:

```markdown
# Pedestrian Detection System: XAI Certification Summary

## System Overview
- Model: [Architecture]
- Performance: [Metrics]
- ODD: [Operating domain]
- ASIL: [Safety level]

## Explainability Approach
[2-3 sentences on XAI methods used]

## Key Findings
### Strengths
- [What does model do well? With XAI evidence]

### Known Limitations
- [What failure modes exist? With XAI evidence]

### Mitigation Strategies
- [How are limitations addressed?]

## Trustworthiness Evidence
- [Summary of validation results]
- [Expert review outcomes]

## Regulatory Compliance
- ISO/IEC TR 5469: [How requirements are met]
- ISO 21448 (SOTIF): [How XAI supports SOTIF analysis]

## Conclusion
[1-2 sentences on overall certification readiness]

---
Prepared by: [Your name]
Date: [Date]
Approved by: [Safety manager, if applicable]
```

---

## Deliverables

Submit a report containing:

1. **Part 1**: XAI method applications with analysis (GradCAM, SHAP, LIME)
2. **Part 2**: 3 failure mode documents with XAI evidence
3. **Part 3**: XAI validation protocol
4. **Part 4**: 1-page executive summary for regulators

**Bonus** (Optional, +15 points):
- Implement actual XAI visualization (Python code) on a sample image
- Compare multiple XAI methods on the same scenario
- Analyze bias in model using XAI (e.g., skin tone sensitivity)

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| **XAI Application** | 25 | Correct understanding and application of GradCAM, SHAP, LIME |
| **Failure Mode Documentation** | 25 | Complete, realistic failure modes with XAI evidence |
| **Validation Protocol** | 20 | Comprehensive and practical validation approach |
| **Certification Package** | 20 | Clear, professional, suitable for regulators |
| **Critical Thinking** | 10 | Identifies limitations, ethical concerns, trade-offs |
| **Total** | 100 | |

---

## References

- **ISO/IEC TR 5469:2024** - Artificial intelligence — Functional safety and AI systems
- **Selvaraju et al. (2017)** - "Grad-CAM: Visual Explanations from Deep Networks"
- **Lundberg & Lee (2017)** - "A Unified Approach to Interpreting Model Predictions" (SHAP)
- **Ribeiro et al. (2016)** - "Why Should I Trust You?" (LIME)
- **EU AI Act** - Requirements for high-risk AI systems

---

*Copyright © 2025 Milin Patel. All Rights Reserved.*
