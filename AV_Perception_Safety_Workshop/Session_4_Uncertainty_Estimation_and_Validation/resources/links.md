# Resources: Uncertainty Estimation and Validation for AV Perception

**Session 4 Reference Materials**

---

## 📚 Key Papers

### Uncertainty Quantification

#### Monte Carlo Dropout
- **Gal & Ghahramani (2016)** - "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"
  - https://arxiv.org/abs/1506.02142
  - 📌 Foundational paper on MC Dropout

- **Kendall & Gal (2017)** - "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
  - https://arxiv.org/abs/1703.04977
  - 📌 Aleatoric vs Epistemic uncertainty decomposition

#### Deep Ensembles
- **Lakshminarayanan et al. (2017)** - "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
  - https://arxiv.org/abs/1612.01474
  - 📌 State-of-the-art ensemble method

#### Bayesian Neural Networks
- **Blundell et al. (2015)** - "Weight Uncertainty in Neural Networks"
  - https://arxiv.org/abs/1505.05424
  - 📌 Bayes by Backprop

- **Graves (2011)** - "Practical Variational Inference for Neural Networks"
  - https://papers.nips.cc/paper/4329-practical-variational-inference-for-neural-networks.pdf
  - 📌 Variational inference for BNNs

#### Evidential Deep Learning
- **Sensoy et al. (2018)** - "Evidential Deep Learning to Quantify Classification Uncertainty"
  - https://arxiv.org/abs/1806.01768
  - 📌 Single forward pass uncertainty

---

### Model Calibration

- **Guo et al. (2017)** - "On Calibration of Modern Neural Networks"
  - https://arxiv.org/abs/1706.04599
  - 📌 Temperature scaling and calibration analysis

- **Naeini et al. (2015)** - "Obtaining Well Calibrated Probabilities Using Bayesian Binning"
  - https://arxiv.org/abs/1411.1135

- **Platt (1999)** - "Probabilistic Outputs for Support Vector Machines"
  - https://www.researchgate.net/publication/2594015_Probabilistic_Outputs_for_Support_Vector_Machines
  - 📌 Original Platt scaling

- **Nixon et al. (2019)** - "Measuring Calibration in Deep Learning"
  - https://arxiv.org/abs/1904.01685

---

### AV-Specific Uncertainty

- **Miller et al. (2019)** - "Evaluating Model Robustness and Uncertainty for Autonomous Vehicles"
  - https://arxiv.org/abs/1905.11929
  - 📌 Uncertainty for AV perception

- **Feng et al. (2018)** - "Deep Multi-Modal Object Detection and Semantic Segmentation for Autonomous Driving"
  - https://arxiv.org/abs/1809.02188

- **Michelmore et al. (2018)** - "Uncertainty Quantification with Statistical Guarantees in End-to-End Autonomous Driving Control"
  - https://arxiv.org/abs/1810.01014

- **McAllister et al. (2017)** - "Concrete Problems for Autonomous Vehicle Safety"
  - https://arxiv.org/abs/1711.03558
  - 📌 Safety challenges and uncertainty

---

### Validation and Testing

#### Statistical Validation
- **Kalra & Paddock (2016)** - "Driving to Safety: How Many Miles of Driving Would It Take to Demonstrate Autonomous Vehicle Reliability?"
  - https://www.rand.org/pubs/research_reports/RR1478.html
  - 📌 The famous "billion miles" paper

- **Zhao et al. (2016)** - "Accelerated Evaluation of Automated Vehicles"
  - https://arxiv.org/abs/1609.01764

#### Scenario-Based Testing
- **Menzel et al. (2018)** - "Scenarios for Development, Test and Validation of Automated Vehicles"
  - https://ieeexplore.ieee.org/document/8500406
  - 📌 Pegasus 6-layer scenario model

- **Ulbrich et al. (2015)** - "Defining and Substantiating the Terms Scene, Situation, and Scenario for Automated Driving"
  - https://ieeexplore.ieee.org/document/7225830

- **Althoff et al. (2018)** - "Automatic Generation of Safety-Critical Test Scenarios for Collision Avoidance of Road Vehicles"
  - https://arxiv.org/abs/1809.07184

#### Simulation-Based Validation
- **Fremont et al. (2019)** - "Scenic: A Language for Scenario Specification and Scene Generation"
  - https://arxiv.org/abs/1809.09310
  - 📌 Scenario specification language

- **Dosovitskiy et al. (2017)** - "CARLA: An Open Urban Driving Simulator"
  - https://arxiv.org/abs/1711.03938
  - 📌 CARLA simulator

---

## 🛠️ Tools and Libraries

### Uncertainty Quantification

