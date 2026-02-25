def stress_index(transit_delay: float, pm25: float, discomfort_index: float) -> float:
    return 0.4 * transit_delay + 0.35 * pm25 + 0.25 * discomfort_index
