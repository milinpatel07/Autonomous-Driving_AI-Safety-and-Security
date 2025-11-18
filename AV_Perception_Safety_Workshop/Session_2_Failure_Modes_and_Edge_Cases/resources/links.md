# Session 2 Resources: Failure Modes and Edge Cases

This document contains links to reports, papers, datasets, tools, and standards relevant to Session 2.

---

## Official Accident Investigation Reports

### NTSB Reports (National Transportation Safety Board)

**Uber ATG Tempe Crash (2018)**
- Full Report: https://www.ntsb.gov/investigations/accidentreports/pages/hwy18mh010.aspx
- Summary: https://www.ntsb.gov/news/press-releases/Pages/NR20191119.aspx
- Report Number: HWY18MH010
- Date: March 18, 2018
- Key Finding: Classification instability, disabled emergency braking, safety driver inattention

**Tesla Autopilot Crashes**
- Florida 2016: https://www.ntsb.gov/investigations/Pages/HWY16FH018.aspx
- Mountain View 2018: https://www.ntsb.gov/investigations/Pages/HWY18FH011.aspx
- Tesla Investigations List: https://www.ntsb.gov/investigations/Pages/tesla.aspx

**General AV Incidents**
- NTSB AV Investigations: https://www.ntsb.gov/investigations/Pages/av.aspx

### California DMV Reports

**Cruise SF Incident (2023)**
- DMV Suspension Order: https://www.dmv.ca.gov/portal/news-and-media/dmv-suspends-cruise-driverless-deployment-and-drivered-testing-permits/
- Analysis: https://techcrunch.com/2023/10/24/california-dmv-suspends-cruises-driverless-autonomous-vehicle-permits/

**Autonomous Vehicle Disengagement Reports**
- Annual Reports: https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/disengagement-reports/
- Analysis by Company: Waymo, Cruise, Zoox, etc.

---

## Research Papers

### Out-of-Distribution Detection

**Foundational Papers**

1. **Hendrycks & Gimpel (2017)** - "A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks"
   - Link: https://arxiv.org/abs/1610.02136
   - GitHub: https://github.com/hendrycks/error-detection

2. **Liang et al. (2018)** - "Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks"
   - Link: https://arxiv.org/abs/1706.02690
   - ODIN method (temperature scaling + input perturbation)

3. **Lee et al. (2018)** - "A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks"
   - Link: https://arxiv.org/abs/1807.03888
   - Mahalanobis distance-based detection
   - GitHub: https://github.com/pokaxpoka/deep_Mahalanobis_detector

4. **Liu et al. (2020)** - "Energy-based Out-of-distribution Detection"
   - Link: https://arxiv.org/abs/2010.03759
   - Energy function for OOD detection
   - GitHub: https://github.com/wetliu/energy_ood

5. **Hein et al. (2019)** - "Why ReLU Networks Yield High-Confidence Predictions Far Away From the Training Data"
   - Link: https://arxiv.org/abs/1812.05720
   - Theoretical analysis of overconfidence

**Advanced Methods**

6. **Bendale & Boult (2016)** - "Towards Open Set Deep Networks"
   - Link: https://arxiv.org/abs/1511.06233
   - OpenMax for open-set recognition

7. **Gal & Ghahramani (2016)** - "Dropout as a Bayesian Approximation"
   - Link: https://arxiv.org/abs/1506.02142
   - Monte Carlo Dropout for uncertainty

8. **Lakshminarayanan et al. (2017)** - "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
   - Link: https://arxiv.org/abs/1612.01474
   - Ensemble methods for uncertainty

**OOD Benchmarks**

9. **Hendrycks et al. (2021)** - "Natural Adversarial Examples"
   - Link: https://arxiv.org/abs/2019.01451
   - ImageNet-A dataset (natural adversarial examples)

10. **Hendrycks et al. (2019)** - "Benchmarking Neural Network Robustness to Common Corruptions and Perturbations"
    - Link: https://arxiv.org/abs/1903.12261
    - ImageNet-C dataset

---

### Adversarial Robustness

**Foundational Papers**

11. **Szegedy et al. (2013)** - "Intriguing properties of neural networks"
    - Link: https://arxiv.org/abs/1312.6199
    - First adversarial examples paper

12. **Goodfellow et al. (2014)** - "Explaining and Harnessing Adversarial Examples"
    - Link: https://arxiv.org/abs/1412.6572
    - Fast Gradient Sign Method (FGSM)

