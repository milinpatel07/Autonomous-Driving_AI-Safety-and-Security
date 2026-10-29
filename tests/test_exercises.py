import math

import pytest

from avsafety import exercises as ex
from avsafety import iso26262, iso21434, sotif, validation


def status(r):
    return r.status


# ---------------------------------------------------------------- result object
def test_result_is_truthy_only_when_correct_and_prints_one_line():
    ok = ex.check_asil("D", "S3", "E4", "C3")
    bad = ex.check_asil("B", "S3", "E4", "C3")
    assert ok and ok.correct and not bad
    assert str(ok).startswith("✓") and str(bad).startswith("✗")
    assert "Hint:" in str(bad) and "See:" in str(bad) and "Hint:" not in str(ok)
    assert repr(ok) == str(ok)


@pytest.mark.parametrize("missing", [None, "", "   ", ...])
def test_missing_answers_never_raise(missing):
    checks = [
        ex.check_asil(missing, "S3", "E2", "C2"),
        ex.check_asil_decomposition(missing, "D"),
        ex.check_hardware_metrics(missing, [{"rate": 10}]),
        ex.check_hw_targets(missing, [{"rate": 10}], "D"),
        ex.check_basic_event_probability(missing, 50, 1e4),
        ex.check_minimal_cut_sets(missing, {"T": ("OR", ["A", "B"])}, "T"),
        ex.check_attack_feasibility(missing, "<=1 week", "layman", "public", "unlimited", "standard"),
        ex.check_risk_value(missing, "Severe", "High"),
        ex.check_cal(missing, "Severe", "Network"),
        ex.check_rss_distance(missing, 25, 25),
        ex.check_criticality_metrics(missing, 30, 25, 20),
        ex.check_validation_target(missing, 1e-6),
        ex.check_sotif_area(missing, True, True),
        ex.check_triggering_condition_table(missing, [{"id": "a", "performance": 0.9}], 0.9),
    ]
    for r in checks:
        assert r.status == "missing" and not r and "Fill in" in r.message


def test_dicts_with_only_none_values_count_as_missing():
    assert ex.check_hardware_metrics({"SPFM": None, "LFM": None}, [{"rate": 1}]).status == "missing"
    assert ex.check_criticality_metrics({"TTC": None}, 30, 25, 20).status == "missing"


# ---------------------------------------------------------------- ISO 26262
@pytest.mark.parametrize("s", ["S1", "S2", "S3"])
@pytest.mark.parametrize("e", ["E1", "E2", "E3", "E4"])
@pytest.mark.parametrize("c", ["C1", "C2", "C3"])
def test_asil_checker_agrees_with_table_everywhere(s, e, c):
    expected = iso26262.determine_asil(s, e, c)
    assert ex.check_asil(expected, s, e, c).correct
    assert ex.check_asil(f"ASIL {expected}" if expected != "QM" else "qm", s, e, c).correct
    for other in iso26262.ASIL_ORDER:
        if other != expected:
            assert ex.check_asil(other, s, e, c).status == "incorrect"


def test_asil_hints_direction_and_zero_class():
    assert "higher" in ex.check_asil("D", "S3", "E2", "C2").hint
    assert "lower" in ex.check_asil("QM", "S3", "E2", "C2").hint
    assert "0" in ex.check_asil("A", "S0", "E4", "C3").hint
    assert ex.check_asil("ASIL E", "S3", "E2", "C2").status == "invalid"
    with pytest.raises(ValueError):
        ex.check_asil("A", "S3", "E5", "C2")  # invalid problem, not a learner error


def test_decomposition():
    for a, b in iso26262.decomposition_options("D"):
        assert ex.check_asil_decomposition((a, b), "D").correct
        assert ex.check_asil_decomposition([b, a], "D").correct
    r = ex.check_asil_decomposition(("B", "B"), "D")
    assert r.status == "incorrect" and "brackets" in r.hint
    assert ex.check_asil_decomposition(("A(D)", "A(D)"), "D").status == "incorrect"
    assert ex.check_asil_decomposition(("C(D)", "B(D)"), "D").status == "incorrect"
    assert ex.check_asil_decomposition("B(D)", "D").status == "invalid"
    assert ex.check_asil_decomposition(("X(D)", "B(D)"), "D").status == "invalid"


FMEDA = [
    {"rate": 15, "dc": 0.99, "dc_latent": 0.90},
    {"rate": 10, "dc": 0.99, "dc_latent": 0.90},
    {"rate": 10, "safe": True},
    {"rate": 15, "dc": 0.90, "dc_latent": 0.60},
    {"rate": 5, "spf": True},
]


