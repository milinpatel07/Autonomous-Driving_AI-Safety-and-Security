# Exercise 8: Design a Complete Validation Strategy

**Session 4: Uncertainty Estimation and Validation**
**Duration:** 60 minutes
**Difficulty:** Advanced

## Objectives

By the end of this exercise, you will:
- Design a comprehensive validation plan for an AV perception system
- Define scenario space using Pegasus 6-layer model
- Create test cases covering ODD boundaries
- Define pass/fail criteria aligned with safety requirements
- Calculate statistical evidence requirements
- Plan field testing approach
- Connect to ISO 26262 V&V requirements

---

## Scenario

You are the **Safety Validation Lead** for an autonomous shuttle project:

**System Details:**
- **Application:** Campus shuttle service
- **ODD:** University campus, <25 mph, daylight and dusk, dry and light rain
- **Perception System:** Multi-camera + LiDAR for pedestrian/cyclist/vehicle detection
- **Safety Goal:** No collisions with vulnerable road users (ASIL-D)
- **Deployment Target:** 6 months from now

**Your task:** Design the complete validation strategy to demonstrate the system is safe for deployment.

---

## Part 1: Define Scenario Space (15 min)

### Task 1.1: Apply Pegasus 6-Layer Model

Define scenarios at each abstraction level:

#### Layer 6: Operational Design Domain (ODD)

**Template:**
```markdown
## ODD Definition

### Geographic
- **Location:** University campus roads
- **Road Types:** 2-lane campus roads, parking lots, pedestrian crossings
- **Speed Limit:** ≤ 25 mph

### Environmental
- **Weather:** Dry, light rain (no heavy rain, no snow)
- **Lighting:** Daylight (sun angle >15°), Dusk (civil twilight)
- **Visibility:** >100m
- **Temperature:** 0°C to 40°C

### Operational
- **Traffic:** Mixed (vehicles, pedestrians, cyclists)
- **Time:** 6 AM - 8 PM (campus operating hours)
- **Passenger Load:** 0-12 passengers

### Exclusions (NOT in ODD)
- Heavy rain, fog, snow
- Night driving (darkness)
- Highway/high-speed roads
- Construction zones (unless mapped)
```

**Your task:** Fill in the complete ODD for the campus shuttle.

#### Layer 5: Scenario Categories

List all high-level categories:

```markdown
## Scenario Categories

1. **Vehicle Interactions**
   - Car following
   - Intersection crossing
   - Lane change avoidance
   - Parked vehicle detection

2. **Vulnerable Road User (VRU) Interactions**
   - Pedestrian crossing
   - Cyclist in lane
   - Pedestrian group behavior
   - Child behavior

3. **Infrastructure Interactions**
   - Traffic sign/signal compliance
   - Speed bump handling
   - Crosswalk detection

4. **Edge Cases**
   - Occlusions
   - Unusual objects
   - Boundary conditions

5. **Environmental Variations**
   - Rain onset
   - Dusk transition
   - Shadows and glare
```

**Your task:** Expand with specific categories for your campus environment.

#### Layer 4: Logical Scenarios

For EACH category, define the full parameter space:

**Example: Pedestrian Crossing**

```python
logical_scenario_pedestrian_crossing = {
    'name': 'Pedestrian Crossing at Marked Crosswalk',
    'category': 'VRU Interaction',

    'parameters': {
        # Pedestrian characteristics
        'pedestrian_type': ['adult', 'child', 'elderly', 'group_2-5'],
        'crossing_direction': ['left_to_right', 'right_to_left', 'bidirectional'],
        'crossing_speed': [0.8, 1.0, 1.2, 1.5, 2.0],  # m/s
        'crossing_angle': [60, 75, 90, 105, 120],  # degrees

        # Pedestrian behavior
        'behavior': ['compliant', 'jaywalking', 'hesitant', 'phone_distracted'],
        'visibility': ['clear', 'partially_occluded', 'emerging'],

        # Ego vehicle state
        'ego_speed': [5, 10, 15, 20, 25],  # mph
        'ego_distance_at_detection': [10, 20, 30, 40, 50],  # meters

        # Environmental conditions
        'weather': ['dry', 'light_rain'],
        'lighting': ['day', 'dusk'],
        'road_condition': ['dry', 'wet'],

        # Infrastructure
        'crosswalk_marking': ['clear', 'faded'],
        'signage': ['present', 'absent'],
    },

    'initial_conditions': {
        'ego_in_lane': True,
        'pedestrian_on_sidewalk': True,
        'clear_view_initially': True
    },

    'triggering_events': [
        'pedestrian_steps_into_road',
        'pedestrian_enters_crosswalk'
    ]
}
```

