import pytest
from app.monitoring.benchmark import drift_benchmark

def test_tc19_drift_sensitivity_benchmark():
    """
    TC-19: Verify drift benchmark suite sensitivity to varying shift magnitudes.
    Traceability: FR-03, FR-08.
    """
    results = drift_benchmark.evaluate_sensitivity([0.0, 0.5, 1.5, 3.0])
    assert len(results) == 4

    # Shift 0.0 should not indicate significant drift
    assert results[0]["shift_magnitude_std"] == 0.0
    assert results[0]["psi_score"] < 0.25
    assert results[0]["drift_indicated"] is False

    # Shift 3.0 should indicate significant drift
    assert results[3]["shift_magnitude_std"] == 3.0
    assert results[3]["psi_score"] >= 0.25
    assert results[3]["drift_indicated"] is True
