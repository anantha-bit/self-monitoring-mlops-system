import time
import uuid
from typing import Dict, Any, List, Optional
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, Response
from pydantic import BaseModel, Field, validator

from app.config import settings
from app.security.auth import get_current_user, require_roles, Role, User
from app.security.audit import audit_logger
from app.monitoring.collector import collector
from app.monitoring.drift import drift_analyzer
from app.models.ml_monitor import ml_monitor
from app.models.dl_monitor import dl_monitor
from app.models.dl_visualizer import latent_analyzer
from app.models.qml_benchmark import qml_benchmark
from app.monitoring.benchmark import drift_benchmark
from app.recovery.validator import validator as candidate_validator
from app.recovery.policy import recovery_policy
from app.recovery.health_checker import health_tripwire
from app.registry.mlflow_adapter import model_registry
from app.security.verifier import audit_verifier

router = APIRouter()

# -----------------
# Request Models
# -----------------
class DLScoreRequest(BaseModel):
    features: List[float] = Field(..., min_length=1, max_length=50)

class QMLSimulateRequest(BaseModel):
    sample_size: int = Field(100, ge=10, le=1000)
    circuit_depth: int = Field(2, ge=1, le=5)
    parameter_shift: Optional[float] = Field(0.0)

class PredictionTelemetryRequest(BaseModel):
    request_id: str = Field(..., max_length=64, description="Unique request correlation ID")
    model_version: str = Field(..., max_length=32)
    latency_ms: float = Field(..., ge=0.0, le=10000.0, description="Latency in milliseconds")
    success: bool
    feature_summary: Optional[Dict[str, float]] = None
    prediction: Optional[int] = Field(None, ge=0, le=10)
    error_message: Optional[str] = Field(None, max_length=256)

class LivePredictionRequest(BaseModel):
    features: List[float] = Field(..., min_length=1, max_length=50)

class DriftAnalysisRequest(BaseModel):
    current_features: Dict[str, List[float]]
    ground_truth_labels: Optional[List[int]] = None
    predictions: Optional[List[int]] = None

class CandidateDecisionRequest(BaseModel):
    decision: str = Field(..., pattern="^(APPROVED|REJECTED)$")
    comment: str = Field("", max_length=500)

class RollbackRequest(BaseModel):
    reason: str = Field(..., min_length=3, max_length=256)

class ExperimentTrainRequest(BaseModel):
    experiment_type: str = Field(..., pattern="^(classical_ml|deep_learning|qml_benchmark)$")
    random_seed: int = Field(42, ge=0, le=999999)
    parameters: Optional[Dict[str, Any]] = None

# -----------------
# Endpoints
# -----------------