def test_hardware_metrics_checker_uses_toolkit():
    ref = iso26262.hardware_metrics(FMEDA)
    assert ex.check_hardware_metrics({"SPFM": ref["SPFM"], "LFM": ref["LFM"], "PMHF_FIT": ref["PMHF_FIT"]}, FMEDA).correct
    assert ex.check_hardware_metrics({"SPFM": round(ref["SPFM"], 3)}, FMEDA).correct
    r = ex.check_hardware_metrics({"SPFM": ref["SPFM"], "LFM": ref["SPFM"]}, FMEDA)
    assert r.status == "incorrect" and "LFM" in r.message and "equals the SPFM" in r.hint
    total = sum(e["rate"] for e in FMEDA)
    r = ex.check_hardware_metrics({"SPFM": 1 - 5 / total}, FMEDA)
    assert "residual" in r.hint
    assert "fraction" in ex.check_hardware_metrics({"SPFM": 100 * ref["SPFM"]}, FMEDA).hint
    assert "FIT" in ex.check_hardware_metrics({"PMHF_FIT": ref["PMHF_per_hour"]}, FMEDA).hint
    assert ex.check_hardware_metrics({"SPFM": "high"}, FMEDA).status == "invalid"


def test_hardware_metrics_accepts_objects():
    class Row:
        def __init__(self, rate, safe_fault=False, single_point=False, dc_rf=0.0, dc_latent=0.0):
            self.rate, self.safe_fault, self.single_point = rate, safe_fault, single_point
            self.dc_rf, self.dc_latent = dc_rf, dc_latent
    objs = [Row(e["rate"], e.get("safe", False), e.get("spf", False), e.get("dc", 0.0), e.get("dc_latent", 0.0))
            for e in FMEDA]
    ref = iso26262.hardware_metrics(FMEDA)
    assert ex.check_hardware_metrics({"LFM": ref["LFM"]}, objs).correct


def test_hw_targets():
    met = iso26262.meets_hw_targets(iso26262.hardware_metrics(FMEDA), "D")
    assert ex.check_hw_targets(dict(met), FMEDA, "D").correct
    assert ex.check_hw_targets(all(met.values()), FMEDA, "D").correct
    assert not ex.check_hw_targets(not all(met.values()), FMEDA, "D")
    flipped = {k: not v for k, v in met.items()}
    assert ex.check_hw_targets(flipped, FMEDA, "D").status == "incorrect"


def test_basic_event_probability():
    q = 1 - math.exp(-50e-9 * 1e4)
    assert ex.check_basic_event_probability(q, 50, 1e4).correct
    assert ex.check_basic_event_probability(5e-4, 50, 1e4).correct  # rare-event approximation is within 2 %
    assert "FIT" in ex.check_basic_event_probability(50 * 1e4, 50, 1e4).hint
    assert ex.check_basic_event_probability(0.3, 50, 1e4).status == "incorrect"


def test_minimal_cut_sets():
    tree = {"T": ("AND", ["G1", "G2"]), "G1": ("OR", ["A", "B"]), "G2": ("OR", ["A", "C"])}
    assert ex.minimal_cut_sets(tree, "T") == [frozenset("A"), frozenset("BC")]
    assert ex.check_minimal_cut_sets([{"A"}, {"B", "C"}], tree, "T").correct
    assert ex.check_minimal_cut_sets(["A", ("C", "B")], tree, "T").correct
    r = ex.check_minimal_cut_sets([{"A"}, {"A", "B"}, {"B", "C"}], tree, "T")
    assert r.status == "incorrect" and "absorption" in r.hint
    assert "missing" in ex.check_minimal_cut_sets([{"A"}], tree, "T").hint
    assert ex.check_minimal_cut_sets([{"A"}, {"BC"}], tree, "T").status == "invalid"
    vote = {"T": ("KOFN", ["A", "B", "C"], 2)}
    assert ex.minimal_cut_sets(vote, "T") == [frozenset("AB"), frozenset("AC"), frozenset("BC")]
    absorb = {"T": ("OR", ["G1", "G2", "G3"]), "G1": ("AND", ["A", "B"]), "G2": ("AND", ["A", "B", "C"]),
              "G3": ("AND", ["A", "G4"]), "G4": ("OR", ["B", "D"])}
    assert ex.minimal_cut_sets(absorb, "T") == [frozenset("AB"), frozenset("AD")]


# ---------------------------------------------------------------- ISO/SAE 21434
FACTORS = ("<=1 week", "proficient", "public", "unlimited", "standard")


def test_attack_feasibility_forms():
    p = iso21434.attack_potential(*FACTORS)
    f = iso21434.feasibility_from_potential(p)
    assert (p, f) == (4, "High")
    for ans in (p, str(p), f, f.lower(), (p, f), {"potential": p, "feasibility": f}):
        assert ex.check_attack_feasibility(ans, *FACTORS).correct, ans
    assert ex.check_attack_feasibility(5, *FACTORS).status == "incorrect"
    r = ex.check_attack_feasibility((4, "Very Low"), *FACTORS)
    assert r.status == "incorrect" and "harder" in r.hint
    assert ex.check_attack_feasibility("Very High", *FACTORS).status == "invalid"


@pytest.mark.parametrize("impact", iso21434.IMPACT_LEVELS)
@pytest.mark.parametrize("feas", iso21434.FEASIBILITY_LEVELS)
def test_risk_value_matrix(impact, feas):
    expected = iso21434.risk_value(impact, feas)
    assert ex.check_risk_value(expected, impact, feas).correct
    assert not ex.check_risk_value(expected % 5 + 1, impact, feas)


