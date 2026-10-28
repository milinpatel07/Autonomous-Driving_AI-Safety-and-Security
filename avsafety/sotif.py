"""Criticality metrics and the RSS longitudinal safety envelope.

RSS: S. Shalev-Shwartz, S. Shammah, A. Shashua, "On a Formal Model of Safe and
Scalable Self-driving Cars", arXiv:1708.06374 (2017), Definition 1.
"""
from __future__ import annotations

import math


def time_to_collision(gap_m: float, v_follow: float, v_lead: float) -> float:
    """TTC in seconds for a follower approaching a leader on the same path (inf if not closing)."""
    closing = v_follow - v_lead
    if gap_m <= 0:
        return 0.0
    return gap_m / closing if closing > 0 else math.inf


def time_headway(gap_m: float, v_follow: float) -> float:
    """THW = gap / follower speed (s)."""
    return gap_m / v_follow if v_follow > 0 else math.inf


def drac(gap_m: float, v_follow: float, v_lead: float) -> float:
    """Deceleration rate to avoid crash, (v_f - v_l)^2 / (2 gap), in m/s^2 (0 if not closing)."""
    closing = v_follow - v_lead
    if closing <= 0:
        return 0.0
    if gap_m <= 0:
        return math.inf
    return closing ** 2 / (2 * gap_m)


def rss_safe_longitudinal_distance(v_rear: float, v_front: float, rho: float = 0.5,
                                   a_max_accel: float = 2.0, b_min_brake: float = 4.0,
                                   b_max_brake: float = 8.0) -> float:
    """Minimal safe longitudinal distance (m) for same-direction driving.

    v_rear / v_front in m/s; rho response time (s); a_max_accel the rear car's worst-case
    acceleration during rho; b_min_brake the rear car's guaranteed braking afterwards;
    b_max_brake the front car's maximum braking. All accelerations positive (m/s^2).
    """
    if min(rho, a_max_accel, b_min_brake, b_max_brake) < 0 or b_min_brake == 0 or b_max_brake == 0:
        raise ValueError("parameters must be positive")
    v_after = v_rear + rho * a_max_accel
    d = (v_rear * rho + 0.5 * a_max_accel * rho ** 2
         + v_after ** 2 / (2 * b_min_brake) - v_front ** 2 / (2 * b_max_brake))
    return max(d, 0.0)


def stopping_distance(v: float, reaction_s: float, decel: float) -> float:
    """Reaction distance plus braking distance (m)."""
    return v * reaction_s + v ** 2 / (2 * decel)