@router.get("/health", tags=["System Health"])
def get_health():
    """
    Service health probe.
    Conforms to FR-01 and TC-01: returns HTTP 200 and required fields.
    """
    return {
        "status": "HEALTHY",
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "active_model_version": model_registry.active_version,
        "timestamp": time.time(),
        "utc_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

@router.get("/api/v1/metrics/summary", tags=["Monitoring"])
def get_metrics_summary(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Read aggregate operational and drift metrics.
    Conforms to FR-02, NFR-07, TC-02.
    """
    summary = collector.get_summary(active_model_version=model_registry.active_version)
    alerts = drift_analyzer.get_alerts()
    open_alerts = [a for a in alerts if a["status"] == "OPEN"]
    
    summary["active_alerts_count"] = len(open_alerts)
    summary["latest_drift_status"] = "DRIFT_DETECTED" if open_alerts else "NO_DRIFT"
    return summary

@router.get("/api/v1/metrics/prometheus", tags=["Monitoring"])
def get_prometheus_metrics():
    """
    Prometheus scraping endpoint.
    Conforms to NFR-07.
    """
    content = collector.export_prometheus_metrics()
    return Response(content=content, media_type="text/plain")

@router.get("/api/v1/alerts", tags=["Monitoring"])
def list_alerts(
    status_filter: Optional[str] = Query(None, alias="status"),
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER]))
):
    """
    List monitoring alerts.
    Conforms to FR-08.
    """
    return drift_analyzer.get_alerts(status_filter=status_filter)

@router.post("/api/v1/events/prediction", status_code=status.HTTP_202_ACCEPTED, tags=["Monitoring"])
def record_prediction_event(
    event: PredictionTelemetryRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.SERVICE]))
):
    """
    Record prediction telemetry event.
    Conforms to FR-02, NFR-09, TC-02, TC-09, TC-13.
    """
    record = collector.record_event(
        request_id=event.request_id,
        model_version=event.model_version,
        latency_ms=event.latency_ms,
        success=event.success,
        feature_summary=event.feature_summary,
        prediction=event.prediction,
        error_message=event.error_message
    )
    return {
        "status": "ACCEPTED",
        "event_id": record["request_id"],
        "ingested_at": record["timestamp"]
    }

@router.post("/api/v1/predict", tags=["Inference"])
def live_predict(
    payload: LivePredictionRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.SERVICE]))
):
    """
    Serve model predictions with automated telemetry tracking.
    """
    start_time = time.time()
    req_id = f"req-{uuid.uuid4().hex[:8]}"
    features_arr = np.array(payload.features).reshape(1, -1)
    
    # Pad or slice to 6 features if necessary for demo stability
    if features_arr.shape[1] < 6:
        features_arr = np.pad(features_arr, ((0, 0), (0, 6 - features_arr.shape[1])), 'constant')
    elif features_arr.shape[1] > 6:
        features_arr = features_arr[:, :6]

    try:
        preds, probs = ml_monitor.predict(features_arr)
        pred_label = int(preds[0])
        prob_val = float(probs[0][pred_label])
        latency_ms = (time.time() - start_time) * 1000.0

        collector.record_event(
            request_id=req_id,
            model_version=model_registry.active_version,
            latency_ms=latency_ms,
            success=True,
            feature_summary={f"f_{i}": float(features_arr[0, i]) for i in range(6)},
            prediction=pred_label
        )

        return {
            "request_id": req_id,
            "model_version": model_registry.active_version,
            "prediction": pred_label,
            "confidence": round(prob_val, 4),
            "latency_ms": round(latency_ms, 2)
        }
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000.0
        collector.record_event(
            request_id=req_id,
            model_version=model_registry.active_version,
            latency_ms=latency_ms,
            success=False,
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail="Inference processing failed.")

@router.post("/api/v1/drift/analyze", tags=["Drift Analysis"])
def analyze_drift(
    request: DriftAnalysisRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Trigger drift analysis against reference distribution.
    Conforms to FR-03, FR-04, FR-08, TC-03, TC-04, TC-06.
    """
    curr_dict = {k: np.array(v, dtype=float) for k, v in request.current_features.items()}
    ground_truth = np.array(request.ground_truth_labels) if request.ground_truth_labels is not None else None
    preds = np.array(request.predictions) if request.predictions is not None else None

    # If reference data not set, initialize from baseline model
    if not drift_analyzer.reference_data:
        ml_monitor.train_baseline()
        drift_analyzer.set_reference_data(ml_monitor.reference_data)

    report = drift_analyzer.compare_windows(
        current_data=curr_dict,
        ground_truth_labels=ground_truth,
        predictions=preds
    )
    return report

@router.post("/api/v1/experiments/train", tags=["Model Experiments"])
def run_model_experiment(
    request: ExperimentTrainRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Execute ML baseline, DL sequence anomaly detector, or isolated QML benchmark.
    Conforms to FR-05, FR-06, FR-07, TC-05, TC-16.
    """
    exp_type = request.experiment_type
    seed = request.random_seed
    params = request.parameters or {}

    if exp_type == "classical_ml":
        res = ml_monitor.train_baseline(
            n_estimators=params.get("n_estimators", 50),
            max_depth=params.get("max_depth", 5)
        )
        # Register as potential candidate
        candidate_id = f"cand-rf-{int(time.time())}"
        model_registry.register_candidate(
            candidate_id=candidate_id,
            model_type=res["model_type"],
            metrics=res["metrics"],
            artifact_path=res["artifact_path"],
            author=user.username
        )
        res["candidate_id"] = candidate_id
        return res

    elif exp_type == "deep_learning":
        # Train autoencoder on baseline training data
        if not ml_monitor.reference_data:
            ml_monitor.train_baseline()
        train_matrix = np.column_stack(list(ml_monitor.reference_data.values()))
        res = dl_monitor.train_sequence_anomaly_model(
            training_data=train_matrix,
            epochs=params.get("epochs", 25),
            lr=params.get("lr", 0.01)
        )
        return res

    elif exp_type == "qml_benchmark":
        res = qml_benchmark.run_benchmark(sample_size=params.get("sample_size", 100))
        return res

@router.get("/api/v1/candidates", tags=["Recovery & Candidates"])
def list_candidates(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER]))):
    """
    List model retraining candidates and status.
    """
    return model_registry.list_candidates()

@router.post("/api/v1/candidates/{candidate_id}/validate", tags=["Recovery & Candidates"])
def validate_candidate(
    candidate_id: str,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Run automated validation gates for candidate.
    Conforms to FR-10, TC-07, TC-18.
    """
    try:
        report = model_registry.validate_candidate(candidate_id)
        return report
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/candidates/{candidate_id}/decision", tags=["Recovery & Candidates"])
def candidate_decision(
    candidate_id: str,
    request: CandidateDecisionRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Approve or reject a model candidate.
    Conforms to FR-10, FR-14, TC-11, TC-12.
    """
    try:
        result = model_registry.record_decision(
            candidate_id=candidate_id,
            decision=request.decision,
            actor=user.username,
            comment=request.comment
        )
        return result
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/models/rollback", tags=["Recovery & Candidates"])
def trigger_rollback(
    request: RollbackRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Rollback to the last known stable model version.
    Conforms to FR-12 and TC-08.
    """
    result = model_registry.rollback(actor=user.username, reason=request.reason)
    return result

@router.get("/api/v1/audit/logs", tags=["Security & Audit"])
def query_audit_logs(
    action: Optional[str] = Query(None),
    actor: Optional[str] = Query(None),
    target_version: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER]))
):
    """
    Query tamper-resistant audit trail.
    Conforms to FR-11, SR-05, TC-12.
    """
    events = audit_logger.query_events(
        action=action,
        actor=actor,
        target_version=target_version,
        limit=limit
    )
    return {"count": len(events), "audit_events": events}

@router.get("/api/v1/models/ml/info", tags=["Machine Learning"])
def get_ml_model_info(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Retrieve Classical Random Forest model metadata, actual feature importances, and dataset descriptors.
    """
    return ml_monitor.get_model_info()

@router.get("/api/v1/models/dl/info", tags=["Deep Learning"])
def get_dl_model_info(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Retrieve PyTorch Sequence Autoencoder architecture details, threshold, and latent parameters.
    """
    dl_monitor.ensure_model_ready()
    return {
        "model_type": "DeepLearning_Autoencoder",
        "model_version": dl_monitor.version,
        "architecture": "PyTorch MLP-Autoencoder [Linear(6, 3) -> ReLU -> Linear(3, 2) -> ReLU -> Linear(2, 3) -> ReLU -> Linear(3, 6)]",
        "input_dimensions": dl_monitor.input_dim,
        "compressed_latent_dimensions": 2,
        "anomaly_threshold": round(dl_monitor.anomaly_threshold, 4),
        "loss_function": "Mean Squared Error (MSE)",
        "optimization": "Adam Optimizer (lr=0.01)"
    }

@router.post("/api/v1/models/dl/score", tags=["Deep Learning"])
def score_dl_sample(
    request: DLScoreRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))
):
    """
    Execute actual PyTorch Autoencoder forward pass on input sample vector.
    Returns 2D latent representation, reconstructed vector, per-feature errors, and anomaly status.
    """
    features_arr = np.array(request.features, dtype=float)
    if len(features_arr) < 6:
        features_arr = np.pad(features_arr, (0, 6 - len(features_arr)), 'constant')
    elif len(features_arr) > 6:
        features_arr = features_arr[:6]

    result = dl_monitor.score_sample(features_arr)
    # Map feature names
    feat_names = ml_monitor.feature_names if ml_monitor.feature_names else [f"feat_{i}" for i in range(6)]
    result["feature_names"] = feat_names
    result["original"] = [round(float(v), 4) for v in features_arr]
    result["per_feature_error_map"] = {
        feat_names[i]: result["feature_errors"][i] for i in range(min(len(feat_names), len(result["feature_errors"])))
    }
    return result

