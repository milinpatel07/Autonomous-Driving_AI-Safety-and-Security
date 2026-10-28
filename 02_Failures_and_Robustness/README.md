# Module 02 · Failures and Robustness

What goes wrong in the real world and why: documented incidents and their investigations, corner cases, out-of-distribution inputs and adversarial attacks on perception.

**4 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Time | Open |
|---|---|---|---|---|
| 01 | [Real-World Incident Case Studies](01_incident_case_studies.ipynb) | Beginner | ~75 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/02_Failures_and_Robustness/01_incident_case_studies.ipynb) |
| 02 | [Corner Cases and Edge Cases](02_corner_cases.ipynb) | Beginner | ~70 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/02_Failures_and_Robustness/02_corner_cases.ipynb) |
| 03 | [Out-of-Distribution (OOD) Detection: Methods and Evaluation](03_out_of_distribution_detection.ipynb) | Intermediate | ~80 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/02_Failures_and_Robustness/03_out_of_distribution_detection.ipynb) |
| 04 | [Adversarial Attacks on Perception](04_adversarial_attacks.ipynb) | Intermediate | ~85 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/02_Failures_and_Robustness/04_adversarial_attacks.ipynb) |

## What you will learn

### 01 · Real-World Incident Case Studies

*Standards:* SAE J3016 (2021), ISO 21448:2022 (context)

- Read an official investigation report (NTSB, NHTSA) and separate *probable cause*, *contributing factors* and press claims
- Reconstruct the Uber ATG Tempe crash (2018) from the NTSB's recorded perception timeline
- Explain the documented findings of the Tesla Williston (2016), Mountain View (2018) and Spring (2021) investigations, including a widely repeated myth
- Describe the Cruise San Francisco incident (2023) and its regulatory consequences
- Classify perception-related failures with a taxonomy that keeps ISO 26262, ISO 21448, ISO/PAS 8800 and ISO/SAE 21434 apart
- Apply root-cause analysis (5 Whys, fishbone) and derive design lessons

### 02 · Corner Cases and Edge Cases

*Standards:* ISO 21448:2022, ISO 34502:2022, ISO 34503:2023

- Distinguish edge cases from corner cases, and the test-engineering from the perception (ML) usage of "corner case"
- Explain the long-tail problem and why rare scenarios matter for validation effort
- Identify and organise corner cases using corner-case levels and the ISO 34502 disturbance categories
- Quantify combinatorial explosion and reduce it with pairwise (combinatorial) testing
- Separate in-ODD corner cases from ODD-exit conditions and prioritise testing consistently
- Relate corner cases to ISO 21448 triggering conditions and functional insufficiencies

### 03 · Out-of-Distribution (OOD) Detection: Methods and Evaluation

*Standards:* ISO 21448:2022, ISO/PAS 8800:2024 (context)

- Explain the OOD problem, and distinguish covariate from semantic shift and near- from far-OOD
- Implement five post-hoc OOD scores: maximum softmax probability (MSP), ODIN, energy, class-conditional Mahalanobis and k-nearest-neighbour (k-NN) distance
- Evaluate detectors correctly with AUROC and FPR at 95% TPR, stating the convention used
- Select hyperparameters and thresholds without touching the test set, and report the realised operating point
- Interpret the limits of OOD detection as a safety measure

### 04 · Adversarial Attacks on Perception

*Standards:* ISO/SAE 21434:2021, UN R155; ISO 21448:2022 (scope boundary)

- Define adversarial examples, threat models and perturbation budgets (with units)
- Implement FGSM and PGD correctly (true labels, clipping, projection, random start) and measure attack success versus budget on a trained model
- Explain physical attacks (adversarial patches) and sensor attacks on cameras, LiDAR and multi-sensor fusion, with their primary sources
- Evaluate defences honestly: adversarial training, input squeezing and the need for adaptive attacks
- Place adversarial robustness in ISO/SAE 21434 TARA terminology and separate it from ISO 21448

---

← [Module 01 · Perception Systems](../01_Perception/README.md) · [Course home](../README.md) · [Module 03 · Functional Safety (ISO 26262)](../03_Functional_Safety_ISO26262/README.md) →
