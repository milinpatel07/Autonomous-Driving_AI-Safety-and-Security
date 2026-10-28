"""ISO 26262:2018 helpers.

Sources: ISO 26262-3:2018 Table 4 (ASIL determination), ISO 26262-9:2018 clause 5
(ASIL decomposition), ISO 26262-5:2018 Tables 4-6 (hardware architectural metric
and PMHF target values).
"""
from __future__ import annotations

ASIL_ORDER = ("QM", "A", "B", "C", "D")

# ISO 26262-3:2018 Table 4. ASIL_TABLE[S][E] -> (C1, C2, C3)
ASIL_TABLE = {
    "S1": {"E1": ("QM", "QM", "QM"), "E2": ("QM", "QM", "QM"), "E3": ("QM", "QM", "A"), "E4": ("QM", "A", "B")},
    "S2": {"E1": ("QM", "QM", "QM"), "E2": ("QM", "QM", "A"), "E3": ("QM", "A", "B"), "E4": ("A", "B", "C")},
    "S3": {"E1": ("QM", "QM", "A"), "E2": ("QM", "A", "B"), "E3": ("A", "B", "C"), "E4": ("B", "C", "D")},
}

_VALID = {"S": ("S0", "S1", "S2", "S3"), "E": ("E0", "E1", "E2", "E3", "E4"), "C": ("C0", "C1", "C2", "C3")}


def determine_asil(severity: str, exposure: str, controllability: str) -> str:
    """Return the ASIL ("QM", "A".."D") for a hazardous event.

    S0, E0 or C0 mean no ASIL is assigned (returned as "QM"). Invalid classes raise
    ``ValueError`` rather than silently defaulting to QM.
    """
    s, e, c = (str(x).strip().upper() for x in (severity, exposure, controllability))
    for val, key in ((s, "S"), (e, "E"), (c, "C")):
        if val not in _VALID[key]:
            raise ValueError(f"invalid {key} class: {val!r}; expected one of {_VALID[key]}")
    if s == "S0" or e == "E0" or c == "C0":
        return "QM"
    return ASIL_TABLE[s][e][int(c[1]) - 1]


def asil_rank(asil: str) -> int:
    """Numeric rank of an ASIL (QM=0 ... D=4)."""
    return ASIL_ORDER.index(asil)


# ISO 26262-9:2018 clause 5.4: permitted decompositions of a requirement's ASIL.
DECOMPOSITIONS = {
    "D": [("C", "A"), ("B", "B"), ("D", "QM")],
    "C": [("B", "A"), ("C", "QM")],
    "B": [("A", "A"), ("B", "QM")],
    "A": [("A", "QM")],
}


def decomposition_options(asil: str) -> list[tuple[str, str]]:
    """Valid ASIL decompositions, written in ISO notation, e.g. ``('B(D)', 'B(D)')``.

    Decomposition requires sufficiently independent elements (dependent failure
    analysis); hardware metrics and PMHF are still evaluated at the original ASIL.
    """
    if asil not in DECOMPOSITIONS:
        raise ValueError(f"ASIL {asil!r} cannot be decomposed")
    return [(f"{a}({asil})", f"{b}({asil})") for a, b in DECOMPOSITIONS[asil]]


# ISO 26262-5:2018 Tables 4, 5 and 6 (target values for the safety goal's ASIL)
SPFM_TARGET = {"B": 0.90, "C": 0.97, "D": 0.99}
LFM_TARGET = {"B": 0.60, "C": 0.80, "D": 0.90}
PMHF_TARGET_PER_HOUR = {"B": 1e-7, "C": 1e-7, "D": 1e-8}


def hardware_metrics(entries) -> dict:
    """Compute SPFM, LFM and a simple PMHF estimate from FMEDA rows.

    Each entry is a mapping with keys
      ``rate`` (failure rate, FIT), ``safe`` (bool, safe fault),
      ``spf`` (bool, single-point fault: not covered by any safety mechanism),
      ``dc`` (diagnostic coverage of the residual-fault mechanism, 0..1),
      ``dc_latent`` (coverage of the latent-fault mechanism, 0..1).

    SPFM = 1 - sum(l_SPF + l_RF) / sum(l)
    LFM  = 1 - sum(l_MPF,latent) / sum(l - l_SPF - l_RF)
    """
    total = spf = rf = latent = 0.0
    for e in entries:
        lam = float(e["rate"])
        total += lam
        if e.get("safe", False):
            continue
        if e.get("spf", False):
            spf += lam
            continue
        dc = float(e.get("dc", 0.0))
        rf += lam * (1 - dc)
        latent += lam * dc * (1 - float(e.get("dc_latent", 0.0)))
    if total <= 0:
        raise ValueError("total failure rate must be positive")
    spfm = 1 - (spf + rf) / total
    denom = total - spf - rf
    lfm = 1 - latent / denom if denom > 0 else 1.0
    pmhf_fit = spf + rf  # first-order estimate, dominant terms only
    return {"SPFM": spfm, "LFM": lfm, "PMHF_FIT": pmhf_fit, "PMHF_per_hour": pmhf_fit * 1e-9}


def meets_hw_targets(metrics: dict, asil: str) -> dict:
    """Compare metrics from :func:`hardware_metrics` against ASIL targets."""
    if asil not in SPFM_TARGET:
        return {"SPFM": True, "LFM": True, "PMHF": True}
    return {
        "SPFM": metrics["SPFM"] >= SPFM_TARGET[asil],
        "LFM": metrics["LFM"] >= LFM_TARGET[asil],
        "PMHF": metrics["PMHF_per_hour"] < PMHF_TARGET_PER_HOUR[asil],
    }
