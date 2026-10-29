"""Reference answers for the classroom template, computed from problem.py with the toolkit.

Used by CI to prove that the grading tests accept correct answers:
    AVSAFETY_ANSWERS=classroom/reference_answers.py python -m pytest -q classroom/assignment
Nothing here is typed in by hand, so the reference cannot drift from the toolkit.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).with_name("assignment")))

import problem as P  # noqa: E402
from avsafety import iso21434, iso26262, sotif, validation  # noqa: E402

Q1_ASIL = iso26262.determine_asil(P.Q1_S, P.Q1_E, P.Q1_C)
Q2_DECOMPOSITION = iso26262.decomposition_options(Q1_ASIL)[0]
_m = iso26262.hardware_metrics(P.Q3_FMEDA)
Q3_SPFM, Q3_LFM = _m["SPFM"], _m["LFM"]
Q4_POTENTIAL = iso21434.attack_potential(*P.Q4_FACTORS)
Q4_FEASIBILITY = iso21434.feasibility_from_potential(Q4_POTENTIAL)
Q5_RISK = iso21434.risk_value(P.Q5_IMPACT, Q4_FEASIBILITY)
Q6_CAL = iso21434.determine_cal(P.Q6_IMPACT, P.Q6_VECTOR) or "none"
Q7_D_MIN_M = sotif.rss_safe_longitudinal_distance(P.Q7_V_REAR_KMH / 3.6, P.Q7_V_FRONT_KMH / 3.6, **P.Q7_PARAMS)
Q8_HOURS = validation.miles_to_demonstrate(P.Q8_RATE, P.Q8_CONFIDENCE, P.Q8_EVENTS)
