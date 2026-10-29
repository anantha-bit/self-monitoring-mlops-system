import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_tc13_invalid_and_oversized_payload():
    """
    TC-13: Submit malformed types, invalid ranges, and oversized payload.
    Verify service safely rejects without crash.
    Traceability: SR-04.
    """
    headers = {"X-API-Key": "service-secret-key-prod-demo"}

    # 1. Invalid negative latency
    res_neg = client.post(
        "/api/v1/events/prediction",
        json={"request_id": "req-invalid", "model_version": "v1.0", "latency_ms": -10.0, "success": True},
        headers=headers
    )
    assert res_neg.status_code == 422

    # 2. Oversized payload (> 5MB)
    huge_str = "A" * (6 * 1024 * 1024)
    res_huge = client.post(
        "/api/v1/events/prediction",
        content=huge_str,
        headers={"Content-Type": "application/json", "X-API-Key": "service-secret-key-prod-demo"}
    )
    assert res_huge.status_code == 413

def test_tc14_secret_leakage_protection():
    """
    TC-14: Search error responses to ensure API keys and passwords are never echoed in error traces.
    Traceability: SR-03, NFR-11.
    """
    # Trigger an authentication error with bad key
    bogus_key = "secret_canary_super_confidential_12345"
    res = client.get("/api/v1/metrics/summary", headers={"X-API-Key": bogus_key})
    assert res.status_code == 401
    
    # Body must not reveal secret values or system tokens
    body_str = res.text
    assert bogus_key not in body_str
    assert settings.ADMIN_API_KEY not in body_str
    assert settings.ML_ENGINEER_API_KEY not in body_str
