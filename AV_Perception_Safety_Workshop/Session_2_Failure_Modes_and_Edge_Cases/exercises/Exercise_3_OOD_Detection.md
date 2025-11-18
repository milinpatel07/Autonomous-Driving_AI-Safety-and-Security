# Exercise 3: Out-of-Distribution Detection System Design

**Session 2: Failure Modes and Edge Cases**
**Duration:** 45 minutes
**Difficulty:** Intermediate

---

## Objective

Design and implement an OOD (Out-of-Distribution) detection system for a Level 4 autonomous shuttle operating on a university campus. Your system should identify when the vehicle encounters scenarios outside its training distribution and trigger appropriate safety responses.

---

## Scenario Description

### Campus Shuttle Specifications

**Vehicle:** 12-passenger electric shuttle
**Operational Design Domain (ODD):**
- **Geography:** University campus roads, parking lots, pedestrian zones
- **Speed:** 5-25 km/h
- **Weather:** Clear to light rain
- **Time:** 7:00 AM - 10:00 PM (daylight and dusk/evening)
- **Road Type:** Paved roads with marked lanes
- **Traffic:** Pedestrians, bicycles, campus buses, delivery vehicles

### In-Distribution Training Data

The shuttle's perception system was trained on:
- 50,000 images from campus during Fall semester
- Conditions: 70% clear weather, 20% cloudy, 10% light rain
- Time: 80% daytime, 15% dusk, 5% early evening
- Objects: Students walking, bicyclists, campus buses, cars
- Locations: 15 routes covering main campus roads

---

## Part 1: OOD Scenario Identification (10 min)

**Task:** Identify potential out-of-distribution scenarios the shuttle might encounter.

### Categories to Consider

1. **Environmental OOD:**
   - Weather conditions not in training data
   - Lighting conditions outside ODD
   - Seasonal changes (winter, spring, summer)

2. **Object OOD:**
   - Novel objects not in training data
   - Rare objects (animals, unusual vehicles)
   - Modified objects (vandalized signs)

3. **Behavioral OOD:**
   - Unexpected human behavior
   - Novel traffic patterns
   - Emergency situations

4. **Infrastructure OOD:**
   - Construction zones
   - Temporary road modifications
   - Special events (graduation, sports games)

5. **Sensor OOD:**
   - Degraded sensor performance
   - Sensor failures or occlusions
   - Novel sensor inputs

### Your Answer

List at least **10 specific OOD scenarios** with:
- Description
- Likelihood (Low/Medium/High)
- Potential danger level (Low/Medium/High/Critical)

**Example:**
```
Scenario: Heavy fog reducing visibility to <20 meters
Likelihood: Medium (during winter mornings)
Danger: High (misses pedestrians, objects)
```

---

## Part 2: OOD Detection Method Selection (10 min)

**Task:** Choose and justify OOD detection method(s) for your system.

### Available Methods

1. **Maximum Softmax Probability**
   - Pros: Simple, fast, no additional training
   - Cons: Often fails, overconfident predictions

2. **Mahalanobis Distance**
   - Pros: Effective, principled statistical approach
   - Cons: Requires computing covariance matrix, memory intensive

3. **Energy-Based Detection**
   - Pros: Strong performance, minimal overhead
   - Cons: Requires careful threshold tuning

4. **Monte Carlo Dropout**
   - Pros: Provides uncertainty estimates, works with existing models
   - Cons: Multiple forward passes (slower), requires dropout layers

5. **Ensemble Methods**
   - Pros: Robust, high accuracy
   - Cons: Expensive (multiple models), slow inference

6. **OpenMax**
   - Pros: Designed for open-set recognition
   - Cons: Complex implementation, requires additional training

### Your Answer

**Chosen Method(s):**
(You may choose multiple methods for an ensemble)

**Justification:**
(Explain why this method is appropriate for campus shuttle)

**Performance Targets:**
- AUROC: [Your target, e.g., 0.95]
- FPR@95: [Your target, e.g., 0.05]
- Latency: [Your target, e.g., <50ms]

**Trade-offs:**
(Discuss trade-offs: accuracy vs speed, memory, complexity)

---

## Part 3: Implementation Design (15 min)

**Task:** Design the OOD detection system architecture.

### System Architecture

Describe your system with the following components:

#### 3.1 Input Processing
- What inputs does your OOD detector receive?
- Any preprocessing steps?

#### 3.2 Feature Extraction
- Which layer(s) of the perception model do you use?
- Why these layers?

#### 3.3 OOD Score Computation
- Detailed algorithm for computing OOD score
- Pseudo-code or mathematical formulation

#### 3.4 Threshold Selection
- How do you set the OOD threshold?
- Static vs adaptive threshold?

#### 3.5 Safety Response Protocol
- What happens when OOD is detected?
- Graded response levels (e.g., caution vs critical)

### Example Architecture

```
Input: Camera image (640x480x3)
  ↓
Perception Model (YOLOv8)
  ↓
Feature Extraction (Penultimate layer, 512-dim)
  ↓
OOD Detector (Mahalanobis Distance)
  ↓
OOD Score (0-100, higher = more OOD)
  ↓
Safety Decision Logic:
  - Score < 30: NORMAL (continue)
  - Score 30-50: CAUTION (reduce speed 20%)
  - Score 50-70: WARNING (reduce speed 50%, alert operator)
  - Score > 70: CRITICAL (initiate safe stop)
```

