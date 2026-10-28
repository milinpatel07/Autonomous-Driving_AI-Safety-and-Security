"""Scenario / ODD coverage: n-wise combinatorial coverage of discretised parameters.

Background: combinatorial testing (e.g. NIST ACTS); scenario parameters per ISO 34502:2022
and ODD attributes per ISO 34503:2023.
"""
from __future__ import annotations

from itertools import combinations, product


def nwise_coverage(domains: dict, scenarios: list[dict], n: int = 2) -> dict:
    """Fraction of all n-way value combinations exercised by ``scenarios``.

    domains:   {parameter: [values, ...]}
    scenarios: list of {parameter: value}
    Returns {'coverage': float, 'covered': int, 'total': int, 'missing': [...]}.
    """
    params = sorted(domains)
    if not 1 <= n <= len(params):
        raise ValueError("n must be between 1 and the number of parameters")
    required = set()
    for combo in combinations(params, n):
        for values in product(*(domains[p] for p in combo)):
            required.add(tuple(zip(combo, values)))
    seen = set()
    for sc in scenarios:
        for combo in combinations(params, n):
            if all(p in sc for p in combo):
                seen.add(tuple((p, sc[p]) for p in combo))
    covered = required & seen
    missing = sorted(required - seen)
    return {"coverage": len(covered) / len(required), "covered": len(covered),
            "total": len(required), "missing": missing}


def full_factorial_size(domains: dict) -> int:
    """Number of concrete combinations in the full factorial design."""
    size = 1
    for values in domains.values():
        size *= len(values)
    return size
