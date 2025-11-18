# Exercise 4: Adversarial Robustness Evaluation

**Session 2: Failure Modes and Edge Cases**
**Duration:** 60 minutes
**Difficulty:** Advanced

---

## Objective

Evaluate the adversarial robustness of a pedestrian detection system for autonomous vehicles. You will implement adversarial attacks, measure their effectiveness, design defenses, and document security requirements per ISO/SAE 21434.

---

## Scenario Description

### System Under Test

**Component:** Pedestrian detection system for AV emergency braking
**Model:** YOLOv8 trained on pedestrian datasets (KITTI, nuScenes)
**Input:** Camera images (1920x1080, RGB)
**Output:** Bounding boxes + confidence scores for detected pedestrians
**Safety Function:** Trigger emergency brake if pedestrian detected <5m ahead

**Safety Requirement:** Must detect pedestrians with >99% recall in ODD

### Threat Model

**Attacker Goal:** Prevent detection of pedestrian → AV fails to brake → collision

**Attack Scenarios:**
1. **Digital:** Modify camera feed (requires hacking vehicle network)
2. **Physical:** Place adversarial patches on pedestrian clothing
3. **Environmental:** Use adversarial projections (laser, LED)

**Assumption:** Attacker has white-box access to model (worst case)

---

## Part 1: Threat Analysis (10 min)

**Task:** Perform threat analysis per ISO/SAE 21434.

### 1.1 Identify Attack Vectors

List possible ways an attacker could compromise pedestrian detection:

| Attack Vector | Method | Feasibility | Impact | Risk Level |
|---------------|--------|-------------|--------|------------|
| Digital attack on camera feed | CAN bus injection | Medium | Critical | HIGH |
| Adversarial patch on clothing | Physical sticker | High | Critical | HIGH |
| ... | ... | ... | ... | ... |

Add at least **5 attack vectors** with analysis.

### 1.2 Attack Tree

Create an attack tree showing:
- Root: "Defeat pedestrian detection"
- Branches: Different attack paths
- Leaves: Specific techniques

**Example:**
```
Defeat Pedestrian Detection
├── Digital Attacks
│   ├── Hack camera feed (requires network access)
│   └── Inject fake images (requires compromised ECU)
├── Physical Attacks
│   ├── Adversarial patch on clothing
│   ├── Adversarial patterns on road
│   └── 3D adversarial objects
└── Sensor Attacks
    ├── Camera blinding (laser)
    └── Lens occlusion (spray, cover)
```

### 1.3 Risk Assessment

For each attack vector, assess:
- **Likelihood:** Low / Medium / High
- **Impact:** Low / Medium / High / Critical
- **Risk:** Combine likelihood × impact

**Prioritize** the top 3 highest-risk attacks to focus on.

---

## Part 2: Implement Adversarial Attacks (20 min)

**Task:** Implement FGSM and PGD attacks on the pedestrian detector.

### 2.1 FGSM Attack

**Algorithm:**
1. Load pedestrian image
2. Run detection, get confidence scores
3. Compute gradient of loss w.r.t. image
4. Perturb image: `x_adv = x + ε * sign(∇L)`
5. Verify detection drops

**Your Implementation:**

```python
def fgsm_attack_pedestrian(image, model, epsilon=0.03):
    """
    FGSM attack on pedestrian detection

    Args:
        image: Input image tensor
        model: Pedestrian detector
        epsilon: Perturbation magnitude

    Returns:
        adversarial_image: Perturbed image
        original_detections: Detections on clean image
        adversarial_detections: Detections on adversarial image
    """
    # TODO: Implement FGSM attack
    pass
```

**Test Cases:**
- Epsilon values: [0.01, 0.03, 0.05, 0.1]
- Dataset: 100 images with pedestrians
- Measure: Detection rate before vs after attack

### 2.2 PGD Attack

**Algorithm:**
Similar to FGSM but iterative (10 steps)

```python
def pgd_attack_pedestrian(image, model, epsilon=0.03, alpha=0.007, num_iter=10):
    """
    PGD attack on pedestrian detection
    """
    # TODO: Implement PGD attack
    pass
```