**Your task:** Define logical scenarios for:
1. Pedestrian crossing (expand above)
2. Cyclist in lane
3. Vehicle cut-in at intersection
4. Child running from behind parked car

Calculate total number of parameter combinations for each!

#### Layer 3: Functional Scenarios

Describe scenarios in functional terms (no specific values):

**Example:**
```markdown
### FS-001: Pedestrian Crossing

**Description:** An adult pedestrian crosses a marked crosswalk perpendicular
to the road while the shuttle approaches at moderate speed in good visibility.

**Actors:**
- Ego vehicle (shuttle)
- Pedestrian (VRU)

**Initial State:**
- Shuttle driving in lane at legal speed
- Pedestrian standing at crosswalk edge
- Clear weather, good visibility

**Action Sequence:**
1. Pedestrian looks both ways
2. Pedestrian begins crossing
3. Shuttle detects pedestrian
4. Shuttle decelerates
5. Shuttle yields to pedestrian
6. Pedestrian completes crossing
7. Shuttle proceeds

**Expected Outcome:**
- Pedestrian detected at >30m distance
- Shuttle begins braking within 0.5s of detection
- Shuttle maintains >3m safety margin
- No collision
```

**Your task:** Write functional scenarios for your 4 logical scenarios.

#### Layer 2: Concrete Scenarios with Ranges

**Example:**
```markdown
### CS-R-001: Pedestrian Crossing (Daytime, Clear)

**Parameters:**
- Pedestrian: Adult, 1.2 m/s ± 0.2
- Distance: 25m ± 5m
- Ego speed: 15 mph ± 2
- Weather: Dry
- Lighting: Daylight (10 AM - 4 PM)
- Crosswalk: Clear markings

**Variations:** Sweep parameters within ranges
- Generate 50 test cases using Latin Hypercube Sampling
```

**Your task:** Define concrete scenario ranges for critical cases.

#### Layer 1: Fully Concrete Scenarios

**Example:**
```markdown
### CS-001: Pedestrian Crossing Nominal

**Exact Parameters:**
- Date/Time: 2024-03-15, 14:30
- Location: GPS coordinates of Main St crosswalk
- Pedestrian: Adult male, 1.75m height, 1.2 m/s constant speed
- Ego speed: 15.0 mph, center of lane
- Weather: Clear, 20°C, 50% humidity
- Lighting: 10,000 lux ambient
- Camera settings: Auto exposure, gain=1.0

**Repeatability:** Can be replayed exactly in simulation or on proving ground
```

**Your task:** Define 5 critical concrete scenarios for regression testing.

---

## Part 2: Test Case Development (15 min)

### Task 2.1: Prioritize Scenarios

Rank scenarios by criticality:

**Criticality Matrix:**

| Scenario | Severity | Likelihood | Difficulty | Priority Score |
|----------|----------|------------|------------|----------------|
| Ped crossing (day, clear) | High | High | Low | 7 |
| Child dart-out | Critical | Medium | High | 9 |
| Cyclist in lane | High | High | Medium | 8 |
| ... | | | | |

**Formula:** Priority = (Severity × 0.5) + (Likelihood × 0.3) + (Difficulty × 0.2)

**Your task:**
1. Create matrix for 20 scenarios
2. Rank them
3. Select top 10 for intensive testing

### Task 2.2: Define Pass/Fail Criteria

For each top-priority scenario, define objective criteria:

**Example: Pedestrian Crossing**

```markdown
### Test Case TC-PED-001

**Scenario:** Adult pedestrian crossing marked crosswalk, daytime

**Pass Criteria:**
1. **Detection:**
   - Pedestrian detected at ≥30m distance: PASS/FAIL
   - Confidence ≥0.85: PASS/FAIL
   - Detection maintained until exit: PASS/FAIL

2. **Response:**
   - Braking initiated within 0.5s of detection: PASS/FAIL
   - Deceleration ≤0.3g (comfortable): PASS/FAIL
   - Stopped with ≥3m margin to pedestrian: PASS/FAIL

3. **Safety:**
   - No collision: PASS/FAIL (CRITICAL)
   - Time-to-collision maintained >3s: PASS/FAIL
   - Post-encroachment time >1.5s: PASS/FAIL

4. **Uncertainty:**
   - Epistemic uncertainty <0.15: PASS/FAIL
   - Calibration ECE <0.05: PASS/FAIL
   - OOD score <0.2: PASS/FAIL

**Overall:** ALL criteria must PASS
```

