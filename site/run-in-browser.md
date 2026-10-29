---
title: Run in your browser
description: Course notebooks that run entirely in the web browser, with no account, installation or server.
---

Every notebook with an **Open in browser** link below runs **entirely in your web browser**: no account, no
installation, no server.
Python runs inside the browser tab ([Pyodide](https://pyodide.org), Python compiled to WebAssembly) in a
[JupyterLite](https://jupyterlite.readthedocs.io) notebook interface. This works where Google Colab is blocked
or a Google login is not an option, for example on some company networks.

**How to start:** open a notebook from the table below and choose **Run → Run All Cells**. The first visit
loads the Python runtime and the scientific packages (up to about 60 MB, which your browser caches); later
visits start in a few seconds. The course toolkit `avsafety` is installed from this website, not from GitHub or PyPI.

**Privacy:** your code, your inputs and your results stay on your device. Notebooks you edit are saved in
this browser's local storage only; use **File → Download** to keep a copy, and clear the site data in your
browser to remove them. Apart from the two notebooks marked "downloads NGSIM data", which fetch
public vehicle trajectories from the US DOT open-data portal (data.transportation.gov), the notebooks make no
network request outside this website; the automated test of the browser edition fails if one does.

**Limitations**

- Notebooks that train or run neural networks need PyTorch, which has no WebAssembly build; they stay on
  [Google Colab](https://colab.research.google.com) or a local Jupyter installation (see the
  [toolkit page](toolkit.md)).
- The KITTI and NHTSA crash-report servers do not permit downloads from web pages hosted elsewhere
  (cross-origin requests; checked October 2026), so notebooks that need these datasets stay on Colab.
- Python in the browser is single-threaded and slower than a native installation (two to four times
  slower in our tests); most notebooks run in 10 to 30 seconds, the slowest in about one and a half minutes.
- Once all cells of a notebook have run, it keeps working without a network connection until you close the
  tab; opening it again offline depends on your browser's cache.

<!-- lite-notebooks:start -->

| Notebook | Runs in the browser |
|---|---|
| 01-01 SAE Levels of Driving Automation and the Operational Design Domain | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=01_Perception/01_sae_levels_and_odd.ipynb) |
| 01-02 Sensor Modalities: Camera, LiDAR and Radar | No: KITTI data cannot be downloaded from a browser |
| 01-03 LiDAR Sensors and Point Clouds | No: KITTI data cannot be downloaded from a browser |
| 01-04 Object Detection on Real Driving Images: from IoU to Per-Class AP on KITTI | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 01-05 Vulnerable Road User Detection on Real Data: Recall, Range and AEB | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 01-06 Sensor Fusion: Calibration, Association and Late Fusion | No: needs PyTorch |
| 01-07 Multi-Object Tracking and State Estimation | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 01-08 Driving Datasets: What KITTI Really Contains, and How to Specify Data for Safety | No: KITTI data cannot be downloaded from a browser |
| 01-09 Trajectory Prediction on Real Highway Data | No: needs PyTorch |
| 02-01 Real-World Incident Case Studies | No: NHTSA crash-report data cannot be downloaded from a browser |
| 02-02 Corner Cases and Edge Cases | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 02-03 Out-of-Distribution (OOD) Detection: Methods and Evaluation | No: needs PyTorch |
| 02-04 Adversarial Attacks on Perception | No: needs PyTorch |
| 03-01 ISO 26262: Functional Safety for Road Vehicles | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb) |
| 03-02 Hazard Analysis and Risk Assessment (HARA) | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/02_hara.ipynb) |
| 03-03 FMEA and FMEDA for Perception Hardware and Software | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) |
| 03-04 Fault Tree Analysis (FTA) and Dependent Failures | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb) |
| 03-05 STPA: System-Theoretic Process Analysis | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 03-06 Verification and Validation for Functional Safety | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| 04-01 ISO 21448: Safety of the Intended Functionality (SOTIF) | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| 04-02 Triggering Conditions and Scenario-Based Evaluation | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 04-03 OOD Monitoring as a SOTIF Safety Measure | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 04-04 Simulation-Based SOTIF Validation | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=04_SOTIF_ISO21448/04_simulation_based_validation.ipynb) |
| 04-05 Criticality Metrics and Responsibility-Sensitive Safety (RSS) | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb) |
| 04-06 An Open SOTIF Perception Benchmark | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 05-01 ISO/SAE 21434: Automotive Cybersecurity Engineering | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 05-02 Threat Analysis and Risk Assessment (TARA) | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=05_Cybersecurity_ISO21434/02_tara.ipynb) |
| 05-03 Attack Surface Analysis for Autonomous Vehicles | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| 05-04 CAN Bus Security and Intrusion Detection | No: downloads from zenodo.org via avsafety.data.can_ids() (cross-origin access not checked) |
| 05-05 V2X Misbehaviour Detection | No: downloads from zenodo.org via avsafety.data.veremi() (cross-origin access not checked) |
| 06-01 AI Safety Standards for Automated Driving: ISO/PAS 8800 and Related Standards | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb) |
| 06-02 Uncertainty Types in Deep Learning | No: needs PyTorch |
| 06-03 Monte Carlo Dropout and Deep Ensembles | No: needs PyTorch |
| 06-04 Calibration and Reliability of Classifier Confidence | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 06-05 Conformal Prediction: Distribution-Free Uncertainty Guarantees | No: KITTI data cannot be downloaded from a browser |
| 06-06 Explainability (XAI) for Perception: Methods, Sanity Checks and Limits as Safety Evidence | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 06-07 End-to-End and Foundation-Model Driving: What Changes for Safety | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb) · downloads NGSIM data |
| 06-08 Statistical Safety Validation of ML-Based Perception and Automated Driving | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb) |
| 07-01 ODD Specification and Runtime Monitoring | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 07-02 Safe Motion Planning and Fallback | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb) · downloads NGSIM data |
| 07-03 Human Factors: Supervision, Takeover and Misuse | No: downloads data directly, which the browser edition does not support |
| 07-04 V2X and Cooperative Driving | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb) |
| 07-05 Field Safety Monitoring with Real Crash Reports | No: NHTSA crash-report data cannot be downloaded from a browser |
| 07-06 Industry Deployment: Status, Evidence and Operations | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb) |
| 08-01 Standards Integration: How ISO 26262, ISO 21448, ISO/SAE 21434 and ISO/PAS 8800 Work Together | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb) |
| 08-02 Automotive Regulation and Type Approval for Automated Driving | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 08-03 Standards Gaps and Open Problems in AV Safety | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb) |
| 08-04 Safety Cases and Goal Structuring Notation (GSN) | [Open in browser](https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/lite/notebooks/index.html?path=08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb) |
| 08-05 Capstone: Pedestrian AEB from Requirement to Release Decision | No: needs PyTorch; KITTI data cannot be downloaded from a browser |
| 08-06 Continuous Assurance: A Safety Case That Updates Itself | No: downloads data directly, which the browser edition does not support |

<!-- lite-notebooks:end -->
