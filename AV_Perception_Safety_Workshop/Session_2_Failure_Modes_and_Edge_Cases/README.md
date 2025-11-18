# Session 2: Failure Modes and Edge Cases in AV Perception

**Duration:** 90 minutes (10:45 - 12:15)
**Instructor:** Milin Patel

## 🎯 Session Objectives

By the end of this session, you will:
- ✅ Analyze real-world autonomous vehicle accidents and their root causes
- ✅ Understand failure taxonomy for AV perception systems
- ✅ Implement out-of-distribution (OOD) detection methods
- ✅ Identify corner cases and edge cases in driving scenarios
- ✅ Understand adversarial attacks on perception systems
- ✅ Apply defensive techniques for adversarial robustness
- ✅ Connect failure modes to ISO 21448 (SOTIF) and ISO/SAE 21434 (Cybersecurity)

## 📋 Session Structure

### Part A: Real-World Failure Analysis (20 min)
- Uber ATG Tempe crash (2018) - detailed breakdown
- Tesla Autopilot incidents
- Cruise SF accident (2023)
- Failure taxonomy and root cause analysis
- Lessons learned for safety engineering

### Part B: Out-of-Distribution Detection (25 min)
- OOD detection methods and algorithms
- Mahalanobis distance, Energy-based, OpenMax
- Uncertainty estimation with MC Dropout
- Implementation and performance metrics
- Connection to ISO 21448 SOTIF

### Part C: Corner Cases and Long Tail (20 min)
- Definition: corner cases vs edge cases
- Long-tail distribution in autonomous driving
- Examples: unusual weather, rare objects
- Simulation-based testing approaches
- Coverage analysis and gap identification

### Part D: Adversarial Attacks (25 min)
- Digital adversarial examples (FGSM, PGD)
- Physical attacks: adversarial patches
- Sensor spoofing (LiDAR, camera)
- Defense mechanisms
- Link to ISO/SAE 21434 cybersecurity standard

## 📓 Jupyter Notebooks

Work through these notebooks in order:

| # | Notebook | Topics | Duration |
|---|----------|--------|----------|
| 7 | `07_AV_Failure_Case_Studies.ipynb` | Real accident analysis, failure taxonomy | 20 min |
| 8 | `08_OOD_Detection.ipynb` | OOD detection methods, uncertainty | 25 min |
| 9 | `09_Corner_Cases_and_Edge_Cases.ipynb` | Long tail, simulation testing | 20 min |
| 10 | `10_Adversarial_Attacks_on_Perception.ipynb` | Adversarial examples, defenses | 25 min |

**Total:** ~90 minutes

## 🚀 Quick Start

### Prerequisites
- ✅ Complete Session 1 (AI Perception Systems)
- ✅ Python environment set up with required packages
- ✅ Basic understanding of object detection and deep learning

### Launch Notebooks
```bash
# From Session_2_Failure_Modes_and_Edge_Cases directory
jupyter lab

# Or from workshop root:
cd AV_Perception_Safety_Workshop
jupyter lab Session_2_Failure_Modes_and_Edge_Cases/notebooks/
```

### Google Colab
All notebooks include Colab badges - click to run in your browser:
1. No installation required
2. Free GPU access
3. Automatic dependency installation

### Running Notebooks
1. Open `07_AV_Failure_Case_Studies.ipynb`
2. Select kernel: **"AV Workshop"** (or use Colab)
3. Run cells sequentially (Shift + Enter)
4. Complete exercises at the end
5. Proceed to next notebook

## 📂 Directory Structure

```
Session_2_Failure_Modes_and_Edge_Cases/
├── README.md                                    # This file
│
├── notebooks/                                   # Jupyter notebooks (main content)
│   ├── 07_AV_Failure_Case_Studies.ipynb        # Real-world accident analysis
│   ├── 08_OOD_Detection.ipynb                  # Out-of-distribution detection
│   ├── 09_Corner_Cases_and_Edge_Cases.ipynb    # Long-tail scenarios
│   └── 10_Adversarial_Attacks_on_Perception.ipynb  # Adversarial robustness
│
├── exercises/                                   # Hands-on exercises
│   ├── Exercise_3_OOD_Detection.md             # Design OOD detector
│   └── Exercise_4_Adversarial_Robustness.md    # Evaluate robustness
│
└── resources/                                   # External links and references
    └── links.md                                # NTSB reports, papers, datasets
```

## 📚 Notebook Details

### Notebook 7: AV Failure Case Studies
**File:** `07_AV_Failure_Case_Studies.ipynb`

**Content:**
- **Uber ATG crash (March 2018):** Pedestrian fatality in Tempe, AZ
  - System architecture and failure points
  - Perception system limitations (misclassification)
  - Safety driver inattention
  - NTSB findings and recommendations
- **Tesla Autopilot incidents:** Multiple crashes involving semi-trucks
  - Camera limitations in high-contrast scenarios
  - False assumptions about system capabilities
- **Cruise SF accident (Oct 2023):** Pedestrian dragging incident
  - Decision-making failure after initial impact
  - Communication with authorities
