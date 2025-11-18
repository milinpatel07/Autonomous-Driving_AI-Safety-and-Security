"""
Calibration Metrics and Methods

This module provides tools for assessing and improving model calibration,
critical for safety-critical AV perception systems.

Author: AV Perception Safety Workshop
Session: 4 - Uncertainty Estimation and Validation
"""

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from scipy.optimize import minimize
from typing import Tuple, Optional
import matplotlib.pyplot as plt


def expected_calibration_error(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Compute Expected Calibration Error (ECE).

    ECE measures the difference between confidence and accuracy.

    Args:
        y_true: True labels [N]
        y_prob: Predicted probabilities [N]
        n_bins: Number of bins for discretization

    Returns:
        ece: Expected Calibration Error (0 = perfect calibration)
    """
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bin_edges[1:-1])

    ece = 0.0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracy = y_true[mask].mean()
            bin_confidence = y_prob[mask].mean()
            bin_size = mask.sum()

            ece += (bin_size / len(y_true)) * abs(bin_accuracy - bin_confidence)

    return ece


def maximum_calibration_error(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Compute Maximum Calibration Error (MCE).

    MCE is the maximum difference between confidence and accuracy across bins.

    Args:
        y_true: True labels
        y_prob: Predicted probabilities
        n_bins: Number of bins

    Returns:
        mce: Maximum Calibration Error
    """
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bin_edges[1:-1])

    max_error = 0.0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracy = y_true[mask].mean()
            bin_confidence = y_prob[mask].mean()
            error = abs(bin_accuracy - bin_confidence)
            max_error = max(max_error, error)

    return max_error


