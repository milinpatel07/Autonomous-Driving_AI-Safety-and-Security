# Glossary of Technical Terms

**Comprehensive terminology reference for autonomous driving, AI safety, and functional safety standards**

**Last Updated:** 2025-12-04
**Version:** 2.0.0

---

## Table of Contents

- [Autonomous Driving](#autonomous-driving)
- [Perception and Sensors](#perception-and-sensors)
- [LiDAR Technology](#lidar-technology)
- [Functional Safety (ISO 26262)](#functional-safety-iso-26262)
- [SOTIF (ISO 21448)](#sotif-iso-21448)
- [Cybersecurity (ISO/SAE 21434)](#cybersecurity-isosae-21434)
- [AI and Machine Learning](#ai-and-machine-learning)
- [Uncertainty Quantification](#uncertainty-quantification)
- [Validation and Verification](#validation-and-verification)
- [Standards and Regulations](#standards-and-regulations)

---

## Autonomous Driving

### ADAS
**Advanced Driver Assistance Systems** - Electronic systems that assist drivers in driving and parking functions using automated technology, such as sensors and cameras. Examples: adaptive cruise control, lane keeping assist, automatic emergency braking.

### AV
**Autonomous Vehicle** - A vehicle capable of sensing its environment and operating without human input. Also called self-driving car, driverless car, or robo-car.

### MRC
**Minimal Risk Condition** - A condition to which a driving automation system may bring a vehicle to reduce the risk of a crash when a given trip cannot or should not be completed (SAE J3016).

### ODD
**Operational Design Domain** - The specific conditions under which a given driving automation system or feature is designed to function (SAE J3016). Includes:
- Geographic area
- Roadway types (highway, urban, rural)
- Speed range
- Environmental conditions (weather, lighting)
- Traffic conditions

### SAE Levels (J3016)
**Levels of Driving Automation** - Six-level classification system (0-5) defining the degree of automation:
- **Level 0**: No automation (human driver performs all tasks)
- **Level 1**: Driver assistance (either steering OR brake/acceleration)
- **Level 2**: Partial automation (both steering AND brake/acceleration)
- **Level 3**: Conditional automation (system drives, human ready to intervene)
- **Level 4**: High automation (system drives, no human intervention within ODD)
- **Level 5**: Full automation (system drives under all conditions)

---

## Perception and Sensors

### Sensor Fusion
The combination of sensory data from multiple sources (camera, LiDAR, radar, GNSS) to produce more accurate, complete, and reliable information than any individual sensor. Types:
- **Early fusion**: Combine raw sensor data
- **Late fusion**: Combine detection results
- **Deep fusion**: Neural networks learn optimal fusion strategy

### Camera
Vision sensor capturing 2D images using photodiodes (CCD or CMOS). Provides high resolution, color information, and texture. Limitations: affected by lighting, weather, lacks direct depth information.

### Radar
**Radio Detection and Ranging** - Sensor using radio waves (typically 24 GHz, 77 GHz) to measure distance and velocity via Doppler effect. Advantages: works in fog/rain, measures velocity directly. Limitations: low resolution, cannot detect stationary objects well.

### GNSS
**Global Navigation Satellite System** - Satellite-based positioning system (GPS, Galileo, GLONASS, BeiDou) providing location and time. Accuracy: 1-5m typical, <10cm with RTK correction.

### IMU
**Inertial Measurement Unit** - Sensor measuring acceleration (accelerometers) and angular velocity (gyroscopes) in 3 axes. Used for dead reckoning and sensor fusion.

### Odometry
Estimation of position change over time from sensor data (wheel encoders, visual odometry, LiDAR odometry).

---

## LiDAR Technology

### LiDAR
**Light Detection and Ranging** - Remote sensing technology that measures distance by illuminating targets with laser light and analyzing the reflected signal. Typical wavelengths: 905nm, 1550nm.

### Point Cloud
3D representation of space as a collection of data points (x, y, z), each representing a surface reflection point. May include intensity (I), color (RGB), or other attributes.

### ToF
**Time-of-Flight** - Distance measurement method based on the round-trip time of a laser pulse. Distance = (c × Δt) / 2, where c = speed of light, Δt = travel time.

### Mechanical Scanning LiDAR
LiDAR system with rotating components (entire sensor or internal mirror) to scan the environment. Examples: Velodyne HDL-64E (360° horizontal FOV, 64 channels).

### Solid-State LiDAR
LiDAR system with no moving mechanical parts, using electronic beam steering (flash, MEMS, optical phased array). Advantages: higher reliability, smaller size, lower cost potential.

### FOV
**Field of View** - Angular extent observable by sensor. For LiDAR:
- **Horizontal FOV**: Azimuth range (e.g., 360° for spinning, 120° for solid-state)
- **Vertical FOV**: Elevation range (e.g., 26.9° for Velodyne HDL-64E)

### 3D Bounding Box
Oriented rectangular cuboid enclosing an object in 3D space. Parameterized by:
- **Position**: (x, y, z) center coordinates
- **Dimensions**: (l, w, h) length, width, height
- **Orientation**: (θ) yaw angle (sometimes pitch, roll)

### Occlusion
Blockage of sensor view by intervening objects. Types:
- **Partial occlusion**: Part of object visible
- **Complete occlusion**: Object entirely hidden
- **Self-occlusion**: Object blocks itself (e.g., vehicle body blocking LiDAR FOV)

### Semantic Segmentation
Pixel-wise (2D) or point-wise (3D) classification assigning each element to a class (car, pedestrian, road, vegetation). All pixels/points of same class treated equally.

### Instance Segmentation
Extension of semantic segmentation that differentiates individual instances within the same class (car #1, car #2). Each object has unique ID.

### Panoptic Segmentation
Unified segmentation combining semantic (stuff classes: road, sky) and instance (thing classes: cars, pedestrians) segmentation.

### Ghost Points
Spurious LiDAR returns caused by:
- **Multi-path reflections**: Laser bounces off multiple surfaces
- **Environmental particles**: Rain droplets, fog, dust, snow
- **Sensor artifacts**: Crosstalk between channels, timing errors

### IoU
**Intersection over Union** - Overlap metric for bounding boxes or segmentation masks. IoU = (Area of Overlap) / (Area of Union). Range: [0, 1], higher is better. Typical threshold: 0.5 for "match".

---

## Functional Safety (ISO 26262)

### ISO 26262
International standard for functional safety of electrical/electronic (E/E) systems in road vehicles. Addresses random hardware failures and systematic faults. Current version: ISO 26262:2018 (12 parts).

### Functional Safety
Absence of unreasonable risk due to hazards caused by malfunctioning behavior of E/E systems. Distinguished from:
- **Nominal performance** (SOTIF addresses)
- **Security** (ISO/SAE 21434 addresses)

### ASIL
**Automotive Safety Integrity Level** - Risk classification scheme (ASIL A, B, C, D) based on severity, exposure, controllability. ASIL D is highest integrity requirement.

### Safety Goal
Top-level safety requirement derived from hazard analysis. Allocated an ASIL. Example: "Prevent unintended acceleration (ASIL D)".

### HARA
**Hazard Analysis and Risk Assessment** - Systematic identification of hazards, analysis of scenarios, and assignment of ASIL. Inputs: vehicle functions, malfunctions, operational situations.

### Severity
Classification of consequences of a hazardous event:
- **S0**: No injuries
- **S1**: Light/moderate injuries
- **S2**: Severe/life-threatening injuries (survival probable)
- **S3**: Life-threatening/fatal injuries (survival uncertain)

### Exposure
Probability of operational situation (driving scenario) in which hazard could occur:
- **E0**: Incredible (<0.1% of operating time)
- **E1**: Very low probability (0.1%-1%)
- **E2**: Low probability (1%-10%)
- **E3**: Medium probability (10%-50%)
- **E4**: High probability (>50%)

### Controllability
Ability of driver or other persons to control a hazard:
- **C0**: Controllable in general
- **C1**: Simple to control
- **C2**: Normally controllable
- **C3**: Difficult to control or uncontrollable

### V-Model
Development process model in ISO 26262 showing correspondence between development phases (left side: requirements → design → implementation) and testing phases (right side: unit test → integration test → system test).

### Safety Mechanism
Technical solution to detect or control faults. Examples: watchdogs, redundancy, plausibility checks, range checks.

### Diagnostic Coverage
Measure of effectiveness of diagnostic mechanisms in detecting faults. Expressed as percentage. Higher ASIL requires higher diagnostic coverage.

### Fail-Safe
System design ensuring safety when failure occurs. For AVs: transition to MRC (minimal risk condition) when fault detected.

### Fail-Operational
System continues to operate safely even with faults (graceful degradation). Required for ASIL D functions without immediate safe state.

---

## SOTIF (ISO 21448)

### ISO 21448 (SOTIF)
**Safety Of The Intended Functionality** - Standard addressing risks from performance limitations and misuse of intended functionality. Complements ISO 26262. Published: June 2022.

### Known Safe
Scenarios in which the system has been verified to operate safely.

### Known Unsafe
Scenarios identified as hazardous. Require mitigation (redesign, warnings, ODD restriction).

### Unknown Safe
Scenarios not yet evaluated but where system would operate safely. Validation aims to maximize this space.

### Unknown Unsafe
Scenarios not yet identified where system may be unsafe (residual risk). Validation aims to discover and minimize.

### Triggering Condition
Specific condition or combination of conditions that triggers performance limitation. Examples:
- Environmental: fog reduces LiDAR range
- Scenario: construction zone with unusual lane markings
- Input: adversarial perturbation

### Performance Limitation
Functional insufficiency in intended behavior. Sources:
- **Sensor limitations**: Occlusions, range limits, weather sensitivity
- **Algorithm limitations**: False positives/negatives, OOD scenarios
- **Specification insufficiencies**: Incomplete requirements

### Specification Insufficiency
Incomplete or incorrect specification of intended functionality. Example: specification doesn't address behavior when both lanes occluded.

### Verification
Confirmation through objective evidence that specified requirements are fulfilled. Answers: "Are we building the system right?"

### Validation
Confirmation that the system meets user needs and is fit for purpose. Answers: "Are we building the right system?"

---

## Cybersecurity (ISO/SAE 21434)

### ISO/SAE 21434
International standard for cybersecurity engineering in road vehicles. Addresses intentional malicious attacks. Published: August 2021. Developed jointly by ISO and SAE.

### TARA
**Threat Analysis and Risk Assessment** - Systematic process to identify assets, threats, attack paths, and determine cybersecurity risk. Outputs: cybersecurity goals, requirements.

### Asset
Element with value requiring protection. Types:
- Safety-critical functions (steering, braking)
- Data (personal, operational, cryptographic keys)
- Software/firmware
- Communication channels

### Threat Agent
Entity capable of initiating threat:
- **Script kiddie**: Low skill, uses existing tools
- **Hacker**: Skilled individual, custom exploits
- **Organized crime**: Resources, financial motivation
- **Nation-state**: Extensive resources, strategic goals

### Attack Path
Sequence of steps attacker takes from entry point to achieving damage scenario. May involve multiple vulnerabilities.

### Attack Feasibility
Likelihood of successful attack based on:
- **Elapsed time**: Effort required (<1 month to >6 months)
- **Specialist expertise**: Layman to expert
- **Knowledge of item**: Public to confidential
- **Window of opportunity**: Seconds to unlimited
- **Equipment**: Standard to bespoke

### CAL
**Cybersecurity Assurance Level** - Similar to ASIL for cybersecurity. Levels: CAL-1 (basic) to CAL-4 (extensive). Determines rigor of security measures.

### Attack Vector
Path or means by which attacker gains unauthorized access. Examples:
- Physical: OBD-II port, USB, JTAG debug
- Wireless: WiFi, Bluetooth, cellular, V2X
- Remote: Cloud APIs, OTA update server

### Defense in Depth
Layered security approach using multiple independent security controls. If one layer fails, others still provide protection.

---

## AI and Machine Learning

### Deep Learning
Subset of machine learning using neural networks with multiple layers (deep architectures). Learns hierarchical feature representations from data.

### CNN
**Convolutional Neural Network** - Neural network architecture using convolution operations. Dominant for computer vision tasks (image classification, object detection, segmentation).

### Object Detection
Computer vision task identifying and localizing objects in images/point clouds. Outputs: class labels and bounding boxes. Architectures: YOLO, R-CNN, SSD.

### IoU (Detection)
Intersection over Union for bounding box overlap. Used as metric for detection accuracy and as threshold for matching predictions to ground truth.

### mAP
**Mean Average Precision** - Standard metric for object detection. Averages AP (Average Precision) across all classes. Computed at various IoU thresholds (e.g., mAP@0.5, mAP@0.5:0.95).

### Precision
Of all predicted positives, what fraction are correct? Precision = TP / (TP + FP). High precision = few false alarms.

### Recall
Of all actual positives, what fraction are detected? Recall = TP / (TP + FN). High recall = few misses.

### False Positive (FP)
Incorrectly detected object (phantom detection). Safety implication: unnecessary braking, conservative behavior.

### False Negative (FN)
Missed object detection. Safety implication: collision risk. More critical than false positives for safety.

### Overfitting
Model memorizes training data, performs poorly on unseen data. Causes: too many parameters, insufficient data, no regularization.

### Regularization
Techniques preventing overfitting: L1/L2 regularization, dropout, data augmentation, early stopping.

### Hyperparameter
Configuration parameter not learned from data. Examples: learning rate, batch size, number of layers, dropout rate.

---

## Uncertainty Quantification

### Aleatoric Uncertainty
**Data uncertainty** - Irreducible uncertainty from noisy observations. Sources: sensor noise, occlusions, ambiguous situations. Cannot be reduced by more training data.

### Epistemic Uncertainty
**Model uncertainty** - Reducible uncertainty from lack of knowledge. Sources: insufficient training data, model capacity. Reducible by more training data or better models.

### MC Dropout
**Monte Carlo Dropout** - Uncertainty estimation method applying dropout at test time. Run multiple stochastic forward passes, measure prediction variance. Estimates epistemic uncertainty.

### Deep Ensembles
Uncertainty estimation by training multiple independent models. Aggregate predictions, measure disagreement. State-of-the-art uncertainty quantification.

### Bayesian Neural Network (BNN)
Neural network with probability distributions over weights (instead of point estimates). Principled uncertainty quantification but computationally expensive.

### Calibration
Alignment between predicted confidence and actual accuracy. Well-calibrated model: if it predicts 80% confidence, it's correct 80% of the time.

### ECE
**Expected Calibration Error** - Quantitative metric for calibration quality. ECE = weighted average of |confidence - accuracy| across confidence bins. Range: [0, 1], lower is better.

### Temperature Scaling
Post-hoc calibration method dividing logits by temperature parameter T before softmax. Optimized on validation set. Improves calibration without affecting accuracy.

---

## Validation and Verification

### Scenario
Description of temporal development between several scenes. Includes actors, road network, environmental conditions. Types:
- **Concrete**: Specific instance with exact parameters
- **Functional**: Abstract description with parameter ranges
- **Logical**: High-level conceptual scenario

### Corner Case
Rare scenario at the edge of operational domain. Difficult to test comprehensively. Examples: unusual pedestrian behavior, construction zones, edge cases in sensor coverage.

### Edge Case
Scenario at boundary conditions of sensor or algorithm capabilities. Examples: maximum detection range, minimum object size, extreme lighting.

### OOD
**Out-of-Distribution** - Input significantly different from training data distribution. Neural networks produce unreliable predictions on OOD inputs. Detection methods: Mahalanobis distance, energy-based, deep ensembles.

### Adversarial Example
Input intentionally perturbed to cause model misclassification. Types:
- **Digital**: Pixel-level perturbations (FGSM, PGD)
- **Physical**: Real-world attacks (adversarial patches on stop signs)

### Simulation-Based Testing
Validation using high-fidelity simulators (CARLA, SUMO, Gazebo). Advantages: safety, repeatability, rare scenario generation. Limitations: sim-to-real gap.

### X-in-the-Loop Testing
Validation at different integration levels:
- **SIL**: Software-in-the-Loop (pure software)
- **HIL**: Hardware-in-the-Loop (real ECUs, simulated vehicle)
- **VIL**: Vehicle-in-the-Loop (real vehicle, virtual environment)
- **DIL**: Driver-in-the-Loop (human driver in simulator)

### FOT
**Field Operational Test** - Real-world testing with instrumented vehicles and safety drivers. Provides statistical evidence of safety but requires millions of test miles.

---

## Standards and Regulations

### UNECE WP.29
United Nations Economic Commission for Europe - Working Party on road vehicle regulations. Develops international vehicle regulations including:
- **R155**: Cybersecurity management system (2021)
- **R156**: Software update management system (2021)

### EU AI Act
European Union regulation on artificial intelligence (2024). Risk-based approach:
- **Unacceptable risk**: Prohibited (e.g., social scoring)
- **High risk**: Strict requirements (includes autonomous driving)
- **Limited/minimal risk**: Transparency obligations

### Type Approval
Regulatory certification that vehicle meets applicable standards before market introduction. Required in EU, harmonized internationally via UNECE.

### Homologation
European term for type approval. Vehicle model certified to meet regulatory requirements.

---

## Acronyms

- **AD**: Autonomous Driving
- **ADAS**: Advanced Driver Assistance Systems
- **AP**: Average Precision
- **ASIL**: Automotive Safety Integrity Level
- **AV**: Autonomous Vehicle
- **BNN**: Bayesian Neural Network
- **CAL**: Cybersecurity Assurance Level
- **CAN**: Controller Area Network
- **CNN**: Convolutional Neural Network
- **CV**: Computer Vision
- **DIL**: Driver-in-the-Loop
- **DL**: Deep Learning
- **ECE**: Expected Calibration Error
- **ECU**: Electronic Control Unit
- **FGSM**: Fast Gradient Sign Method
- **FOT**: Field Operational Test
- **FOV**: Field of View
- **FP**: False Positive
- **FN**: False Negative
- **GNSS**: Global Navigation Satellite System
- **HARA**: Hazard Analysis and Risk Assessment
- **HIL**: Hardware-in-the-Loop
- **HSM**: Hardware Security Module
- **IMU**: Inertial Measurement Unit
- **IoU**: Intersection over Union
- **LiDAR**: Light Detection and Ranging
- **mAP**: Mean Average Precision
- **MC**: Monte Carlo
- **MEMS**: Micro-Electro-Mechanical Systems
- **ML**: Machine Learning
- **MRC**: Minimal Risk Condition
- **ODD**: Operational Design Domain
- **OOD**: Out-of-Distribution
- **OPA**: Optical Phased Array
- **OTA**: Over-the-Air
- **PGD**: Projected Gradient Descent
- **SIL**: Software-in-the-Loop
- **SOTIF**: Safety Of The Intended Functionality
- **TARA**: Threat Analysis and Risk Assessment
- **ToF**: Time-of-Flight
- **V2X**: Vehicle-to-Everything (V2V, V2I, V2P, V2N)
- **VIL**: Vehicle-in-the-Loop

---

**End of Glossary**

For detailed explanations, see relevant module documentation and notebooks.