- **Failure taxonomy:** Classification of failure modes
- **Root cause analysis framework:** 5 Whys, Fishbone diagrams
- **Lessons learned:** Design principles for safer systems

**Key Concepts:**
- Perception failures: misclassification, missed detection
- Sensor limitations: weather, lighting, occlusions
- System-level failures: integration, timing, fallback
- Human factors: over-reliance, mode confusion

**Visualizations:**
- Timeline of Uber crash events
- Failure taxonomy tree diagram
- Sensor field-of-view limitations
- Comparative analysis of incidents

---

### Notebook 8: Out-of-Distribution Detection
**File:** `08_OOD_Detection.ipynb`

**Content:**
- **OOD problem definition:** In-distribution vs out-of-distribution
- **Detection methods:**
  - **Mahalanobis distance-based:** Statistical distance in feature space
  - **Energy-based detection:** Energy score from neural network
  - **OpenMax:** Open-set recognition with extreme value theory
  - **Uncertainty-based:** Monte Carlo Dropout, ensembles
- **Implementation:** Code examples for each method
- **Performance metrics:** AUROC, FPR@95, detection accuracy
- **Visualizations:** Feature space projections, score distributions
- **Safety implications:** Connection to ISO 21448 SOTIF
- **Real-world examples:** Novel objects, unusual scenarios

**Key Concepts:**
- Closed-set vs open-set recognition
- Known unknowns (edge cases) vs unknown unknowns
- Confidence calibration
- Safety monitoring and fallback strategies

**Code Implementation:**
```python
# Example: Mahalanobis distance OOD detector
ood_detector = MahalanobisOOD(model, train_data)
score = ood_detector.compute_score(test_image)
is_ood = score > threshold
```

**Exercises:**
- Implement OOD detector for KITTI dataset
- Compare different OOD methods
- Analyze false positive/negative cases
- Design safety response for OOD detections

---

### Notebook 9: Corner Cases and Edge Cases
**File:** `09_Corner_Cases_and_Edge_Cases.ipynb`

**Content:**
- **Definitions:**
  - **Edge case:** Boundary of ODD (e.g., max speed, weather limit)
  - **Corner case:** Rare combination of conditions (e.g., wet road + sunset glare + cyclist)
- **Long-tail distribution:** 80-20 rule in autonomous driving
  - 80% of miles: Common scenarios
  - 20% of miles: 80% of safety-critical events
- **Examples from real deployments:**
  - Unusual weather: Sandstorms, heavy fog, snow
  - Rare objects: Overturned truck, animals, debris
  - Infrastructure edge cases: Missing lane markings, construction zones
- **Scenario generation:** Simulation-based testing
- **Coverage analysis:** How to measure test completeness
- **Campus shuttle case study:** Identify corner cases for university deployment

**Key Concepts:**
- Scenario taxonomy
- Operational Design Domain (ODD) boundaries
- Test coverage metrics
- Simulation vs real-world testing

**Visualizations:**
- Long-tail distribution plot
- Corner case scenario matrix
- Coverage heat maps
- Example challenging images

**Interactive Exercise:**
- Given campus shuttle ODD, identify potential corner cases
- Prioritize by risk (likelihood × severity)
- Propose mitigation strategies

---

### Notebook 10: Adversarial Attacks on Perception
**File:** `10_Adversarial_Attacks_on_Perception.ipynb`

**Content:**
- **Adversarial examples explained:** Small perturbations cause misclassification
- **Digital attacks (white-box):**
  - **FGSM (Fast Gradient Sign Method):** Single-step attack
  - **PGD (Projected Gradient Descent):** Iterative attack
  - **C&W attack:** Optimization-based
- **Physical attacks:**
  - **Adversarial patches on stop signs:** Misclassify as speed limit
  - **Adversarial stickers on road signs**
  - **Adversarial eyeglass frames:** Evade face recognition
- **Sensor spoofing:**
  - **LiDAR spoofing:** Inject phantom obstacles
  - **Camera blinding:** Laser attacks
  - **GPS spoofing:** Location manipulation
- **Defense mechanisms:**
  - **Adversarial training:** Train on adversarial examples
  - **Input validation:** Detect anomalous inputs
  - **Ensemble methods:** Multiple models vote
  - **Certified defenses:** Provable robustness bounds
- **Connection to ISO/SAE 21434:** Cybersecurity standard for road vehicles
- **Code demonstrations:** Generate and defend against attacks

**Key Concepts:**
- Threat modeling for AVs
- Attack surface analysis
- Security vs safety trade-offs
- Certification challenges

**Code Implementation:**
```python
# FGSM attack example
epsilon = 0.03
perturbed_image = fgsm_attack(image, epsilon, model, target_class)

# Adversarial training defense
model = adversarial_training(model, train_data, attack_method=PGD)
```

**Visualizations:**
- Original vs adversarial image (imperceptible difference)
- Adversarial patch on stop sign
- Attack success rate vs epsilon
- Defense effectiveness comparison

