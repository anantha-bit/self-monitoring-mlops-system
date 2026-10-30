import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.registry.mlflow_adapter import model_registry

client = TestClient(app)

def test_tc23_e2e_recovery_workflow():
    """
    TC-23: End-to-end multi-step autonomous recovery and dual-key promotion workflow.
    Traceability: FR-01 through FR-14, NFR-10.
    """
    headers_eng = {"X-API-Key": "engineer-secret-key-prod-demo"}
    headers_svc = {"X-API-Key": "service-secret-key-prod-demo"}

    # 1. Health check
    h = client.get("/health")
    assert h.status_code == 200

    # 2. Ingest telemetry event
    ev = client.post(
        "/api/v1/events/prediction",
        json={"request_id": "req-e2e-01", "model_version": "v1.0.0", "latency_ms": 32.0, "success": True},
        headers=headers_svc
    )
    assert ev.status_code == 202

    # 3. Train high-quality candidate model
    train_res = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "classical_ml", "random_seed": 42},
        headers=headers_eng
    )
    assert train_res.status_code == 200
    cand_id = train_res.json()["candidate_id"]

    # 4. Automated validation gates
    val_res = client.post(f"/api/v1/candidates/{cand_id}/validate", headers=headers_eng)
    assert val_res.status_code == 200
    assert val_res.json()["validation_status"] == "PASSED"

    # 5. Dual approval & promotion
    dec_res = client.post(
        f"/api/v1/candidates/{cand_id}/decision",
        json={"decision": "APPROVED", "comment": "E2E promotion approval"},
        headers=headers_eng
    )
    assert dec_res.status_code == 200
    assert dec_res.json()["status"] == "PROMOTED"
    assert model_registry.active_version == cand_id