@router.post("/api/v1/models/qml/simulate", tags=["Quantum ML"])
def simulate_qml_benchmark(
    request: QMLSimulateRequest,
    user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))
):
    """
    Execute 4-qubit Variational Quantum Circuit simulation with statevector probabilities.
    Strictly isolated experimental benchmark according to FR-07.
    """
    return qml_benchmark.simulate_statevector(
        sample_size=request.sample_size,
        depth=request.circuit_depth,
        parameter_shift=request.parameter_shift or 0.0
    )

@router.get("/api/v1/drift/reference", tags=["Drift Analysis"])
def get_drift_reference_distribution(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Retrieve baseline reference distributions, statistics, and histogram data for all 6 features.
    """
    if not drift_analyzer.reference_data:
        ml_monitor.train_baseline()
        drift_analyzer.set_reference_data(ml_monitor.reference_data)

    feature_distributions = {}
    for feat_name, arr in drift_analyzer.reference_data.items():
        counts, bin_edges = np.histogram(arr, bins=10)
        feature_distributions[feat_name] = {
            "mean": round(float(np.mean(arr)), 4),
            "std": round(float(np.std(arr)), 4),
            "min": round(float(np.min(arr)), 4),
            "max": round(float(np.max(arr)), 4),
            "bins": [round(float(b), 2) for b in bin_edges],
            "counts": [int(c) for c in counts],
            "sample_values": [round(float(v), 2) for v in arr[:30]]
        }
    return {
        "status": "INITIALIZED",
        "features": feature_distributions,
        "sample_count": len(next(iter(drift_analyzer.reference_data.values()))) if drift_analyzer.reference_data else 0
    }

@router.get("/api/v1/drift/benchmark", tags=["Drift Analysis"])
def run_drift_sensitivity_benchmark(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Run empirical sensitivity and robustness benchmark across shift magnitudes for KS and PSI estimators.
    """
    results = drift_benchmark.evaluate_sensitivity([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    return {
        "benchmark_suite": "Two-Sample KS and PSI Sensitivity Suite",
        "sample_size": drift_benchmark.sample_size,
        "results": results
    }

@router.get("/api/v1/registry/overview", tags=["Model Registry"])
def get_registry_overview(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Get full lifecycle view of model registry: production, candidates, archived, and rollback history.
    """
    return model_registry.get_registry_overview()

@router.get("/api/v1/audit/verify", tags=["Security & Audit"])
def verify_audit_chain(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER]))):
    """
    Cryptographically verify the SHA-256 hash chain of the tamper-resistant audit ledger.
    """
    is_valid, msg = audit_verifier.verify_chain(audit_logger._memory_cache)
    return {
        "verified": is_valid,
        "message": msg,
        "total_records": len(audit_logger._memory_cache),
        "latest_integrity_hash": audit_logger._last_hash
    }

@router.get("/api/v1/system/telemetry", tags=["Monitoring"])
def get_system_telemetry(user: User = Depends(require_roles([Role.ADMIN, Role.ML_ENGINEER, Role.VIEWER, Role.SERVICE]))):
    """
    Get live system telemetry stream, latencies, collector queue, and tripwire health.
    """
    summary = collector.get_summary(active_model_version=model_registry.active_version)
    tripwire_healthy, tripwire_status = health_tripwire.check_telemetry(
        summary["error_rate"],
        summary["latency_p95_ms"]
    )
    return {
        "summary": summary,
        "recent_events": collector.recent_events[-20:] if collector.recent_events else [],
        "latencies_sample": collector.latencies[-30:] if collector.latencies else [],
        "tripwire": {
            "healthy": tripwire_healthy,
            "status": tripwire_status,
            "consecutive_failures": health_tripwire.consecutive_failures
        },
        "drift_status": "DRIFT_DETECTED" if len(drift_analyzer.get_alerts(status_filter="OPEN")) > 0 else "NO_DRIFT",
        "open_alerts": drift_analyzer.get_alerts(status_filter="OPEN"),
        "timestamp": time.time()
    }
