import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tc05_ml_dl_qml_experiment_tracking():
    """
    TC-05: Run Classical ML baseline, DL autoencoder anomaly model, and QML simulator benchmark.
    Verify metadata, reproducibility parameters, and isolation.
    Traceability: FR-05, FR-06, FR-07, NFR-04.
    """
    headers = {"X-API-Key": "engineer-secret-key-prod-demo"}

    # 1. Classical ML Baseline
    res_ml = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "classical_ml", "random_seed": 42},
        headers=headers
    )
    assert res_ml.status_code == 200
    ml_data = res_ml.json()
    assert ml_data["model_type"] == "Classical_RandomForest"
    assert "accuracy" in ml_data["metrics"]
    assert ml_data["metrics"]["accuracy"] > 0.85
    assert "candidate_id" in ml_data

    # 2. Deep Learning Sequence Anomaly Model (PyTorch)
    res_dl = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "deep_learning", "random_seed": 42, "parameters": {"epochs": 15}},
        headers=headers
    )
    assert res_dl.status_code == 200
    dl_data = res_dl.json()
    assert dl_data["model_type"] == "DeepLearning_Autoencoder"
    assert "final_train_loss" in dl_data
    assert "anomaly_threshold" in dl_data
    assert "pytorch_version" in dl_data["environment"]

    # 3. Quantum Machine Learning (QML) Simulator Benchmark
    res_qml = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "qml_benchmark", "random_seed": 42},
        headers=headers
    )
    assert res_qml.status_code == 200
    qml_data = res_qml.json()
    assert qml_data["model_type"] == "Quantum_Variational_Classifier_Simulator"
    assert qml_data["quantum_circuit"]["num_qubits"] == 4
    assert qml_data["governance"]["production_eligible"] is False
    assert qml_data["governance"]["isolation_status"] == "ISOLATED_EXPERIMENT_ONLY"

def test_tc16_experiment_reproducibility():
    """
    TC-16: Run same ML experiment twice with identical seed and configuration.
    Verify exact reproduction of metrics.
    Traceability: NFR-04.
    """
    headers = {"X-API-Key": "engineer-secret-key-prod-demo"}

    res1 = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "classical_ml", "random_seed": 123},
        headers=headers
    )
    res2 = client.post(
        "/api/v1/experiments/train",
        json={"experiment_type": "classical_ml", "random_seed": 123},
        headers=headers
    )

    data1 = res1.json()
    data2 = res2.json()

    assert data1["metrics"]["accuracy"] == data2["metrics"]["accuracy"]
    assert data1["metrics"]["f1_score"] == data2["metrics"]["f1_score"]
    assert data1["metrics"]["roc_auc"] == data2["metrics"]["roc_auc"]
