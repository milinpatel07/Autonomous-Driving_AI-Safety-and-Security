---
marp: true
theme: course
class: m04
paginate: true
size: 16:9
header: "Module 04 · SOTIF (ISO 21448)"
footer: "Autonomous Driving: AI Safety and Security · Milin Patel"
---

<!-- _class: title m04 -->
<!-- _paginate: false -->
<!-- _header: "" -->

# Module 04 · SOTIF (ISO 21448)
## Hazards without a fault: finding, measuring and limiting them

Six notebooks · about 45 slides · two lectures (weeks 8 and 9 of the 14-week plan)

<!--
Purpose of the module in one sentence: a system can be free of faults and still be unsafe, and ISO 21448 is the
standard that deals with that case.

Plan for the two lectures:
- Lecture 1 (week 8): notebooks 04-01 and 04-02. What SOTIF is, the four scenario areas, validation targets,
  triggering conditions measured on real KITTI frames.
- Lecture 2 (week 9): notebooks 04-03 to 04-06. Monitors, simulation, criticality metrics and RSS, the benchmark.

Every figure in this deck is an output of the notebooks. If a student asks "where does this number come from",
the footer names the notebook; the cell can be re-run in Colab.
-->

---

# This module answers the question in the orange box

![w:1120](diagrams/course_map_04.svg)

<!--
Show where we are. Modules 01 and 02 established how perception works and how it fails. Module 03 covered one
cause of harm: malfunctions (ISO 26262). Module 04 takes the second cause: the function works exactly as
designed, and the design is not good enough for the situation.

Ask the class: "The camera is healthy, the software has no bug, the pedestrian is not detected. Which standard
covers this?" Most students answer ISO 26262. That is the misconception this module removes.
-->

---

# What you bring from Modules 01–03, and where to revise it

| You need | Why it matters here | Revise in |
|---|---|---|
| Recall of a detector, measured on labelled frames | SOTIF requirements on perception are stated as recall | 01-04, 01-05 |
| A confidence interval on a measured proportion | 144 pedestrians do not give an exact recall | 01-05, slide 4 |
| Stopping distance from speed, reaction time, deceleration | it fixes the range in which detection matters | 01-05, slide 5 |
| Hazard, hazardous event, safety goal, ASIL | SOTIF reuses the hazard analysis of ISO 26262 | 03-02 |
| ODD (operational design domain) | the main measure SOTIF uses is to restrict it | 01-01 |
| Out-of-distribution input | basis of the runtime monitor in 04-03 | 02-03 |

<!--
Spend two minutes here. Students who missed Module 01 or 03 will be lost later without these six terms.
The next two slides refresh the two quantitative ones, because every result in this module depends on them.
-->

---

# A recall measured on 144 pedestrians is uncertain by about ±8 percentage points

![w:1050](diagrams/recall_interval.svg)

<div class="take">Read every recall in this module together with its interval. A requirement is met only if the lower bound is above it.</div>

<!--
Background slide. The curve is the half-width of the exact (Clopper–Pearson) 95 % interval as a function of the
number of labelled objects.

Three points to make:
1. With about 150 objects, a recall of 0.65 is known to roughly ±0.08. That is the sample size of notebook 04-02.
2. The interval shrinks with the square root of n: four times the data for half the width.
3. High recall is easier to pin down than medium recall (green curve below the orange one), but showing 0.99
   needs thousands of objects.

The decision rule used throughout: "meets" if the one-sided lower bound is above the requirement, "does not
meet" if the upper bound is below, otherwise "inconclusive". Inconclusive is a legitimate and frequent result.
-->

---

# The braking distance decides which pedestrians matter: at 60 km/h, those within 32 m

![w:1050](diagrams/stopping_distance.svg)

<div class="take">A recall averaged over all distances is not a safety statement. State it for the range the function needs.</div>

<!--
Background slide. Stopping distance = reaction distance + braking distance = v·t + v²/(2a).

With the parameters of notebook 04-02 (0.5 s system reaction, 6 m/s² deceleration) the AEB needs to see a
pedestrian 31.5 m ahead at 60 km/h; the notebook rounds up to 32 m. A wet road (4 m/s²) or a slower reaction
moves the range out quickly; this is why the derived requirement must name its assumptions.

The capstone (08-05) uses slightly different parameters and gets 33.1 m. Same method, different assumptions.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-01</span>

# ISO 21448: Safety of the Intended Functionality

- What does SOTIF cover, and what does it leave to ISO 26262 and ISO/SAE 21434?
- How are scenarios sorted into Areas 1–4?
- How much driving is needed to show that a residual risk is acceptable?
- What can be said about scenarios nobody has thought of?

<!--
Notebook 04-01 is mostly conceptual, with two computations: the validation target and the discovery curve.
Time: about 35 minutes of the first lecture.
-->

---

# ISO 26262 covers malfunctions; ISO 21448 covers a fault-free system that is still unsafe