#### Python Libraries
- **Uncertainty Toolbox**
  - https://github.com/uncertainty-toolbox/uncertainty-toolbox
  - Comprehensive uncertainty analysis toolkit

- **TensorFlow Probability**
  - https://www.tensorflow.org/probability
  - Bayesian deep learning in TensorFlow

- **Pyro (PyTorch)**
  - https://pyro.ai/
  - Probabilistic programming and Bayesian inference

- **Edward2 (TensorFlow)**
  - https://github.com/google/edward2
  - Probabilistic modeling

- **NetCal**
  - https://github.com/fabiankueppers/calibration-framework
  - Calibration framework for neural networks

#### Bayesian Tools
- **GPyTorch**
  - https://gpytorch.ai/
  - Gaussian Processes in PyTorch

- **BayesOpt**
  - https://github.com/rmcantin/bayesopt
  - Bayesian optimization

### Simulators

#### Open-Source Simulators
- **CARLA**
  - https://carla.org/
  - 📌 Most popular open-source AV simulator

- **SUMO**
  - https://eclipse.dev/sumo/
  - Traffic simulation platform

- **SUMMIT**
  - https://github.com/AdaCompNUS/summit
  - Multi-agent simulation

#### Commercial Simulators
- **IPG CarMaker**
  - https://ipg-automotive.com/products-solutions/software/carmaker/

- **dSPACE**
  - https://www.dspace.com/en/inc/home/products/sw/simulation_and_validation.cfm

- **ANSYS**
  - https://www.ansys.com/products/systems/ansys-avxcelerate

### Scenario Tools

- **OpenSCENARIO**
  - https://www.asam.net/standards/detail/openscenario/
  - Standard format for scenario description

- **Scenic**
  - https://github.com/BerkeleyLearnVerify/Scenic
  - Probabilistic scenario specification

- **CommonRoad**
  - https://commonroad.in.tum.de/
  - Benchmark scenarios

---

## 📖 Standards and Guidelines

### ISO Standards

#### ISO 26262 - Functional Safety
- **ISO 26262-1:2018** - Vocabulary
- **ISO 26262-6:2018** - Product development at the software level
- **ISO 26262-8:2018** - Supporting processes (Validation)
  - 📌 Section 8.4.2: Validation of safety requirements
- **ISO 26262-10:2018** - Guideline on ISO 26262

Resources:
- Overview: https://www.iso.org/standard/68383.html
- Tutorial: https://www.ni.com/en-us/innovations/white-papers/11/overview-of-iso-26262.html

#### ISO 21448 - SOTIF (Safety of the Intended Functionality)
- **ISO/PAS 21448:2019** - Road vehicles — Safety of the intended functionality
  - 📌 Critical for ML-based perception systems
  - Addresses performance limitations and unknown scenarios

Resources:
- Overview: https://www.iso.org/standard/70939.html
- Explanation: https://www.sae.org/standards/content/iso/pas21448/

#### ISO/TR 4804
- **ISO/TR 4804:2020** - Road vehicles — Safety and cybersecurity for automated driving systems

### SAE Standards

- **SAE J3016** - Taxonomy of Driving Automation
  - https://www.sae.org/standards/content/j3016_202104/

- **SAE J3018** - Guidelines for Safe On-Road Testing
  - https://www.sae.org/standards/content/j3018_201812/

### Other Guidelines

- **UL 4600** - Standard for Safety for the Evaluation of Autonomous Products
  - https://ul.org/UL4600
  - 📌 Comprehensive AV safety standard

- **NHTSA AV Testing Framework**
  - https://www.nhtsa.gov/automated-vehicles-safety

- **Euro NCAP AEB Test Protocol**
  - https://www.euroncap.com/en/vehicle-safety/safety-campaigns/2018-automated-emergency-braking/

---

## 📊 Datasets

### For Uncertainty Evaluation

#### Corruption Benchmarks
- **ImageNet-C**
  - https://github.com/hendrycks/robustness
  - Common corruptions benchmark

- **COCO-C**
  - Apply ImageNet-C corruptions to COCO for object detection

#### Out-of-Distribution Detection
- **nuScenes-C**
  - https://github.com/kxhit/nuScenes-C
  - Corruptions for autonomous driving

- **Shifts Dataset**
  - https://github.com/yandex-research/shifts
  - Real-world distribution shifts

#### AV Datasets with Edge Cases
- **nuScenes**
  - https://www.nuscenes.org/
  - Diverse weather, lighting conditions

- **Waymo Open Dataset**
  - https://waymo.com/open/
  - Large-scale, diverse scenarios

