# Copyright (c) 2025 Milin Patel
# Hochschule Kempten - University of Applied Sciences
#
# Autonomous Driving: AI Safety and Security Workshop
# Comprehensive educational materials covering AI-based perception, ISO 26262,
# ISO 21448 (SOTIF), ISO/SAE 21434, and uncertainty quantification for autonomous vehicles.
#
# This project is licensed under the MIT License.
# See the LICENSE file in the root directory for full license text.

"""
Validation Utilities for AV Perception Systems

This module provides tools for safety validation and testing,
including scenario generation, coverage metrics, and test planning.

Author: Milin Patel
Institution: Hochschule Kempten
Session: 4 - Uncertainty Estimation and Validation
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Callable
from enum import Enum
import json


class ScenarioType(Enum):
    """Types of test scenarios."""
    NOMINAL = "nominal"
    EDGE_CASE = "edge_case"
    CORNER_CASE = "corner_case"
    FAILURE_MODE = "failure_mode"


class SafetyLevel(Enum):
    """Safety criticality levels."""
    SAFE = "safe"
    CAUTION = "caution"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class TestScenario:
    """Represents a single test scenario."""
    id: str
    name: str
    scenario_type: ScenarioType
    safety_level: SafetyLevel
    parameters: Dict
    expected_behavior: str
    pass_criteria: Dict
    ood_probability: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.scenario_type.value,
            'safety_level': self.safety_level.value,
            'parameters': self.parameters,
            'expected_behavior': self.expected_behavior,
            'pass_criteria': self.pass_criteria,
            'ood_probability': self.ood_probability
        }


@dataclass
class TestResult:
    """Represents test execution result."""
    scenario_id: str
    passed: bool
    metrics: Dict
    failure_reason: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'scenario_id': self.scenario_id,
            'passed': self.passed,
            'metrics': self.metrics,
            'failure_reason': self.failure_reason,
            'timestamp': self.timestamp
        }


class ScenarioGenerator:
    """
    Generate test scenarios for AV perception validation.

    Implements parameter-space sampling for systematic coverage.
    """

    def __init__(self, seed: int = 42):
        """Initialize generator."""
        self.rng = np.random.RandomState(seed)

    def generate_pedestrian_scenarios(
        self,
        n_scenarios: int = 100,
        parameter_ranges: Optional[Dict] = None
    ) -> List[TestScenario]:
        """
        Generate pedestrian crossing scenarios.

        Args:
            n_scenarios: Number of scenarios to generate
            parameter_ranges: Dict of parameter ranges (uses defaults if None)

        Returns:
            List of test scenarios
        """
        if parameter_ranges is None:
            parameter_ranges = {
                'pedestrian_speed': (0.5, 2.0),  # m/s
                'pedestrian_distance': (5.0, 50.0),  # m
                'ego_speed': (10.0, 50.0),  # km/h
                'weather': ['clear', 'rain', 'fog'],
                'lighting': ['day', 'dusk', 'night'],
                'occlusion': [True, False]
            }

        scenarios = []

        for i in range(n_scenarios):
            # Sample parameters
            ped_speed = self.rng.uniform(*parameter_ranges['pedestrian_speed'])
            ped_dist = self.rng.uniform(*parameter_ranges['pedestrian_distance'])
            ego_speed = self.rng.uniform(*parameter_ranges['ego_speed'])
            weather = self.rng.choice(parameter_ranges['weather'])
            lighting = self.rng.choice(parameter_ranges['lighting'])
            occlusion = self.rng.choice(parameter_ranges['occlusion'])

            # Compute difficulty score
            difficulty = self._compute_difficulty(
                ped_speed, ped_dist, ego_speed, weather, lighting, occlusion
            )

            # Determine scenario type and safety level
            scenario_type, safety_level = self._classify_scenario(difficulty)

            # Create scenario
            scenario = TestScenario(
                id=f"PED_{i:04d}",
                name=f"Pedestrian Crossing {i+1}",
                scenario_type=scenario_type,
                safety_level=safety_level,
                parameters={
                    'pedestrian_speed': ped_speed,
                    'pedestrian_distance': ped_dist,
                    'ego_speed': ego_speed,
                    'weather': weather,
                    'lighting': lighting,
                    'occlusion': occlusion
                },
                expected_behavior="Detect pedestrian and brake if necessary",
                pass_criteria={
                    'detection_distance': 30.0,  # meters
                    'detection_confidence': 0.8,
                    'brake_time': 2.0  # seconds
                },
                ood_probability=self._estimate_ood_probability(weather, lighting)
            )

            scenarios.append(scenario)

        return scenarios

    def _compute_difficulty(
        self,
        ped_speed: float,
        ped_dist: float,
        ego_speed: float,
        weather: str,
        lighting: str,
        occlusion: bool
    ) -> float:
        """Compute scenario difficulty score (0-100)."""
        score = 0.0

        # Higher ego speed = harder
        score += (ego_speed / 50.0) * 25

        # Shorter distance = harder
        score += (1 - ped_dist / 50.0) * 25

        # Faster pedestrian = harder
        score += (ped_speed / 2.0) * 15

        # Environmental factors
        if occlusion:
            score += 15
        if weather != 'clear':
            score += 10
        if lighting != 'day':
            score += 10

        return min(score, 100)

    def _classify_scenario(
        self,
        difficulty: float
    ) -> Tuple[ScenarioType, SafetyLevel]:
        """Classify scenario based on difficulty."""
        if difficulty < 30:
            return ScenarioType.NOMINAL, SafetyLevel.SAFE
        elif difficulty < 50:
            return ScenarioType.NOMINAL, SafetyLevel.CAUTION
        elif difficulty < 70:
            return ScenarioType.EDGE_CASE, SafetyLevel.WARNING
        else:
            return ScenarioType.CORNER_CASE, SafetyLevel.CRITICAL

    def _estimate_ood_probability(self, weather: str, lighting: str) -> float:
        """Estimate probability scenario is OOD."""
        prob = 0.0

        if weather == 'fog':
            prob += 0.3
        elif weather == 'rain':
            prob += 0.1

        if lighting == 'night':
            prob += 0.2
        elif lighting == 'dusk':
            prob += 0.1

        return min(prob, 1.0)


class CoverageAnalyzer:
    """
    Analyze test coverage for systematic validation.
    """

    def __init__(self, parameter_bins: Dict[str, int]):
        """
        Initialize coverage analyzer.

        Args:
            parameter_bins: Dict mapping parameter names to number of bins
        """
        self.parameter_bins = parameter_bins
        self.total_bins = np.prod(list(parameter_bins.values()))
        self.covered_bins = set()

    def update_coverage(self, scenarios: List[TestScenario]):
        """
        Update coverage with tested scenarios.

        Args:
            scenarios: List of tested scenarios
        """
        for scenario in scenarios:
            bin_id = self._discretize_scenario(scenario)
            self.covered_bins.add(bin_id)

    def _discretize_scenario(self, scenario: TestScenario) -> Tuple:
        """Convert scenario to discrete bin identifier."""
        # Simplified discretization
        params = scenario.parameters

        bin_id = []

        # Discretize continuous parameters
        if 'pedestrian_speed' in params:
            bin_id.append(int(params['pedestrian_speed'] * 2))
        if 'pedestrian_distance' in params:
            bin_id.append(int(params['pedestrian_distance'] / 5))
        if 'ego_speed' in params:
            bin_id.append(int(params['ego_speed'] / 10))

        # Add categorical parameters
        if 'weather' in params:
            bin_id.append(params['weather'])
        if 'lighting' in params:
            bin_id.append(params['lighting'])
        if 'occlusion' in params:
            bin_id.append(params['occlusion'])

        return tuple(bin_id)

    def get_coverage_percentage(self) -> float:
        """Get current coverage percentage."""
        return len(self.covered_bins) / self.total_bins * 100

    def get_uncovered_regions(self) -> List[Dict]:
        """Identify uncovered parameter regions."""
        # Simplified: return statistics
        return [{
            'total_bins': self.total_bins,
            'covered_bins': len(self.covered_bins),
            'uncovered_bins': self.total_bins - len(self.covered_bins)
        }]


class StatisticalValidator:
    """
    Compute statistical validation requirements.

    Based on Kalra & Paddock analysis.
    """

    def __init__(self, baseline_rate: float, confidence: float = 0.95):
        """
        Initialize validator.

        Args:
            baseline_rate: Baseline failure rate (failures per mile)
            confidence: Desired confidence level
        """
        self.baseline_rate = baseline_rate
        self.confidence = confidence

    def miles_needed(self, improvement_factor: float = 1.2) -> float:
        """
        Compute miles needed to demonstrate improvement.

        Args:
            improvement_factor: How much better than baseline (e.g., 1.2 = 20% better)

        Returns:
            Miles needed for zero-failure proof
        """
        target_rate = self.baseline_rate / improvement_factor

        # For zero failures, upper confidence bound:
        # λ_upper = -ln(1 - confidence) / n_miles
        # We want λ_upper <= target_rate

        miles = -np.log(1 - self.confidence) / target_rate

        return miles

    def confidence_interval(
        self,
        miles_driven: float,
        failures_observed: int
    ) -> Tuple[float, float]:
        """
        Compute confidence interval for failure rate.

        Poisson distribution for rare events.

        Args:
            miles_driven: Total miles driven
            failures_observed: Number of failures

        Returns:
            (lower_bound, upper_bound) for failure rate
        """
        from scipy import stats

        # Poisson confidence interval
        alpha = 1 - self.confidence

        if failures_observed == 0:
            lower = 0
            upper = -np.log(alpha) / miles_driven
        else:
            lower = stats.chi2.ppf(alpha/2, 2*failures_observed) / (2*miles_driven)
            upper = stats.chi2.ppf(1-alpha/2, 2*(failures_observed+1)) / (2*miles_driven)

        return lower, upper


class PerformanceMetrics:
    """
    Compute safety-specific performance metrics.
    """

    @staticmethod
    def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Compute comprehensive metrics.

        Args:
            y_true: True labels
            y_pred: Predicted labels

        Returns:
            Dictionary of metrics
        """
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        tn = np.sum((y_true == 0) & (y_pred == 0))
        fn = np.sum((y_true == 1) & (y_pred == 0))

        accuracy = (tp + tn) / (tp + fp + tn + fn) if (tp + fp + tn + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        # Safety-critical metrics
        fnr = fn / (tp + fn) if (tp + fn) > 0 else 0  # False Negative Rate
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # False Positive Rate

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'false_negative_rate': fnr,
            'false_positive_rate': fpr,
            'true_positives': int(tp),
            'false_positives': int(fp),
            'true_negatives': int(tn),
            'false_negatives': int(fn)
        }

    @staticmethod
    def safety_score(metrics: Dict[str, float], weights: Optional[Dict] = None) -> float:
        """
        Compute weighted safety score.

        Args:
            metrics: Performance metrics
            weights: Weight for each metric (higher weight = more important)

        Returns:
            Safety score (0-100, higher is better)
        """
        if weights is None:
            # Default: heavily weight recall (don't miss detections!)
            weights = {
                'recall': 0.5,
                'precision': 0.2,
                'f1_score': 0.3
            }

        score = 0.0
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight * 100

        # Penalty for high FNR (safety critical!)
        fnr_penalty = metrics.get('false_negative_rate', 0) * 50
        score = max(0, score - fnr_penalty)

        return min(score, 100)


