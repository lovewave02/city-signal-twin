from __future__ import annotations


def stress_index(transit_delay: float, pm25: float, discomfort_index: float) -> float:
    """Weighted stress score (0-100ish for typical city ranges)."""
    return 0.4 * transit_delay + 0.35 * pm25 + 0.25 * discomfort_index


def discomfort_index(temp_c: float, humidity_pct: float) -> float:
    """Approximate discomfort metric derived from temperature/humidity.

    Formula is a practical approximation for visualization (not a medical index).
    """
    return 0.81 * temp_c + 0.01 * humidity_pct * (0.99 * temp_c - 14.3) + 46.3
