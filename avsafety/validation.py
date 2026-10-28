"""Statistical validation of failure rates (driving-distance arguments).

Background: N. Kalra and S. M. Paddock, "Driving to Safety", RAND RR-1478 (2016),
https://www.rand.org/pubs/research_reports/RR1478.html — e.g. ~275 million
failure-free miles are needed to show, with 95 % confidence, that a fatality rate
is below the 2013 US human rate of 1.09 per 100 million miles.
"""
from __future__ import annotations

import math

from scipy import stats


def miles_to_demonstrate(rate_per_mile: float, confidence: float = 0.95, failures: int = 0) -> float:
    """Exposure n such that observing ``failures`` events shows rate < ``rate_per_mile``.

    Uses the one-sided Poisson (chi-square) upper bound; for zero failures this is
    n = -ln(1 - C) / rate.
    """
    if not 0 < confidence < 1 or rate_per_mile <= 0 or failures < 0:
        raise ValueError("invalid arguments")
    return stats.chi2.ppf(confidence, 2 * (failures + 1)) / (2 * rate_per_mile)


def poisson_rate_interval(events: int, exposure: float, confidence: float = 0.95) -> tuple[float, float]:
    """Exact (Garwood) two-sided confidence interval for a Poisson rate events/exposure."""
    alpha = 1 - confidence
    lo = 0.0 if events == 0 else stats.chi2.ppf(alpha / 2, 2 * events) / 2
    hi = stats.chi2.ppf(1 - alpha / 2, 2 * (events + 1)) / 2
    return lo / exposure, hi / exposure


def poisson_upper_bound(events: int, exposure: float, confidence: float = 0.95) -> float:
    """One-sided upper confidence bound on a Poisson rate."""
    return stats.chi2.ppf(confidence, 2 * (events + 1)) / 2 / exposure


def fleet_years(miles: float, vehicles: int = 100, miles_per_vehicle_year: float = 24 * 365 * 25) -> float:
    """Years a fleet needs to accumulate ``miles``.

    The default (24 h/day at 25 mph average, 100 vehicles) mirrors the RAND fleet assumption.
    """
    return miles / (vehicles * miles_per_vehicle_year)


def zero_failure_confidence(exposure: float, rate: float) -> float:
    """Confidence that rate < ``rate`` after ``exposure`` with no failures: 1 - exp(-rate * n)."""
    return 1 - math.exp(-rate * exposure)