**Exercises:**
- Generate FGSM attack on traffic sign classifier
- Evaluate model robustness
- Implement input validation defense
- Analyze physical attack feasibility

---

## 🧪 Exercises

### Exercise 3: OOD Detection System Design
**File:** `exercises/Exercise_3_OOD_Detection.md`

**Scenario:** Design an OOD detector for a Level 4 autonomous shuttle operating on a university campus.

**Tasks:**
1. Define in-distribution scenarios (training data)
2. Identify potential OOD scenarios
3. Select appropriate OOD detection method(s)
4. Implement and test on sample data
5. Define safety response protocol for OOD detections
6. Estimate performance requirements (AUROC, FPR)

**Learning Goals:**
- Apply OOD detection to real scenario
- Understand trade-offs between methods
- Connect to safety requirements

---

### Exercise 4: Adversarial Robustness Evaluation
**File:** `exercises/Exercise_4_Adversarial_Robustness.md`

**Scenario:** Evaluate robustness of a pedestrian detection system to adversarial attacks.

**Tasks:**
1. Implement FGSM and PGD attacks
2. Measure attack success rate vs perturbation strength
3. Test adversarial training defense
4. Analyze physical attack feasibility
5. Propose additional defenses
6. Document security requirements (per ISO/SAE 21434)

**Learning Goals:**
- Hands-on adversarial attack generation
- Understand attack-defense arms race
- Apply cybersecurity thinking to AVs

---

## 📖 Resources

### NTSB Reports
- [Uber ATG Crash Report (2018)](https://www.ntsb.gov/investigations/accidentreports/pages/hwy18mh010.aspx)
- [Tesla Autopilot Crashes](https://www.ntsb.gov/investigations/pages/tesla.aspx)

### Research Papers
- **OOD Detection:**
  - Hendrycks & Gimpel (2017) - "A Baseline for Detecting Misclassified and OOD Examples"
  - Lee et al. (2018) - "A Simple Unified Framework for Detecting OOD Examples"
- **Adversarial Robustness:**
  - Goodfellow et al. (2014) - "Explaining and Harnessing Adversarial Examples"
  - Madry et al. (2018) - "Towards Deep Learning Models Resistant to Adversarial Attacks"
  - Eykholt et al. (2018) - "Robust Physical-World Attacks on Deep Learning Visual Classification"

### Standards & Guidelines
- **ISO 21448:2022** - Safety Of The Intended Functionality (SOTIF)
- **ISO/SAE 21434:2021** - Road vehicles — Cybersecurity engineering

See `resources/links.md` for complete list.

---

## 🔗 Connection to Other Sessions

### Session 1: AI Perception Systems
- **Built on:** Object detection, sensor modalities, datasets
- **Extends to:** Understanding when and why systems fail

### Session 3: Safety Standards & Verification
- **Prepares for:** Applying ISO 26262, SOTIF, ISO 21448
- **Connection:** Failure modes inform safety requirements

### Session 4: Uncertainty Estimation
- **Leads to:** Quantifying uncertainty for safer decisions
- **Connection:** OOD detection is form of uncertainty estimation

---

## ⏱️ Time Management

**Suggested schedule for 90-minute session:**

| Time | Activity | Materials |
|------|----------|-----------|
| 0-5 min | Review Session 1, introduce Session 2 | Slides |
| 5-25 min | AV failure case studies | Notebook 7 |
| 25-50 min | OOD detection methods | Notebook 8 |
| 50-70 min | Corner cases and edge cases | Notebook 9 |
| 70-88 min | Adversarial attacks and defenses | Notebook 10 |
| 88-90 min | Wrap-up, preview Session 3 | Slides |

**Flexibility:** Adjust based on audience pace. Priority: Notebooks 7, 8, 10.

---

## 🎯 Learning Outcomes Assessment

After completing Session 2, you should be able to:

- [ ] Explain root causes of major AV accidents (Uber, Tesla, Cruise)
- [ ] Implement at least one OOD detection method
- [ ] Identify corner cases for a given ODD
- [ ] Generate adversarial examples using FGSM or PGD
- [ ] Describe defenses against adversarial attacks
- [ ] Connect failure modes to ISO 21448 and ISO/SAE 21434

**Self-check:** Complete exercises and reflect on safety implications.

---

## 💡 Tips for Success

1. **Think critically** - Don't just run code, understand why failures occur
2. **Safety mindset** - Always consider "what could go wrong?"
3. **Real-world focus** - Connect concepts to actual AV deployments
4. **Experimentation** - Try edge cases, break the system intentionally
5. **Standards awareness** - Keep ISO 21448 and 21434 in mind
6. **Ethical considerations** - AV failures have real human consequences

---

## 📧 Questions or Issues?

- **During workshop:** Ask instructor
- **After workshop:** Open GitHub issue
- **Technical problems:** Check `setup_instructions.md`

---

**Ready to understand why AV systems fail? Start with Notebook 7!**

```bash
jupyter lab notebooks/07_AV_Failure_Case_Studies.ipynb
```

---

*Last updated: 2025-01-18*