def test_risk_value_invalid():
    assert ex.check_risk_value(7, "Severe", "High").status == "invalid"
    assert ex.check_risk_value(2.5, "Severe", "High").status == "invalid"


@pytest.mark.parametrize("impact", ["Severe", "Major", "Moderate"])
@pytest.mark.parametrize("vector", ["Physical", "Local", "Adjacent", "Network"])
def test_cal_table(impact, vector):
    cal = iso21434.determine_cal(impact, vector)
    for ans in (cal, f"CAL {cal}", str(cal)):
        assert ex.check_cal(ans, impact, vector).correct
    assert not ex.check_cal(cal % 4 + 1, impact, vector)


def test_cal_negligible_and_hints():
    assert ex.check_cal("none", "Negligible", "Network").correct
    assert ex.check_cal("CAL 1", "Negligible", "Network").status == "incorrect"
    assert "negligible" in ex.check_cal("none", "Severe", "Network").hint
    assert "attack vector" in ex.check_cal(1, "Severe", "Network").hint
    assert ex.check_cal("CAL 5", "Severe", "Network").status == "invalid"


# ---------------------------------------------------------------- SOTIF and validation
def test_rss_distance_and_diagnostics():
    v_r, v_f = 100 / 3.6, 80 / 3.6
    d = sotif.rss_safe_longitudinal_distance(v_r, v_f)
    assert ex.check_rss_distance(d, v_r, v_f).correct
    assert ex.check_rss_distance(round(d, 1), v_r, v_f).correct
    assert "km/h" in ex.check_rss_distance(sotif.rss_safe_longitudinal_distance(100, 80), v_r, v_f).hint
    no_acc = sotif.rss_safe_longitudinal_distance(v_r, v_f, a_max_accel=0.0)
    assert "accelerate" in ex.check_rss_distance(no_acc, v_r, v_f).hint
    swapped = sotif.rss_safe_longitudinal_distance(v_r, v_f, b_min_brake=8.0, b_max_brake=4.0)
    assert "b_min" in ex.check_rss_distance(swapped, v_r, v_f).hint
    assert ex.check_rss_distance(0.0, 5, 40).correct
    neg = 5 * 0.5 + 0.25 + 6 ** 2 / 8 - 40 ** 2 / 16
    assert "negative" in ex.check_rss_distance(neg, 5, 40).hint


def test_criticality_metrics():
    ans = {"TTC": sotif.time_to_collision(30, 25, 20), "THW": sotif.time_headway(30, 25), "DRAC": sotif.drac(30, 25, 20)}
    assert ex.check_criticality_metrics(ans, 30, 25, 20).correct
    assert ex.check_criticality_metrics({"TTC": "inf", "DRAC": 0}, 30, 25, 25).correct
    assert ex.check_criticality_metrics({"TTC": math.inf}, 30, 25, 25).correct
    r = ex.check_criticality_metrics({"TTC": 1.2, "THW": 1.2}, 30, 25, 20)
    assert r.status == "incorrect" and r.message.startswith("TTC") and "closing" in r.hint


def test_validation_target():
    n = validation.miles_to_demonstrate(1e-6, 0.95, 0)
    assert ex.check_validation_target(n, 1e-6).correct
    assert ex.check_validation_target(3.0e6, 1e-6).correct  # -ln(0.05) = 2.996
    assert "confidence" in ex.check_validation_target(1e6, 1e-6).hint
    assert "1 - C" in ex.check_validation_target(-math.log(0.95) / 1e-6, 1e-6).hint
    assert "2(k + 1)" in ex.check_validation_target(n, 1e-6, failures=2).hint


@pytest.mark.parametrize("known,hazardous,area", [(True, False, 1), (True, True, 2), (False, True, 3), (False, False, 4)])
def test_sotif_area(known, hazardous, area):
    assert ex.check_sotif_area(area, known, hazardous).correct
    assert ex.check_sotif_area(f"Area {area}", known, hazardous).correct
    assert not ex.check_sotif_area(area % 4 + 1, known, hazardous)


def test_triggering_condition_table():
    rows = [{"id": "SC-1", "performance": 0.95}, {"id": "SC-2", "performance": 0.75},
            {"id": "SC-3", "performance": 0.90}]
    assert ex.check_triggering_condition_table({"SC-1": 1, "SC-2": "Area 2", "SC-3": "area 1"}, rows, 0.90).correct
    r = ex.check_triggering_condition_table({"SC-1": 1, "SC-2": 2, "SC-3": 2}, rows, 0.90)
    assert r.status == "incorrect" and "SC-3" in r.message and ">=" in r.hint
    r = ex.check_triggering_condition_table({"SC-1": 1, "SC-2": 3}, rows, 0.90)
    assert "known" in r.hint and "SC-3" in r.message
    assert ex.check_triggering_condition_table({"SC-1": "Area X"}, rows, 0.90).status == "invalid"