### 2.3 Attack Evaluation

**Metrics:**
1. **Attack Success Rate (ASR):** % of images where detection dropped below threshold
2. **Confidence Reduction:** Average decrease in detection confidence
3. **Detection Recall:** Recall on adversarial examples

**Report:**

| Attack | Epsilon | ASR | Avg Conf Reduction | Recall |
|--------|---------|-----|-------------------|--------|
| FGSM | 0.01 | ? | ? | ? |
| FGSM | 0.03 | ? | ? | ? |
| FGSM | 0.05 | ? | ? | ? |
| PGD | 0.03 | ? | ? | ? |

**Questions:**
- At what epsilon does ASR exceed 50%?
- Is PGD more effective than FGSM?
- What is the safety implication? (missed detections)

---

## Part 3: Physical Attack Simulation (10 min)

**Task:** Design and simulate a physical adversarial patch attack.

### 3.1 Patch Design

**Objective:** Create a patch that, when worn on clothing, prevents pedestrian detection.

**Constraints:**
- Patch size: Max 30cm × 30cm (printable)
- Placement: Chest area of pedestrian
- Viewing angle: 0° to 45° (front to side view)
- Distance: 5m to 50m

**Design Process:**
1. Generate patch via optimization (expectation over transformations)
2. Apply random rotations, scales, positions
3. Simulate camera noise, lighting variations
4. Optimize to minimize detection confidence

**Pseudo-code:**

```python
# Expectation Over Transformations (EOT)
for epoch in range(num_epochs):
    for pedestrian_image in dataset:
        # Random transformations
        patch_transformed = random_transform(adversarial_patch)
        image_with_patch = apply_patch(pedestrian_image, patch_transformed)

        # Detection
        detections = model(image_with_patch)

        # Loss: Minimize detection confidence
        loss = detection_confidence(detections)

        # Update patch
        patch_gradient = compute_gradient(loss, adversarial_patch)
        adversarial_patch -= learning_rate * patch_gradient
```

### 3.2 Simulation Testing

**Scenarios:**
1. Pedestrian walking toward vehicle (0m to 50m)
2. Pedestrian crossing from left (lateral motion)
3. Pedestrian crossing from right
4. Multiple pedestrians (patch on one)
5. Different lighting (day, dusk, night)
6. Different weather (clear, rain, fog)

**Metrics:**
- Detection rate at each distance
- Critical distance where detection fails
- Robustness across scenarios

### 3.3 Feasibility Analysis

**Question:** Is this attack feasible in real world?

**Consider:**
- Printing quality (can printer reproduce patch accurately?)
- Viewing angle robustness (does it work from all angles?)
- Lighting robustness (does it work in different lighting?)
- Detection: Would such a patch be noticed by humans/security?

---

## Part 4: Design Defense Mechanisms (15 min)

**Task:** Design defenses against adversarial attacks.

### 4.1 Adversarial Training

**Strategy:** Include adversarial examples in training data.

**Implementation Plan:**
1. Generate adversarial examples (FGSM, PGD)
2. Mix with clean training data (ratio 1:1)
3. Train model on combined dataset
4. Evaluate on both clean and adversarial test sets

**Expected Results:**
- Robustness improves (higher recall on adversarial examples)
- Clean accuracy may decrease slightly
- Trade-off: Balance clean vs adversarial performance

**Your Design:**
- Training procedure details
- Dataset composition (clean vs adversarial)
- Hyperparameters (epsilon for training attacks)

### 4.2 Input Preprocessing Defense

**Idea:** Preprocess images to remove adversarial perturbations.

**Methods:**
1. **JPEG Compression:** Lossy compression removes high-frequency noise
2. **Gaussian Blur:** Smooth image to remove perturbations
3. **Median Filter:** Remove outlier pixel values
4. **Total Variation Denoising:** Minimize image total variation