**Your task:** Define detailed pass/fail criteria for your top 10 scenarios.

### Task 2.3: Coverage Analysis

Calculate parameter space coverage:

```python
# Example calculation
pedestrian_crossing_space = {
    'ped_speed': 5 bins (0.8-2.0 m/s),
    'distance': 6 bins (10-50m),
    'ego_speed': 5 bins (5-25 mph),
    'weather': 2 options,
    'lighting': 2 options,
    'behavior': 4 options
}

total_combinations = 5 * 6 * 5 * 2 * 2 * 4 = 2,400 possible scenarios
```

**Your task:**
1. Calculate total scenario space for each category
2. Determine feasible test coverage (budget, time, resources)
3. Design sampling strategy (random, stratified, adversarial)

---

## Part 3: Validation Phases (15 min)

### Task 3.1: Phase 1 - SIL (Simulation)

**Objectives:**
- Cover broad scenario space
- Test functional requirements
- Initial uncertainty validation

**Plan:**

```markdown
## SIL Phase

**Duration:** 2 months

**Simulator:** CARLA or similar

**Test Scenarios:**
- Total: 10,000 scenarios
  - Pedestrian: 4,000 (varied parameters)
  - Cyclist: 2,500
  - Vehicle: 2,500
  - Edge cases: 1,000

**Test Process:**
1. Generate scenarios using Latin Hypercube Sampling
2. Run automated tests (parallel simulation)
3. Log all detections, decisions, and outcomes
4. Analyze failures and edge cases

**Success Criteria:**
- Recall >98% on all VRU scenarios
- Precision >90%
- Zero critical failures (collisions with VRUs)
- ECE <0.05
- Coverage >90% of parameter space

**Deliverables:**
- Test report with metrics
- Failure analysis
- Updated ODD based on limitations found
```

**Your task:** Complete the SIL plan with specific metrics and thresholds.

### Task 3.2: Phase 2 - HIL (Hardware-in-Loop)

**Objectives:**
- Validate on real sensors and compute
- Test real-time performance
- Verify sensor fusion

**Your task:** Design HIL plan including:
- Number of scenarios (suggest 500-1000)
- Focus areas (e.g., sensor edge cases)
- Pass criteria
- Duration and resources

### Task 3.3: Phase 3 - VIL (Proving Ground)

**Objectives:**
- Test complete system
- Validate critical scenarios safely
- Verify emergency behaviors

**Your task:** Design VIL plan:
- Test track requirements
- Soft targets / robot pedestrians
- Safety protocols
- Number of test runs per scenario
- Data collection plan

### Task 3.4: Phase 4 - FOT (Field Test)

**Objectives:**
- Real-world validation
- Discover long-tail scenarios
- Build statistical evidence

**Your task:** Design FOT plan:
- Geographic area on campus
- Number of miles to drive
- Safety driver protocols
- Data collection and monitoring
- Disengagement criteria
- Public communication plan

---

## Part 4: Statistical Evidence (10 min)

### Task 4.1: Calculate Miles Needed

Using Kalra & Paddock analysis:

**Assumptions:**
- Baseline accident rate: 1 per 100,000 miles (better than human drivers)
- Target improvement: 50% better than baseline
- Confidence level: 95%

**Your task:**
1. Calculate miles needed to demonstrate this statistically
2. Estimate time required with your fleet
3. Justify surrogate metrics if full validation is impractical

### Task 4.2: Design Surrogate Metrics

Since full statistical proof is impractical, define surrogates:

**Example Surrogates:**
```markdown
## Surrogate Metrics for Safety

1. **Critical Interventions**
   - Measure: Safety driver takeovers per 1,000 miles
   - Target: <1 intervention per 1,000 miles
   - Easier to measure than actual accidents

2. **Near-Miss Events**
   - Measure: Time-to-collision <2s events
   - Target: <5 near-misses per 10,000 miles

3. **Disengagements**
   - Measure: System-initiated disengagements
   - Target: <2 per 1,000 miles

4. **Uncertainty Alerts**
   - Measure: High epistemic uncertainty events
   - Target: <10 per 1,000 miles
   - Indicates approaching ODD boundaries
```

**Your task:** Define 5 surrogate metrics with justification for why they predict safety.

---

## Part 5: ISO 26262 Compliance (5 min)

### Task 5.1: Map to V&V Requirements

Connect your plan to ISO 26262-8 (Supporting Processes):

**Table 1: Requirements Traceability**