### Your Design

*Provide detailed architecture diagram or description*

---

## Part 4: Safety Response Design (10 min)

**Task:** Define safety responses for different OOD detection levels.

### Response Levels

For each OOD score range, define:
1. Vehicle action (speed, steering, braking)
2. Alert/notification (driver, remote operator, passengers)
3. Logging (what data to record)
4. Recovery procedure (how to resume normal operation)

### Template

| OOD Score | Level | Vehicle Action | Alert | Logging | Recovery |
|-----------|-------|----------------|-------|---------|----------|
| 0-30 | NORMAL | Continue | None | Normal logs | N/A |
| 30-50 | CAUTION | ? | ? | ? | ? |
| 50-70 | WARNING | ? | ? | ? | ? |
| 70-100 | CRITICAL | ? | ? | ? | ? |

### Connection to ISO 21448 SOTIF

**Question:** How does your OOD detection system address ISO 21448 requirements?

*Your answer:*
- How does it help identify "unknown unsafe scenarios"?
- What is the Minimum Risk Condition (MRC) for OOD detection?
- How do you validate the OOD detector itself?

---

## Part 5: Validation and Testing (10 min)

**Task:** Design a validation plan for your OOD detector.

### Testing Strategy

#### 5.1 Simulation Testing
- What simulation environments will you use?
- How many OOD scenarios to test? (be specific)
- What metrics to measure?

#### 5.2 Real-World Testing
- How to safely test OOD scenarios in real world?
- Which scenarios can be tested on campus?
- Which require special test facilities?

#### 5.3 Performance Metrics
Define success criteria:
- AUROC: Minimum acceptable value?
- FPR@95: Maximum acceptable value?
- False negative rate: Critical OOD scenarios?
- False positive rate: Impact on operations?

#### 5.4 Edge Cases for OOD Detector
- What could cause your OOD detector to fail?
- How do you test these edge cases?

### Your Validation Plan

*Provide detailed testing strategy*

---

## Bonus Challenge (Optional)

### Multi-Sensor OOD Detection

**Task:** Extend your OOD detector to use multiple sensor modalities (camera + LiDAR + radar).

**Questions:**
1. How do you fuse OOD scores from different sensors?
2. What if sensors disagree (camera says OOD, LiDAR says in-distribution)?
3. How does sensor fusion improve robustness?

### Adaptive Thresholds

**Task:** Design an adaptive threshold that changes based on context.

**Scenarios:**
- Lower threshold (more conservative) during:
  - Rush hours with heavy pedestrian traffic
  - Night operation
  - Poor weather conditions

- Higher threshold (more permissive) during:
  - Low-traffic periods
  - Familiar routes with recent validation
  - Optimal conditions

**How would you implement this?**

---

## Deliverables

Submit the following:

1. **OOD Scenario List** (10+ scenarios with likelihood and danger)
2. **Method Selection** (chosen method with justification)
3. **System Architecture** (detailed design with diagrams)
4. **Safety Response Protocol** (table with actions for each level)
5. **Validation Plan** (testing strategy with metrics)
6. **ISO 21448 Analysis** (connection to SOTIF requirements)

---

## Evaluation Criteria

Your solution will be evaluated on:

- **Completeness:** All parts addressed thoroughly
- **Technical Correctness:** Sound methodology and reasoning
- **Safety Focus:** Appropriate consideration of safety implications
- **Practicality:** Feasible to implement and deploy
- **Creativity:** Novel approaches or insights

---

## Resources

### Research Papers

1. **Hendrycks & Gimpel (2017)** - "A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks"
   - Link: https://arxiv.org/abs/1610.02136

2. **Lee et al. (2018)** - "A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks"
   - Link: https://arxiv.org/abs/1807.03888

3. **Liu et al. (2020)** - "Energy-based Out-of-distribution Detection"
   - Link: https://arxiv.org/abs/2010.03759

4. **Liang et al. (2018)** - "Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks"
   - Link: https://arxiv.org/abs/1706.02690

### Standards

- **ISO 21448:2022** - Road vehicles — Safety of the intended functionality (SOTIF)
- **ISO 26262:2018** - Road vehicles — Functional safety

### Code Examples

See Notebook 8 (`08_OOD_Detection.ipynb`) for implementation examples.

---

## Example Solution Outline

*(For instructor reference - do not distribute to students initially)*

### Recommended Approach

1. **Method:** Ensemble of Mahalanobis Distance + Energy-Based
   - Mahalanobis for distribution-based detection
   - Energy for model confidence assessment
   - Combine scores with weighted average

2. **Thresholds:**
   - Tune on validation set with known OOD scenarios
   - Target: AUROC > 0.95, FPR@95 < 0.05
   - Adaptive threshold based on context (time, location, weather)

3. **Safety Response:**
   - Graded response with 4 levels
   - Always err on side of caution
   - Log all OOD detections for offline analysis

4. **Validation:**
   - 1000+ simulated OOD scenarios
   - 100+ real-world test cases (safe scenarios)
   - Continuous monitoring in deployment

---

**Good luck! Remember: Safety is paramount. When in doubt, be conservative.**

*Last updated: 2025-01-18*
