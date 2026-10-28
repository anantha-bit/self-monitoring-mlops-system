import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_tc10_monitoring_worker_failure_isolation():
    """
    TC-10: Simulate an internal exception inside drift/monitoring analyzer.
    Verify the primary health endpoint and prediction service remain online (NFR-02).
    Traceability: NFR-02.
    """
    # Verify health endpoint is 200 before fault injection
    health1 = client.get("/health")
    assert health1.status_code == 200

    # Inject simulated fault in drift analyzer
    with patch("app.monitoring.drift.drift_analyzer.compare_windows", side_effect=RuntimeError("Worker isolated fault")):
        try:
            client.post(
                "/api/v1/drift/analyze",
                json={"current_features": {"feat_0": [1.0, 2.0, 3.0]}},
                headers={"X-API-Key": "engineer-secret-key-prod-demo"}
            )
        except Exception:
            pass

    # Health endpoint must remain fully available despite worker fault
    health2 = client.get("/health")
    assert health2.status_code == 200
    assert health2.json()["status"] == "HEALTHY"
