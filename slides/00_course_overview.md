---
marp: true
theme: course
paginate: true
size: 16:9
header: "Course overview"
footer: "Autonomous Driving: AI Safety and Security · Milin Patel"
---

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _header: "" -->

# Autonomous Driving: AI Safety and Security
## Course overview: what the eight modules cover and how they connect

Milin Patel · Hochschule Kempten – University of Applied Sciences

<!--
This deck is the first lecture, or the introduction before the module decks. About 20 slides, 60–75 minutes.

Goal of the lecture: students leave knowing (1) the four causes of harm the course is organised around,
(2) the running example that connects all modules, and (3) how a notebook is used in the lab.
-->

---

# One question runs through the course: when is an automated vehicle safe enough to release?

<div class="cols">
<div>

**What students do**
- measure a real detector on real driving data
- analyse hazards and threats with the methods industry uses
- turn measurements into requirements, restrictions and evidence
- build the argument that leads to a release decision

</div>
<div>

**What the course contains**
- 8 modules, 50 notebooks, each runs in Colab on a CPU
- real data: KITTI, NGSIM, NHTSA crash reports, CAN attack logs
- ISO 26262, ISO 21448, ISO/SAE 21434, ISO/PAS 8800, UN regulations
- a tested Python toolkit, a safety case maintained as code

</div>
</div>

<div class="take">Every number on these slides is computed in a notebook that students can run and change.</div>

<!--
Set expectations. This is not a course about building a self-driving stack. It is about how one finds out
whether a stack is safe and secure enough, and how that is argued to someone who does not trust you.
-->

---

# Tempe 2018: the pedestrian was detected 5.6 s before impact; a path conflict was recognised only 1.2 s before

![w:1100](nb:02_Failures_and_Robustness/01_incident_case_studies.ipynb#5bb7f607)

<!-- _footer: "Source: notebook 02-01 · NTSB report HAR-19/03" -->

<!--
The Uber ATG crash in Tempe, Arizona, March 2018, reconstructed from the NTSB report (HAR-19/03).

Read the figure from left to right: the object was classified as vehicle, other and bicycle in turn. Each
re-classification discarded the tracking history, so the predicted path restarted as "static" and stayed "not on
path" until 1.5 s before impact. At 1.2 s the emergency was recognised, and a 1 s action suppression (introduced
against false alarms) delayed the response; the operator took the wheel 0.02 s before impact. The vehicle's
factory AEB was deactivated in ADS mode.

NTSB's probable cause is the operator's distraction; the contributing factors include Uber ATG's inadequate
safety risk assessment and safety culture. On the technical side, nothing in the chain is a hardware fault: the
design did not consider pedestrians crossing outside a crosswalk (a specification insufficiency, Module 04), and
the false-alarm trade-off was resolved in favour of comfort (the same trade-off as in 04-03 and 03-02).
-->

---

# Most perception failures are not malfunctions: 15 of 22 failure types fall under SOTIF

