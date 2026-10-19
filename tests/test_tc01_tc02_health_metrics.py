import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.monitoring.collector import collector

client = TestClient(app)

def test_tc01_health_endpoint():
    """
    TC-01: Verify GET /health returns HTTP 200 and required fields.
    Traceability: FR-01.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "app_name" in data
    assert "app_version" in data
    assert "active_model_version" in data
    assert "timestamp" in data

def test_tc02_prediction_metrics_collection():
    """
    TC-02: Submit 20 successful and 2 failed synthetic events; query summary/metrics.
    Traceability: FR-02, NFR-07.
    """
    collector.clear()
    headers = {"X-API-Key": "service-secret-key-prod-demo"}

    # Submit 20 successful events
    for i in range(20):
        payload = {
            "request_id": f"req-test-success-{i}",
            "model_version": "v1.0.0",
            "latency_ms": 35.5 + i,
            "success": True,
            "prediction": 1
        }
        res = client.post("/api/v1/events/prediction", json=payload, headers=headers)
        assert res.status_code == 202

    # Submit 2 failed events
    for j in range(2):
        payload = {
            "request_id": f"req-test-fail-{j}",
            "model_version": "v1.0.0",
            "latency_ms": 150.0,
            "success": False,
            "error_message": "Timeout in model inference backend"
        }
        res = client.post("/api/v1/events/prediction", json=payload, headers=headers)
        assert res.status_code == 202

    # Query summary
    summary_res = client.get("/api/v1/metrics/summary", headers={"X-API-Key": "viewer-secret-key-prod-demo"})
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["total_requests"] == 22
    assert summary["successful_requests"] == 20
    assert summary["failed_requests"] == 2
    assert summary["error_rate"] == round(2 / 22, 4)
    assert summary["latency_p95_ms"] > 0.0

def test_tc09_latency_and_throughput():
    """
    TC-09: Verify throughput and latency for 100+ events without count loss.
    Traceability: NFR-01, NFR-09.
    """
    headers = {"X-API-Key": "service-secret-key-prod-demo"}
    initial_total = collector.total_requests

    batch_size = 100
    for k in range(batch_size):
        payload = {
            "request_id": f"req-batch-{k}",
            "model_version": "v1.0.0",
            "latency_ms": 25.0,
            "success": True,
            "prediction": 0
        }
        res = client.post("/api/v1/events/prediction", json=payload, headers=headers)
        assert res.status_code == 202

    summary = collector.get_summary()
    assert summary["total_requests"] == initial_total + batch_size
    assert summary["latency_p95_ms"] < 500.0  # NFR-01 SLO check
