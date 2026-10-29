---
title: Normative references
---

The course cites clauses, paragraphs and articles of standards and regulations. Each citation is listed
in [`references/normative.yaml`](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/references/normative.yaml) with what the course states, the edition and the source it was checked against. `scripts/check_references.py` keeps this page in step with the notebooks; do not edit it by hand.

Verification: **official text** = checked against the published text; **official summary** = against
an official table of contents, summary or data dictionary (the full text is paywalled or unavailable);
**secondary** = against a reputable secondary source; **unverified** = not yet checked.

## UN Regulation No. 157 — Automated Lane Keeping Systems (ALKS)

01 series of amendments, E/ECE/TRANS/505/Rev.3/Add.156/Amend.4 (3 March 2023; authentic text ECE/TRANS/WP.29/2022/59/Rev.1; in force 4 January 2023). Source: <https://unece.org/transport/vehicle-regulations-wp29/standards/addenda-1958-agreement-regulations-141-160> (official text, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [04-03](../04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb), [04-05](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [site/glossary.md](glossary.md), [site/industry.md](industry.md), [site/standards-map.md](standards-map.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 2.2 | Definition of the transition demand (request from the system to the driver to take back the DDT). | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 2.7 | Definition of the minimum risk manoeuvre, quoted verbatim. | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 2.9.2 | The maximum operational speed is selected by the system "under current environmental and sensor conditions". | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 5.1.8 | The manufacturer takes measures against reasonably foreseeable misuse by the driver and tampering. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.2.3.1 | Operation up to 130 km/h; a specified maximum speed above 60 km/h only with MRM lane-change capability (01 series). | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 5.4 | Transition demand and system operation during the transition phase (heading). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.4.2.1 | For a planned event, the transition demand comes early enough that an MRM would stop the vehicle before the event. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.4.2.4 | A regular lane change is not started when a transition demand is known to occur during it. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 5.4.3 | The system keeps operating during the transition phase and may reduce speed. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.4.3.2 | The transition demand is escalated at the latest 4 s after it starts (with a haptic warning, 6.4.1(c)). | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.4.4.1 | Without driver response an MRM starts at the earliest 10 s after the start of the transition demand. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.4.4.1.1 | An MRM may start immediately in case of a severe ALKS or vehicle failure. | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 5.5 | Minimum risk manoeuvre (heading); ends in standstill with hazard lights. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.5.1 | The MRM brings the vehicle to standstill in a target stop area, unless the driver deactivates the system (01 series). | official text | — |
| 5.5.2 | During the MRM the vehicle is slowed down aiming at a deceleration demand not greater than 4.0 m/s²; hazard lights at the start of the MRM. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 5.5.3 | An MRM ends only when the system is deactivated or the vehicle is at standstill. | official text | [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb) |
| 5.5.5 | Reactivation after an MRM only after a new engine start/run cycle. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.1 | Driver availability recognition system (presence, belt, availability). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.1.2 | A transition demand starts if the driver is out of the seat for more than 1 s or the belt is unbuckled. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.1.3 | The system detects whether the driver is available to respond to a transition demand. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.1.3.1 | At least two availability criteria within the last 30 s; otherwise a warning and a transition demand at the latest after 15 s; documented justification. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.1.4 | Other activities on on-board displays are suspended at a transition demand or deactivation. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.2 | Activation, deactivation and driver input (heading). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.2.3 | Activation only on deliberate driver action when all listed conditions hold, incl. (g) roads where pedestrians and cyclists are prohibited. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.2.4 | Deliberate deactivation, protected against unintentional action, with the driver in lateral control. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 6.2.5.2 | During a transition demand or MRM, deactivation by taking the steering control only if the driver is attentive (6.3.1.1). | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.2.5.3 | Deactivation during an emergency manoeuvre may be delayed until the collision risk has disappeared. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 6.2.6 | No automatic transition to a function providing continuous longitudinal/lateral control after deactivation; AEBS, ESC, BAS, ESF are not deactivated with the ALKS. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.3 | System override (heading). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.3.1.1 | Driver attentiveness criteria (gaze on road or mirrors, head movement towards the driving task). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.4 | Information to the driver (heading). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.4.1 | Transition demand by optical plus acoustic and/or haptic signal; at the latest after 4 s a haptic warning and escalation (6.4.1(c)). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| 6.4.2.3 | Deactivation is indicated optically, plus an acoustic signal unless it follows a transition demand that had one. | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| 8 | Data Storage System for Automated Driving (DSSAD). | official text | [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb) |
| Annex 3 | Guidance on traffic disturbance critical scenarios (cut-in, cut-out, deceleration) with human-driver performance models. | official text | [04-05](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb) |
| Annex 4 | Special requirements for the safety aspects of electronic control systems and audit (safety concept, field monitoring). | official text | [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Annex 4 3.4.4 | The safety approach "may be based on" FMEA, FTA and STPA "or any similar process" (b); the inspection covers items (i)–(viii), incl. foreseeable misuse (vi) and cyber-attacks (viii). | official text | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| Annex 4 3.5.4 | Processes to monitor safety-relevant incidents caused by the engaged ALKS and to report critical incidents. | official text | [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb) |
| Annex 5 | Test specifications for ALKS. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |

## UN Regulation No. 155 — Cyber security and cyber security management system

Original version, entry into force 22 January 2021 (OJ L 82, 9.3.2021, published as [2021/387]). Source: <https://eur-lex.europa.eu/eli/reg/2021/387/oj> (official text, checked 2026-10-29).

Cited in: [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [site/industry.md](industry.md), [site/standards-map.md](standards-map.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 4.3.1 | Annex 5 Part A groups threats in seven high-level categories, paragraphs 4.3.1–4.3.7. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 7.2.2.2 | Processes the CSMS must contain, items (a)–(h); (g) monitoring, detection and response. | official text | [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 7.2.2.5 | The CSMS manages dependencies on contracted suppliers, service providers and sub-organisations. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 7.3.7 | Measures to detect and prevent cyber-attacks, support monitoring, and provide data forensic capability. | official text | [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) |
| 7.4.1 | Report the outcome of monitoring (7.2.2.2(g)) at least once a year. | official text | [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb) |
| Annex 5 | List of threats and corresponding mitigations. | official text | [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Annex 5 Part A | Vulnerabilities or attack methods related to the threats (Table A1). | official text | [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |

## UN Regulation No. 156 — Software update and software update management system

Original version, entry into force 22 January 2021 (OJ L 82, 9.3.2021, [2021/388]); a 01 series of amendments has since been adopted (globalautoregs.com, as of October 2026). Source: <https://eur-lex.europa.eu/eli/reg/2021/388/oj> (official text, checked 2026-10-29).

Cited in: [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [site/industry.md](industry.md), [site/standards-map.md](standards-map.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

## Regulation (EU) 2024/1689 — Artificial Intelligence Act

OJ L, 12.7.2024; amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI). Source: <https://eur-lex.europa.eu/eli/reg/2024/1689/oj> (official text, checked 2026-10-29).

Cited in: [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Annex I Section B | Annex I Section B lists Union harmonisation legislation incl. Regulations (EU) 2018/858 and 2019/2144; Annex I-linked high-risk obligations apply from 2 August 2028 after Reg. (EU) 2026/1744. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Annex III | Stand-alone high-risk use cases (point 2 covers safety components in road-traffic management, not vehicles); obligations apply from 2 December 2027 after Reg. (EU) 2026/1744. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 2(2) | For high-risk AI under Art. 6(1) and Annex I Section B only listed provisions apply directly; originally Art. 6(1), Arts 102–109 and 112, after Reg. (EU) 2026/1744 Art. 6(1), Art. 60a and Arts 102–112. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 5 | Prohibited AI practices. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 6(1) | AI systems that are safety components of products under Annex I legislation are high-risk. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 9 | Risk management system. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 10 | Data and data governance; data sets "to the best extent possible, free of errors and complete" (Art. 10(3)). | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 11 | Technical documentation. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 12 | Record-keeping (logging). | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 13 | Transparency and provision of information to deployers (instructions for use). | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 14 | Human oversight. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 15 | Accuracy, robustness and cybersecurity. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 50 | Transparency obligations for providers and deployers of certain AI systems. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 60a | Article inserted by Reg. (EU) 2026/1744 (testing in real-world conditions for Annex I Section B products); listed in the amended Art. 2(2). | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 86 | Right to explanation of individual decision-making (deployers of Annex III systems). | official text | [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb) |
| Art. 102-109 | Articles 102–109 amend sectoral acts (including vehicle type-approval acts); Art. 112 is evaluation and review. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 107 | Article 107 amends Regulation (EU) 2018/858 (Art. 5(4)) so that delegated acts on AI safety components take Chapter III Section 2 into account. | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 109 | Article 109 amends Regulation (EU) 2019/2144 (Art. 11(3)) for implementing acts on AI safety components. | official text | [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Chapter III Section 2 | Requirements for high-risk AI systems (Arts 8–15). | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |

## Regulation (EU) 2026/1744 — Digital Omnibus on AI (amends Regulations 2024/1689, 2018/1139, 2023/1230)

Regulation of 8 July 2026, OJ L, 24.7.2026. Source: <https://eur-lex.europa.eu/eli/reg/2026/1744/oj> (official text, checked 2026-10-29).

Cited in: [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Art. 1 | Article 1 amends Regulation (EU) 2024/1689, among others replacing Art. 2(2) and Art. 113 (application dates). | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| Art. 113 | Amended Art. 113 of Regulation (EU) 2024/1689 postpones high-risk obligations to 2 December 2027 (Annex III) and 2 August 2028 (Annex I products). | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb) |

## Commission Implementing Regulation (EU) 2022/1426 — type approval of the ADS of fully automated vehicles

Consolidated version of 24 March 2026 (amended by Implementing Regulation (EU) 2026/481 of 3 March 2026). Source: <https://eur-lex.europa.eu/eli/reg_impl/2022/1426/oj> (official text, checked 2026-10-29).

Cited in: [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [site/industry.md](industry.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Annex III Part 4 | Principles for the credibility assessment of a virtual toolchain used in ADS validation. | official text | [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb) |
| Annex III Part 5 | In-service monitoring and reporting; safety-critical occurrences without delay, listed short-term occurrences within one month, annual report. | official text | [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb) |

## Commission Implementing Regulation (EU) 2026/481 amending Implementing Regulation (EU) 2022/1426

Regulation of 3 March 2026, OJ L, 4.3.2026. Source: <https://eur-lex.europa.eu/eli/reg_impl/2026/481/oj> (official text, checked 2026-10-29).

Cited in: [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

## Regulation (EU) 2019/2144 — General Safety Regulation

OJ L 325, 16.12.2019. Source: <https://eur-lex.europa.eu/eli/reg/2019/2144/oj> (official text, checked 2026-10-29).

Cited in: [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Annex II | Requirements and application dates. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| Art. 3(5) | Definitions of driver drowsiness and attention warning (5) and advanced driver distraction warning (6). | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| Art. 6(1) | Advanced vehicle systems for all motor vehicles, incl. DDAW (c) and ADDW (d). | official text | [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |
| Art. 6(3) | DDAW and ADDW do not continuously record or retain data beyond what is necessary in the closed-loop system. | official text | [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb) |

## Regulation (EU) 2018/858 — approval and market surveillance of motor vehicles

OJ L 151, 14.6.2018 (Article 5(4) added by Article 107 of Regulation (EU) 2024/1689). Source: <https://eur-lex.europa.eu/eli/reg/2018/858/oj> (official text, checked 2026-10-29).

Cited in: [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

## Regulation (EU) 2024/2847 — Cyber Resilience Act

OJ L, 20.11.2024. Source: <https://eur-lex.europa.eu/eli/reg/2024/2847/oj> (official text, checked 2026-10-29).

Cited in: [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Art. 2(2)(c) | The CRA does not apply to products with digital elements to which Regulation (EU) 2019/2144 applies. | official text | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |

## Commission Delegated Regulation (EU) 2025/1535 (Cyber Resilience Act exclusion for L-category vehicles)

as cited. Source: <https://eur-lex.europa.eu/eli/reg_del/2025/1535/oj> (**unverified**, checked 2026-10-29).

Cited in: [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb).

## Directive (EU) 2024/2853 — liability for defective products

OJ L, 18.11.2024. Source: <https://eur-lex.europa.eu/eli/dir/2024/2853/oj> (**unverified**, checked 2026-10-29).

Cited in: [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

## Commission Delegated Regulation (EU) 2021/1341 — driver drowsiness and attention warning (DDAW)

as cited. Source: <https://eur-lex.europa.eu/eli/reg_del/2021/1341/oj> (**unverified**, checked 2026-10-29).

Cited in: [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb).

## Commission Delegated Regulation (EU) 2023/2590 — advanced driver distraction warning (ADDW)

as cited. Source: <https://eur-lex.europa.eu/eli/reg_del/2023/2590/oj> (**unverified**, checked 2026-10-29).

Cited in: [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb).

## Straßenverkehrsgesetz (German Road Traffic Act), §§ 1a–1l

Consolidated text on gesetze-im-internet.de. Source: <https://www.gesetze-im-internet.de/stvg/> (official text, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 1a-1l | Rules for motor vehicles with automated (§§ 1a–1c) and autonomous (§§ 1d–1l) driving functions. | official text | [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 1d-1l | Act on Autonomous Driving (2021) — Level 4 operation in defined operating areas with technical supervision. | official text | [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |

## Straßenverkehrs-Ordnung (German Road Traffic Regulations)

StVO 2013, consolidated text on gesetze-im-internet.de. Source: <https://www.gesetze-im-internet.de/stvo_2013/__3.html> (official text, checked 2026-10-29).

Cited in: [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), `avsafety/perturb.py`.

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 3(1) | With visibility below 50 m due to fog, snow or rain, no faster than 50 km/h. | official text | [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), `avsafety/perturb.py` |

## Autonome-Fahrzeuge-Genehmigungs-und-Betriebs-Verordnung

Ordinance of 24 June 2022. Source: <https://www.gesetze-im-internet.de/afgbv/> (**unverified**, checked 2026-10-29).

Cited in: [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb).

## NHTSA Standing General Order 2021-01 on crash reporting (ADS and Level 2 ADAS)

Third Amended SGO, reports from 16 June 2025; first issued 29 June 2021. Source: <https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting> (official summary, checked 2026-10-29).

Cited in: [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), `avsafety/__init__.py`, `avsafety/data.py`, [site/datasets.md](datasets.md), [site/glossary.md](glossary.md), [site/industry.md](industry.md), [site/observatory.md](observatory.md), [site/safety-case.md](safety-case.md).

## ISO 26262:2018 — Road vehicles — Functional safety (series)

Second edition (2018), parts 1–12. Source: <https://www.iso.org/standard/68383.html> (official summary, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [01-02](../01_Perception/02_sensor_modalities.ipynb), [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-02](../06_AI_Safety_ISO_PAS_8800/02_uncertainty_types.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [site/glossary.md](glossary.md), [site/index.md](index.md), [site/run-in-browser.md](run-in-browser.md), [site/safety-case.md](safety-case.md), [site/standards-map.md](standards-map.md), [site/teaching.md](teaching.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

## ISO 26262-2:2018 — Part 2 Management of functional safety

Second edition, 2018. Source: <https://www.iso.org/standard/68384.html> (official summary, checked 2026-10-29).

Cited in: [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/industry.md](industry.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 6 | Project-dependent safety management, incl. safety case (6.4.8) and confirmation measures (6.4.9–6.4.12). | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| Annex E | Informative guidance on the potential interaction of functional safety with cybersecurity. | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [templates/TARA_Template.md](../templates/TARA_Template.md) |
| Table 1 | Required confirmation measures and degree of independence (I0–I3) per ASIL. | secondary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [templates/HARA_Template.md](../templates/HARA_Template.md) |

## ISO 26262-3:2018 — Part 3 Concept phase

Second edition, 2018. Source: <https://www.iso.org/standard/68385.html> (official summary, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [site/glossary.md](glossary.md), [site/industry.md](industry.md), [site/interactive-tools.md](interactive-tools.md), [site/toolkit.md](toolkit.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 5 | Item definition. | official summary | [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [site/industry.md](industry.md), [templates/HARA_Template.md](../templates/HARA_Template.md) |
| 6 | Hazard analysis and risk assessment (HARA), safety goals. | official summary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [site/industry.md](industry.md) |
| 7 | Functional safety concept. | official summary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [templates/HARA_Template.md](../templates/HARA_Template.md) |
| Annex B | Informative annex on hazard analysis and risk assessment (S, E, C classes and examples). | official summary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [templates/HARA_Template.md](../templates/HARA_Template.md) |
| Table 4 | ASIL determination from S, E and C (reproduced in avsafety.iso26262 and tested). | secondary | [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md) |

## ISO 26262-4:2018 — Part 4 Product development at the system level

Second edition, 2018. Source: <https://www.iso.org/standard/68386.html> (official summary, checked 2026-10-29).

Cited in: [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [site/industry.md](industry.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 6 | Technical safety concept. | official summary | — |
| 7 | System and item integration and testing. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| 8 | Safety validation. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |

## ISO 26262-5:2018 — Part 5 Product development at the hardware level

Second edition, 2018. Source: <https://www.iso.org/standard/68387.html> (official summary, checked 2026-10-29).

Cited in: [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [06-02](../06_AI_Safety_ISO_PAS_8800/02_uncertainty_types.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [site/glossary.md](glossary.md), [site/industry.md](industry.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 8 | Evaluation of the hardware architectural metrics (SPFM, LFM). | official summary | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) |
| 9 | Evaluation of safety goal violations due to random hardware failures (PMHF). | official summary | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb) |
| Annex C | Normative annex defining the hardware architectural metrics. | official summary | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) |
| Annex D | Informative annex on the evaluation of diagnostic coverage (low/medium/high tables). | official summary | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb) |
| Table 4 | Target values for SPFM (Table 4), LFM (Table 5) and PMHF (Table 6) per ASIL. | **unverified** | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py` |

## ISO 26262-6:2018 — Part 6 Product development at the software level

Second edition, 2018. Source: <https://www.iso.org/standard/68388.html> (official summary, checked 2026-10-29).

Cited in: [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [site/industry.md](industry.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 9 | Software unit verification. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| 10 | Software integration and verification. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| 11 | Testing of the embedded software. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| Table 7 | Methods for software unit verification (2018 numbering). | **unverified** | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| Table 9 | Structural coverage metrics at the software unit level (2018 numbering). | **unverified** | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |

## ISO 26262-8:2018 — Part 8 Supporting processes

Second edition, 2018. Source: <https://www.iso.org/standard/68390.html> (official summary, checked 2026-10-29).

Cited in: [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 5 | Interfaces within distributed developments (development interface agreement, DIA). | official summary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [templates/HARA_Template.md](../templates/HARA_Template.md) |
| 8 | Change management (impact analysis of modifications). | official summary | [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb) |
| 9 | Verification. | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb) |
| 11 | Confidence in the use of software tools (TI, TD, TCL). | official summary | [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |

## ISO 26262-9:2018 — Part 9 ASIL-oriented and safety-oriented analyses

Second edition, 2018. Source: <https://www.iso.org/standard/68391.html> (official summary, checked 2026-10-29).

Cited in: [01-02](../01_Perception/02_sensor_modalities.ipynb), [01-06](../01_Perception/06_sensor_fusion.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [site/glossary.md](glossary.md), [site/industry.md](industry.md), [site/safety-case.md](safety-case.md), [templates/HARA_Template.md](../templates/HARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 5 | Requirements decomposition with respect to ASIL tailoring (ASIL decomposition); permitted schemes in 5.4. | official summary | [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), `avsafety/exercises.py`, `avsafety/iso26262.py`, [site/industry.md](industry.md) |
| 7 | Analysis of dependent failures (DFA). | official summary | [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [site/industry.md](industry.md), [templates/HARA_Template.md](../templates/HARA_Template.md) |
| 8 | Safety analyses (inductive and deductive). | official summary | [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [site/industry.md](industry.md) |

## ISO 21448:2022 — Road vehicles — Safety of the intended functionality (SOTIF)

First edition, 2022 (stage 90.92 to be revised; ISO/WD 21448 at stage 20.60, ISO Open Data, 28 October 2026). Source: <https://www.iso.org/standard/77490.html> (official summary, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [01-02](../01_Perception/02_sensor_modalities.ipynb), [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-04](../01_Perception/04_object_detection.ipynb), [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [01-06](../01_Perception/06_sensor_fusion.ipynb), [01-07](../01_Perception/07_multi_object_tracking.ipynb), [01-08](../01_Perception/08_driving_datasets.ipynb), [01-09](../01_Perception/09_trajectory_prediction.ipynb), [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [02-03](../02_Failures_and_Robustness/03_out_of_distribution_detection.ipynb), [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-03](../04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [04-05](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-02](../06_AI_Safety_ISO_PAS_8800/02_uncertainty_types.ipynb), [06-03](../06_AI_Safety_ISO_PAS_8800/03_mc_dropout_and_deep_ensembles.ipynb), [06-04](../06_AI_Safety_ISO_PAS_8800/04_calibration.ipynb), [06-05](../06_AI_Safety_ISO_PAS_8800/05_conformal_prediction.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [07-03](../07_Runtime_Assurance_and_Operations/03_human_factors_and_takeover.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), `avsafety/exercises.py`, `avsafety/perturb.py`, [site/glossary.md](glossary.md), [site/index.md](index.md), [site/industry.md](industry.md), [site/run-in-browser.md](run-in-browser.md), [site/safety-case.md](safety-case.md), [site/standards-map.md](standards-map.md), [site/teaching.md](teaching.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 4.2 | SOTIF principles, incl. the SOTIF-related hazardous event model (4.2.1). | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| 4.2.2 | The four scenario areas (known/unknown × hazardous/not hazardous). | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 5 | Specification and design. | official summary | [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 6 | Identification and evaluation of hazards, incl. acceptance criteria for the residual risk (6.5). | official summary | [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-07](../01_Perception/07_multi_object_tracking.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 7 | Identification and evaluation of potential functional insufficiencies and triggering conditions. | official summary | [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-07](../01_Perception/07_multi_object_tracking.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 8 | Functional modifications addressing SOTIF-related risks. | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 9 | Definition of the verification and validation strategy (acceptance criteria → validation targets). | official summary | [01-04](../01_Perception/04_object_detection.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 10 | Evaluation of known scenarios (Area 2). | official summary | [01-04](../01_Perception/04_object_detection.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 11 | Evaluation of unknown scenarios (Area 3). | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 12 | Evaluation of the achievement of the SOTIF (release recommendation). | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| 13 | Operation phase activities (field monitoring, SOTIF issue evaluation and resolution). | official summary | [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/industry.md](industry.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md) |
| Annex A | Annex A (general guidance on SOTIF) discusses the interaction with ISO 26262. | **unverified** | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb) |
| Annex B | Guidance on scenario and system analyses; STPA illustrated in B.4. | secondary | [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb) |
| Annex C | Guidance on SOTIF verification and validation (incl. validation targets). | official summary | [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb) |

## ISO/SAE 21434:2021 — Road vehicles — Cybersecurity engineering

First edition, 2021 (stage 90.92; ISO/SAE AWI 21434 registered, ISO Open Data, 28 October 2026). Source: <https://www.iso.org/standard/70918.html> (official summary, checked 2026-10-29).

Cited in: [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), `avsafety/exercises.py`, `avsafety/iso21434.py`, [site/glossary.md](glossary.md), [site/index.md](index.md), [site/industry.md](industry.md), [site/interactive-tools.md](interactive-tools.md), [site/run-in-browser.md](run-in-browser.md), [site/safety-case.md](safety-case.md), [site/standards-map.md](standards-map.md), [site/teaching.md](teaching.md), [site/toolkit.md](toolkit.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 5 | Organizational cybersecurity management. | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [templates/TARA_Template.md](../templates/TARA_Template.md) |
| 6 | Project dependent cybersecurity management (cybersecurity case, assessment, release for post-development). | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) |
| 7 | Distributed cybersecurity activities (interface agreements with suppliers). | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb) |
| 8 | Continual cybersecurity activities (monitoring, event evaluation, vulnerability analysis and management). | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 8.3 | Cybersecurity monitoring (8.3) and cybersecurity event evaluation (8.4). | secondary | [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) |
| 8.5 | Vulnerability analysis (8.5) and vulnerability management (8.6). | secondary | [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| 9 | Concept (item definition, cybersecurity goals, cybersecurity concept). | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [templates/TARA_Template.md](../templates/TARA_Template.md) |
| 9.3 | Item definition. | secondary | [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb) |
| 9.4 | Cybersecurity goals (and claims). | secondary | [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) |
| 9.5 | Cybersecurity concept. | secondary | [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) |
| 10 | Product development (cybersecurity specifications, verification). | official summary | [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb) |
| 10.4.2 | Integration and verification (cybersecurity verification of the implemented controls). | secondary | [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb) |
| 11 | Cybersecurity validation at vehicle level. | official summary | [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 12 | Production. | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 13 | Operations and maintenance (incident response, updates). | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 14 | End of cybersecurity support and decommissioning. | official summary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb) |
| 15 | Threat analysis and risk assessment (TARA) methods. | official summary | [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), `avsafety/iso21434.py`, [site/glossary.md](glossary.md), [site/industry.md](industry.md), [templates/TARA_Template.md](../templates/TARA_Template.md) |
| 15.6 | Attack path analysis. | secondary | [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| 15.7 | Attack feasibility rating. | secondary | [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb) |
| Annex E | Informative annex on cybersecurity assurance levels (CAL). | secondary | [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), `avsafety/iso21434.py`, [site/glossary.md](glossary.md), [site/toolkit.md](toolkit.md), [templates/TARA_Template.md](../templates/TARA_Template.md) |
| Annex F | Informative guidelines for impact rating; safety impact uses ISO 26262 severity classes. | secondary | [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb) |
| Annex G | Informative guidelines for attack feasibility rating; attack-potential approach (G.2) with values from ISO/IEC 18045. | secondary | [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb), [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), `avsafety/exercises.py` |
| Annex H | Informative example application of the TARA methods (headlamp), incl. the example risk matrix the course uses. | secondary | [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), `avsafety/exercises.py` |

## ISO/PAS 8800:2024 — Road vehicles — Safety and artificial intelligence

First edition, December 2024 (stage 60.60; ISO/PWI PAS 8800-1 and -2 registered, ISO Open Data, 28 October 2026). Source: <https://www.iso.org/standard/83303.html> (official summary, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-04](../01_Perception/04_object_detection.ipynb), [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [01-06](../01_Perception/06_sensor_fusion.ipynb), [01-08](../01_Perception/08_driving_datasets.ipynb), [01-09](../01_Perception/09_trajectory_prediction.ipynb), [02-01](../02_Failures_and_Robustness/01_incident_case_studies.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [02-03](../02_Failures_and_Robustness/03_out_of_distribution_detection.ipynb), [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [03-01](../03_Functional_Safety_ISO26262/01_iso26262_fundamentals.ipynb), [03-02](../03_Functional_Safety_ISO26262/02_hara.ipynb), [03-03](../03_Functional_Safety_ISO26262/03_fmea_and_fmeda.ipynb), [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb), [03-05](../03_Functional_Safety_ISO26262/05_stpa.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-03](../04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-02](../06_AI_Safety_ISO_PAS_8800/02_uncertainty_types.ipynb), [06-03](../06_AI_Safety_ISO_PAS_8800/03_mc_dropout_and_deep_ensembles.ipynb), [06-04](../06_AI_Safety_ISO_PAS_8800/04_calibration.ipynb), [06-05](../06_AI_Safety_ISO_PAS_8800/05_conformal_prediction.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/index.md](index.md), [site/industry.md](industry.md), [site/run-in-browser.md](run-in-browser.md), [site/safety-case.md](safety-case.md), [site/standards-map.md](standards-map.md), [site/teaching.md](teaching.md), [templates/HARA_Template.md](../templates/HARA_Template.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md), [templates/TARA_Template.md](../templates/TARA_Template.md).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| 8 | Assurance arguments for AI systems. | official summary | [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb) |
| 14 | Measures during operation (field data collection, continual re-evaluation of the assurance argument). | official summary | [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb) |

## ISO/TS 5083:2025 — Road vehicles — Safety for automated driving systems — Design, verification and validation

First edition, April 2025 (stage 90.92; ISO/WD TS 5083 at stage 20.60, ISO Open Data, 28 October 2026). Source: <https://www.iso.org/standard/81920.html> (official summary, checked 2026-10-29).

Cited in: [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/industry.md](industry.md), [site/standards-map.md](standards-map.md).

## ISO 34502:2022 — Road vehicles — Test scenarios for automated driving systems — Scenario-based safety evaluation framework

First edition, 2022. Source: <https://www.iso.org/standard/78951.html> (official summary, checked 2026-10-29).

Cited in: [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-05](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), `avsafety/coverage.py`, [site/standards-map.md](standards-map.md), [site/toolkit.md](toolkit.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md).

## ISO 34503:2023 — Road vehicles — Test scenarios for automated driving systems — Specification for operational design domain

First edition, 2023. Source: <https://www.iso.org/standard/78952.html> (official summary, checked 2026-10-29).

Cited in: [01-01](../01_Perception/01_sae_levels_and_odd.ipynb), [01-08](../01_Perception/08_driving_datasets.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-04](../07_Runtime_Assurance_and_Operations/04_v2x_cooperative_driving.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), `avsafety/coverage.py`, [site/glossary.md](glossary.md), [site/standards-map.md](standards-map.md), [site/toolkit.md](toolkit.md), [templates/SOTIF_Analysis_Template.md](../templates/SOTIF_Analysis_Template.md).

## ISO 24089:2023 — Road vehicles — Software update engineering

First edition, 2023. Source: <https://www.iso.org/standard/77796.html> (official summary, checked 2026-10-29).

Cited in: [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [05-03](../05_Cybersecurity_ISO21434/03_attack_surface_analysis.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [templates/TARA_Template.md](../templates/TARA_Template.md).

## ISO/IEC 18045 — Methodology for IT security evaluation

Cited without edition as the source of the attack-potential factor values of ISO/SAE 21434 Annex G. Source: <https://www.iso.org/standard/72889.html> (official summary, checked 2026-10-29).

Cited in: [02-04](../02_Failures_and_Robustness/04_adversarial_attacks.ipynb), [05-01](../05_Cybersecurity_ISO21434/01_iso21434_fundamentals.ipynb), [05-02](../05_Cybersecurity_ISO21434/02_tara.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), `avsafety/iso21434.py`, [templates/TARA_Template.md](../templates/TARA_Template.md).

## UL 4600 — Standard for Safety for the Evaluation of Autonomous Products

Edition 3, released 17 March 2023. Source: <https://www.ul.com/news/ul-4600-edition-3-updates-incorporate-autonomous-trucking> (official summary, checked 2026-10-29).

Cited in: [04-01](../04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb), [04-05](../04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb), [06-01](../06_AI_Safety_ISO_PAS_8800/01_ai_safety_standards.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [06-08](../06_AI_Safety_ISO_PAS_8800/08_statistical_safety_validation.ipynb), [07-01](../07_Runtime_Assurance_and_Operations/01_odd_and_runtime_monitoring.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [07-05](../07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb), [07-06](../07_Runtime_Assurance_and_Operations/06_industry_deployment.ipynb), [08-01](../08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb), [08-02](../08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb), [08-03](../08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb), [08-04](../08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), [site/glossary.md](glossary.md), [site/industry.md](industry.md), [site/safety-case.md](safety-case.md), [site/standards-map.md](standards-map.md).

## IEC 61508-6:2010 — Functional safety of E/E/PE safety-related systems — Part 6 Guidelines on the application of IEC 61508-2 and -3

Edition 2.0, 2010. Source: <https://webstore.iec.ch/en/publication/5520> (official summary, checked 2026-10-29).

Cited in: [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb).

| Locator | The course states | Verification | Cited in |
|---|---|---|---|
| Annex D | Methodology for quantifying the effect of hardware-related common cause failures (beta factor). | official summary | [03-04](../03_Functional_Safety_ISO26262/04_fault_tree_analysis.ipynb) |

## KITTI Vision Benchmark Suite (object detection and tracking)

Archives on the KITTI S3 bucket (avg-kitti), labels of 11 May 2018. Source: <https://www.cvlibs.net/datasets/kitti/> (official text, checked 2026-10-29).

Cited in: [01-02](../01_Perception/02_sensor_modalities.ipynb), [01-03](../01_Perception/03_lidar_point_clouds.ipynb), [01-04](../01_Perception/04_object_detection.ipynb), [01-05](../01_Perception/05_vulnerable_road_user_detection.ipynb), [01-06](../01_Perception/06_sensor_fusion.ipynb), [01-07](../01_Perception/07_multi_object_tracking.ipynb), [01-08](../01_Perception/08_driving_datasets.ipynb), [02-02](../02_Failures_and_Robustness/02_corner_cases.ipynb), [03-06](../03_Functional_Safety_ISO26262/06_verification_and_validation.ipynb), [04-02](../04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb), [04-03](../04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb), [04-04](../04_SOTIF_ISO21448/04_simulation_based_validation.ipynb), [04-06](../04_SOTIF_ISO21448/06_sotif_benchmark.ipynb), [06-04](../06_AI_Safety_ISO_PAS_8800/04_calibration.ipynb), [06-05](../06_AI_Safety_ISO_PAS_8800/05_conformal_prediction.ipynb), [06-06](../06_AI_Safety_ISO_PAS_8800/06_explainability.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), [08-05](../08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb), [08-06](../08_Standards_Regulation_and_Safety_Case/06_continuous_assurance.ipynb), `avsafety/__init__.py`, `avsafety/bench.py`, `avsafety/data.py`, `avsafety/perturb.py`, [site/benchmark.md](benchmark.md), [site/datasets.md](datasets.md), [site/index.md](index.md), [site/industry.md](industry.md), [site/run-in-browser.md](run-in-browser.md), [site/safety-case.md](safety-case.md), [site/teaching.md](teaching.md), [site/toolkit.md](toolkit.md).

## Next Generation Simulation (NGSIM) vehicle trajectories, US DOT open data

data.transportation.gov dataset 8ect-6jqj. Source: <https://data.transportation.gov/d/8ect-6jqj> (official text, checked 2026-10-29).

Cited in: [01-09](../01_Perception/09_trajectory_prediction.ipynb), [06-07](../06_AI_Safety_ISO_PAS_8800/07_end_to_end_and_foundation_models.ipynb), [07-02](../07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb), `avsafety/__init__.py`, `avsafety/data.py`, [site/datasets.md](datasets.md), [site/index.md](index.md), [site/industry.md](industry.md), [site/run-in-browser.md](run-in-browser.md), [site/toolkit.md](toolkit.md).

## ROAD — Real ORNL Automotive Dynamometer CAN intrusion dataset (Verma et al., 2024)

Zenodo record 10462796. Source: <https://doi.org/10.5281/zenodo.10462796> (official text, checked 2026-10-29).

Cited in: [05-04](../05_Cybersecurity_ISO21434/04_can_bus_intrusion_detection.ipynb), `avsafety/__init__.py`, `avsafety/data.py`, [site/datasets.md](datasets.md), [site/index.md](index.md), [site/run-in-browser.md](run-in-browser.md), [site/toolkit.md](toolkit.md).

## VeReMi Extension V2X misbehaviour dataset (Kamel et al., 2020)

Zenodo record 20090854. Source: <https://doi.org/10.5281/zenodo.20090854> (official text, checked 2026-10-29).

Cited in: [05-05](../05_Cybersecurity_ISO21434/05_v2x_misbehaviour_detection.ipynb), `avsafety/__init__.py`, `avsafety/data.py`, [site/datasets.md](datasets.md), [site/index.md](index.md), [site/run-in-browser.md](run-in-browser.md), [site/toolkit.md](toolkit.md).
