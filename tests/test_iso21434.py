import pytest

from avsafety import iso21434 as cs


def test_attack_potential_extremes():
    assert cs.attack_potential("<=1 day", "layman", "public", "unlimited", "standard") == 0
    worst = cs.attack_potential(">6 months", "multiple experts", "strictly confidential", "difficult", "multiple bespoke")
    assert worst == 19 + 8 + 11 + 10 + 9
    assert cs.feasibility_from_potential(worst) == "Very Low"


@pytest.mark.parametrize("ap,rating", [(0, "High"), (13, "High"), (14, "Medium"), (19, "Medium"),
                                       (20, "Low"), (24, "Low"), (25, "Very Low")])
def test_feasibility_bands(ap, rating):
    assert cs.feasibility_from_potential(ap) == rating


def test_layman_public_standard_is_high_feasibility():
    # Regression: the original notebook mapped this profile to "Very Low".
    ap = cs.attack_potential("<=1 week", "layman", "public", "unlimited", "standard")
    assert cs.feasibility_from_potential(ap) == "High"


def test_risk_matrix():
    assert cs.risk_value("Severe", "High") == 5
    assert cs.risk_value("Severe", "Very Low") == 2
    assert cs.risk_value("Moderate", "Medium") == 2
    assert cs.risk_value("Negligible", "High") == 1
    with pytest.raises(ValueError):
        cs.risk_value("Severe", "Very High")


def test_cal():
    assert cs.determine_cal("Severe", "Network") == 4
    assert cs.determine_cal("Severe", "Physical") == 2
    assert cs.determine_cal("Moderate", "Local") == 1
    assert cs.determine_cal("Negligible", "Network") is None


@pytest.mark.parametrize("vector,score", [
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8),
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", 10.0),
    ("CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", 7.8),
    ("CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H", 8.1),
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N", 6.1),
    ("CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N", 0.0),
])
def test_cvss31(vector, score):
    assert cs.cvss31_base_score(vector) == score


def test_cvss_feasibility_mapping():
    expl = cs.cvss31_exploitability("N", "L", "N", "N")
    assert cs.feasibility_from_cvss_exploitability(expl) == "High"
    assert cs.feasibility_from_cvss_exploitability(cs.cvss31_exploitability("P", "H", "H", "R")) == "Very Low"