- **CADC** (Canadian Adverse Driving Conditions)
  - https://cadcd.uwaterloo.ca/
  - Snow, ice, adverse weather

- **Dense Dataset**
  - https://www.uni-ulm.de/in/driveu/projects/dense-dataset/
  - Adverse weather (rain, fog, snow)

---

## 🎓 Courses and Tutorials

### Online Courses

- **Deep Learning Specialization (Coursera)** - Andrew Ng
  - https://www.coursera.org/specializations/deep-learning
  - Includes Bayesian basics

- **Probabilistic Machine Learning** - Philipp Hennig
  - https://uni-tuebingen.de/en/faculties/faculty-of-science/departments/computer-science/lehrstuehle/methods-of-machine-learning/probabilistic-machine-learning/

- **Autonomous Vehicles Specialization** (Coursera) - University of Toronto
  - https://www.coursera.org/specializations/self-driving-cars
  - Module on safety and testing

### Video Lectures

- **Uncertainty in Deep Learning** - Yarin Gal
  - https://www.youtube.com/watch?v=HumFmLu3CJ8

- **Calibration in Machine Learning** - Chuan Guo
  - https://www.youtube.com/watch?v=fCmFMdYoD0I

### Tutorials

- **Bayesian Deep Learning Tutorial**
  - http://bayesiandeeplearning.org/

- **Uncertainty Toolbox Tutorial**
  - https://uncertainty-toolbox.github.io/

---

## 📝 Technical Reports and White Papers

### Industry Reports

- **Waymo Safety Report (2020)**
  - https://waymo.com/safety/
  - 📌 Industry best practice

- **Tesla Autopilot Safety Report**
  - https://www.tesla.com/VehicleSafetyReport

- **Cruise Safety Report**
  - https://getcruise.com/safety/

### Research Projects

- **Pegasus Project**
  - https://www.pegasusprojekt.de/en/
  - 📌 German research on AV validation

- **ENABLE-S3**
  - https://www.enable-s3.eu/
  - European automated driving validation

- **L3Pilot**
  - https://www.l3pilot.eu/
  - Large-scale automated driving pilot

---

## 🔧 Code Examples and Repositories

### Uncertainty Quantification Examples

- **Simple and Scalable Uncertainty Estimation**
  - https://github.com/google-research/google-research/tree/master/uq_benchmark_2019

- **Deep Ensembles Implementation**
  - https://github.com/axelbrando/Mixture-of-Neural-Networks

- **MC Dropout Examples**
  - https://github.com/yaringal/DropoutUncertaintyExps

### AV Perception Examples

- **YOLOv8 with Uncertainty**
  - https://github.com/ultralytics/ultralytics
  - (Add custom uncertainty wrapper)

- **MMDetection**
  - https://github.com/open-mmlab/mmdetection
  - Rich object detection framework

### Validation Tools

- **Scenic Examples**
  - https://github.com/BerkeleyLearnVerify/Scenic/tree/main/examples

- **CARLA Scenarios**
  - https://github.com/carla-simulator/scenario_runner

---

## 🌐 Communities and Forums

### Research Communities

- **BayesianDeepLearning.org**
  - http://bayesiandeeplearning.org/

- **ICML Workshop on Uncertainty & Robustness**
  - Annual workshop

- **NeurIPS Probabilistic ML**
  - https://neurips.cc/

### Industry Forums

- **Autonomous Vehicle Safety Consortium**
  - https://avsc.bsi-group.com/

- **SAE Automated Driving Standards**
  - https://www.sae.org/standards/content/j3016_202104/

---

## 📧 Contact and Support

For questions about Session 4 materials:
- GitHub Issues: (Your workshop repo)
- Discussion Forum: (Your workshop forum)

---

## 🔄 Updates

This resource list is maintained and updated regularly. Last updated: 2024-01-15

**Contributions welcome!** Submit a PR if you find useful resources.

---

## ⭐ Recommended Reading Path

**For beginners:**
1. Guo et al. (2017) - Calibration
2. Gal & Ghahramani (2016) - MC Dropout
3. Lakshminarayanan et al. (2017) - Ensembles

**For AV practitioners:**
1. Miller et al. (2019) - AV Uncertainty
2. Kalra & Paddock (2016) - Validation requirements
3. Menzel et al. (2018) - Scenario-based testing
4. ISO 21448 - SOTIF standard

**For researchers:**
1. Kendall & Gal (2017) - Uncertainty decomposition
2. Sensoy et al. (2018) - Evidential learning
3. Fremont et al. (2019) - Scenic specification
4. Full Bayesian approaches

---

**Happy learning! Stay safe on the road to autonomous driving! 🚗🤖**
