"""Grading tests: one test per question, checked with avsafety.exercises.

The reference values are computed by the course toolkit from problem.py, so these tests
contain no answer key. Set AVSAFETY_ANSWERS to the path of another answers file to grade it.
"""
import importlib.util
import os
from pathlib import Path

from avsafety import exercises as ex
from avsafety import iso21434

import problem as P


def _load_answers():
    path = Path(os.environ.get("AVSAFETY_ANSWERS", Path(__file__).with_name("answers.py")))
    spec = importlib.util.spec_from_file_location("answers", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = _load_answers()


def _expect(result):
    assert result.correct, "\n" + str(result)


def test_q1_asil():
    _expect(ex.check_asil(A.Q1_ASIL, P.Q1_S, P.Q1_E, P.Q1_C, exercise="Q1"))


def test_q2_decomposition():
    from avsafety.iso26262 import determine_asil
    asil = determine_asil(P.Q1_S, P.Q1_E, P.Q1_C)
    _expect(ex.check_asil_decomposition(A.Q2_DECOMPOSITION, asil, exercise="Q2"))


def test_q3_hardware_metrics():
    _expect(ex.check_hardware_metrics({"SPFM": A.Q3_SPFM, "LFM": A.Q3_LFM}, P.Q3_FMEDA, exercise="Q3"))


def test_q4_attack_feasibility():
    _expect(ex.check_attack_feasibility((A.Q4_POTENTIAL, A.Q4_FEASIBILITY), *P.Q4_FACTORS, exercise="Q4"))


def test_q5_risk_value():
    feasibility = iso21434.feasibility_from_potential(iso21434.attack_potential(*P.Q4_FACTORS))
    _expect(ex.check_risk_value(A.Q5_RISK, P.Q5_IMPACT, feasibility, exercise="Q5"))


def test_q6_cal():
    _expect(ex.check_cal(A.Q6_CAL, P.Q6_IMPACT, P.Q6_VECTOR, exercise="Q6"))


def test_q7_rss_distance():
    _expect(ex.check_rss_distance(A.Q7_D_MIN_M, P.Q7_V_REAR_KMH / 3.6, P.Q7_V_FRONT_KMH / 3.6, **P.Q7_PARAMS,
                                  exercise="Q7"))


def test_q8_validation_target():
    _expect(ex.check_validation_target(A.Q8_HOURS, P.Q8_RATE, P.Q8_CONFIDENCE, P.Q8_EVENTS, exercise="Q8"))
