import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tc24_prometheus_live_export():
    """
    TC-24: Prometheus text-format scrape live validation.
    Traceability: NFR-07.
    """
    res = client.get("/api/v1/metrics/prometheus")
    assert res.status_code == 200
    assert "text/plain" in res.headers["content-type"]
    text = res.text
    assert "mlops_predictions_total" in text
    assert "mlops_prediction_errors_total" in text
    assert "mlops_prediction_latency_p95_milliseconds" in text
    assert "mlops_error_rate" in text