13. **Madry et al. (2018)** - "Towards Deep Learning Models Resistant to Adversarial Attacks"
    - Link: https://arxiv.org/abs/1706.06083
    - PGD attack and adversarial training
    - GitHub: https://github.com/MadryLab/cifar10_challenge

14. **Carlini & Wagner (2017)** - "Towards Evaluating the Robustness of Neural Networks"
    - Link: https://arxiv.org/abs/1608.04644
    - C&W attack (optimization-based)
    - GitHub: https://github.com/carlini/nn_robust_attacks

**Physical Adversarial Attacks**

15. **Kurakin et al. (2016)** - "Adversarial examples in the physical world"
    - Link: https://arxiv.org/abs/1607.02533
    - Printed adversarial examples

16. **Eykholt et al. (2018)** - "Robust Physical-World Attacks on Deep Learning Visual Classification"
    - Link: https://arxiv.org/abs/1707.08945
    - Adversarial patches on stop signs
    - GitHub: https://github.com/evtimovi/robust_physical_perturbations

17. **Brown et al. (2017)** - "Adversarial Patch"
    - Link: https://arxiv.org/abs/1712.09665
    - Universal adversarial patches

18. **Athalye et al. (2018)** - "Synthesizing Robust Adversarial Examples"
    - Link: https://arxiv.org/abs/1707.07397
    - EOT (Expectation Over Transformations)

**Defenses**

19. **Papernot et al. (2016)** - "Distillation as a Defense to Adversarial Perturbations"
    - Link: https://arxiv.org/abs/1511.04508
    - Defensive distillation

20. **Samangouei et al. (2018)** - "Defense-GAN: Protecting Classifiers Against Adversarial Attacks Using Generative Models"
    - Link: https://arxiv.org/abs/1805.06605
    - GAN-based defense

21. **Cohen et al. (2019)** - "Certified Adversarial Robustness via Randomized Smoothing"
    - Link: https://arxiv.org/abs/1902.02918
    - Provable robustness guarantees
    - GitHub: https://github.com/locuslab/smoothing

22. **Xie et al. (2019)** - "Feature Denoising for Improving Adversarial Robustness"
    - Link: https://arxiv.org/abs/1812.03411
    - Denoising-based defense

**Sensor Attacks (LiDAR, Camera)**

23. **Cao et al. (2019)** - "Adversarial Sensor Attack on LiDAR-based Perception in Autonomous Driving"
    - Link: https://arxiv.org/abs/1907.06826
    - LiDAR spoofing attacks

24. **Petit et al. (2015)** - "Remote Attacks on Automated Vehicles Sensors"
    - Link: https://www.semanticscholar.org/paper/Remote-Attacks-on-Automated-Vehicles-Sensors-Petit-Stottelaar/
    - Camera, LiDAR, radar attacks

25. **Nassi et al. (2020)** - "Phantom of the ADAS: Securing Advanced Driver-Assistance Systems from Split-Second Phantom Attacks"
    - Link: https://arxiv.org/abs/2006.12152
    - Projector-based attacks on perception

---

### Corner Cases and Long Tail

26. **Breitenstein et al. (2020)** - "Systematically Identifying Confounding Scenarios and Corner Cases"
    - Link: https://arxiv.org/abs/2005.10284

27. **Brostoff et al. (2021)** - "Long-tail Learning for Autonomous Driving"
    - Link: Various sources, search on Google Scholar

28. **Zendel et al. (2018)** - "WildDash - Creating Hazard-Aware Benchmarks"
    - Link: https://arxiv.org/abs/1804.04928
    - Dataset: http://www.wilddash.cc/

29. **Hasirlioglu et al. (2020)** - "Reproducible Fog Simulation for Testing Automotive Surround Sensors"
    - Link: https://ieeexplore.ieee.org/document/9197277

---

## Standards and Guidelines

### ISO/SAE Standards

**ISO 21448:2022 - SOTIF (Safety Of The Intended Functionality)**
- Official: https://www.iso.org/standard/77490.html
- Overview: https://www.iso.org/news/ref2703.html
- Summary: Addresses safety risks from functional insufficiencies and misuse
- Key Concepts: Known/unknown safe/unsafe scenarios, validation, verification

**ISO/SAE 21434:2021 - Cybersecurity Engineering**
- Official: https://www.iso.org/standard/70918.html
- Overview: https://www.sae.org/standards/content/iso/sae21434/
- Summary: Cybersecurity engineering for road vehicles
- Key Concepts: Threat analysis (TARA), security-by-design, incident response

