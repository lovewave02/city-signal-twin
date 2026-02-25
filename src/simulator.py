from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from .model import discomfort_index, stress_index

AREAS = [
    {"id": "gangnam", "name": "Gangnam", "lat": 37.4979, "lon": 127.0276},
    {"id": "hongdae", "name": "Hongdae", "lat": 37.5563, "lon": 126.9236},
    {"id": "jamsil", "name": "Jamsil", "lat": 37.5133, "lon": 127.1028},
    {"id": "gwanghwamun", "name": "Gwanghwamun", "lat": 37.5759, "lon": 126.9769},
    {"id": "yeouido", "name": "Yeouido", "lat": 37.5219, "lon": 126.9245},
]


def make_city_signals(seed: int = 42) -> dict:
    rng = Random(seed)
    rows = []
    for area in AREAS:
        transit_delay = round(rng.uniform(8, 35), 1)
        pm25 = round(rng.uniform(12, 58), 1)
        temp_c = round(rng.uniform(-2, 32), 1)
        humidity = round(rng.uniform(25, 85), 1)

        d_idx = round(discomfort_index(temp_c, humidity), 1)
        s_idx = round(stress_index(transit_delay, pm25, d_idx), 1)

        rows.append(
            {
                **area,
                "transit_delay_min": transit_delay,
                "pm25": pm25,
                "temp_c": temp_c,
                "humidity_pct": humidity,
                "discomfort_index": d_idx,
                "stress_index": s_idx,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "areas": rows,
    }


def make_hourly_trend(hours: int = 12, seed: int = 42) -> list[dict]:
    rng = Random(seed)
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

    baseline = 41.0
    trend: list[dict] = []
    for i in range(hours):
        ts = now - timedelta(hours=hours - i - 1)
        drift = (i - hours / 2) * 0.6
        noise = rng.uniform(-2.0, 2.0)
        score = round(max(10.0, min(100.0, baseline + drift + noise)), 1)
        trend.append({"ts": ts.isoformat(), "avg_stress_index": score})

    return trend
