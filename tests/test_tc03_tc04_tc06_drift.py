import pytest
import numpy as np
from fastapi.testclient import TestClient
from app.main import app
from app.monitoring.drift import drift_analyzer
from app.models.ml_monitor import ml_monitor

client = TestClient(app)

@pytest.fixture(autouse=True)
def init_baseline():
    ml_monitor.train_baseline()
    drift_analyzer.set_reference_data(ml_monitor.reference_data)

def test_tc03_stable_reference_data():
    """
    TC-03: Compare current sample from the same distribution as reference.
    Traceability: FR-03.
    """
    # Sample from exact reference distributions with minor Gaussian noise
    stable_features = {}
    for col, vals in ml_monitor.reference_data.items():
        sample = np.random.choice(vals, size=40, replace=True) + np.random.normal(0, 0.01, size=40)
        stable_features[col] = sample.tolist()

    res = client.post(
        "/api/v1/drift/analyze",
        json={"current_features": stable_features},
        headers={"X-API-Key": "engineer-secret-key-prod-demo"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["drift_status"] in ["NO_DRIFT", "DRIFT_WARNING"]
    assert data["drift_detected"] is False

def test_tc04_shifted_input_data_triggers_alert():
    """
    TC-04: Submit feature-shifted data and verify drift detection and alert generation.
    Traceability: FR-03, FR-08.
    """
    # Create shifted data: shift mean of all features by 5 standard deviations
    shifted_features = {}
    for col, vals in ml_monitor.reference_data.items():
        mean_val = float(np.mean(vals))
        std_val = float(np.std(vals))
        shifted = np.random.normal(mean_val + 5 * std_val, std_val, size=50)
        shifted_features[col] = shifted.tolist()

    res = client.post(
        "/api/v1/drift/analyze",
        json={"current_features": shifted_features},
        headers={"X-API-Key": "engineer-secret-key-prod-demo"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["drift_detected"] is True
    assert data["drift_status"] == "DRIFT_DETECTED"
    assert len(data["new_alerts"]) >= 1

    # Verify alert appears in /api/v1/alerts
    alerts_res = client.get("/api/v1/alerts", headers={"X-API-Key": "viewer-secret-key-prod-demo"})
    assert alerts_res.status_code == 200
    alerts = alerts_res.json()
    assert any(a["metric"] == "INPUT_DATA_DRIFT" for a in alerts)

def test_tc06_no_ground_truth_labels():
    """
    TC-06: Query model health/drift summary before labels arrive.
    Verify measured_accuracy is None / UNAVAILABLE and not fabricated.
    Traceability: FR-04.
    """
    test_features = {
        col: vals[:20].tolist() for col, vals in ml_monitor.reference_data.items()
    }
    res = client.post(
        "/api/v1/drift/analyze",
        json={"current_features": test_features, "ground_truth_labels": None},
        headers={"X-API-Key": "engineer-secret-key-prod-demo"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["evaluation"]["ground_truth_status"] == "UNAVAILABLE"
    assert data["evaluation"]["measured_accuracy"] is None
