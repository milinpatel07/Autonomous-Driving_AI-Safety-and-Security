# Module 06 · AI Safety (ISO/PAS 8800)

Making machine-learning components trustworthy enough for a safety argument: the AI-safety standards, uncertainty and its decomposition, ensembles, calibration and conformal guarantees on real detections, explainability, the safety of end-to-end and foundation-model driving, and statistical validation.

**8 notebooks** · each runs in Google Colab on CPU; real-data notebooks download the frames and records they need on demand.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [AI Safety Standards for Automated Driving: ISO/PAS 8800 and Related Standards](01_ai_safety_standards.ipynb) | Intermediate | ISO/PAS 8800:2024, ISO/IEC TR 5469:2024, ISO/TS 5083:2025, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb) |
| 02 | [Uncertainty Types in Deep Learning](02_uncertainty_types.ipynb) | Intermediate | ISO 21448:2022, ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/02_uncertainty_types.ipynb) |
| 03 | [Monte Carlo Dropout and Deep Ensembles](03_mc_dropout_and_deep_ensembles.ipynb) | Intermediate | ISO/PAS 8800:2024, ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/03_mc_dropout_and_deep_ensembles.ipynb) |
| 04 | [Calibration and Reliability of Classifier Confidence](04_calibration.ipynb) | Intermediate | ISO/PAS 8800:2024, ISO 21448:2022 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/04_calibration.ipynb) |
| 05 | [Conformal Prediction: Distribution-Free Uncertainty Guarantees](05_conformal_prediction.ipynb) | Intermediate/Advanced | ISO/PAS 8800:2024, ISO 21448:2022 (SOTIF) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/05_conformal_prediction.ipynb) |
| 06 | [Explainability (XAI) for Perception: Methods, Sanity Checks and Limits as Safety Evidence](06_explainability.ipynb) | Intermediate | ISO/PAS 8800:2024, ISO/IEC TR 5469:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb) |
| 07 | [End-to-End and Foundation-Model Driving: What Changes for Safety](07_end_to_end_and_foundation_models.ipynb) | Advanced | ISO/PAS 8800:2024, ISO 21448:2022, ISO/TS 5083:2025, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb) |
| 08 | [Statistical Safety Validation of ML-Based Perception and Automated Driving](08_statistical_safety_validation.ipynb) | Intermediate | ISO 21448:2022, ISO/PAS 8800:2024, ISO 34502:2022, ISO/TS 5083:2025, UL 4600 (3rd ed., 2023) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb) |

## What you will learn

### 01 · AI Safety Standards for Automated Driving: ISO/PAS 8800 and Related Standards

- Explain why machine-learning (ML) components need safety guidance beyond ISO 26262 and ISO 21448.
- Describe the scope and structure of **ISO/PAS 8800:2024** *Road vehicles — Safety and artificial intelligence*: AI safety lifecycle, AI system / AI component / AI model, AI safety requirements, data-related considerations, verification and validation, safety analysis, assurance argument, and measures during operation.
- Draw a sharp boundary between ISO 26262 (E/E malfunctions), ISO 21448 (functional insufficiencies and triggering conditions) and ISO/PAS 8800 (AI-specific insufficiencies and errors).
- Place the surrounding documents correctly: ISO/IEC TR 5469, ISO/IEC 22989, ISO/IEC 42001, ISO/IEC 5259, ISO/TS 5083, UL 4600 and the EU AI Act.
- Turn data-quality wishes into **verifiable dataset requirements** derived from the ODD and the AI safety requirements.
- Explain why field monitoring of an ML component relies on label-free proxies plus periodic labelled audits.

### 02 · Uncertainty Types in Deep Learning

- Distinguish **aleatoric** (data) and **epistemic** (model/knowledge) uncertainty, and know their limits as concepts.
- Use the two standard decompositions consistently:
- classification: *total predictive entropy = expected entropy (aleatoric) + mutual information (epistemic)*;
- regression: *total variance = mean predicted variance (aleatoric) + variance of the predicted means (epistemic)* (law of total variance).
- Compute both decompositions from an ensemble on a toy problem with a data gap.
- Identify sources of uncertainty in AV perception and connect them to ISO 21448 and ISO/PAS 8800.
- Sketch an uncertainty-aware decision rule and explain why its thresholds must be validated.

### 03 · Monte Carlo Dropout and Deep Ensembles

- Implement **Monte Carlo (MC) dropout** correctly: dropout active at test time, *every other layer (e.g. BatchNorm) in evaluation mode*.
- Implement a **deep ensemble** and compute the entropy / mutual-information decomposition from both methods.
- Evaluate uncertainty properly: accuracy, NLL and Brier score on a **held-out in-distribution (ID) test set**, and OOD detection with **AUROC** and **FPR at 95 % TPR** on near and far OOD sets.
- Recognise the limits: ReLU networks can stay confident far from the data, so uncertainty is not a guaranteed OOD detector.
- Measure the inference cost honestly (warm-up, repeated timing, batched sampling).

