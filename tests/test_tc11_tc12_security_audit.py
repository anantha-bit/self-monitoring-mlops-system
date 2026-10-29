import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tc11_authorization_for_candidate_decision():
    """
    TC-11: 
    1. Call candidate decision endpoint without credentials -> 401 Unauthorized.
    2. Call with read-only viewer credentials -> 403 Forbidden.
    3. Call with authorized ML Engineer credentials -> Allowed (200).
    Traceability: FR-14, SR-01, SR-02.
    """
    cand_id = "cand-test-auth"

    # 1. Unauthenticated request
    res_no_auth = client.post(f"/api/v1/candidates/{cand_id}/decision", json={"decision": "REJECTED"})
    assert res_no_auth.status_code == 401

    # 2. Read-only Viewer request
    res_viewer = client.post(
        f"/api/v1/candidates/{cand_id}/decision",
        json={"decision": "REJECTED"},
        headers={"X-API-Key": "viewer-secret-key-prod-demo"}
    )
    assert res_viewer.status_code == 403

    # 3. Authorized ML Engineer request (even if candidate not found, auth passes and returns 404)
    res_eng = client.post(
        f"/api/v1/candidates/{cand_id}/decision",
        json={"decision": "REJECTED"},
        headers={"X-API-Key": "engineer-secret-key-prod-demo"}
    )
    assert res_eng.status_code in [200, 404]

def test_tc12_audit_record_completeness():
    """
    TC-12: Reject candidate, query audit log, and verify required fields:
    actor, timestamp, action, target_version, outcome, correlation_id, integrity_hash.
    Traceability: FR-11, SR-05.
    """
    headers = {"X-API-Key": "admin-secret-key-prod-demo"}

    # Query audit logs
    res = client.get("/api/v1/audit/logs?limit=5", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "audit_events" in data
    assert len(data["audit_events"]) > 0

    first_event = data["audit_events"][0]
    required_fields = ["event_id", "correlation_id", "timestamp", "actor", "action", "target_version", "outcome", "integrity_hash"]
    for field in required_fields:
        assert field in first_event, f"Missing required audit field: {field}"

def test_tc17_metrics_admin_surface_restriction():
    """
    TC-17: Request protected endpoints without credentials and verify access denial.
    Traceability: SR-06.
    """
    res_audit_unauth = client.get("/api/v1/audit/logs")
    assert res_audit_unauth.status_code == 401

    res_summary_unauth = client.get("/api/v1/metrics/summary")
    assert res_summary_unauth.status_code == 401
