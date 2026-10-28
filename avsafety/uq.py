"""Uncertainty quantification utilities: calibration metrics, temperature scaling,
split conformal prediction.

References: C. Guo et al., "On Calibration of Modern Neural Networks", ICML 2017;
A. N. Angelopoulos and S. Bates, "A Gentle Introduction to Conformal Prediction and
Distribution-Free Uncertainty Quantification", arXiv:2107.07511.
"""
from __future__ import annotations

import numpy as np
from scipy import optimize


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    z = np.asarray(logits, dtype=np.float64) / temperature
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def reliability_bins(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15):
    """Per-bin (confidence, accuracy, count) using top-label confidence and equal-width bins."""
    probs = np.asarray(probs); labels = np.asarray(labels)
    conf = probs.max(axis=1)
    correct = (probs.argmax(axis=1) == labels).astype(float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    idx = np.clip(np.digitize(conf, edges[1:-1], right=True), 0, n_bins - 1)
    out = []
    for b in range(n_bins):
        m = idx == b
        out.append((conf[m].mean() if m.any() else np.nan,
                     correct[m].mean() if m.any() else np.nan, int(m.sum())))
    return out


def expected_calibration_error(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> float:
    """ECE = sum_b |B_b|/n * |acc(B_b) - conf(B_b)| (top-label, equal-width bins)."""
    n = len(labels)
    return float(sum(cnt / n * abs(acc - c) for c, acc, cnt in reliability_bins(probs, labels, n_bins) if cnt))


def brier_score(probs: np.ndarray, labels: np.ndarray) -> float:
    """Multi-class Brier score (mean squared error to the one-hot label)."""
    probs = np.asarray(probs)
    onehot = np.eye(probs.shape[1])[np.asarray(labels)]
    return float(np.mean(np.sum((probs - onehot) ** 2, axis=1)))


def negative_log_likelihood(probs: np.ndarray, labels: np.ndarray, eps: float = 1e-12) -> float:
    probs = np.asarray(probs)
    return float(-np.mean(np.log(np.clip(probs[np.arange(len(labels)), labels], eps, 1.0))))


def fit_temperature(val_logits: np.ndarray, val_labels: np.ndarray) -> float:
    """Temperature T > 0 minimising validation NLL (fit on a held-out set, never on test)."""
    def nll(log_t):
        return negative_log_likelihood(softmax(val_logits, np.exp(log_t)), val_labels)
    res = optimize.minimize_scalar(nll, bounds=(-3.0, 3.0), method="bounded")
    return float(np.exp(res.x))


def conformal_threshold(cal_probs: np.ndarray, cal_labels: np.ndarray, alpha: float = 0.1) -> float:
    """Split-conformal threshold q for the score s = 1 - p(true class).

    Prediction sets {y : 1 - p_y <= q} then contain the true label with probability
    >= 1 - alpha under exchangeability.
    """
    n = len(cal_labels)
    if not 0 < alpha < 1 or n == 0:
        raise ValueError("invalid alpha or empty calibration set")
    scores = 1.0 - np.asarray(cal_probs)[np.arange(n), cal_labels]
    level = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(scores, level, method="higher"))


def conformal_sets(probs: np.ndarray, threshold: float) -> np.ndarray:
    """Boolean matrix (n_samples x n_classes): class included in the prediction set."""
    return (1.0 - np.asarray(probs)) <= threshold
