---
title: 'Autonomous Driving: AI Safety and Security — an open, executable course from perception to safety cases'
tags:
  - automated driving
  - functional safety
  - ISO 26262
  - SOTIF
  - ISO 21448
  - ISO/SAE 21434
  - ISO/PAS 8800
  - safety case
  - Jupyter
authors:
  - name: Milin Patel
    affiliation: 1
affiliations:
  - name: Hochschule Kempten – University of Applied Sciences, Germany
    index: 1
date: 29 October 2026
bibliography: paper.bib
---

# Summary

*Autonomous Driving: AI Safety and Security* is an open course in eight modules and fifty Jupyter notebooks
[@kluyver2016jupyter] that teaches how an automated vehicle perceives and predicts, how it fails, and how engineers
argue that it is safe and secure enough to release. It covers functional safety (ISO 26262 [@iso26262]), safety of
the intended functionality (SOTIF, ISO 21448 [@iso21448]), cybersecurity engineering (ISO/SAE 21434 [@iso21434]),
safety and artificial intelligence (ISO/PAS 8800 [@isopas8800]), runtime assurance, regulation and safety cases
[@ul4600]. Every notebook runs on a CPU in Google Colab. Perception, prediction and field-safety notebooks work on
real public data — KITTI images, LiDAR scans and labels [@geiger2012kitti; @geiger2013vision], NGSIM vehicle
trajectories [@ngsim] and NHTSA crash reports [@nhtsa_sgo] — fetched a few frames at a time. One running example,
a pedestrian automatic emergency braking function, links the modules and ends in a capstone that takes it from
item definition to a release decision.

# Statement of need

The standards that govern automated-driving safety are process and method documents: they define work products
such as a hazard analysis, a fault tree, a triggering-condition analysis, a threat analysis or a validation target,
but they contain no data and no executable examples, and they are paywalled. Teaching material therefore tends to
fall into two groups. Textbooks and lecture slides explain the standards but leave students without a way to
compute or test anything; machine-learning and robotics courses are executable but stop at accuracy metrics and do
not connect a detector's errors to a safety goal, an acceptance criterion or a safety argument. Students and
engineers moving into safety roles need both: the normative reasoning and the experience of producing the
evidence from data. A frequently discussed example is statistical validation: showing that a failure rate is below
that of human drivers by driving alone requires hundreds of millions of failure-free miles
[@kalra2016driving]; learners should be able to reproduce such a number, vary its assumptions and see why the
standards combine several kinds of evidence.

To the author's knowledge, no openly licensed material combines the four standards above in one executable
sequence on real data. This course is written for final-year bachelor's and master's students in automotive,
electrical and computer engineering and computer science, for lecturers who want to adopt or adapt such a course,
and for engineers in industry who need a practical introduction to safety and security work products.

# Learning objectives

After the course, learners can (i) evaluate a camera or LiDAR detector on real frames by recall per distance and
occlusion and relate its errors to vehicle-level hazards; (ii) carry out a HARA, an FMEDA with hardware metrics and
a fault tree analysis, and justify an ASIL decomposition; (iii) separate triggering conditions from functional
insufficiencies, derive validation targets from acceptance criteria, and compute criticality metrics and the
Responsibility-Sensitive Safety distance [@shalevshwartz2017formal]; (iv) perform a TARA from assets to treatment
decisions, including attack feasibility, risk value and cybersecurity assurance level; (v) produce and judge
uncertainty evidence (calibration, conformal prediction) for machine-learning components; and (vi) assemble these
results into a structured safety argument that supports or blocks a release. The teaching guide in the repository
maps each module to assessable outcomes and to a fourteen-week and a five-day schedule.

# Instructional design

The course follows a worked-example-then-practice design. Each notebook opens with learning objectives and
prerequisites, develops one method on the running example with computed (never hand-entered) results, and closes
with an *In industry* section that names the work product, its owner and what reviewers check, followed by key
takeaways, self-assessment questions with hidden answers and references checked against their sources. Illustrative numbers are
labelled as such, so learners can tell measured from assumed values.

Normative tables and formulas — the ASIL table, hardware-metric targets, attack-potential and risk tables, the RSS
distance, Poisson confidence bounds, calibration and conformal methods — are implemented once in a small Python
package, `avsafety`, whose unit tests check them against the published values. The notebooks cross-check their
own code against it, and auto-checked exercises use it to give immediate, formative feedback: a wrong answer
receives a hint that points to the section explaining the step, with no hand-maintained answer key. The same
checkers grade an assignment template for courses that use repository-based submission. Browser tools for the
ASIL, TARA, RSS and validation-target calculations let learners explore parameters without code.

Real data serve a pedagogical purpose: a pedestrian missed in an occluded KITTI frame makes a performance
insufficiency concrete in a way that synthetic examples do not. Where open data are unavailable, the course uses
the author's SOTIF-PCOD dataset of simulated LiDAR scenes for SOTIF-related conditions [@patel2024sotifpcod;
@patel2024simulation] as an optional extension. The later modules add a SOTIF perception benchmark with a fixed
evaluation protocol, a safety case for the running example kept as machine-checkable data whose evidence is
re-evaluated automatically when the material changes, and pages that track the evolving standards and incident
landscape, so that the course itself demonstrates continuous assurance.

# Story of the project

The material grew out of the author's research on SOTIF, uncertainty and assurance arguments for machine-learning
perception [@patel2023misuse; @patel2025sotifslr; @patel2026uncertainty; @patel2026dempster; @patel2026gsn] and
began as a hands-on workshop on perception safety. It was then restructured into a complete course with a shared
running example, a tested toolkit, real data and a capstone, so that it can be used for self-study, adopted as a
whole semester course, or mined for single notebooks and exercises. The repository contains a teaching guide with
a semester and an industry-training schedule, an assessment design with a rubric for the final project, and an
autograded assignment template. Contributions and error reports follow the repository's contributing guide;
corrections to normative content require a verifiable source.

# References