def generate_test_report(
    scenarios: List[TestScenario],
    results: List[TestResult],
    output_file: Optional[str] = None
) -> Dict:
    """
    Generate comprehensive test report.

    Args:
        scenarios: List of test scenarios
        results: List of test results
        output_file: Optional JSON file to save report

    Returns:
        Report dictionary
    """
    # Aggregate statistics
    total_tests = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total_tests - passed

    # Group by safety level
    critical_scenarios = [s for s in scenarios if s.safety_level == SafetyLevel.CRITICAL]
    critical_results = [r for r in results if any(s.id == r.scenario_id for s in critical_scenarios)]
    critical_passed = sum(1 for r in critical_results if r.passed)

    report = {
        'summary': {
            'total_scenarios': len(scenarios),
            'total_tests': total_tests,
            'passed': passed,
            'failed': failed,
            'pass_rate': passed / total_tests if total_tests > 0 else 0
        },
        'critical_scenarios': {
            'total': len(critical_scenarios),
            'tested': len(critical_results),
            'passed': critical_passed,
            'pass_rate': critical_passed / len(critical_results) if critical_results else 0
        },
        'scenarios': [s.to_dict() for s in scenarios],
        'results': [r.to_dict() for r in results]
    }

    # Save if requested
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    print("Validation utilities loaded successfully!")
    print("\nAvailable classes:")
    print("  - ScenarioGenerator: Generate test scenarios")
    print("  - CoverageAnalyzer: Analyze test coverage")
    print("  - StatisticalValidator: Compute statistical requirements")
    print("  - PerformanceMetrics: Safety-specific metrics")
    print("\nExample usage:")
    print("  gen = ScenarioGenerator()")
    print("  scenarios = gen.generate_pedestrian_scenarios(n_scenarios=100)")
    print("  ")
    print("  validator = StatisticalValidator(baseline_rate=1e-8)")
    print("  miles_needed = validator.miles_needed(improvement_factor=1.2)")
