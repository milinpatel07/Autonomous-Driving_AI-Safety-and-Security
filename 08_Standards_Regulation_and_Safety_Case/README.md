# Module 08 · Standards, Regulation and Safety Case

Bringing it together: how the standards interlock, what type approval and regulation require, where the standards still have gaps, how to argue safety with a structured safety case, and a capstone that takes a pedestrian AEB function from requirement to release decision.

**5 notebooks** · each runs in Google Colab on CPU, without dataset downloads.

| # | Notebook | Level | Standards | Open |
|---|---|---|---|---|
| 01 | [Standards Integration: How ISO 26262, ISO 21448, ISO/SAE 21434 and ISO/PAS 8800 Work Together](01_standards_integration.ipynb) | Intermediate | ISO 26262:2018, ISO 21448:2022, ISO/SAE 21434:2021, ISO/PAS 8800:2024, ISO/TS 5083:2025, UL 4600 (3rd ed.), ISO 34502:2022, ISO 34503:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/08_Standards_Regulation_and_Safety_Case/01_standards_integration.ipynb) |
| 02 | [Automotive Regulation and Type Approval for Automated Driving](02_regulation_and_type_approval.ipynb) | Intermediate | UN R155, R156, R157, UN ADS Regulation (2026); Reg. (EU) 2018/858, 2019/2144, 2022/1426, 2024/1689; ISO/SAE 21434:2021, ISO 24089:2023 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/08_Standards_Regulation_and_Safety_Case/02_regulation_and_type_approval.ipynb) |
| 03 | [Standards Gaps and Open Problems in AV Safety](03_standards_gaps.ipynb) | Advanced | ISO 26262:2018, ISO 21448:2022, ISO/SAE 21434:2021, ISO/PAS 8800:2024, ISO/TS 5083:2025, UL 4600 (3rd ed.) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/08_Standards_Regulation_and_Safety_Case/03_standards_gaps.ipynb) |
| 04 | [Safety Cases and Goal Structuring Notation (GSN)](04_safety_case_gsn.ipynb) | Advanced | GSN Community Standard v3 (2021), UL 4600 (3rd ed., 2023), ISO/TS 5083:2025, ISO/PAS 8800:2024 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/08_Standards_Regulation_and_Safety_Case/04_safety_case_gsn.ipynb) |
| 05 | [Capstone: Pedestrian AEB from Requirement to Release Decision](05_capstone_aeb_from_requirement_to_release.ipynb) | Advanced | ISO 26262:2018, ISO 21448:2022, ISO/SAE 21434:2021, ISO/PAS 8800:2024, UL 4600 (3rd ed.) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb) |

## What you will learn

### 01 · Standards Integration: How ISO 26262, ISO 21448, ISO/SAE 21434 and ISO/PAS 8800 Work Together

- Compare the scope, hazard source and key work products of the main AV safety and security documents
- Explain where the standards interface: shared item definition, HARA ↔ SOTIF hazard evaluation ↔ TARA impact rating, and safety–security co-engineering
- Decide which standard's cause analysis applies to a given hazard, without treating them as exclusive
- Carry out a combined HARA + SOTIF + TARA record for an AEB example, keeping ASIL, SOTIF acceptance and CAL side by side (they are not one scale)
- Identify the real coordination points between the disciplines (updates, degradation, logging, diagnostics) and document them traceably

### 02 · Automotive Regulation and Type Approval for Automated Driving

- Distinguish type approval (UNECE / EU / China) from self-certification (US) and name the actors involved
- Place the main AV regulations on a dated global timeline and say what each requires
- Map UN R155 CSMS processes to ISO/SAE 21434 clauses and UN R156 SUMS to ISO 24089
- State the UN R157 (ALKS) transition-demand timings and model them
- Explain correctly how the EU AI Act reaches vehicles (Art. 2(2), Annex I Section B), including the 2026 change of dates
- Assemble an evidence checklist for an SAE Level 3 motorway system seeking EU approval

### 03 · Standards Gaps and Open Problems in AV Safety

- Identify the limitations of the current standards for ML-based automated driving, and which gaps newer documents now address
- Explain why ISO 26262's assumptions do not transfer directly to ML components
- Describe the SOTIF 'unknown hazardous scenarios' (Area 3) problem and what ISO 21448 does and does not prescribe
- Discuss open research problems (verification, data representativeness, validation at scale, continual learning, multi-agent effects)
- Separate published facts from opinion when reasoning about the future of standards

### 04 · Safety Cases and Goal Structuring Notation (GSN)

- Explain what a **safety case** is in terms of **claims, arguments and evidence**, and why automated driving standards increasingly centre on it.
- Name and draw the **GSN elements** of the GSN Community Standard (Version 3, 2021) and the two relationships *SupportedBy* and *InContextOf*.
- Describe **argument patterns**, **modules** and **confidence arguments**, including the idea of **defeaters** in eliminative argumentation.
- Summarise what **UL 4600**, **ISO/TS 5083:2025**, **ISO/PAS 8800:2024** and **AMLAS** expect of an assurance argument.
- Build, validate and render a GSN argument in Python for *"the AEB pedestrian function is acceptably safe within its ODD"*, combining ISO 26262, ISO 21448, ISO/PAS 8800 and ISO/SAE 21434 evidence.
- Automate routine checks: undeveloped goals, type errors, stale evidence and open defeaters.

### 05 · Capstone: Pedestrian AEB from Requirement to Release Decision

- Trace one function, pedestrian automated emergency braking (AEB), from item definition and HARA through the functional safety concept to a release decision, reusing the course's work products instead of re-deriving them.
- Derive a quantitative perception requirement from vehicle dynamics and verify it on **real KITTI images with a real detector**, including recall by distance and occlusion.
- Turn measured performance insufficiencies into SOTIF measures: an ODD restriction computed from the data, and triggering conditions handed to the validation plan.
- Use calibration and split conformal prediction as evidence, and state what each does and does not guarantee.
- Combine the TARA, the validation target and scenario coverage into a GSN-shaped evidence table.
- Compute a release checklist and decision (*release / release with ODD restriction / do not release*), and explain why the evidence in a notebook can never be enough on its own.

---

← [Module 07 · Runtime Assurance and Operations](../07_Runtime_Assurance_and_Operations/README.md) · [Course home](../README.md)
