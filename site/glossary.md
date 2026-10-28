---
title: Glossary
---

Short working definitions. Where a standard defines the term, the definition paraphrases it; consult the standard for the normative wording.

ADS — Automated driving system
: Hardware and software that together perform the entire dynamic driving task on a sustained basis (SAE J3016 Levels 3–5).

ASIL — Automotive Safety Integrity Level
: One of four levels (A lowest … D highest) specifying the item's necessary requirements of ISO 26262 and safety measures to avoid unreasonable residual risk. Determined from severity, exposure and controllability in the HARA. "QM" means no ASIL is required.

ASIL decomposition
: Splitting a safety requirement into redundant requirements implemented by sufficiently independent elements, each with a lower ASIL, written e.g. B(D) + B(D) (ISO 26262-9).

Attack feasibility
: The ease of successfully carrying out an attack path, rated High / Medium / Low / Very Low (ISO/SAE 21434), e.g. from attack potential, attack vector or CVSS exploitability.

CAL — Cybersecurity Assurance Level
: A level (CAL 1–4) expressing the rigour of assurance activities for a cybersecurity goal (ISO/SAE 21434, informative Annex E). Not a risk value.

Calibration
: Agreement between predicted confidence and observed accuracy; measured e.g. with expected calibration error (ECE) and reliability diagrams.

Conformal prediction
: A distribution-free method that turns any model's scores into prediction sets or intervals with a guaranteed finite-sample coverage rate, provided the data are exchangeable.

Controllability (C)
: The ability to avoid the specified harm by timely reactions of the persons involved (driver or other traffic participants), rated C0–C3 in a HARA.

DDT — Dynamic driving task
: The real-time operational and tactical functions required to operate a vehicle in on-road traffic (SAE J3016).

Epistemic / aleatoric uncertainty
: Uncertainty due to limited knowledge or data (reducible) versus inherent randomness or noise in the observations (irreducible).

Exposure (E)
: The probability of the operational situation in which a hazardous event can occur, rated E0–E4 by duration or frequency.

FMEA / FMEDA
: Failure Mode and Effects (and Diagnostic) Analysis: an inductive analysis of how components fail and what that causes; FMEDA adds failure rates and diagnostic coverage to compute ISO 26262 hardware metrics.

FTA — Fault tree analysis
: A deductive analysis that decomposes an undesired top event into combinations of basic events through logic gates.

FTTI — Fault tolerant time interval
: Minimum time span from the occurrence of a fault to a possible hazardous event if the safety mechanisms are not activated (ISO 26262-1).

Functional insufficiency
: An insufficiency of specification or a performance insufficiency of the intended functionality that can contribute to a hazardous behaviour when triggered (ISO 21448).

GSN — Goal Structuring Notation
: A graphical notation for safety arguments using goals (claims), strategies, solutions (evidence), context, assumptions and justifications.

HARA — Hazard analysis and risk assessment
: The ISO 26262-3 method to identify and categorise hazardous events of an item and derive safety goals with ASILs.

MRC / MRM — Minimal risk condition / manoeuvre
: The stable, stopped (or otherwise low-risk) state an ADS brings the vehicle to when the trip cannot or should not continue, and the manoeuvre that achieves it.

ODD — Operational design domain
: The operating conditions under which a driving automation system is specifically designed to function (SAE J3016); taxonomy in ISO 34503.

OOD — Out-of-distribution
: Inputs that differ from the distribution the model was trained on; detecting them is a key runtime safety measure for ML.

PMHF — Probabilistic metric for random hardware failures
: The average probability per hour of violating a safety goal due to random hardware failures (ISO 26262-5); targets e.g. < 10⁻⁸ /h for ASIL D.

RSS — Responsibility-Sensitive Safety
: A formal model (Shalev-Shwartz et al., 2017) defining safe distances and proper responses so that an AV never causes a collision under stated assumptions.

Safety case
: A structured argument, supported by evidence, that a system is acceptably safe for a given application in a given environment.

Safety goal
: A top-level safety requirement resulting from the HARA, at vehicle level, with an ASIL (ISO 26262).

SOTIF — Safety of the intended functionality
: The absence of unreasonable risk due to hazards resulting from functional insufficiencies of the intended functionality or from reasonably foreseeable misuse (ISO 21448).

SPFM / LFM
: Single-point fault metric and latent fault metric: ISO 26262-5 hardware architectural metrics with ASIL-dependent targets (e.g. ≥ 99 % and ≥ 90 % for ASIL D).

SPI — Safety performance indicator
: A metric used to monitor and validate the claims of a safety case during operation (UL 4600).

TARA — Threat analysis and risk assessment
: The ISO/SAE 21434 clause 15 method: assets and damage scenarios → threat scenarios → impact → attack paths → feasibility → risk value → risk treatment.

Triggering condition
: A specific condition of a scenario that initiates a subsequent system reaction contributing to hazardous behaviour or to reasonably foreseeable misuse (ISO 21448).

TTC — Time to collision
: The time until two road users collide if they keep their current speeds and paths.