![h:470](nb:02_Failures_and_Robustness/01_incident_case_studies.ipynb#75e54c65)

<!-- _footer: "Source: notebook 02-01" -->

<!--
The failure taxonomy of notebook 02-01 sorts 22 failure types of perception systems by the standard that
primarily covers them: 15 ISO 21448, 4 ISO 26262, 2 ISO/SAE 21434, 1 ISO/PAS 8800.

This is the reason the course does not stop after functional safety. ISO 26262 was written for systems whose
intended function is fully specified; a learned perception function is not.
-->

---

# Four causes of harm, four standards, one safety argument

![w:1150](diagrams/four_causes.svg)

<!--
The structure of the course in one picture. Modules 03 to 06 each take one cause.

- E/E malfunction: ISO 26262 (Module 03)
- Functional insufficiency: ISO 21448, SOTIF (Module 04)
- Malicious manipulation: ISO/SAE 21434 (Module 05)
- ML-specific insufficiency: ISO/PAS 8800 (Module 06)

They are complementary, not alternatives. A real hazard may involve more than one cause; Module 08 brings them
into one argument. The same four branches appear in the GSN safety case of 08-04.
-->

---

# The eight modules: how it works and fails, four causes of harm, operation and argument

![w:1150](diagrams/course_map.svg)

<!--
Read the map left to right.

- 01 and 02: what the vehicle perceives and predicts, measured on real data, and how such systems have failed.
- 03 to 06: the four standards, each answering one question.
- 07 and 08: what happens after release (monitoring, fallback, field data), and how everything is argued for
  type approval and kept up to date.

The questions in italics are the ones to write on the board at the start of each module.
-->

---

# Each module takes something from the previous ones and hands something on

| Module | Takes from earlier modules | Hands on |
|---|---|---|
| 01 Perception | – | recall per distance and occlusion, the ODD, trajectory errors |
| 02 Failures | detector behaviour (01) | incident causal chains, OOD inputs, adversarial attacks |
| 03 ISO 26262 | the AEB item, failure modes (01, 02) | hazards, safety goals and ASILs, fault trees |
| 04 SOTIF | recall and ODD (01), OOD (02), hazards (03) | triggering conditions, ODD restrictions, validation targets, RSS |
| 05 ISO/SAE 21434 | attacks (02), safety goals (03) | threats, risk values, CAL, intrusion detection |
| 06 ISO/PAS 8800 | the detector (01), insufficiencies (04) | calibration, conformal bounds, statistical validation |
| 07 Operations | ODD (01), monitor and RSS (04), uncertainty (06) | runtime monitors, fallback, field safety indicators |
| 08 Safety case | everything | GSN argument, release decision, continuous assurance |

<!--
This table is the answer to "why is this module here?". Use it at the start of each module lecture: point at
the row, say what is taken over and what will be produced.
-->

---

# One running example connects the modules: a pedestrian AEB

![w:1150](diagrams/aeb_thread.svg)

<!--
Automated emergency braking for pedestrians, urban roads up to 60 km/h. It is simple enough to understand in
one sentence and hard enough to need every module.

The thread ends in the capstone (08-05) with the release decision DO NOT RELEASE, with reasons. That is the
intended outcome: students learn to show why the evidence is not enough, which is what a safety assessor does.

The next eight slides show one result per module along this thread.
-->

---

# 01 · A fully visible pedestrian is detected with 0.89 probability at 30 km/h braking distance, 0.51 at 50 km/h on a wet road

![h:470](nb:01_Perception/05_vulnerable_road_user_detection.ipynb#8cb95a2e)

<!-- _footer: "Source: notebook 01-05 · KITTI (CC BY-NC-SA 3.0) · torchvision Faster R-CNN (MobileNetV3)" -->

<!--
Recall of vulnerable road users against distance on real KITTI frames, with the stopping distances at 30 and
50 km/h on dry and wet roads.

At 30 km/h the stopping distance is 8.5–10.5 m, where the fitted recall is about 0.9 for fully visible
pedestrians. At 50 km/h it is 19–24.5 m, where recall is much lower. This one plot already contains the main
SOTIF question of Module 04: the detector works, but not far enough for the speed.
-->

---

# 03 · In the AEB hazard analysis, unintended braking is rated higher (ASIL D) than a missed pedestrian

![w:1100](nb:03_Functional_Safety_ISO26262/02_hara.ipynb#42776e9d)

<!-- _footer: "Source: notebook 03-02" -->

<!--
Four hazardous events of the AEB item, rated by severity, exposure and controllability.

Students usually expect the missed pedestrian to be the worst case. But the AEB is a driver assistance function:
the driver is still responsible and can brake (controllability). Unintended full braking on a road with
following traffic at about 1 s headway on a motorway (S3, E4, C3) cannot be controlled by most following
drivers: ASIL D. The pedestrian event HE-01 is rated S3/E2/C2, ASIL A; the stationary-traffic event HE-02 ASIL B.

Consequence for the whole course: every attempt to increase recall by lowering the detector threshold creates
false positives, which feed the ASIL D hazard. Safety goals: SG-01 (ASIL D) avoid unintended deceleration,
SG-02 (ASIL B in the capstone) avoid omission of braking.
-->

---

# 04 · Fog shortens the range in which the detector meets its requirement, and with it the safe speed

![w:1150](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#42b592ba)

<!-- _footer: "Source: notebook 04-02 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Physically based fog on real KITTI frames. In clear air the 65 % recall requirement holds to about 22 m, which
supports 49 km/h; in the densest fog tested, 15 m and 38 km/h.

This turns a triggering condition (fog) into a measure (an ODD restriction or a speed limit), which is the core
of ISO 21448. Module 04 deck, slides 17–18.
-->

---

# 05 · The threat analysis follows the same path from asset to decision as the hazard analysis

![w:1150](nb:05_Cybersecurity_ISO21434/02_tara.ipynb#a9d5b8d0)

<div class="take">In the capstone TARA of the perception-to-brake path, three threats are treated; one (TS-04) stays open and blocks the release.</div>

<!-- _footer: "Source: notebooks 05-02 and 08-05 · ISO/SAE 21434:2021, clause 15" -->

<!--
ISO/SAE 21434 clause 15: assets and damage scenarios → threat scenarios → impact rating → attack paths →
attack feasibility → risk value → risk treatment → cybersecurity goals and claims, with a CAL.

The parallel with the HARA is intended; Module 08-01 shows where the two analyses must be co-ordinated
(an attack that causes unintended braking violates SG-01).

CAL (cybersecurity assurance level) sets the rigour of the work, not the size of the risk. Module 05 explains
why this distinction matters.
-->

---

# 06 · A conformal interval holds 90 % on average, but not in every distance band

![w:1150](nb:06_AI_Safety_ISO_PAS_8800/05_conformal_prediction.ipynb#1b134345/1)

<div class="take">A fixed ±2.77 m band covers 100 % of near objects but only 72 % beyond 40 m; a relative (±10 %) band stays close to 90 % in every band.</div>

<!-- _footer: "Source: notebook 06-05 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Distance estimates of detected objects, with conformal prediction intervals calibrated on 4,945 objects.

Conformal prediction gives a guarantee on the marginal coverage (averaged over all test objects), not on each
subgroup. The far objects, which matter for the AEB at higher speed, are exactly where the absolute interval
fails. ISO/PAS 8800 asks for uncertainty evidence; Module 06 shows what that evidence does and does not
guarantee.
-->

---

# 07 · In ten real-traffic episodes, an RSS safety shield removes the collision and every TTC below 1.5 s

![w:1180](nb:07_Runtime_Assurance_and_Operations/02_safe_motion_planning_and_fallback.ipynb#7db35e35)

<div class="take">Nominal planner: 1 collision in 10 episodes, median minimum TTC 1.54 s. With the shield: no collision, 15.15 s.</div>

<!-- _footer: "Source: notebook 07-02 · NGSIM US-101 trajectories (US DOT, public domain)" -->

<!--
The RSS safe distance of Module 04-05 becomes a runtime component: a shield that overrides the planner when the
gap falls below d_min. Episodes are replayed in real NGSIM traffic around the ego vehicle.

Left: one point per episode. Middle and right: one episode in detail; the shield keeps the gap above the RSS
distance at the cost of harder braking (down to −4 m/s²).

The same module also covers the ODD monitor (07-01: hysteresis and dwell time cut 55 mode changes to 11), the
driver (07-03) and field data (next slide).
-->

---

# 07 · Field data: whether a robotaxi is safer than humans depends on the human benchmark chosen

![h:410](nb:07_Runtime_Assurance_and_Operations/05_field_safety_monitoring.ipynb#967f5529)

<div class="take">Waymo rider-only: 0.60 injury-reported crashes per million miles (Jul 2025 – Jun 2026); the reduction against humans ranges with the benchmark.</div>

<!-- _footer: "Source: notebook 07-05 · NHTSA Standing General Order reports, Waymo Safety Impact Data Hub (data as of the notebook run)" -->

<!--
Same numerator, four different human benchmarks: observed or adjusted, dynamic or overall. The point is not the
headline number but that the comparison depends on how exposure and outcome are matched (roads, vehicle types,
reporting thresholds).

The figures change monthly with new NHTSA data; the course website's field-safety page is refreshed every month.
Check the date before quoting a number.

Link to Module 04: this is the operation phase (ISO 21448 clause 13), where Area 3 scenarios are discovered.
-->

---

# 08 · The capstone measures PR-01 on 40 KITTI frames: recall falls with distance and occlusion

![w:1150](nb:08_Standards_Regulation_and_Safety_Case/05_capstone_aeb_from_requirement_to_release.ipynb#b43d7e56)

<div class="take">Within 33.1 m (stopping distance at 60 km/h): recall 0.745, one-sided lower bound 0.646 on 102 pedestrians, against a requirement of 0.90.</div>

<!-- _footer: "Source: notebook 08-05 · KITTI (CC BY-NC-SA 3.0) · torchvision Faster R-CNN (MobileNetV3)" -->

<!--
The capstone assembles every module's evidence for the pedestrian AEB: item and ODD, HARA and safety goals,
functional safety concept with a fault tree, the perception requirement PR-01 measured on 40 KITTI frames chosen
by rule, calibration and conformal evidence, TARA, validation target, GSN summary and release rules.

This slide is the perception evidence; the next one is the decision.
-->

---

<!-- _class: compact -->

# 08 · The release decision is DO NOT RELEASE, and the report says exactly why

| Rule | Criterion | Category | Result |
|---|---|---|---|
| R1–R3 | safety goals complete; FTA below the ASIL D target; mechanisms within FTTI | blocking | pass |
| R4 | PR-01 met in the ODD (≤ 60 km/h): lower bound 0.646 < 0.90 | ODD-restrictable | **fail** |
| R5 | score calibration ECE ≤ 0.05 on held-out frames (0.022) | advisory | pass |
| R6 | conformal recall threshold verified: 19 % of pedestrians never detected | advisory | **fail** |
| R7 | cybersecurity residual risks acceptable: TS-04 open | blocking | **fail** |
| R8, R9 | validation targets shown; scenarios cover the ODD pairwise | blocking | **evidence not yet produced** |

<div class="take">Even with R8 and R9 produced and positive, the decision stays DO NOT RELEASE because of R4, R6 and R7.</div>

<!-- _footer: "Source: notebook 08-05, section 9" -->

<!--
The decision is the correct outcome for a COCO-pretrained detector evaluated on 40 daytime frames. Students learn
more from a well-argued "no" than from a forced "yes".

Note the categories of failure: some are blocking, some can be resolved by an ODD restriction, some are advisory.
The release rule says in advance which is which, so the decision is not negotiated after the results are known.

The final project asks students to change one thing (class, speed, detector, threat) and argue the decision again.
-->

---

# The concepts are taught once and used again across the course

![w:1180](diagrams/concept_map.svg)

<!--
Each number is the count of notebooks in a module whose text uses the concept at least three times (computed
from the notebooks when the slides are built). The red frame marks where the concept is taught in depth.

Read it as a revision guide: a student who does not know what an ODD is will have trouble in seven of the eight
modules. The background slides at the start of each module deck point back to the teaching notebook.
-->

---

# Every notebook follows the same structure

<div class="cols3">
<div class="box">

### 1. Question
learning objectives; the standard clauses it relates to

### 2. Concept
the method, with the reasoning a reviewer would ask for

</div>
<div class="box">

### 3. Real data
KITTI, NGSIM, NHTSA, CAN logs; downloaded on demand

### 4. Computed result
figures and a printed text summary of every figure

</div>
<div class="box">

### 5. Exercises
auto-checked in many notebooks; answers checked by the toolkit

### 6. In industry, key takeaways
how the method is used in practice; self-assessment questions; references

</div>
</div>

<div class="take">The slides show the computed results (step 4). The lab works through steps 3 to 5.</div>

<!--
The printed text summary under each figure is deliberate: it makes every figure accessible to screen readers
and gives students a sentence to check their reading of the plot against.
-->

---

# The data are real and openly available; every source names its licence

| Data | Used for | Licence |
|---|---|---|
| KITTI object detection and tracking | detection, fog/low-light evaluation, OOD monitor, benchmark, capstone | CC BY-NC-SA 3.0 |
| NGSIM trajectories | trajectory prediction, end-to-end driving, safe planning | public domain (US DOT) |
| NHTSA Standing General Order crash reports | incidents, human factors, field monitoring | US government data |
| ROAD CAN intrusion dataset | CAN bus intrusion detection | CC BY 4.0 |
| VeReMi Extension (simulated V2X) | V2X misbehaviour detection | CC BY 4.0 |
| SOTIF-PCOD (optional, CARLA) | LiDAR detection in SOTIF conditions | see IEEE DataPort |

<!-- _footer: "Source: site/datasets.md" -->

<!--
KITTI is non-commercial (CC BY-NC-SA 3.0). Slides that show KITTI images carry the attribution in the footer;
keep it if you reuse a slide.

Synthetic data are used where real data cannot be shared or do not exist (e.g. the rare-event simulation in
04-04), and every such figure says so.
-->

---

# Suggested schedule: 14 weeks, one lecture and one lab per week

| Weeks | Module | Lab notebooks (core) |
|---|---|---|
| 1–3 | 01 Perception and Prediction, start of 02 | 01-01, 01-02, 01-04, 01-05, 01-09, 02-01 |
| 4 | 02 Failures and Robustness | 02-02, 02-03 |
| 5–7 | 03 Functional Safety (ISO 26262) | 03-01 to 03-06 · project milestone 1 (HARA) |
| 8–9 | 04 SOTIF (ISO 21448) | 04-01, 04-02, 04-05, 04-06 |
| 10–11 | 05 Cybersecurity, start of 06 | 05-01, 05-02, 05-04, 06-01, 06-02 · milestone 2 (TARA) |
| 12–13 | 06 AI Safety, 07 Operations | 06-04, 06-05, 06-08, 07-01, 07-02 |
| 14 | 08 Regulation and safety case | 08-04, 08-05 · final project |

<!-- _footer: "Source: site/teaching.md (5 ECTS; assessment: checked exercises 10 %, HARA/TARA project 40 %, final project 50 %)" -->

<!--
Full plan, learning outcomes, the five-day industry variant and the grading rubric are on the teaching page of
the course website. A 2.5 ECTS version keeps weeks 1, 5–10 and 14.
-->

---

# What students need before the first lab

<div class="cols">
<div>

**Required**
- Python with NumPy, pandas, Matplotlib
- probability: distributions, conditional probability, confidence bounds
- kinematics with constant acceleration
- a Google account (Colab) or a local Python 3.9 or newer

</div>
<div>

**Not required**
- a GPU or a driving stack
- access to the standards (paywalled; the notebooks teach the concepts with clause references)
- prior safety or security training

**Where gaps are closed:** each module deck starts with the background it needs and the notebook to revise.

</div>
</div>

<!--
The two background topics that cause most trouble in practice are confidence intervals on proportions and
stopping distance. Both get a refresher slide at the start of Module 04, and the first time they are used in
Module 01.
-->

---

# How to use these slides

- **Speaker notes** hold the explanation, the questions to ask and the common mistakes. Press **P** in the HTML version for presenter view; in PowerPoint they are in the notes pane.
- **Footers** name the notebook behind every figure; open it in Colab to show the computation live.
- **Rebuild** after re-running a notebook: `python scripts/build_slides.py --pdf --pptx`. The figures are taken from the committed notebooks, so the slides never drift from the results.
- **Adapt:** the decks are Markdown files in `slides/`; edit a title, reorder slides, or add your own.

<div class="take">One deck per module, plus this overview. A module deck covers one to three lectures.</div>

<!--
The PowerPoint export is image-based: each slide is a picture, with the speaker notes as text. For editable
slides in an institutional template, copy titles and figures from the Markdown source.
-->
