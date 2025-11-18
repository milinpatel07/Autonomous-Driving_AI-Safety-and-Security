"""
Uncertainty Estimation Helper Functions

This module provides utilities for uncertainty quantification in deep learning,
specifically focused on AV perception tasks.

Author: AV Perception Safety Workshop
Session: 4 - Uncertainty Estimation and Validation
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, List, Optional


class MCDropout:
    """
    Monte Carlo Dropout for uncertainty estimation.

    Enables dropout at test time to approximate Bayesian inference.
    """

    def __init__(self, model: nn.Module, n_samples: int = 50):
        """
        Initialize MC Dropout.

        Args:
            model: PyTorch model with dropout layers
            n_samples: Number of MC samples for uncertainty estimation
        """
        self.model = model
        self.n_samples = n_samples

    def enable_dropout(self):
        """Enable dropout layers even in eval mode."""
        for module in self.model.modules():
            if isinstance(module, nn.Dropout):
                module.train()

    def predict_with_uncertainty(
        self,
        x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Get predictions with uncertainty estimates.

        Args:
            x: Input tensor [batch_size, ...]

        Returns:
            mean: Mean predictions [batch_size, num_classes]
            epistemic_std: Epistemic uncertainty (std) [batch_size, num_classes]
            entropy: Predictive entropy [batch_size]
        """
        self.model.eval()  # Set to eval mode
        self.enable_dropout()  # But keep dropout active

        predictions = []

        with torch.no_grad():
            for _ in range(self.n_samples):
                output = self.model(x)

                # Convert to probabilities
                if output.shape[1] > 1:  # Multi-class
                    probs = F.softmax(output, dim=1)
                else:  # Binary
                    probs = torch.sigmoid(output)

                predictions.append(probs)

        # Stack predictions: [n_samples, batch_size, num_classes]
        predictions = torch.stack(predictions)

        # Compute mean and std
        mean = predictions.mean(dim=0)
        epistemic_std = predictions.std(dim=0)

        # Compute predictive entropy
        entropy = -torch.sum(mean * torch.log(mean + 1e-10), dim=1)

        return mean, epistemic_std, entropy

    def predict_classification(
        self,
        x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Predict class labels with confidence.

        Args:
            x: Input tensor

        Returns:
            predictions: Class predictions [batch_size]
            confidence: Prediction confidence [batch_size]
        """
        mean, _, _ = self.predict_with_uncertainty(x)

        predictions = mean.argmax(dim=1)
        confidence = mean.max(dim=1)[0]

        return predictions, confidence


class DeepEnsemble:
    """
    Deep Ensemble for uncertainty estimation.

    Maintains multiple independently trained models.
    """

    def __init__(self, models: List[nn.Module]):
        """
        Initialize ensemble.

        Args:
            models: List of trained models
        """
        self.models = models
        self.n_models = len(models)

    def predict_with_uncertainty(
        self,
        x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Get ensemble predictions with uncertainty.

        Args:
            x: Input tensor

        Returns:
            mean: Mean predictions across models
            epistemic_std: Model disagreement (epistemic uncertainty)
            entropy: Predictive entropy
        """
        predictions = []

        for model in self.models:
            model.eval()
            with torch.no_grad():
                output = model(x)

                # Convert to probabilities
                if output.shape[1] > 1:
                    probs = F.softmax(output, dim=1)
                else:
                    probs = torch.sigmoid(output)

                predictions.append(probs)

        # Stack: [n_models, batch_size, num_classes]
        predictions = torch.stack(predictions)

        # Statistics
        mean = predictions.mean(dim=0)
        epistemic_std = predictions.std(dim=0)
        entropy = -torch.sum(mean * torch.log(mean + 1e-10), dim=1)

        return mean, epistemic_std, entropy

    def predict_classification(
        self,
        x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Predict with ensemble."""
        mean, _, _ = self.predict_with_uncertainty(x)
        predictions = mean.argmax(dim=1)
        confidence = mean.max(dim=1)[0]
        return predictions, confidence


def uncertainty_decomposition(
    predictions: torch.Tensor
) -> Tuple[float, float, float]:
    """
    Decompose total uncertainty into aleatoric and epistemic components.

    For classification, following Kendall & Gal (2017):
    - Total uncertainty = Entropy of mean prediction
    - Aleatoric = Mean of entropies
    - Epistemic = Total - Aleatoric

    Args:
        predictions: Tensor of shape [n_samples, batch_size, num_classes]

    Returns:
        total_uncertainty: Total predictive uncertainty
        aleatoric: Irreducible uncertainty (data noise)
        epistemic: Reducible uncertainty (model uncertainty)
    """
    # Mean prediction across samples
    mean_pred = predictions.mean(dim=0)

    # Total uncertainty: entropy of mean prediction
    total_uncertainty = -torch.sum(
        mean_pred * torch.log(mean_pred + 1e-10),
        dim=1
    ).mean().item()

    # Aleatoric: mean of entropies
    entropies = -torch.sum(
        predictions * torch.log(predictions + 1e-10),
        dim=2
    )
    aleatoric = entropies.mean().item()

    # Epistemic: total - aleatoric
    epistemic = total_uncertainty - aleatoric

    return total_uncertainty, aleatoric, epistemic


def mutual_information(predictions: torch.Tensor) -> torch.Tensor:
    """
    Compute mutual information between predictions and model parameters.

    MI = H[y|x] - E[H[y|x,θ]]

    This is equivalent to epistemic uncertainty for classification.

    Args:
        predictions: [n_samples, batch_size, num_classes]

    Returns:
        mi: Mutual information [batch_size]
    """
    # Mean prediction
    mean_pred = predictions.mean(dim=0)

    # Entropy of mean (total uncertainty)
    H_mean = -torch.sum(mean_pred * torch.log(mean_pred + 1e-10), dim=1)

    # Mean of entropies (aleatoric)
    entropies = -torch.sum(predictions * torch.log(predictions + 1e-10), dim=2)
    E_H = entropies.mean(dim=0)

    # Mutual information (epistemic)
    mi = H_mean - E_H

    return mi


def variation_ratio(predictions: torch.Tensor) -> torch.Tensor:
    """
    Compute variation ratio: fraction of predictions NOT in modal class.

    Simple uncertainty measure: 0 = all agree, 1 = maximum disagreement.

    Args:
        predictions: [n_samples, batch_size, num_classes]

    Returns:
        vr: Variation ratio [batch_size]
    """
    # Get predicted classes for each sample
    pred_classes = predictions.argmax(dim=2)  # [n_samples, batch_size]

    # Find modal class
    modal_class = torch.mode(pred_classes, dim=0)[0]  # [batch_size]

    # Count predictions that match modal class
    matches = (pred_classes == modal_class.unsqueeze(0)).float()
    match_freq = matches.mean(dim=0)

    # Variation ratio = 1 - frequency of modal class
    vr = 1 - match_freq

    return vr


class UncertaintyThresholdClassifier:
    """
    Classifier that uses uncertainty for decision-making.

    Implements uncertainty-aware thresholds for safety-critical decisions.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.8,
        epistemic_threshold: float = 0.1,
        fallback_action: str = "reject"
    ):
        """
        Initialize uncertainty-aware classifier.

        Args:
            confidence_threshold: Minimum confidence for positive prediction
            epistemic_threshold: Maximum epistemic uncertainty allowed
            fallback_action: What to do when uncertain ("reject", "conservative", etc.)
        """
        self.confidence_threshold = confidence_threshold
        self.epistemic_threshold = epistemic_threshold
        self.fallback_action = fallback_action

    def classify_with_uncertainty(
        self,
        mean_pred: torch.Tensor,
        epistemic_unc: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Classify with uncertainty-based decision logic.

        Args:
            mean_pred: Mean predictions [batch_size, num_classes]
            epistemic_unc: Epistemic uncertainty [batch_size, num_classes]

        Returns:
            decisions: Final decisions [batch_size]
            flags: Uncertainty flags [batch_size] (0=confident, 1=uncertain)
        """
        batch_size = mean_pred.shape[0]

        # Get predicted class and confidence
        confidence, pred_class = mean_pred.max(dim=1)

        # Check epistemic uncertainty for predicted class
        epistemic_for_pred = epistemic_unc.gather(1, pred_class.unsqueeze(1)).squeeze(1)

        # Flag uncertain predictions
        uncertain = (confidence < self.confidence_threshold) | \
                   (epistemic_for_pred > self.epistemic_threshold)

        # Make decisions
        decisions = pred_class.clone()

        if self.fallback_action == "reject":
            decisions[uncertain] = -1  # Reject uncertain
        elif self.fallback_action == "conservative":
            # For binary: choose safer option (e.g., assume pedestrian present)
            decisions[uncertain] = 1

        return decisions, uncertain.long()


def compute_ood_score(
    mean_pred: torch.Tensor,
    epistemic_unc: torch.Tensor,
    entropy: torch.Tensor
) -> torch.Tensor:
    """
    Compute out-of-distribution score.

    Combines multiple uncertainty signals.

    Args:
        mean_pred: Mean predictions
        epistemic_unc: Epistemic uncertainty
        entropy: Predictive entropy

    Returns:
        ood_score: OOD score [batch_size] (higher = more likely OOD)
    """
    # Maximum probability (lower = more uncertain)
    max_prob = mean_pred.max(dim=1)[0]

    # Average epistemic uncertainty
    avg_epistemic = epistemic_unc.mean(dim=1)

    # Normalize and combine
    # OOD is characterized by: low max_prob, high epistemic, high entropy
    ood_score = (1 - max_prob) * 0.4 + \
                avg_epistemic * 0.4 + \
                (entropy / np.log(mean_pred.shape[1])) * 0.2

    return ood_score


if __name__ == "__main__":
    print("Uncertainty estimation utilities loaded successfully!")
    print("\nAvailable functions:")
    print("  - MCDropout: Monte Carlo Dropout implementation")
    print("  - DeepEnsemble: Deep ensemble implementation")
    print("  - uncertainty_decomposition: Decompose total/aleatoric/epistemic")
    print("  - mutual_information: Compute epistemic uncertainty")
    print("  - variation_ratio: Simple disagreement measure")
    print("  - UncertaintyThresholdClassifier: Uncertainty-aware decisions")
    print("  - compute_ood_score: Out-of-distribution detection")
