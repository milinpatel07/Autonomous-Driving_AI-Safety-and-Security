---
title: Teaching with this course
---

This page is for lecturers and trainers who want to adopt the course. Everything here is reusable as it stands:
the notebooks, the [templates](../templates/HARA_Template.md), the [autograded assignment template](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/classroom/README.md)
and the assessment design below. Notebook numbers are module-notebook, e.g. 03-02 is the HARA notebook in Module 03.
Notebooks marked ✓ contain auto-checked exercises.

## Prerequisites

- **Programming:** Python with NumPy, pandas and Matplotlib at the level of a first programming course. Every
  notebook explains its code; nobody needs a GPU or a local installation (Google Colab is enough).
- **Mathematics:** probability (distributions, conditional probability, confidence bounds), basic statistics and
  constant-acceleration kinematics.
- **Engineering:** an introduction to vehicle systems or control is helpful, not required. No prior knowledge of
  the standards is assumed; they are paywalled, so the notebooks teach their concepts with clause references.
- **Level:** final-year bachelor's or master's students in automotive, electrical, computer or mechanical
  engineering, computer science or mechatronics; engineers moving into safety, SOTIF or security roles.

## Learning outcomes

Each outcome is written so that it can be assessed; the last column names where it is assessed (C = weekly
checked exercises, P = HARA/TARA project, F = final project, E = written or oral examination, if used).

| Module | On successful completion, students can … | Assessed |
|---|---|---|
| 01 Perception and Prediction | evaluate an object detector on real KITTI frames by recall per distance and occlusion class, and explain how sensor modality, fusion and tracking change the errors that reach planning | F, E |
| 02 Failures and Robustness | analyse a documented AV incident as a causal chain, and detect out-of-distribution and adversarial inputs with a stated false-alarm rate | E |
| 03 Functional Safety | perform a HARA (S, E, C with rationale → ASIL → safety goal with safe state and FTTI); compute SPFM, LFM and PMHF from an FMEDA; derive minimal cut sets and justify an ASIL decomposition by independence | C, P, F |
| 04 SOTIF | distinguish triggering conditions from functional insufficiencies; place scenarios in Areas 1–4; derive a validation target from an acceptance criterion; compute TTC, THW, DRAC and the RSS safe distance and judge their assumptions | C, F, E |
| 05 Cybersecurity | carry out a TARA from asset to treatment decision, rate attack feasibility by attack potential, determine risk value and CAL, and explain why CAL is not a risk measure | C, P |
| 06 AI Safety | quantify and evaluate predictive uncertainty (calibration error, conformal coverage), state what each guarantee does and does not cover, and compute the exposure needed for a statistical safety claim | F, E |
| 07 Runtime Assurance and Operations | specify an ODD monitor and a fallback, and define safety performance indicators from field data (NHTSA reports) | F, E |
| 08 Standards, Regulation and Safety Case | map work products across ISO 26262, ISO 21448, ISO/SAE 21434 and ISO/PAS 8800, place them in the type-approval context, and build a GSN safety argument that leads to a defensible release decision | P, F |

## One-semester course (14 weeks)

Designed for 5 ECTS: per week a 90-minute lecture and a 90-minute lab, plus self-study and the project (about
150 hours of student work in total). The lecture motivates and frames the topic; in the lab, students run the
*core* notebooks in pairs and solve their exercises; *self-study* notebooks deepen the topic before the next week.

| Week | Lecture | Core lab notebooks | Self-study | Assessment |
|---|---|---|---|---|
| 1 | Automated driving, SAE levels, ODD; sensors | 01-01, 01-02 | 01-03 | |
| 2 | Object detection and vulnerable road users on real data | 01-04, 01-05 | 01-06, 01-07 | |
| 3 | Datasets, prediction, what real incidents teach | 01-09, 02-01 | 01-08 | |
| 4 | Corner cases, out-of-distribution inputs, adversarial attacks | 02-02, 02-03 | 02-04 | |
| 5 | ISO 26262 and the HARA | 03-01, 03-02 ✓ | | checked exercises; project brief |
| 6 | FMEA/FMEDA and fault tree analysis | 03-03 ✓, 03-04 ✓ | | checked exercises |
| 7 | STPA; verification and validation | 03-05, 03-06 | | project milestone 1: item definition and HARA |
| 8 | SOTIF: triggering conditions, Areas 1–4, acceptance criteria | 04-01 ✓, 04-02 | | checked exercises |
| 9 | SOTIF validation: monitors, simulation, criticality metrics, benchmark | 04-05 ✓, 04-06 | 04-03, 04-04 | checked exercises |
| 10 | ISO/SAE 21434 and the TARA | 05-01 ✓, 05-02 ✓ | 05-03 | checked exercises |
| 11 | In-vehicle and V2X defences; ISO/PAS 8800 | 05-04, 06-01, 06-02 | 05-05 | project milestone 2: TARA and co-engineering |
| 12 | Uncertainty evidence: ensembles, calibration, conformal prediction | 06-04, 06-05 | 06-03, 06-06 | final project starts |
| 13 | Statistical validation; runtime assurance and operations | 06-08, 07-01, 07-02 | 06-07, 07-03, 07-05 | |
| 14 | Regulation, safety cases, continuous assurance | 08-04, 08-05 | 07-04, 07-06, 08-01, 08-02, 08-03, 08-06 | final project due after the lecture period |