**Your Design:**
- Which preprocessing method(s) to use?
- Parameters (compression quality, blur kernel size, etc.)
- Performance impact (speed, accuracy)

**Evaluate:**
- Does preprocessing reduce attack success rate?
- Does it harm clean image performance?

### 4.3 Ensemble Detection

**Idea:** Use multiple models; adversarial example may not transfer to all.

**Implementation:**
1. Train 3-5 different pedestrian detectors
   - Different architectures (YOLOv8, Faster R-CNN, RetinaNet)
   - Different training data
   - Different augmentations
2. Detection logic: Majority vote or maximum confidence

**Your Design:**
- Which models to ensemble?
- Fusion logic (how to combine outputs?)
- Computational cost

### 4.4 Anomaly Detection

**Idea:** Detect adversarial inputs before feeding to model.

**Methods:**
1. **Statistical Tests:** Check pixel value distributions
2. **Autoencoder:** High reconstruction error for adversarial inputs
3. **Adversarial Detector:** Train separate model to detect attacks

**Your Design:**
- Which anomaly detection method?
- Integration with main detection pipeline
- False positive rate (flagging clean images)

### 4.5 Defense Evaluation

**Test your defenses:**

| Defense | ASR (FGSM ε=0.03) | ASR (PGD ε=0.03) | Clean Recall | Latency Increase |
|---------|------------------|------------------|--------------|------------------|
| None (baseline) | ? | ? | 99% | 0ms |
| Adversarial Training | ? | ? | ? | 0ms |
| JPEG Compression | ? | ? | ? | +5ms |
| Ensemble (3 models) | ? | ? | ? | +30ms |
| Anomaly Detection | ? | ? | ? | +10ms |

**Questions:**
- Which defense is most effective?
- What are the trade-offs?
- Can you combine multiple defenses?

---

## Part 5: ISO/SAE 21434 Documentation (15 min)

**Task:** Document cybersecurity requirements per ISO/SAE 21434.

### 5.1 Cybersecurity Goals

Define security goals for pedestrian detection system:

1. **Availability:** System must remain operational (resist DoS)
2. **Integrity:** Detections must be trustworthy (resist manipulation)
3. **Confidentiality:** Model weights protected (resist model extraction)

**For this exercise, focus on Integrity.**

### 5.2 Security Requirements

Specify requirements in following format:

| Req ID | Requirement | Rationale | Verification |
|--------|-------------|-----------|--------------|
| SEC-01 | Pedestrian detection shall maintain >95% recall under FGSM attack (ε≤0.05) | Resist digital attacks | Adversarial testing with 1000 test images |
| SEC-02 | System shall detect adversarial patches with >90% accuracy | Resist physical attacks | Simulation with 500 patch scenarios |
| SEC-03 | ... | ... | ... |

Add at least **6 security requirements** covering:
- Digital attack resistance
- Physical attack resistance
- Sensor attack detection
- Monitoring and logging
- Update and patching

### 5.3 Security Testing Plan

**Test Categories:**

1. **Penetration Testing:**
   - White-box attacks (model known)
   - Black-box attacks (model unknown)
   - Gray-box attacks (partial knowledge)

2. **Robustness Testing:**
   - Systematic epsilon sweep (0.0 to 0.1)
   - Multiple attack methods (FGSM, PGD, C&W)
   - Physical attack simulations

3. **Defense Validation:**
   - Effectiveness against known attacks
   - Impact on clean performance
   - Computational overhead

4. **Continuous Monitoring:**
   - Deploy anomaly detectors in vehicle
   - Log suspicious inputs
   - Regular model updates

**Your Test Plan:**
- Specific test cases (at least 10)
- Pass/fail criteria
- Testing frequency (during development, before deployment, in operation)

### 5.4 Risk Mitigation Summary

Document how each defense mitigates identified threats:

| Threat | Risk Level (Before) | Defense | Risk Level (After) | Residual Risk Acceptance |
|--------|---------------------|---------|--------------------|-----------------------|
| FGSM digital attack | HIGH | Adversarial training | MEDIUM | Acceptable with monitoring |
| Physical patch | HIGH | Ensemble + anomaly detection | MEDIUM | Acceptable with sensor fusion |
| ... | ... | ... | ... | ... |

