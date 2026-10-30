import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.recovery.policy import recovery_policy

client = TestClient(app)

def test_tc25_recovery_policy_and_app_endpoints():
    """
    TC-25: Recovery policy boundary tests and application navigation routes.
    Traceability: FR-09, FR-13.
    """
    # 1. Normal telemetry -> ineligible
    eval1 = recovery_policy.evaluate_retraining_trigger(drift_status="NO_DRIFT", error_rate=0.01, p95_latency_ms=40.0)
    assert eval1["retraining_eligible"] is False

    # 2. Severe drift -> eligible
    eval2 = recovery_policy.evaluate_retraining_trigger(drift_status="DRIFT_DETECTED", error_rate=0.01, p95_latency_ms=40.0)
    assert eval2["retraining_eligible"] is True

    # 3. High error rate -> eligible
    eval3 = recovery_policy.evaluate_retraining_trigger(drift_status="NO_DRIFT", error_rate=0.08, p95_latency_ms=40.0)
    assert eval3["retraining_eligible"] is True

    # 4. Latency breach -> eligible
    eval4 = recovery_policy.evaluate_retraining_trigger(drift_status="NO_DRIFT", error_rate=0.01, p95_latency_ms=600.0)
    assert eval4["retraining_eligible"] is True

    # 5. Root redirect and dashboard HTML
    res_root = client.get("/", follow_redirects=False)
    assert res_root.status_code in [302, 307]

    res_dash = client.get("/dashboard")
    assert res_dash.status_code == 200
    assert "Self-Monitoring MLOps Dashboard" in res_dash.text