A shorter course (2.5 ECTS) keeps weeks 1, 5–10 and 14. For a security-focused course, swap weeks 3–4 for
05-03 to 05-05 and 02-04.

## Five-day industry training

For engineers in the automotive industry; each day is about two hours of input and four to five hours of guided
work on the notebooks, on the participants' own laptops or in Colab.

| Day | Theme | Notebooks | Output of the day |
|---|---|---|---|
| 1 | Automated driving and how it fails | 01-01, 01-04, 01-05, 02-01, 02-03 | detector evaluation on KITTI; incident causal chain |
| 2 | Functional safety | 03-02 ✓, 03-03 ✓, 03-04 ✓, 03-06 | HARA and FMEDA for the participants' own function |
| 3 | SOTIF | 04-01 ✓, 04-02, 04-05 ✓, 04-06 | triggering-condition table and validation target |
| 4 | Cybersecurity and co-engineering | 05-01 ✓, 05-02 ✓, 08-01 | TARA with the safety interface |
| 5 | AI safety evidence and the safety case | 06-04, 06-05, 06-08, 08-04, 08-05 | release argument for the capstone function |

## Assessment design

Assessment follows the outcomes table: computation is checked automatically and often; judgement is assessed in
the project and the final project, where it can be seen.

| Component | Weight | Form |
|---|---|---|
| Weekly checked exercises | 10 % | ✓ cells in the notebooks (formative, unlimited attempts) and the graded problem set of the [assignment template](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/classroom/README.md) |
| HARA/TARA project | 40 % | pairs; one function chosen from ACC, lane-keeping assist or automated valet parking, documented with the [HARA](../templates/HARA_Template.md) and [TARA](../templates/TARA_Template.md) templates; two milestones (weeks 7 and 11) with written feedback |
| Final project | 50 % | individual; the capstone 08-05 extended to a variant, with a report (about 10 pages) and a 15-minute oral defence |

**Final project variants** (each changes the evidence, so results cannot be copied from the notebook): the
cyclist instead of the pedestrian class; a higher speed range of the ODD; a different detector or score threshold;
an added TARA threat on the perception-to-brake path; a field-monitoring argument with NHTSA reports (07-05).

**Rubric for the final project**

| Criterion (weight) | Excellent | Adequate | Insufficient |
|---|---|---|---|
| Traceability (20 %) | every safety goal, requirement and piece of evidence is traced both ways; changes in the variant are propagated | main chain traced; gaps are few and acknowledged | ratings, requirements and evidence are disconnected |
| Correctness of analyses (20 %) | S/E/C, ASIL, metrics, feasibility, CAL and statistical bounds are correct and justified | minor errors that do not change a decision | errors that change an ASIL, CAL or the release decision |
| Evidence from real data (20 %) | the variant's evidence is computed on real data with stated sample sizes and uncertainty | evidence computed, uncertainty or sample size missing | evidence copied, invented or unsupported |
| Safety argument and decision (25 %) | GSN argument with explicit assumptions and defeaters; the release decision follows from the evidence and states its conditions (e.g. ODD restriction) | argument complete but assumptions implicit | decision asserted without an argument |
| Limitations and communication (15 %) | states what the evidence cannot show and what would be needed in practice; clear, concise report and defence | limitations listed generically | limitations missing; report hard to follow |

The oral defence checks that the student can explain and change their own analysis (for example: "what happens
to the ASIL if C2 becomes C3?"); it is the main safeguard of authorship.

## Autograding

The [assignment template](https://github.com/milinpatel07/Autonomous-Driving_AI-Safety-and-Security/blob/main/classroom/README.md) is a starter repository with eight questions, an `answers.py`
for the students and one pytest test per question. The tests use `avsafety.exercises`, which computes every
reference value with the same tested toolkit the notebooks use, so changing the question parameters each term is
enough to issue a new problem set. GitHub Classroom, the usual host for such templates, was retired on 28 August 2026 ([GitHub changelog](https://github.blog/changelog/2026-08-27-github-classroom-deprecated));
the template's README describes how to run it with Classroom 50 or with a plain GitHub organisation (as of October 2026).

## Certificates

This repository does not issue certificates: a certificate is only meaningful when an institution has verified
the work. The route that works is the institution's own:

1. Grade with the template and the rubric above; export the scores (Classroom 50 exports a CSV per assignment)
   and combine them with the project and final-project marks in the institution's learning-management system.
2. The examination office issues the record of achievement or transcript in the usual way, naming the learning
   outcomes and, for credit-bearing courses, the ECTS credits.
3. For short courses and industry training, an institution can additionally issue a digital badge in the
   **Open Badges 3.0** format (1EdTech; credentials follow the W3C Verifiable Credentials Data Model v2.0).
   The badge names the institution as issuer, describes the achievement and its criteria (use the learning
   outcomes above), can link evidence such as the graded final project, and is cryptographically signed, so
   anyone can verify it. Badges are issued from the institution's badge platform, not from this repository.

Please cite the course when you adopt it (see [About](about.md)); the author is glad to hear where it is used.