### 04 · Calibration and Reliability of Classifier Confidence

- Define calibration precisely (top-label confidence vs observed accuracy).
- Measure it with a **reliability diagram**, **expected calibration error (ECE)** and the proper scoring rules **NLL** and **Brier score**, each with a **bootstrap confidence interval**.
- Fit **temperature scaling** correctly (minimise validation NLL over $T>0$), plus Platt scaling and isotonic regression, using a strict train / validation / test protocol.
- Explain what calibration does and does not change (accuracy, ranking, thresholded decisions).
- Use calibrated probabilities for **expected-cost decisions** and see how calibration degrades under **distribution shift**.
- Measure and recalibrate the confidence of a **real object detector on KITTI images**: state the matching rule, use a frame-level bootstrap, analyse slices, and relate the result to the AEB safety goals.

### 05 · Conformal Prediction: Distribution-Free Uncertainty Guarantees

- State the finite-sample coverage guarantee of **split conformal prediction** and explain why it is *distribution-free* and needs only **exchangeability**, not a correct model.
- Build prediction **sets** for classification with two score functions — **LAC** (least-ambiguous, one minus the softmax probability of a class) and **APS** (adaptive) — and compare their set sizes.
- Build prediction **intervals** for regression with **conformalised quantile regression (CQR)** and read them as a time-to-collision estimate.
- Verify empirical coverage over many random splits, and see where **conditional** (class-wise) coverage fails — motivating **Mondrian/class-conditional** conformal.
- Show that **distribution shift breaks exchangeability** with a synthetic "fog" shift, and recover coverage with **weighted** and **adaptive (ACI)** conformal prediction.
- Connect prediction-set *size* to a conservative safety behaviour and to a **SOTIF / ISO/PAS 8800** assurance argument.
- Conformalise a **real monocular distance estimate** on KITTI labels, check coverage per distance band and per class (Mondrian), and see coverage collapse for occluded and truncated objects.

### 06 · Explainability (XAI) for Perception: Methods, Sanity Checks and Limits as Safety Evidence

- Understand where explainability supports safety work: debugging, safety analysis of AI errors, incident investigation and communication; and where it does not.
- Implement **gradient saliency**, **Grad-CAM**, **integrated gradients**, **occlusion sensitivity** and **Shapley values** from scratch on a small CNN, and state precisely what each one computes.
- Check the **additivity** property of Shapley values ($f(x) = \phi_0 + \sum_i\phi_i$) and the **completeness** property of integrated gradients numerically.
- Run the **model-randomisation sanity check** (Adebayo et al., 2018) and a localisation check against known object masks.
- Use XAI to uncover a **shortcut** (a spurious feature) that a test-set accuracy figure would hide.
- Explain detections of a **real object detector on KITTI images** (pedestrian and car) with gradient saliency, Grad-CAM and whole-detector occlusion, and run the randomisation sanity check on it.
- Explain why post-hoc explanations are, at best, supporting evidence in an ISO/PAS 8800 assurance argument.

### 07 · End-to-End and Foundation-Model Driving: What Changes for Safety

- Distinguish **modular**, **monolithic end-to-end**, **modular end-to-end**, **vision-language(-action)** and **world-model** approaches to automated driving, using verified and dated examples.
- Explain the safety-relevant failure modes these approaches add or sharpen: **compounding error under covariate shift**, **causal confusion**, **shortcut learning**, **distribution shift**, **hallucination** and the **loss of intermediate interfaces** for monitoring.
- Train a small **imitation-learning driving policy** on real lead-vehicle speed profiles from NGSIM and **demonstrate** behaviour-cloning failure, its repair with **DAgger**, and **causal confusion** from a nuisance input.
- Wrap a learned policy with an **RSS-based runtime shield** and a lateral **Simplex** monitor, and quantify what it fixes and what it cannot.
- State what evidence **ISO/PAS 8800**, **ISO 21448** and **UL 4600** would require for a learned driving policy, and name the main open problems as of October 2026.

### 08 · Statistical Safety Validation of ML-Based Perception and Automated Driving

- Explain why "drive until it is safe" does not work, and reproduce the **RAND "Driving to Safety"** numbers exactly.
- Distinguish **functional, logical and concrete scenarios** (Menzel et al., 2018) from the **PEGASUS 6-layer model** of scenario content (Scholtes et al., 2021).
- Measure **parameter-space coverage** correctly, and explain why coverage is not residual-risk evidence.
- Compute **zero-failure demonstration bounds**, **exact Poisson confidence intervals** and the miles needed for a **superiority test with power**.
- Choose safety-relevant perception metrics and turn acceptance criteria into statistically meaningful statements.
- Describe **safety performance indicators (SPIs)** and **shadow mode** as operation-phase evidence.

---

← [Module 05 · Cybersecurity (ISO/SAE 21434)](../05_Cybersecurity_ISO21434/README.md) · [Course home](../README.md) · [Module 07 · Runtime Assurance and Operations](../07_Runtime_Assurance_and_Operations/README.md) →