![w:1000](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#6d25ca04)

<!-- _footer: "Source: notebook 04-01" -->

<!--
The two standards share one thing: the vehicle-level hazard list (centre). Everything else is split by cause.

- Left: E/E malfunctions. Random hardware faults and systematic hardware/software faults. Example: the camera
  ECU loses power.
- Right: functional insufficiencies. The specification is incomplete, or the performance is not enough, or the
  driver misuses the function in a foreseeable way. Example: a fault-free camera misses a pedestrian at dusk.
- Outside both: attacks, handled by ISO/SAE 21434 (Module 05).

Common mistake: calling a detector miss a "failure" in the ISO 26262 sense. Nothing failed; the detector did
what it was trained to do.
-->

---

# A hazard needs a triggering condition in the scenario and an insufficiency in the system

<div class="cols">
<div class="box">

### Triggering condition (in the scenario)
- dense fog, low sun, darkness
- pedestrian behind a parked car
- dirt on the camera window
- driver who keeps hands off the wheel

</div>
<div class="box">

### Functional insufficiency (in the system)
- **performance**: the detector's recall drops in fog
- **specification**: the function was never specified for children running out

</div>
</div>

**Causal chain:** triggering condition → functional insufficiency → hazardous behaviour → harm (if not controlled)

<div class="take">Fog alone is not a hazard. Fog plus a detector that cannot cope with fog is.</div>

<!--
This is the vocabulary of the rest of the module. ISO 21448:2022 (clause 3) distinguishes the two
insufficiency types; the notebook's register uses exactly these columns.

Exercise for the class: classify "AEB brakes for a plastic bag". Triggering condition: plastic bag on the
road. Insufficiency: performance (classification). Hazardous behaviour: unintended braking. Harm: rear-end
collision. Note the link to Module 03: unintended braking is the ASIL D hazard of the AEB item.
-->

---

# SOTIF work moves scenarios out of Areas 2 and 3 until the residual risk is acceptable

![h:470](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#6ea7b899)

<!-- _footer: "Source: notebook 04-01" -->

<!--
The four areas of ISO 21448 (known/unknown × hazardous/not hazardous).

- Area 2 (known, hazardous): treat it. Functional modification or ODD restriction moves the scenario to Area 1.
- Area 3 (unknown, hazardous): the dangerous one. Analysis, testing and field monitoring move scenarios from
  Area 3 to Area 2, where they can be treated.
- Area 4 (unknown, not hazardous): needs no action.

The goal is not an empty Area 3, which cannot be shown, but an argument that the residual risk from Areas 2 and
3 is below the acceptance criterion.
-->

---

# The ISO 21448 activity flow is a loop: unacceptable residual risk sends you back to clause 8

![w:1120](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#4e5aea1c)

<!-- _footer: "Source: notebook 04-01" -->

<!--
Clauses 5 to 13 of ISO 21448:2022. Walk the boxes once:
5 specification and design → 6 hazard identification and acceptance criteria → 7 insufficiencies and
triggering conditions → 8 functional modification → 9 verification and validation strategy → 10 known
scenarios → 11 unknown scenarios → 12 evaluation of SOTIF achievement → 13 operation phase.

Two feedback paths: from 12 back to 8 (residual risk not acceptable), and from 13 back to 5 (new triggering
conditions found in the field). Module 07 is about the second path.
-->

---

# Showing fewer than 1 hazardous event per 100,000 h needs about 300,000 h of event-free driving

![h:440](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#b2793fa3/1)

<div class="take">λ < 10⁻⁵ /h at 95 % confidence: 299,573 h with zero events, 775,366 h if three events occur (≈ 18 million km at 60 km/h).</div>

<!-- _footer: "Source: notebook 04-01" -->

<!--
This is the validation target of clause 6: the exposure needed to demonstrate an acceptance criterion.

With zero events, the upper 95 % bound of a Poisson rate is −ln(0.05)/T ≈ 3/T. Setting 3/T = 10⁻⁵ gives
T ≈ 300,000 h. Each observed event pushes the line up.

Point out the slope: one order of magnitude stricter criterion = one order of magnitude more driving. This is
why test driving alone cannot carry the argument, and why simulation (04-04) and scenario-based testing (04-02)
exist. Kalra and Paddock (2016) make the same argument in miles.

The 10⁻⁵ /h is an illustrative criterion, not a value from the standard. ISO 21448 asks for a criterion; it
does not set one.
-->

---

# The share of unknown scenarios cannot be measured, but the chance of meeting a new one can

![w:1150](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#3baddab7)

<div class="take">After 200,000 encounters the Good–Turing estimate is 6.96 % that the next one is new; the true "coverage" (57 %) is unknowable outside a simulation.</div>

<!-- _footer: "Source: notebook 04-01 (synthetic data with 50,000 scenario classes)" -->

<!--
Left: the number of distinct scenario classes keeps rising. Without knowing the total (dashed line, known here
only because the data are synthetic) no one can say what fraction has been seen.

Right: the Good–Turing estimate N1/N (share of classes seen exactly once) tracks the true probability that the
next encounter is new. This is a statement that can be made from data, and it is the honest replacement for
"we covered 95 % of scenarios".

Link: Module 07 (field monitoring) is where these encounters are collected after release.
-->

---

# One hazard list, one architecture, one safety case: the two standards run in parallel

![h:480](nb:04_SOTIF_ISO21448/01_sotif_fundamentals.ipynb#a5c8e623)

<!-- _footer: "Source: notebook 04-01" -->

<!--
In practice the same team does both. The dashed links are the integration points: a shared hazard list,
consistent targets, one architecture with traceable requirements, a coordinated test plan, one safety case.

Module 08-01 returns to this with all four standards.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-02</span>

# Triggering conditions and scenario-based evaluation

- How is a triggering-condition catalogue structured?
- How much does fog, darkness or dirt reduce the recall of a real detector on real frames?
- How does a measurement become an ODD restriction?
- What does scenario coverage say about residual risk, and what does it not?

<!--
The core notebook of the module. It measures a real torchvision detector on 30 KITTI frames with 185 labelled
pedestrians under physically based fog, low light and lens dirt. About 45 minutes.
-->

---

# 32 triggering conditions, sorted by the 6-layer model; faults and attacks are kept out

![h:480](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#8e4bb936)

<!-- _footer: "Source: notebook 04-02 · 6-layer model: Scholtes et al. (2021)" -->

<!--
The 6-layer model (road network, roadside structures, temporary modifications, dynamic objects, environment,
digital information) gives a checklist so that whole categories are not forgotten. The notebook adds sensor
exposure and driver behaviour/misuse.

Equally important is what the catalogue excludes: 5 E/E faults (ISO 26262) and 3 security items (ISO/SAE 21434)
were moved out. Mixing causes in one table is a common review finding.
-->

---

# Fog is added per pixel from LiDAR depth, so distant objects fade first

![w:1150](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#f4ca3fc3)

<!-- _footer: "Source: notebook 04-02 · KITTI frame 004704 (CC BY-NC-SA 3.0)" -->

<!--
Koschmieder's law: transmission t = exp(−3d/V), with d the distance to the object and V the meteorological
visibility (the distance at which contrast drops to 5 %). Depth comes from the KITTI LiDAR scan, densified.

Why this matters: a uniform contrast reduction would make near and far pedestrians equally hard. Real fog hurts
far objects first, and that is exactly what moves the detection range.

Limitation to state: the model has no scattering blur, no headlight glare, no droplets. It is a model of fog,
not real fog. The benchmark (04-06) repeats this warning.
-->

---

# Pedestrian recall falls from 0.77 in clear air to 0.52 at 25 m visibility

![h:450](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#9c269d98/1)

<div class="take">The 65 % requirement is met in clear air, clearly violated at V = 25 m, and inconclusive in between (144 pedestrians per level).</div>

<!-- _footer: "Source: notebook 04-02 · KITTI (CC BY-NC-SA 3.0) · torchvision Faster R-CNN (MobileNetV3)" -->

<!--
Each point: recall of pedestrians within 32 m (the AEB range from slide 5), with its 95 % interval.

How to read it:
- Clear air: lower bound above 65 % → meets.
- V = 25 m: upper bound below 65 % → does not meet. This is a performance insufficiency, measured.
- V = 300 to 40 m: the interval contains 65 % → inconclusive. More data, not more opinion, resolves it.

Cars (orange) have only about 13 instances per point: the intervals are so wide that nothing can be concluded.
That is the right answer, not a failure of the method.

The 65 % is an illustrative derived requirement for the notebook. The capstone uses 90 % (PR-01).
-->

---

# Even in clear air the requirement holds only to about 22 m: that supports 49 km/h, not 60

![w:1150](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#42b592ba)

<div class="take">The measurement becomes an ODD restriction: 49 km/h in clear air, about 38 km/h in the densest fog tested.</div>

<!-- _footer: "Source: notebook 04-02 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Left: fitted detection probability against distance, one curve per visibility. The dashed line is the 65 %
requirement; where a curve crosses it is the range the evidence supports.

Right: the highest speed whose stopping distance fits inside that range.

The lesson: the range-aggregated recall of the previous slide (0.77 in clear air, "meets") hides that recall at
25–32 m is below the requirement. A requirement should be stated per distance band, otherwise near pedestrians
pay for far ones.

This is clause 8 of ISO 21448 in practice: restrict the ODD (or the speed) to where the evidence holds.
-->

---

# Darkness and lens dirt are triggering conditions for the same detector

![w:1180](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#cb7428eb/1)

<div class="take">Recall falls from 77 % to 27 % at 1/256 of daylight exposure; behind a dirt blob it is 51 % against 69 % beside it.</div>

<!-- _footer: "Source: notebook 04-02 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Low light is simulated with a Poisson–Gaussian sensor noise model (Foi et al., 2008): less light, then gain,
so noise dominates. Lens dirt is a defocused blob covering 25 % of the image.

Note for the dirt result: the average over the image would hide the effect. The relevant comparison is a
pedestrian behind the dirt against one beside it. The benchmark report (04-06) splits it the same way.
-->

---

# Fog also removes LiDAR returns: points per pedestrian fall from 112 to 30 at V = 25 m

![w:1100](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#ca70826d/1)

<div class="take">Camera and LiDAR degrade under the same condition, so LiDAR is not an independent confirmation in dense fog.</div>

<!-- _footer: "Source: notebook 04-02 · KITTI frame 004704 (CC BY-NC-SA 3.0)" -->

<!--
Same frame, attenuation model applied to the real scan: 56,395 returns in clear air, 43,005 at V = 35 m, and
far returns disappear first, as for the camera.

Connection to Module 03: an ASIL decomposition or a redundancy argument assumes independence. A common
triggering condition (fog) breaks that independence. This is a dependent-failure argument, now on the SOTIF side.

The model omits backscatter (false near returns), which real fog adds; Hahner et al. (2021) model it.
-->

---

# The measurements become an entry in the SOTIF analysis

| Condition | Measured effect | Measure (clause 8) | Verification |
|---|---|---|---|
| Dense fog | recall ≤ 32 m: 77 % → 52 % at V ≤ 25 m | speed limit ≈ 38 km/h below the boundary; visibility estimation | real-fog data or fog chamber; closed-loop AEB test |
| Night, unlit road | 77 % → 27 % at 1/256 exposure | low-light training data, radar confirmation | night drives with labelled pedestrians |
| Dirt on lens | 69 % beside, 51 % behind dirt | blockage detection and cleaning; degrade and inform | detector rate on dirty/clean sets |
| Occluded pedestrian | 84 % visible → 40 % largely occluded | lower speed next to parked cars; tracking | occlusion scenarios in simulation and proving ground |
| Dense fog, LiDAR | 112 → 30 points per pedestrian | do not count LiDAR as independent in fog | real-fog LiDAR data |

<!-- _footer: "Source: notebook 04-02, section 5.7" -->

<!--
This is the format used in industry triggering-condition analyses: condition, parameter range, measured
effect, measure, verification.

Three properties make it useful to an assessor, and all three come from measurement: the boundary is stated
with its uncertainty, the effect is quantified on the component that will be released, and every row says how
it will be verified.

What it does not show: whether the vehicle is hazardous at the boundary (needs closed-loop evaluation, clause 10)
and which conditions are missing from the catalogue (Area 3, clause 11).
-->

---

# A scenario is described at three levels; tests are run on concrete scenarios

![w:1150](diagrams/scenario_levels.svg)

<div class="take">The ODD says where the function may operate (ISO 34503); a scenario says what happens there (ISO 34502).</div>

<!--
Functional → logical → concrete (Menzel et al., 2018). A logical scenario is a parameter space; a concrete
scenario is one point in it. Simulation tools take concrete scenarios, written for example in ASAM OpenSCENARIO.

Students often confuse ODD and scenario. ODD: "urban roads, ≤ 60 km/h, daylight and dusk, dry or wet". Scenario:
"pedestrian steps out behind a parked car while the ego vehicle drives at 50 km/h". The ODD constrains which
scenarios must be evaluated.
-->

---

# 15 well-chosen tests cover every pair of parameter values; random sampling needs about 60

![h:450](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#9d49d5bd/1)

<!-- _footer: "Source: notebook 04-02" -->

<!--
The logical scenario of the notebook has 648 concrete scenarios, 432 of them physically valid. 2-wise
(pairwise) coverage asks: has every pair of parameter values appeared together in at least one test?

The greedy pairwise suite (stars) reaches 100 % 2-wise coverage with 15 tests and 65 % 3-wise coverage. Random
sampling needs about 60 tests for full pairwise coverage.

Pairwise testing is efficient because many failures are caused by one or two interacting parameters. Not all:
the notebook finds 36 hazardous scenarios caused by interactions of three or more parameters.
-->

---

# After the pairwise suite, 417 of 432 valid scenarios are still not evaluated

![h:400](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#2c086d1f)

<div class="take">100 % pairwise coverage is a statement about the test design, not about residual risk.</div>

<!-- _footer: "Source: notebook 04-02" -->

<!--
The 15 tests sort 10 scenarios into Area 1 and 5 into Area 2. Everything else is "known, not yet evaluated".
Area 3 and 4 are not on this chart at all: they lie outside the parameter space that was defined.

Ask: "What would you report to a project manager who asks whether the scenario space is covered?" Good answer:
"Every value pair is tested; 5 hazardous combinations found; 417 scenarios are unevaluated; scenarios outside
the parameterisation are not addressed by this test."
-->

---

# Simulation, proving ground and public road answer different questions

![h:470](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#1394aa66)

<!-- _footer: "Source: notebook 04-02 (orders of magnitude indicative)" -->

<!--
More scenarios at the bottom, more realism at the top. Analysis (HARA, STPA, FMEA, formal methods) spans all
layers. A validation strategy (clause 9) assigns each question to the cheapest environment that can answer it
credibly, and states how the environments are correlated. Notebook 04-04 is about that credibility.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-03</span>

# OOD monitoring as a SOTIF safety measure

- Where does a runtime monitor sit in the ISO 21448 causal chain?
- Which signal from a real detector reveals degraded conditions?
- How is the threshold set from a safety requirement, and what does it cost in availability?

<!--
Start of the second lecture. Recap in one sentence: 04-02 found conditions where the detector is not good
enough. 04-03 asks: can the vehicle notice, at runtime, that it is in such a condition?
-->

---

# A monitor turns "the detector is not good enough here" into a detectable event

![w:1150](nb:04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb#c1a0ad72)

<!-- _footer: "Source: notebook 04-03" -->

<!--
The monitor sits between the perception model and the decision. Its threshold comes from a safety requirement
(R-MON-1: detect at least 90 % of degraded frames); its false-alarm rate decides availability.

The event log feeds back into SOTIF: every alarm in the field is a candidate triggering condition. This is how
Area 3 scenarios are discovered after release (clause 13, Module 07).

Link to Module 02-03: there, OOD detection was evaluated on digits. Here it is used on a real detector, with a
requirement.
-->

---

# Feature-space distance separates degraded from adequate frames (AUROC 0.98)

![w:1180](nb:04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb#c36dede6)

<!-- _footer: "Source: notebook 04-03 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Six candidate signals were extracted from the detector: low top scores, proposal entropy, low-confidence boxes,
energy, feature norm, and the k-nearest-neighbour distance of the backbone features to clear-weather frames.

"Degraded" is defined by the requirement, not by eye: the conditions where pedestrian recall within 32 m is
demonstrably below 65 % (fog 25 m and low light 1/256).

The signal was selected on calibration frames and checked on held-out test frames (AUROC 0.98 on both). Selecting
and reporting on the same frames would overstate it.
-->

---

# On a real tunnel entry the alarm is raised 0.2 s after the first dark frame

![w:1100](nb:04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb#f628d1ae)

<div class="take">16/16 dark frames flagged; the 3-of-5 filter suppresses 3 isolated flags in 2.4 s of normal driving.</div>

<!-- _footer: "Source: notebook 04-03 · KITTI tracking sequence 0015 (CC BY-NC-SA 3.0)" -->

<!--
A real sequence, not a perturbation. Top: the monitor signal; it jumps when the image goes dark. Bottom: single
frames flagged (grey) and the alarm after temporal filtering (black, 3 of the last 5 frames).

Filtering trades latency for fewer false alarms. 0.2 s is short compared with a 300 ms FTTI only if the
fallback is fast; that is a system question.

Be honest about the limit: 2.4 s of normal driving says nothing about false alarms per hour.
-->

---

# Detecting 90 % of degraded frames costs 7 % false alarms on clear frames

![h:450](nb:04_SOTIF_ISO21448/03_ood_monitoring_as_safety_measure.ipynb#daa05956)

<div class="take">Before filtering that is about 2,400 flagged clear frames per hour: a safety-versus-availability decision to record, not to hide.</div>

<!-- _footer: "Source: notebook 04-03" -->

<!--
The ROC curve read as a decision: the requirement (dashed line, TPR ≥ 90 %) fixes the threshold, and the
false-positive rate is the price.

Options to record in the SOTIF analysis when the price is too high: a better signal (combine signals, add a
visibility or exposure sensor), temporal filtering, or a milder reaction (warning instead of MRM).

A monitor that is never allowed to cost availability will be tuned until it detects nothing.
-->

---

# The reaction to an alarm depends on who is responsible for the fallback

| | L2 (driver supervises) | L3 (driver is fallback-ready) | L4 (no driver needed) |
|---|---|---|---|
| On alarm | hands-on request, function degrades with a message | transition demand; MRM if no takeover | minimal risk manoeuvre |
| Time budget | immediate (driver is monitoring) | takeover time, e.g. several seconds | the system must cope alone |
| Monitor requirement | warning reliability | must detect before the takeover time runs out | must detect and act within the ODD |

<div class="take">The same monitor signal needs a different requirement at each level of automation.</div>

<!-- _footer: "Source: notebook 04-03, section 7 · SAE J3016 (2021)" -->

<!--
The notebook replays the darkness episode with three reaction policies. At L2 the reaction is mostly a message;
at L3 it is a transition demand followed by a minimal risk manoeuvre if the driver does not take over (UN R157
for ALKS defines this sequence); at L4 the vehicle itself must reach a minimal risk condition.

Link: Module 07-01 and 07-02 implement the fallback; 07-03 covers takeover time and the driver.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-04</span>

# Simulation-based SOTIF validation

- What can simulation show, and when can its results be trusted?
- How are perception results traced to vehicle-level acceptance criteria?
- How can a 10⁻⁵ event be estimated without 10⁷ runs?

<!--
Note on data: the notebook is built for the SOTIF-PCOD data set (CARLA, 21 weather and time-of-day conditions).
If the data set is not downloaded, it uses a synthetic performance model with the same 21-condition structure.
The figures here are from the synthetic model; say so in the lecture.
-->

---

# A sensor model decides what simulation can show: rain removes far returns and adds near clutter

![w:1180](nb:04_SOTIF_ISO21448/04_simulation_based_validation.ipynb#2d51445b)

<!-- _footer: "Source: notebook 04-04 (toy LiDAR model)" -->

<!--
Three vehicles at 15, 35 and 55 m. Clear: all returns. Medium rain: fewer far returns, clutter near the sensor.
Heavy rain: the 55 m vehicle almost disappears (10 of 150 returns).

The point: if the simulator's rain model does not do this, simulation in rain proves nothing about rain. The
sensor model is part of the evidence and needs its own validation (next slides).
-->

---

# In the 21-condition campaign, only heavy rain brings recall clearly below the requirement

![w:1150](nb:04_SOTIF_ISO21448/04_simulation_based_validation.ipynb#f633dd2c/1)

<div class="take">3 of 21 conditions are candidate triggering conditions (all heavy rain); 7 detector–condition pairs need more samples.</div>

<!-- _footer: "Source: notebook 04-04 (synthetic performance model with the SOTIF-PCOD structure)" -->

<!--
Same decision rule as in 04-02: candidates are conditions where the upper bound of recall is below the derived
requirement. They are candidates, to be confirmed in closed loop, because recall is a component metric and the
acceptance criterion is at vehicle level.

A common error to name: treating an AP threshold as an "ISO criterion". ISO 21448 sets no perception metric; the
team derives one from the vehicle-level acceptance criterion and must justify the derivation.
-->

---

# Simulation evidence can be used only where it agrees with real data

| Condition | Simulation vs real recall (tolerance ±0.05) | Use of simulation evidence |
|---|---|---|
| ClearNoon | agrees | usable |
| CloudySunset | agrees | usable |
| ClearNight | agrees | usable |
| MidRainNoon | disagrees | not usable unadjusted |
| HardRainNoon | inconclusive | collect more real data first |

<div class="take">Credibility is assessed per condition, and it is weakest exactly where the triggering conditions are.</div>

<!-- _footer: "Source: notebook 04-04, section 4" -->

<!--
A sim-to-real correlation check: the same detector on paired real and simulated conditions.

Credibility has three parts in practice: the sim-to-real gap (this table), tool confidence (ISO 26262-8 tool
qualification) and the credibility assessment of the virtual toolchain as asked for by type approval
(Regulation (EU) 2022/1426 for automated driving systems).

The uncomfortable result: rain, the condition we most want to simulate, is where agreement is worst.
-->

---

# Importance sampling estimates a 10⁻⁵ event with about 1,600 times fewer runs

![w:1150](nb:04_SOTIF_ISO21448/04_simulation_based_validation.ipynb#6311cad9)

<div class="take">±10 % precision: 40.7 million naive runs or 25,969 importance-sampled runs. The estimated 1.39 × 10⁻⁵ /h does not meet the 10⁻⁵ /h criterion.</div>

<!-- _footer: "Source: notebook 04-04" -->

<!--
Cut-in scenario with two parameters: gap at cut-in and closing speed. Left: naive Monte Carlo with naturalistic
parameters, 0 collisions in 3,000 runs. Right: a proposal distribution shifted towards the collision boundary,
764 collisions in 3,000 runs; each sample is weighted by the ratio of densities, so the estimate is unbiased.

The result is a probability per cut-in (9.43 × 10⁻⁶), converted to a rate per hour with the cut-in frequency.
The criterion is not met, so the conclusion is a functional modification, not more testing.

Distinguish: coverage-oriented sampling (find all behaviours) and distribution-oriented sampling (estimate a
rate). Importance sampling is the second kind.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-05</span>

# Criticality metrics and Responsibility-Sensitive Safety

- What do TTC, THW, DRAC and PET measure, and when are they wrong?
- What is the RSS safe distance, and which assumptions does it rest on?
- Does following RSS prevent collisions in a cut-in?

<!--
The notebook moves from perception to behaviour: how close was a situation to a collision, and what is a safe
distance. Students need constant-acceleration kinematics.
-->

---

# Constant-speed metrics react late: TTC warns 0.74 s after required deceleration does

![w:1180](nb:04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb#82d98214)

<div class="take">Lead brakes at 1.0 s; required deceleration exceeds 5 m/s² at 1.3 s, TTC drops below 3 s at 2.04 s, DRAC exceeds 5 m/s² at 3.41 s; collision at 4.31 s.</div>

<!-- _footer: "Source: notebook 04-05" -->

<!--
Definitions: TTC = gap / closing speed (assumes both keep their speed); THW = gap / own speed; DRAC = deceleration
needed to avoid the collision assuming the lead keeps its speed; required deceleration assumes the lead keeps
braking.

The metric that knows the lead is braking reacts first. TTC and DRAC assume constant speed and are late by
0.7–2.1 s. Every metric carries an assumption; a threshold on a metric is only as good as that assumption.

Also: TTC is infinite when the vehicles are not closing, and longitudinal metrics are blind to lateral
conflicts (PET in the notebook covers crossing conflicts).
-->

---

# Starting at the RSS distance the worst case ends at zero gap; at 90 % of it, in a collision

![w:1180](nb:04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb#022e4d5d)

<!-- _footer: "Source: notebook 04-05 · RSS: Shalev-Shwartz et al. (2017)" -->

<!--
RSS longitudinal safe distance: the rear car may accelerate with a_max during its response time ρ and then
brakes with at least b_min; the front car brakes with at most b_max. d_min is the gap that survives this worst
case.

The numerical check confirms the formula: from 100 % of d_min (86.8 m at 100 vs 80 km/h) the minimum gap is
0.00 m; from 90 % it is −8.68 m, a collision. RSS is tight, not conservative, under its own assumptions.

Default parameters give 22.8 m at 50 km/h (1.65 s time gap) and 69.4 m at 100 km/h (2.5 s).
-->

---

# The assumed braking of the rear car dominates: 0.5 m/s² less adds 14.8 m at 100 km/h

![w:1180](nb:04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb#75306da2)

<!-- _footer: "Source: notebook 04-05" -->

<!--
Heat maps of d_min over response time ρ and the braking parameters. One-at-a-time sensitivity at 100 km/h:
b_min −0.5 m/s² → +14.8 m; ρ +0.1 s → +4.3 m; b_max +0.5 m/s² → +2.8 m; a_max +0.5 m/s² → +1.9 m.

These parameters are not given by RSS; they are design choices that must be justified (IEEE 2846-2022 is a
standard about exactly such assumptions). A guaranteed braking b_min also has to hold on a wet road.
-->

---

# Safety costs throughput: the default RSS parameters need 1.65 s at 50 km/h and 2.5 s at 100 km/h

![w:1180](nb:04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb#c82582e4)

<!-- _footer: "Source: notebook 04-05" -->

<!--
Three parameter sets. "Assertive" gives 0.5–0.8 s time gaps (shorter than the 2-second rule), "cautious" 3.8–6.3 s.
The right panel converts the gap into an upper bound on lane throughput.

This is the safety–usefulness trade-off: a cautious envelope that nobody wants to drive behind is not a
solution, and an assertive one has to be justified with real braking capability.
-->

---

# Over 99 cut-ins, naive control collides in 60 and RSS in 22; RSS is never worse

![w:1180](nb:04_SOTIF_ISO21448/05_criticality_metrics_and_rss.ipynb#808409b6/1)

<div class="take">13 of the 22 RSS collisions start from a gap the cut-in vehicle made unsafe; in the other 9 the lead brakes harder than RSS assumes.</div>

<!-- _footer: "Source: notebook 04-05" -->

<!--
Grid over the initial cut-in gap g0 and the lead's braking. Left: adaptive cruise (1.0 s) plus AEB; right: the
RSS proper response.

Read the remaining RSS collisions carefully:
- 13 of them: the cut-in vehicle created the dangerous situation laterally. RSS assigns responsibility to it.
  RSS guarantees the ego vehicle does not cause a collision under the assumptions, not that it is never involved.
- 9 of them: the lead brakes harder than b_max, so an assumption is violated.
- At g0 ≤ 15 m both collide whatever happens: no longitudinal controller can help.

There is no cell where RSS collides and the naive controller does not.
-->

---

<!-- _class: notebook m04 -->
<!-- _footer: "" -->

<span class="nb">NOTEBOOK 04-06</span>

# An open SOTIF perception benchmark

- How do you compare detectors on SOTIF conditions in a way others can reproduce?
- How does the same measurement lead to different release decisions under different requirements?
- What can such a benchmark claim, and what not?

<!--
04-02 analysed one detector. The benchmark fixes every choice in advance (frames by rule, ignore regions, one
declared threshold, versioned specification with a hash) so that any detector can be evaluated the same way.
It is also available as a command-line tool and a CI regression gate.
-->

---

# Eight conditions, applied identically to every detector

![h:490](nb:04_SOTIF_ISO21448/06_sotif_benchmark.ipynb#c7b47235)

<!-- _footer: "Source: notebook 04-06 · KITTI frame 006761 (CC BY-NC-SA 3.0)" -->

<!--
Clear, fog at V = 200, 100, 50, 25 m, low light at 1/64 and 1/256, lens dirt covering 25 %. Random elements are
seeded per frame, so every detector sees exactly the same pixels.

Fog transmission at V = 50 m: 0.55 at 10 m, 0.22 at 25 m, 0.05 at 50 m. The 5 % at d = V is the definition of
meteorological visibility.

120 frames chosen by a rule (at least two pedestrians within 40 m, fixed seed), not by hand.
-->

---

# Recall falls with distance and with occlusion; occlusion cannot be removed by restricting the ODD

![w:1180](nb:04_SOTIF_ISO21448/06_sotif_benchmark.ipynb#99b016fe)

<div class="take">Clear air: recall 0.70 at 0–10 m, 0.12 beyond 40 m. Largely occluded pedestrians are rarely detected even in clear air.</div>

<!-- _footer: "Source: notebook 04-06 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
Left: recall per distance band for four fog levels; fog removes distant pedestrians first, as Koschmieder's law
predicts. Right: occlusion and truncation in clear air.

Fog can be handled by an ODD restriction plus a visibility monitor. Occlusion by parked cars cannot be excluded
from urban driving; it needs a functional measure (lower speed next to parked cars, tracking of partly visible
objects). This is the difference between the two kinds of measure in clause 8.
-->

---

# The same measurement gives three release decisions under three requirements

![w:1180](nb:04_SOTIF_ISO21448/06_sotif_benchmark.ipynb#66519919)

<div class="take">Against the 65 % requirement (TC-04-02) clear air supports 35 km/h; against PR-01 (90 % within 33.1 m) no speed is supported.</div>

<!-- _footer: "Source: notebook 04-06" -->

<!--
Bars: highest speed whose stopping distance the evidence covers, per condition, for three requirements. PR-01 is
the capstone requirement (recall ≥ 0.90, 95 % one-sided, within the stopping distance at 60 km/h).

Two details:
- "No supported speed" can mean insufficient performance or insufficient evidence. With fewer than 29
  pedestrians even a perfect detector cannot show 0.90 at 95 % confidence (0.05^(1/n)).
- Fog at V = 50 m supports a higher speed than clear air. That is sampling noise at the boundary (one grid
  step, inside the intervals), not evidence that fog helps.

The requirement must be declared before the test and stored with the result.
-->

---

# Faster R-CNN finds about 43 % of pedestrians in clear air; SSDlite at its declared threshold almost none

![w:1150](nb:04_SOTIF_ISO21448/06_sotif_benchmark.ipynb#63243d9f)

<div class="take">Lowering the threshold from 0.5 to 0.3 adds 5 points of recall and 1.6 false positives per frame. In the AEB, the false positive is the ASIL D hazard.</div>

<!-- _footer: "Source: notebook 04-06 · KITTI (CC BY-NC-SA 3.0)" -->

<!--
SSDlite resizes the input to 320 × 320, so a pedestrian 30 m away covers a few pixels, and its scores are lower.
At threshold 0.1 it finds about a third of the pedestrians, with dozens of false positives per frame.

The threshold is part of the submitted system. Choosing it after seeing the results is what the benchmark's
threshold policy forbids.

Link to Module 03: in the AEB item, unintended braking (SG-01) is ASIL D and the missed pedestrian (SG-02) is
ASIL B. A detector that wins on recall by lowering its threshold can lose the safety argument.
-->

---

# What the benchmark can show, and what it cannot

| It can show | It cannot show |
|---|---|
| how a detector degrades under documented models of fog, low light and dirt, on real images and labels | how it behaves in real fog, night or rain: KITTI has none |
| recall per condition with honest intervals | vehicle-level safety: it measures a component |
| whether an update is a regression (CI gate) | conditions that are not in the specification (Area 3) |
| which ODD restriction the evidence supports | that 120 frames represent a city: about 250 pedestrians in the PR-01 scope suffice only for a detector with true recall ≈ 0.95 |

<!-- _footer: "Source: notebook 04-06, section 7" -->

<!--
Ask students to fill in a row of their own before showing the table. The honest list of limits is part of the
result; a benchmark that hides it is advertising.

A real campaign needs thousands of labelled instances per condition, real adverse-weather data (for example
nuScenes night and rain scenes, SOTIF-PCOD for LiDAR in simulation) and closed-loop tests.
-->

---

# What Module 04 hands to the next modules

<div class="cols">
<div>

- **→ 05 Cybersecurity:** the 3 attack items excluded from the triggering-condition catalogue are analysed in the TARA
- **→ 06 AI safety:** the detector's insufficiencies are ML-specific; ISO/PAS 8800 adds data and uncertainty evidence
- **→ 07 Operations:** the monitor of 04-03 and the ODD restriction of 04-02 run in the vehicle; field data feed clause 13

</div>
<div>

- **→ 08 Safety case:** PR-01, the benchmark result and the supported speed are evidence in the capstone and the GSN argument
- **Carried forward:** validation target (06-08, 07-05), Areas 1–4 (07-05), RSS (06-07, 07-02)

</div>
</div>

<div class="take">SOTIF gives the method; Modules 05–08 add the other causes, the runtime measures and the argument.</div>

<!--
Close the module with the course map in mind. The AEB example continues: in 06 the same detector gets
calibration and conformal evidence, in 07 the monitor and field indicators, in 08 everything is assembled and
the release decision is DO NOT RELEASE, with reasons.
-->

---

# Terms of this module

<div class="cols small">
<div>

- **Functional insufficiency:** specification or performance insufficiency of the intended function
- **Triggering condition:** a scenario condition that, together with an insufficiency, leads to hazardous behaviour
- **Areas 1–4:** known/unknown × hazardous/not hazardous scenarios
- **Acceptance criterion:** the residual-risk level the argument must show, e.g. events per hour
- **Validation target:** the exposure needed to demonstrate the acceptance criterion

</div>
<div>

- **ODD restriction:** limiting where or how the function operates so that the evidence covers it
- **n-wise coverage:** share of all value combinations of n parameters that appear in the tests
- **OOD monitor:** runtime check that the input differs from what the component was validated on
- **Importance sampling:** sampling from a shifted distribution and reweighting, to estimate rare events
- **RSS safe distance:** the gap that survives the worst case under stated braking and response assumptions

</div>
</div>

<!--
Use as a revision slide or hand-out. Full definitions are in the course glossary (site/glossary.md).
-->

---

# Exercises and discussion

1. **Validation target (04-01):** the acceptance criterion is tightened to 10⁻⁶ /h. How many event-free hours are needed now? What does one observed event change?
2. **Triggering-condition table (04-02):** write the table row for "low sun in front of the camera". Which measure is a functional modification, which an ODD restriction?
3. **Monitor (04-03):** the team cannot accept 2,400 flagged frames per hour. Name three options and what each costs.
4. **RSS (04-05):** a truck follows a car. Which RSS parameters change, and in which direction does d_min move?
5. **Benchmark (04-06):** why does "no supported speed" not always mean that the detector is bad?

<!--
Questions 1 and 4 correspond to auto-checked exercises in the notebooks (04-01 exercise 1, 04-05 exercise 5).
Question 2 extends the notebook's LKA exercise. Answers to 1: about 3.0 million hours with zero events; one
event raises the requirement to about 4.7 million hours (Poisson upper bound with k = 1).
-->

---

# References

<div class="small">

- ISO 21448:2022 *Road vehicles — Safety of the intended functionality.*
- ISO 26262:2018 *Road vehicles — Functional safety*; ISO/SAE 21434:2021; ISO/PAS 8800:2024.
- ISO 34502:2022 *Scenario based safety evaluation framework*; ISO 34503:2023 *Specification for operational design domain.*
- IEEE 2846-2022 *Assumptions in safety-related models for automated driving systems.*
- Kalra, N., Paddock, S. M. (2016). Driving to safety. *Transportation Research Part A* 94, 182–193.
- Menzel, T., Bagschik, G., Maurer, M. (2018). Scenarios for development, test and validation of automated vehicles. *IEEE IV*, 1821–1827.
- Scholtes, M. et al. (2021). 6-Layer model for a structured description and categorization of urban traffic and environment. *IEEE Access* 9, 59131–59147.
- Shalev-Shwartz, S., Shammah, S., Shashua, A. (2017). On a formal model of safe and scalable self-driving cars. arXiv:1708.06374.
- Sakaridis, C., Dai, D., Van Gool, L. (2018). Semantic foggy scene understanding with synthetic data. *IJCV* 126, 973–992.
- Geiger, A., Lenz, P., Urtasun, R. (2012). Are we ready for autonomous driving? The KITTI vision benchmark suite. *CVPR*, 3354–3361.
- Patel, M., Jung, R., Khatun, M. (2025). A systematic literature review on safety of the intended functionality for automated driving systems. SAE Technical Paper 2025-01-5030.

</div>

<!--
Full reference lists with DOIs are at the end of each notebook and in references/normative.yaml.
-->
