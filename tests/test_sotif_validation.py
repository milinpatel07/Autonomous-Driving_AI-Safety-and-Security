import math

import pytest

from avsafety import sotif, validation


def test_ttc_thw_drac():
    assert sotif.time_to_collision(20, 15, 10) == pytest.approx(4.0)
    assert sotif.time_to_collision(20, 10, 15) == math.inf
    assert sotif.time_headway(30, 15) == pytest.approx(2.0)
    assert sotif.drac(25, 15, 5) == pytest.approx(2.0)


def test_rss_distance():
    assert sotif.rss_safe_longitudinal_distance(0, 0) == pytest.approx(0.375)
    # faster rear vehicle needs more distance; faster front vehicle needs less
    d = sotif.rss_safe_longitudinal_distance(25, 25)
    assert sotif.rss_safe_longitudinal_distance(30, 25) > d > sotif.rss_safe_longitudinal_distance(25, 30)
    assert sotif.rss_safe_longitudinal_distance(0, 50) == 0.0


def test_rand_275_million_miles():
    n = validation.miles_to_demonstrate(1.09e-8, 0.95, 0)
    assert n == pytest.approx(2.75e8, rel=0.01)
    assert n == pytest.approx(-math.log(0.05) / 1.09e-8, rel=1e-9)
    assert validation.miles_to_demonstrate(1.09e-8, 0.95, 3) > n


def test_poisson_interval():
    lo, hi = validation.poisson_rate_interval(0, 1.0, 0.95)
    assert lo == 0 and hi == pytest.approx(3.689, abs=1e-3)
    lo, hi = validation.poisson_rate_interval(10, 100.0, 0.95)
    assert lo < 0.1 < hi
    assert validation.zero_failure_confidence(n := 2.75e8, 1.09e-8) == pytest.approx(0.95, abs=1e-3)
    assert validation.fleet_years(n) == pytest.approx(12.5, abs=0.1)