**ISO 26262:2018 - Functional Safety**
- Official: https://www.iso.org/standard/68383.html
- Overview: https://www.iso.org/obp/ui/#iso:std:iso:26262:-1:ed-2:v1:en
- Summary: Electrical/electronic systems safety
- ASIL levels: A, B, C, D (D = highest)

**SAE J3016 - Levels of Driving Automation**
- Official: https://www.sae.org/standards/content/j3016_202104/
- Free summary: https://www.sae.org/news/2019/01/sae-updates-j3016-automated-driving-graphic
- Defines: Levels 0-5 of automation

### Regulatory Guidance

**NHTSA (National Highway Traffic Safety Administration)**
- AV Policy: https://www.nhtsa.gov/vehicle-manufacturers/automated-vehicles-safety
- Voluntary Safety Self-Assessment: https://www.nhtsa.gov/automated-vehicles-safety/voluntary-safety-self-assessment

**European Commission - Type Approval**
- Regulation (EU) 2019/2144: https://eur-lex.europa.eu/eli/reg/2019/2144/oj
- UNECE WP.29 Regulations: https://unece.org/transport/vehicle-regulations

---

## Datasets for Testing

### Autonomous Driving Datasets

**KITTI**
- Website: http://www.cvlibs.net/datasets/kitti/
- Description: Benchmark for stereo, optical flow, visual odometry, 3D object detection
- Size: 15,000+ images, LiDAR, GPS/IMU

**nuScenes**
- Website: https://www.nuscenes.org/
- Description: Full surround view, 1000 scenes, 1.4M images
- Paper: https://arxiv.org/abs/1903.11027

**Waymo Open Dataset**
- Website: https://waymo.com/open/
- Description: 1,000 segments, LiDAR, camera, labels
- Paper: https://arxiv.org/abs/1912.04838

**BDD100K (Berkeley DeepDrive)**
- Website: https://bdd-data.berkeley.edu/
- Description: 100,000 videos, diverse weather/lighting/locations
- Paper: https://arxiv.org/abs/1805.04687

**Cityscapes**
- Website: https://www.cityscapes-dataset.com/
- Description: Urban street scenes, semantic segmentation
- Paper: https://arxiv.org/abs/1604.01685

**ApolloScape**
- Website: http://apolloscape.auto/
- Description: Large-scale, diverse scenarios
- Paper: https://arxiv.org/abs/1803.06184

### Edge Case / Corner Case Datasets

**ImageNet-C (Corruptions)**
- GitHub: https://github.com/hendrycks/robustness
- Description: Common corruptions and perturbations

**ImageNet-A (Adversarial)**
- GitHub: https://github.com/hendrycks/natural-adv-examples
- Description: Natural adversarial examples

**ACDC (Adverse Conditions)**
- Website: https://acdc.vision.ee.ethz.ch/
- Description: Fog, night, rain, snow
- Paper: https://arxiv.org/abs/2104.13395

**WildDash**
- Website: http://www.wilddash.cc/
- Description: Hazard-aware benchmark with unusual scenarios

**nuImages**
- Website: https://www.nuscenes.org/nuimages
- Description: Diverse conditions extension of nuScenes

---

## Tools and Software

### Adversarial Robustness Toolkits

**IBM Adversarial Robustness Toolbox (ART)**
- GitHub: https://github.com/Trusted-AI/adversarial-robustness-toolbox
- Docs: https://adversarial-robustness-toolbox.readthedocs.io/
- Features: Attack, defense, detection methods

**CleverHans**
- GitHub: https://github.com/cleverhans-lab/cleverhans
- Docs: https://cleverhans.readthedocs.io/
- Features: Adversarial attack library (TensorFlow, PyTorch)

**Foolbox**
- GitHub: https://github.com/bethgelab/foolbox
- Docs: https://foolbox.readthedocs.io/
- Features: Adversarial attacks for PyTorch, TensorFlow, JAX

**RobustBench**
- Website: https://robustbench.github.io/
- GitHub: https://github.com/RobustBench/robustbench
- Features: Benchmark and leaderboard for adversarial robustness

### Uncertainty Estimation

**Uncertainty Toolbox**
- GitHub: https://github.com/uncertainty-toolbox/uncertainty-toolbox
- Features: Visualization and metrics for predictive uncertainty

**TensorFlow Probability**
- Website: https://www.tensorflow.org/probability
- Features: Bayesian deep learning, uncertainty quantification

### AV Simulation Platforms

**CARLA**
- Website: http://carla.org/
- GitHub: https://github.com/carla-simulator/carla
- Description: Open-source simulator for autonomous driving

