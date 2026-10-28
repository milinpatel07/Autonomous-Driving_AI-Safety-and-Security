"""ISO/SAE 21434:2021 TARA helpers.

Sources: ISO/SAE 21434:2021 clause 15 and informative Annexes E (CAL), G (attack
feasibility rating approaches) and H (example risk matrix); the attack-potential
values originate from ISO/IEC 18045. CVSS v3.1 per the FIRST specification
(https://www.first.org/cvss/v3.1/specification-document).

Note: Annexes E, G and H are *informative*. Organisations may define their own
methods; these functions implement the examples given in the standard.
"""
from __future__ import annotations

import math

IMPACT_LEVELS = ("Negligible", "Moderate", "Major", "Severe")
FEASIBILITY_LEVELS = ("Very Low", "Low", "Medium", "High")

# Attack-potential factor values (Annex G.2, from ISO/IEC 18045)
ELAPSED_TIME = {"<=1 day": 0, "<=1 week": 1, "<=1 month": 4, "<=6 months": 17, ">6 months": 19}
EXPERTISE = {"layman": 0, "proficient": 3, "expert": 6, "multiple experts": 8}
KNOWLEDGE = {"public": 0, "restricted": 3, "confidential": 7, "strictly confidential": 11}
WINDOW = {"unlimited": 0, "easy": 1, "moderate": 4, "difficult": 10}
EQUIPMENT = {"standard": 0, "specialized": 4, "bespoke": 7, "multiple bespoke": 9}


def attack_potential(elapsed_time: str, expertise: str, knowledge: str, window: str, equipment: str) -> int:
    """Sum of the five attack-potential factor values."""
    try:
        return (ELAPSED_TIME[elapsed_time] + EXPERTISE[expertise] + KNOWLEDGE[knowledge]
                + WINDOW[window] + EQUIPMENT[equipment])
    except KeyError as exc:
        raise ValueError(f"unknown factor value: {exc}") from None


def feasibility_from_potential(potential: int) -> str:
    """Attack feasibility rating from attack potential (0-13 High ... >=25 Very Low)."""
    if potential < 0:
        raise ValueError("attack potential must be non-negative")
    if potential <= 13:
        return "High"
    if potential <= 19:
        return "Medium"
    if potential <= 24:
        return "Low"
    return "Very Low"


# Attack-vector-based approach (Annex G.4)
FEASIBILITY_FROM_VECTOR = {"Network": "High", "Adjacent": "Medium", "Local": "Low", "Physical": "Very Low"}

# Example risk matrix (Annex H): RISK_MATRIX[impact][feasibility] -> risk value 1..5
RISK_MATRIX = {
    "Severe": {"Very Low": 2, "Low": 3, "Medium": 4, "High": 5},
    "Major": {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4},
    "Moderate": {"Very Low": 1, "Low": 2, "Medium": 2, "High": 3},
    "Negligible": {"Very Low": 1, "Low": 1, "Medium": 1, "High": 1},
}


def risk_value(impact: str, feasibility: str) -> int:
    """Risk value (1 = lowest, 5 = highest) from impact and attack feasibility."""
    if impact not in RISK_MATRIX or feasibility not in FEASIBILITY_LEVELS:
        raise ValueError(f"invalid impact/feasibility: {impact!r}, {feasibility!r}")
    return RISK_MATRIX[impact][feasibility]


# Example CAL determination (Annex E): impact x attack vector. CAL expresses the
# rigour of assurance activities for a cybersecurity goal; it is not a risk measure.
CAL_TABLE = {
    "Severe": {"Physical": 2, "Local": 3, "Adjacent": 4, "Network": 4},
    "Major": {"Physical": 1, "Local": 2, "Adjacent": 3, "Network": 4},
    "Moderate": {"Physical": 1, "Local": 1, "Adjacent": 2, "Network": 3},
}


def determine_cal(impact: str, attack_vector: str):
    """Return CAL 1-4, or ``None`` when no CAL is assigned (negligible impact)."""
    if impact == "Negligible":
        return None
    if impact not in CAL_TABLE or attack_vector not in FEASIBILITY_FROM_VECTOR:
        raise ValueError(f"invalid impact/attack vector: {impact!r}, {attack_vector!r}")
    return CAL_TABLE[impact][attack_vector]


# ---------------------------------------------------------------- CVSS v3.1
_AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
_AC = {"L": 0.77, "H": 0.44}
_PR_U = {"N": 0.85, "L": 0.62, "H": 0.27}
_PR_C = {"N": 0.85, "L": 0.68, "H": 0.50}
_UI = {"N": 0.85, "R": 0.62}
_CIA = {"H": 0.56, "L": 0.22, "N": 0.0}


def _roundup(x: float) -> float:
    """CVSS v3.1 Roundup (Appendix A of the specification)."""
    i = round(x * 100000)
    return i / 100000.0 if i % 10000 == 0 else (math.floor(i / 10000) + 1) / 10.0


def cvss31_exploitability(av: str, ac: str, pr: str, ui: str, scope: str = "U") -> float:
    pr_table = _PR_C if scope == "C" else _PR_U
    return 8.22 * _AV[av] * _AC[ac] * pr_table[pr] * _UI[ui]


def cvss31_base_score(vector: str) -> float:
    """Base score from a vector such as ``'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'``."""
    parts = dict(p.split(":") for p in vector.split("/") if not p.startswith("CVSS"))
    s = parts["S"]
    iss = 1 - (1 - _CIA[parts["C"]]) * (1 - _CIA[parts["I"]]) * (1 - _CIA[parts["A"]])
    impact = 6.42 * iss if s == "U" else 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    expl = cvss31_exploitability(parts["AV"], parts["AC"], parts["PR"], parts["UI"], s)
    if impact <= 0:
        return 0.0
    if s == "U":
        return _roundup(min(impact + expl, 10))
    return _roundup(min(1.08 * (impact + expl), 10))


def feasibility_from_cvss_exploitability(expl: float) -> str:
    """Annex G.3 mapping of the CVSS exploitability sub-score to attack feasibility."""
    if expl >= 2.96:
        return "High"
    if expl >= 2.00:
        return "Medium"
    if expl >= 1.06:
        return "Low"
    return "Very Low"