def reliability_diagram_data(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute data for reliability diagram.

    Args:
        y_true: True labels
        y_prob: Predicted probabilities
        n_bins: Number of bins

    Returns:
        bin_centers: Center of each bin
        bin_accuracies: Actual accuracy in each bin
        bin_counts: Number of samples in each bin
    """
    bin_edges = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_indices = np.digitize(y_prob, bin_edges[1:-1])

    bin_accuracies = []
    bin_confidences = []
    bin_counts = []

    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracies.append(y_true[mask].mean())
            bin_confidences.append(y_prob[mask].mean())
            bin_counts.append(mask.sum())
        else:
            bin_accuracies.append(0)
            bin_confidences.append(bin_centers[i])
            bin_counts.append(0)

    return (np.array(bin_confidences),
            np.array(bin_accuracies),
            np.array(bin_counts))


class TemperatureScaling:
    """
    Temperature Scaling for calibration.

    Learns a single parameter T to scale logits: p = softmax(z/T)
    """

    def __init__(self):
        self.temperature = 1.0

    def fit(self, logits: np.ndarray, labels: np.ndarray, max_iter: int = 50):
        """
        Learn optimal temperature on validation set.

        Args:
            logits: Model logits before softmax [N, num_classes] or [N] for binary
            labels: True labels [N]
            max_iter: Maximum optimization iterations

        Returns:
            self
        """
        # Convert to tensors
        if logits.ndim == 1:
            logits = logits.reshape(-1, 1)
            labels = labels.reshape(-1, 1)
            is_binary = True
        else:
            is_binary = False

        logits_tensor = torch.FloatTensor(logits)
        labels_tensor = torch.LongTensor(labels) if not is_binary else torch.FloatTensor(labels)

        # Optimize temperature to minimize NLL
        def nll_criterion(T):
            T = T[0]  # Scipy passes array
            if T <= 0:
                return 1e10  # Invalid temperature

            scaled_logits = logits_tensor / T

            if is_binary:
                loss = F.binary_cross_entropy_with_logits(
                    scaled_logits.squeeze(), labels_tensor.squeeze()
                )
            else:
                loss = F.cross_entropy(scaled_logits, labels_tensor)

            return loss.item()

        # Optimize
        result = minimize(
            nll_criterion,
            x0=np.array([1.0]),
            method='L-BFGS-B',
            bounds=[(0.01, 10.0)],
            options={'maxiter': max_iter}
        )

        self.temperature = result.x[0]
        return self

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        """
        Get calibrated probabilities.

        Args:
            logits: Model logits

        Returns:
            Calibrated probabilities
        """
        if logits.ndim == 1:
            logits = logits.reshape(-1, 1)
            is_binary = True
        else:
            is_binary = False

        logits_tensor = torch.FloatTensor(logits)
        scaled_logits = logits_tensor / self.temperature

        if is_binary:
            probs = torch.sigmoid(scaled_logits).numpy().flatten()
        else:
            probs = F.softmax(scaled_logits, dim=1).numpy()

        return probs


class PlattScaling:
    """
    Platt Scaling for calibration.

    Fits logistic regression: p = sigmoid(A*z + B)
    """

    def __init__(self):
        self.lr = LogisticRegression()

    def fit(self, logits: np.ndarray, labels: np.ndarray):
        """
        Fit Platt scaling.

        Args:
            logits: Model logits or scores
            labels: True labels

        Returns:
            self
        """
        if logits.ndim == 1:
            logits = logits.reshape(-1, 1)

        self.lr.fit(logits, labels)
        return self

    def predict_proba(self, logits: np.ndarray) -> np.ndarray:
        """
        Get calibrated probabilities.

        Args:
            logits: Model logits

        Returns:
            Calibrated probabilities
        """
        if logits.ndim == 1:
            logits = logits.reshape(-1, 1)

        probs = self.lr.predict_proba(logits)
        return probs[:, 1] if probs.shape[1] == 2 else probs


class IsotonicCalibration:
    """
    Isotonic Regression for calibration.

    Non-parametric calibration method.
    """

    def __init__(self):
        self.iso_reg = IsotonicRegression(out_of_bounds='clip')

    def fit(self, probs: np.ndarray, labels: np.ndarray):
        """
        Fit isotonic regression.

        Args:
            probs: Predicted probabilities (after sigmoid/softmax)
            labels: True labels

        Returns:
            self
        """
        self.iso_reg.fit(probs, labels)
        return self

    def predict_proba(self, probs: np.ndarray) -> np.ndarray:
        """
        Get calibrated probabilities.

        Args:
            probs: Uncalibrated probabilities

        Returns:
            Calibrated probabilities
        """
        return self.iso_reg.predict(probs)


def plot_reliability_diagram(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
    title: str = "Reliability Diagram",
    ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """
    Plot reliability diagram.

    Args:
        y_true: True labels
        y_prob: Predicted probabilities
        n_bins: Number of bins
        title: Plot title
        ax: Matplotlib axes (creates new if None)

    Returns:
        ax: Matplotlib axes with plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    # Get diagram data
    bin_confs, bin_accs, bin_counts = reliability_diagram_data(
        y_true, y_prob, n_bins
    )

    # Plot perfect calibration line
    ax.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Perfect calibration')

    # Plot actual calibration
    valid_mask = bin_counts > 0
    ax.scatter(
        bin_confs[valid_mask],
        bin_accs[valid_mask],
        s=bin_counts[valid_mask],
        c='blue',
        alpha=0.6,
        edgecolors='black',
        linewidth=2,
        label='Actual'
    )

    # Add bars showing gap
    for conf, acc, count in zip(bin_confs, bin_accs, bin_counts):
        if count > 0:
            color = 'red' if conf > acc else 'green'
            ax.plot([conf, conf], [acc, conf], color=color, alpha=0.3, linewidth=2)

    ax.set_xlabel('Confidence', fontsize=12)
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    # Add ECE to title
    ece = expected_calibration_error(y_true, y_prob, n_bins)
    ax.text(0.05, 0.95, f'ECE = {ece:.4f}',
           transform=ax.transAxes,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
           fontsize=11)

    return ax


def binary_calibration_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute calibration curve for binary classification.

    Args:
        y_true: True binary labels
        y_prob: Predicted probabilities for positive class
        n_bins: Number of bins

    Returns:
        prob_true: Fraction of positives in each bin
        prob_pred: Mean predicted probability in each bin
    """
    bins = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins[1:-1])

    prob_true = []
    prob_pred = []

    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            prob_true.append(y_true[mask].mean())
            prob_pred.append(y_prob[mask].mean())
        else:
            prob_true.append(0)
            prob_pred.append((bins[i] + bins[i+1]) / 2)

    return np.array(prob_true), np.array(prob_pred)


class ClasswiseECE:
    """
    Classwise Expected Calibration Error.

    Computes ECE separately for each class (better for multi-class).
    """

    def __init__(self, n_bins: int = 10):
        self.n_bins = n_bins

    def compute(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        Compute classwise ECE.

        Args:
            y_true: True labels [N]
            y_prob: Predicted probabilities [N, num_classes]

        Returns:
            ece: Average ECE across classes
            class_eces: ECE for each class
        """
        num_classes = y_prob.shape[1]
        class_eces = []

        for c in range(num_classes):
            # Binary labels: is it class c?
            y_true_binary = (y_true == c).astype(float)
            y_prob_class = y_prob[:, c]

            ece = expected_calibration_error(
                y_true_binary, y_prob_class, self.n_bins
            )
            class_eces.append(ece)

        return np.mean(class_eces), np.array(class_eces)


def confidence_histogram(
    y_prob: np.ndarray,
    n_bins: int = 10,
    ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """
    Plot histogram of prediction confidences.

    Args:
        y_prob: Predicted probabilities
        n_bins: Number of bins
        ax: Matplotlib axes

    Returns:
        ax: Axes with histogram
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))

    ax.hist(y_prob, bins=n_bins, alpha=0.7, color='steelblue',
           edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Confidence', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Prediction Confidence Distribution', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    return ax


if __name__ == "__main__":
    print("Calibration utilities loaded successfully!")
    print("\nAvailable functions:")
    print("  - expected_calibration_error: Compute ECE")
    print("  - maximum_calibration_error: Compute MCE")
    print("  - reliability_diagram_data: Get data for plotting")
    print("  - plot_reliability_diagram: Visualize calibration")
    print("\nCalibration methods:")
    print("  - TemperatureScaling: Single parameter, preserves accuracy")
    print("  - PlattScaling: Two parameters, more flexible")
    print("  - IsotonicCalibration: Non-parametric, most flexible")
    print("\nExample usage:")
    print("  scaler = TemperatureScaling()")
    print("  scaler.fit(val_logits, val_labels)")
    print("  calibrated_probs = scaler.predict_proba(test_logits)")
