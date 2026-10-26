import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.registry.mlflow_adapter import model_registry

client = TestClient(app)

def test_tc07_promotion_without_validation_is_blocked():
    """
    TC-07: Attempt to approve and promote a candidate before validation.
    Verify promotion is BLOCKED and model version is unchanged.
    Traceability: FR-10, NFR-10.
    """
    headers = {"X-API-Key": "engineer-secret-key-prod-demo"}

    # Train a new candidate
    train_res = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "classical_ml", "random_seed": 77},
        headers=headers
    )
    cand_id = train_res.json()["candidate_id"]
    initial_active_version = model_registry.active_version

    # Attempt to approve without running validation first
    decision_res = client.post(
        f"/api/v1/candidates/{cand_id}/decision",
        json={"decision": "APPROVED", "comment": "Premature approval attempt"},
        headers=headers
    )
    assert decision_res.status_code == 200
    res_data = decision_res.json()
    assert res_data["status"] == "BLOCKED"
    assert "Promotion blocked" in res_data["message"]
    assert model_registry.active_version == initial_active_version

def test_tc18_candidate_validation_regression_gate():
    """
    TC-18: Submit a candidate with metrics below quality gate.
    Verify validation fails and promotion is blocked.
    Traceability: FR-10, NFR-10.
    """
    headers = {"X-API-Key": "engineer-secret-key-prod-demo"}

    # Register an underperforming candidate
    bad_cand_id = "cand-underperforming-001"
    model_registry.register_candidate(
        candidate_id=bad_cand_id,
        model_type="Classical_RandomForest",
        metrics={
            "accuracy": 0.65,  # Below 0.80 threshold
            "f1_score": 0.60,
            "latency_p95_ms": 200.0  # Above 150ms SLO
        },
        artifact_path="data/models/bad.joblib",
        author="test_runner"
    )

    # Validate candidate
    val_res = client.post(f"/api/v1/candidates/{bad_cand_id}/validate", headers=headers)
    assert val_res.status_code == 200
    report = val_res.json()
    assert report["validation_status"] == "FAILED"
    assert report["all_gates_passed"] is False
    assert report["can_promote"] is False

    # Attempt to approve failed candidate
    decision_res = client.post(
        f"/api/v1/candidates/{bad_cand_id}/decision",
        json={"decision": "APPROVED", "comment": "Force approve regression candidate"},
        headers=headers
    )
    assert decision_res.json()["status"] == "BLOCKED"

def test_tc08_rollback_on_failure():
    """
    TC-08: Trigger rollback to stable version and verify restoration and audit event.
    Traceability: FR-12.
    """
    headers = {"X-API-Key": "engineer-secret-key-prod-demo"}
    stable_ver = model_registry.last_stable_version

    rollback_res = client.post(
        "/api/v1/models/rollback",
        json={"reason": "Simulated post-promotion latency spike"},
        headers=headers
    )
    assert rollback_res.status_code == 200
    data = rollback_res.json()
    assert data["status"] == "ROLLED_BACK"
    assert data["active_version"] == stable_ver
    assert "audit_event_id" in data
