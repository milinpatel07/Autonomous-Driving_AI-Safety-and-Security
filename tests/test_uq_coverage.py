import numpy as np
import pytest

from avsafety import coverage, uq


def _synthetic(t_true=2.0, n=20000, k=5, seed=0):
    rng = np.random.default_rng(seed)
    logits = rng.normal(0, 3, size=(n, k))
    p = uq.softmax(logits, t_true)
    labels = np.array([rng.choice(k, p=row) for row in p])
    return logits, labels


def test_temperature_recovered():
    logits, labels = _synthetic()
    assert uq.fit_temperature(logits[:10000], labels[:10000]) == pytest.approx(2.0, rel=0.1)


def test_calibration_improves_after_scaling():
    logits, labels = _synthetic()
    val, test = slice(0, 10000), slice(10000, None)
    t = uq.fit_temperature(logits[val], labels[val])
    before = uq.expected_calibration_error(uq.softmax(logits[test]), labels[test])
    after = uq.expected_calibration_error(uq.softmax(logits[test], t), labels[test])
    assert after < before / 2
    assert uq.negative_log_likelihood(uq.softmax(logits[test], t), labels[test]) < \
        uq.negative_log_likelihood(uq.softmax(logits[test]), labels[test])
    assert 0 <= uq.brier_score(uq.softmax(logits[test], t), labels[test]) <= 2


def test_conformal_coverage():
    logits, labels = _synthetic(t_true=1.0, seed=1)
    p = uq.softmax(logits)
    q = uq.conformal_threshold(p[:5000], labels[:5000], alpha=0.1)
    sets = uq.conformal_sets(p[5000:], q)
    cov = sets[np.arange(len(sets)), labels[5000:]].mean()
    assert cov >= 0.89


def test_nwise_coverage():
    domains = {"weather": ["clear", "rain"], "light": ["day", "night"], "road": ["urban", "highway"]}
    scen = [{"weather": "clear", "light": "day", "road": "urban"},
            {"weather": "rain", "light": "night", "road": "highway"}]
    r1 = coverage.nwise_coverage(domains, scen, n=1)
    assert r1["coverage"] == 1.0
    r2 = coverage.nwise_coverage(domains, scen, n=2)
    assert r2["total"] == 12 and r2["covered"] == 6
    assert coverage.full_factorial_size(domains) == 8