**LGSVL Simulator (SVL)**
- Website: https://www.svlsimulator.com/
- GitHub: https://github.com/lgsvl/simulator
- Description: Unity-based, sensor simulation, ROS integration

**AirSim**
- Website: https://microsoft.github.io/AirSim/
- GitHub: https://github.com/microsoft/AirSim
- Description: Unreal Engine-based, drones and cars

**SUMMIT**
- Paper: https://arxiv.org/abs/2007.04404
- Description: Simulator with focus on rare events

---

## Videos and Talks

### Accident Analysis Videos

**Uber ATG Crash Dashcam Footage**
- Link: https://www.youtube.com/watch?v=R5DUnZdCKlo (Search for official release)
- Warning: Sensitive content

**Tesla Autopilot Incidents Compilation**
- Search: "Tesla Autopilot crash compilation" on YouTube
- Various channels analyze incidents

**Cruise SF Incident Analysis**
- Tech news channels: TechCrunch, The Verge, etc.

### Technical Talks

**Adversarial Examples for Autonomous Driving**
- CVPR, ICCV, NeurIPS workshops
- Search: "Adversarial examples autonomous driving" on YouTube

**SOTIF and Validation**
- SAE Webinars: https://www.sae.org/
- ISO Training: https://www.iso.org/

### Safety Lectures

**MIT 6.S094: Deep Learning for Self-Driving Cars**
- Website: https://selfdrivingcars.mit.edu/
- Lectures on safety, validation, edge cases

**Waymo Safety Report**
- Website: https://waymo.com/safety/
- Detailed methodology for safety validation

---

## Interactive Tools and Demos

**Robustness Gym**
- GitHub: https://github.com/robustness-gym/robustness-gym
- Interactive robustness evaluation

**What-If Tool (Google)**
- Website: https://pair-code.github.io/what-if-tool/
- Visualize model behavior, test counterfactuals

**netron (Model Viewer)**
- Website: https://netron.app/
- Visualize neural network architectures

---

## Organizations and Communities

**NHTSA Automated Vehicles**
- Website: https://www.nhtsa.gov/vehicle-manufacturers/automated-vehicles-safety

**SAE International**
- Website: https://www.sae.org/
- Standards, conferences, training

**ISO Technical Committees**
- ISO/TC 22/SC 32: Electrical and electronic components and systems
- ISO/TC 22/SC 33: Vehicle dynamics and chassis components

**Academic Research Groups**
- UC Berkeley DeepDrive: https://deepdrive.berkeley.edu/
- MIT AgeLab: https://agelab.mit.edu/
- Stanford CARS: https://cars.stanford.edu/
- CMU Robotics Institute: https://www.ri.cmu.edu/

**Industry Consortia**
- Autoware Foundation: https://www.autoware.org/
- Apollo Auto: http://apollo.auto/
- CARLA Community: https://carla.org/

---

## Blogs and News

**Technical Blogs**
- Waymo Blog: https://blog.waymo.com/
- Cruise Medium: https://medium.com/cruise
- Tesla AI Blog: https://www.tesla.com/AI
- Mobileye Blog: https://www.mobileye.com/blog/

**News Outlets (AV Focus)**
- The Robot Report: https://www.therobotreport.com/
- Automotive News: https://www.autonews.com/
- Ars Technica (Autonomous Vehicles): https://arstechnica.com/cars/
- The Verge Transportation: https://www.theverge.com/transportation

---

## Books (Recommended)

1. **"Towards Safe and Reliable AI for Autonomous Vehicles"** - Edited by Philip Koopman
   - Focus on safety validation, testing, standards

2. **"Deep Learning for Autonomous Driving"** - Edited by Raquel Urtasun et al.
   - Technical foundations, perception, planning

3. **"Safety Assurance for Autonomous Vehicles"** - Various authors
   - ISO 26262, SOTIF, V&V methodologies

4. **"Adversarial Robustness for Machine Learning"** - Pin-Yu Chen et al.
   - Theory and practice of adversarial ML

---

## Contact and Support

**For Questions:**
- Open GitHub issues on this repository
- Email instructor: [instructor email]
- Office hours: [schedule]

**For Contributions:**
- Submit pull requests with additional resources
- Share relevant papers, tools, datasets
- Report broken links

---

**Last Updated:** 2025-01-18

**Maintained by:** Milin Patel, Hochschule Kempten

---

## License

This resource list is provided for educational purposes. Links are to publicly available materials. Please respect copyright and licensing terms of linked content.
