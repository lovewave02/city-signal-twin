from src.model import stress_index


def test_stress_index_positive():
    assert stress_index(1.0, 1.0, 1.0) > 0