---

## Bonus Challenge 1: Certified Defense (Optional)

**Task:** Implement randomized smoothing for certified robustness.

**Algorithm:**
1. Add Gaussian noise to input image
2. Run detection multiple times (e.g., 100)
3. Return majority vote prediction
4. Compute certified radius (provable robustness)

**Questions:**
- What is the certified radius for your detector?
- How does noise level affect accuracy vs robustness?
- Is this practical for real-time AV perception?

---

## Bonus Challenge 2: Transferability Study (Optional)

**Task:** Analyze attack transferability across models.

**Procedure:**
1. Train 3 different pedestrian detectors
2. Generate adversarial examples on Model A
3. Test on Models B and C
4. Measure transfer success rate

**Questions:**
- Do adversarial examples transfer?
- Which model pairs have highest transferability?
- Implications for ensemble defense?

---

## Deliverables

Submit the following:

1. **Threat Analysis Report**
   - Attack vectors (5+)
   - Attack tree diagram
   - Risk assessment table

2. **Attack Implementation**
   - Code for FGSM and PGD attacks
   - Attack evaluation results (ASR, confidence, recall)
   - Physical patch simulation (optional but recommended)

3. **Defense Design**
   - Descriptions of 4+ defense mechanisms
   - Implementation details
   - Defense evaluation results

4. **ISO/SAE 21434 Documentation**
   - 6+ security requirements
   - Security testing plan
   - Risk mitigation summary

5. **Final Recommendation**
   - Which defenses to deploy?
   - System architecture with security layers
   - Residual risks and acceptance criteria

---

## Evaluation Criteria

Your solution will be evaluated on:

- **Threat Analysis:** Comprehensive identification of attack vectors
- **Attack Implementation:** Correct implementation and thorough testing
- **Defense Design:** Creative and effective defense mechanisms
- **Security Documentation:** Complete ISO/SAE 21434 compliance
- **Critical Thinking:** Analysis of trade-offs and limitations
- **Safety Focus:** Appropriate consideration of safety implications

---

## Resources

### Research Papers

1. **Goodfellow et al. (2014)** - "Explaining and Harnessing Adversarial Examples"
   - Link: https://arxiv.org/abs/1412.6572

2. **Madry et al. (2018)** - "Towards Deep Learning Models Resistant to Adversarial Attacks"
   - Link: https://arxiv.org/abs/1706.06083

3. **Eykholt et al. (2018)** - "Robust Physical-World Attacks on Deep Learning Visual Classification"
   - Link: https://arxiv.org/abs/1707.08945

4. **Athalye et al. (2018)** - "Synthesizing Robust Adversarial Examples"
   - Link: https://arxiv.org/abs/1707.07397

5. **Cohen et al. (2019)** - "Certified Adversarial Robustness via Randomized Smoothing"
   - Link: https://arxiv.org/abs/1902.02918

### Standards

- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering
- **ISO 26262:2018** - Road vehicles — Functional safety
- **ISO 21448:2022** - Safety of the intended functionality (SOTIF)

### Code Examples

- See Notebook 10 (`10_Adversarial_Attacks_on_Perception.ipynb`)
- IBM Adversarial Robustness Toolbox: https://github.com/Trusted-AI/adversarial-robustness-toolbox
- CleverHans: https://github.com/cleverhans-lab/cleverhans

---

## Safety Warning

**IMPORTANT:** This exercise is for educational purposes to improve AV safety.

**DO NOT:**
- Deploy actual adversarial attacks on real autonomous vehicles
- Share attack methods for malicious purposes
- Test on public roads or real pedestrians

**DO:**
- Use for improving robustness of safety systems
- Share knowledge to advance AV security research
- Follow responsible disclosure for vulnerabilities

---

**Good luck! Remember: The goal is to make AVs safer by understanding and defending against adversarial threats.**

*Last updated: 2025-01-18*