| ISO 26262-8 Requirement | Validation Phase | Evidence |
|-------------------------|------------------|----------|
| 8.4.2.5: Test coverage adequate | SIL | 90% param space coverage |
| 8.4.2.6: Safety goals validated | VIL + FOT | Zero critical failures |
| 8.4.2.7: Known limitations documented | All phases | ODD definition, uncertainty boundaries |
| 8.4.2.8: Residual risks acceptable | FOT | Statistical analysis, surrogate metrics |

**Your task:** Complete the traceability matrix for all relevant ISO 26262-8 clauses.

### Task 5.2: Safety Argument

Write a brief safety argument (1 page):

**Structure:**
```markdown
## Safety Argument: Campus Shuttle Perception System

### Claim
The perception system is sufficiently safe for campus shuttle operation within the defined ODD.

### Evidence
1. **Extensive Testing:**
   - 10,000 simulation scenarios
   - 500 HIL tests
   - 100 proving ground tests
   - 5,000 miles field testing

2. **Performance Metrics:**
   - Recall >98% on VRU detection
   - Zero critical failures in testing
   - Interventions <1 per 1,000 miles

3. **Uncertainty Management:**
   - Calibrated model (ECE <0.05)
   - OOD detection validated
   - Fallback to safe state when uncertain

### Argument
Given the comprehensive testing across all validation phases, meeting all pass criteria,
and demonstrating robust uncertainty quantification, we have sufficient confidence
that the system will operate safely within the defined ODD.

### Residual Risks
- Long-tail scenarios not covered in testing
- Potential sensor degradation over time
- Novel scenarios outside ODD

### Mitigation
- Continuous monitoring in operation
- Uncertainty-based runtime checks
- Regular system updates and revalidation
```

---

## Submission Requirements

### Deliverables

1. **Validation Plan Document (10-15 pages)**
   - ODD definition
   - Scenario hierarchy (all 6 layers)
   - Test case specifications
   - Phase plans (SIL, HIL, VIL, FOT)
   - Pass/fail criteria
   - Statistical evidence plan

2. **Test Coverage Analysis**
   - Parameter space calculations
   - Coverage maps
   - Sampling strategy

3. **ISO 26262 Compliance Matrix**
   - Requirements traceability
   - Evidence mapping

4. **Safety Argument**
   - Claims, evidence, reasoning
   - Residual risk analysis

5. **Budget and Timeline**
   - Resource requirements
   - Critical path
   - Risk mitigation plan

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Scenario Definition** | 20 | Complete Pegasus 6-layer model, well-defined parameters |
| **Test Coverage** | 15 | Systematic coverage strategy, justified sampling |
| **Pass Criteria** | 15 | Objective, measurable, safety-focused criteria |
| **Validation Phases** | 20 | Comprehensive SIL/HIL/VIL/FOT plans |
| **Statistical Evidence** | 10 | Realistic evidence plan, good surrogate metrics |
| **ISO 26262 Compliance** | 10 | Clear traceability, complete safety argument |
| **Feasibility** | 5 | Realistic budget, timeline, resources |
| **Quality** | 5 | Professional, thorough, well-organized |
| **Total** | 100 | |

---

## Bonus Challenges (Optional)

### Bonus 1: Automated Test Generation (+10 points)
- Implement code to automatically generate scenarios from logical definition
- Use genetic algorithms or RL to find edge cases

### Bonus 2: Continuous Validation (+10 points)
- Design strategy for continuous validation during operation
- Shadow mode testing, A/B testing, etc.

### Bonus 3: Multi-Agent Scenarios (+15 points)
- Define scenarios with multiple interacting agents
- Pedestrian + cyclist + vehicle simultaneously

---

## Resources

### Standards
- ISO 26262-8: Supporting Processes (Validation)
- ISO 21448: SOTIF
- UL 4600: Automated Driving Systems

### Papers
- Kalra & Paddock (2016): "Driving to Safety"
- Pegasus Project: "6-Layer Scenario Model"
- Waymo Safety Report (2020)
- NHTSA AV Testing Framework

### Tools
- CARLA Simulator
- Scenic (scenario specification language)
- OpenSCENARIO format

---

## Tips for Success

1. **Be Systematic:** Use structured approach (Pegasus model)
2. **Prioritize:** Focus intensive testing on critical scenarios
3. **Be Realistic:** Budget and timeline must be feasible
4. **Think Safety:** Every decision should improve safety
5. **Document Everything:** Traceability is key for compliance

**Remember:** This validation plan is how you demonstrate your AV is safe enough for public roads. Take it seriously!

Good luck!
