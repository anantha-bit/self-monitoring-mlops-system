Software Architecture and Design Specification

Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery

Deliverable 3 — Architecture & Design

Version 1.0

Prepared on: 10 October 2026

Team Members:

Anantha Krishna M A — PES1UG24AM036

AKASH G K — PES1UG24AM022

AMIT PRASAD S G — PES1UG24AM033

Department: CSE (AI & ML)

Document Control

Field

Value

Document title

Architecture and Design - Self-Monitoring MLOps System

Version

Version 1.0

Status

Draft for academic review

Date

10 October 2026

Owner

[Student Name / USN / Section]

Review note

Replace bracketed identity fields and confirm institution-specific template requirements before submission.

1. Introduction

1.1 Purpose

This document describes the proposed architecture and detailed design for the Self-Monitoring MLOps System, including component responsibilities, architectural pattern, security architecture, sequence flows, API contracts, error handling, and traceability to the SRS.

1.2 Scope and design principles

Keep routine monitoring independent of long-running training and QML jobs.

Treat drift as a signal for investigation, not proof of accuracy loss.

Require validation and authorization before promotion.

Record model, dataset, code, configuration, and experiment versions for reproducibility.

Make QML experimental and non-blocking for production recovery.

Prefer observable, testable modules with explicit interfaces.

2. Architecture Overview

2.1 Architectural pattern

The design uses a layered, modular service architecture with event-driven background analysis. The API layer handles requests and authorization; the monitoring layer collects and aggregates telemetry; model-analysis workers execute ML/DL and optional QML experiments; a policy/orchestration layer decides whether to alert or create a candidate; and persistence/observability services store metadata and expose metrics. This pattern isolates expensive jobs and supports independent testing.

2.2 Component diagram

Figure 1. High-level component architecture (logical view).

2.3 Component descriptions

Component

Responsibilities

Key interfaces

Prediction API / Existing model

Serve predictions and provide response/error observations.

REST prediction endpoint; emits request metadata.

Monitoring Collector

Normalize events, aggregate windows, capture latency/errors, attach correlation IDs.

Internal event interface; metrics endpoint.

Drift & Quality Analyzer (ML)

Compute statistical drift indicators, anomaly scores, and optional degradation-risk classification.

Input: reference/current window summaries; output: score/status.

Sequence / Pattern Analyzer (DL)

Evaluate temporal patterns using an LSTM/autoencoder experiment; forecast anomaly/performance trend where data supports it.

Asynchronous job interface; outputs score, model version and metrics.

Experimental QML Benchmark

Run small simulator-based QML comparisons; store outcomes separately.

Offline job interface; cannot directly trigger promotion.

Policy & Recovery Orchestrator

Apply thresholds, deduplicate alerts, decide whether candidate evaluation is permitted, enforce approval/validation gates.

Policy API; job queue; audit events.

MLflow Model Registry / Experiment Tracker

Store run metadata, artifacts, metrics and model versions.

MLflow tracking/registry APIs.

Metrics Store / Audit Log

Expose operational telemetry and persist security/lifecycle events.

Prometheus scrape endpoint; append-oriented audit interface.

Dashboard / Alerting

Display model health, alerts, candidate outcomes, and historical trends.

Dashboard queries; Grafana panels or simple web UI.

2.4 Data flow

Prediction requests produce output plus latency and error metadata.

The collector aggregates current windows and compares them with the reference window.

ML and DL analyzers evaluate monitoring features; QML runs separately as an experiment.

The policy engine applies configured thresholds and determines whether to alert or initiate candidate evaluation.

The candidate training pipeline records artifacts and metrics; the validator checks acceptance gates.

An authorized ML Engineer approves or rejects the candidate; only an approved, valid candidate can be promoted.

Post-promotion checks monitor health. Failed checks trigger rollback to the last known stable version.

Metrics and lifecycle actions are displayed and retained for review.

2.5 Deployment view

The initial demonstration may run as Docker Compose services: API/dashboard, monitoring worker, MLflow, and Prometheus/Grafana. A local volume or lightweight database can persist prototype metadata. In a later deployment, services can be separated into containers and scheduled independently. Kubernetes is optional and not required for the minimum viable prototype.

3. Security Architecture

3.1 Security controls

Control

Design decision

Related requirement

Authentication

Require credentials/token for model-management, approval and administrative endpoints.

SR-01, FR-14

Authorization

Use role-based permissions: read-only viewer, ML Engineer, administrator; enforce server-side.

SR-02

Secret management

Read secrets from environment or secret store; exclude .env and credentials from version control.

SR-03

Input validation

Validate JSON schema, content type, size, numeric bounds, and allowed state transitions.

SR-04

Auditability

Append structured events for approvals, promotions, rollback, configuration changes and denied actions.

SR-05, FR-11

Network restriction

Restrict metrics and admin surfaces to trusted network or authenticated access.

SR-06

Artifact integrity

Record model version, artifact identifier/hash, run ID and source commit for candidates.

FR-10, NFR-04

Safe automation

Separate candidate evaluation from promotion; require validation and human approval.

NFR-10

3.2 Threats and mitigations

Unauthorized model promotion: server-side RBAC, approval gate, and audit event.

Poisoned or malformed monitoring input: schema/range validation and bounded payload sizes.

Secret leakage through logs: structured logging with redaction and synthetic secret scanning tests.

Compromised candidate artifact: record artifact hash and registry version; validate before promotion.

Denial of service from expensive experiments: execute DL/QML jobs asynchronously with resource limits.

False drift alarm: use configurable thresholds, suppress duplicate alerts, and distinguish drift from measured accuracy loss.

4. Detailed Design

4.1 Module design

Module

Suggested package/file

Main operations

API routes

app/api/routes.py

health(), get_metrics(), list_alerts(), candidate_decision()

Monitoring collector

app/monitoring/collector.py

record_event(), aggregate_window(), export_metrics()

Drift analyzer

app/monitoring/drift.py

compare_windows(), compute_drift_status()

ML experiment

app/models/ml_monitor.py

fit(), evaluate(), save_run_metadata()

DL experiment

app/models/dl_monitor.py

fit_sequence_model(), score_window(), evaluate()

QML benchmark

app/models/qml_benchmark.py

run_benchmark(), save_comparison()

Recovery policy

app/recovery/policy.py

evaluate_trigger(), candidate_eligible(), can_promote()

Validation service

app/recovery/validator.py

validate_candidate(), compare_to_stable()

Registry adapter

app/registry/mlflow_adapter.py

register_candidate(), promote(), rollback()

Audit logger

app/security/audit.py

record_event(), query_events()

4.2 Sequence diagram 1 — Routine monitoring cycle

Figure 2. Logical sequence of a routine monitoring cycle. The monitor writes metrics and requests drift analysis; the result is reflected in alert/dashboard state.

4.3 Sequence diagram 2 — Controlled retraining and promotion

Figure 3. Logical sequence of candidate evaluation and promotion. Human approval and validation are both required; otherwise the stable model remains active.

4.4 API design

The following REST API is a proposed contract for the prototype. All management endpoints require authentication. Exact schemas and status codes should be reflected in OpenAPI generated by FastAPI.

Method and path

Purpose

Request / response summary

Access

GET /health

Liveness/readiness summary.

Response: status, app_version, timestamp.

Public only on local demo; otherwise trusted network.

GET /api/v1/metrics/summary

Read aggregate health metrics.

Response: count, error_rate, latency_p95, drift_status, model_version.

Authenticated viewer.

GET /api/v1/alerts

List alerts.

Optional status/severity filters; response includes alert_id, metric, observed_value, created_at.

Authenticated viewer.

POST /api/v1/events/prediction

Submit/record prediction metadata.

Body: request_id, model_version, latency_ms, success, feature_summary; response: accepted/event_id.

Service identity.

POST /api/v1/candidates/{candidate_id}/validate

Run or retrieve candidate validation.

Response: checks, metrics, pass/fail, run_id.

ML Engineer/admin.

POST /api/v1/candidates/{candidate_id}/decision

Approve or reject a validated candidate.

Body: decision, comment; response: state, audit_event_id.

Authorized ML Engineer/admin.

POST /api/v1/models/rollback

Rollback to stable version.

Body: target_version, reason; response: active_version, outcome.

Administrator or designated ML Engineer.

4.5 Example API payloads

POST /api/v1/events/prediction — illustrative request:

{  "request_id": "req-demo-001",  "model_version": "baseline-1",  "latency_ms": 42.7,  "success": true,  "feature_summary": {"feature_a_mean": 0.31, "feature_b_missing_rate": 0.02}}

Illustrative response: HTTP 202 Accepted with event_id and ingestion status. Raw sensitive feature values should not be sent unless explicitly justified and protected.

4.6 Error handling

Condition

HTTP / system behavior

Logging and recovery

Malformed JSON/schema

400 Bad Request or 422 Unprocessable Entity.

Record request ID and safe validation reason; do not log secrets.

Missing/invalid credentials

401 Unauthorized.

Record security event without credential value.

Insufficient role

403 Forbidden.

Record denied action and actor where known.

Unknown resource/version

404 Not Found.

Return stable error schema.

Conflicting candidate state

409 Conflict.

Do not change active model; return current state.

Rate/size limit exceeded

413 or 429 as appropriate.

Reject request; maintain service availability.

Analyzer or QML worker failure

API remains available; job marked failed.

Log stack trace only in protected logs, emit failure metric and alert.

Registry unavailable

503 Service Unavailable for affected action.

Retry bounded transient failures; never claim promotion succeeded.

Candidate validation fails

Return validation status; no promotion.

Retain stable model; record failed checks.

4.7 Persistence and data model

Entity

Important fields

PredictionEvent

event_id, request_id, timestamp, model_version, latency_ms, success, feature_summary_ref

MonitoringWindow

window_id, start/end, sample_count, drift_metrics, quality_metrics_if_available

Alert

alert_id, type, severity, observed_value, threshold, status, created_at, acknowledged_by

ExperimentRun

run_id, method, model_version, dataset_version, code_commit, seed, metrics, runtime, artifact_uri

ModelCandidate

candidate_id, source_run_id, artifact_hash, validation_status, decision, approver, status

AuditEvent

event_id, actor, action, target, timestamp, outcome, correlation_id

4.8 Model evaluation design

Classical ML: use a transparent baseline such as Isolation Forest or gradient boosting depending on whether the target is anomaly detection or supervised degradation risk.

DL: use an LSTM or autoencoder only if enough sequential observations are available; otherwise document the data limitation and use a small controlled demonstration.

QML: compare a small quantum-kernel or variational classifier on a reduced feature subset and identical split where feasible. Log simulator and package versions, seeds, runtime, and metrics.

Compare methods using appropriate measures (e.g., precision/recall/F1 for labeled drift cases, false-alert rate, detection delay, runtime, and memory). Do not claim QML advantage without evidence.

Evaluate the recovery process with validation gates, promotion-blocking tests, and rollback tests.

5. Traceability to SRS

SRS requirement

Design element

Verification

FR-01, FR-02

API routes; collector; metrics exporter

TC-01, TC-02

FR-03, FR-04, FR-08

Drift analyzer; quality metrics logic; alert manager

TC-03, TC-04, TC-06

FR-05, FR-06, FR-07

ML/DL workers; isolated QML benchmark

TC-05

FR-09, FR-10

Recovery policy; validator; approval route

TC-07, TC-11

FR-11, SR-05

Audit logger and persistence

TC-12, SEC-05

FR-12

Registry adapter and rollback policy

TC-08

FR-13, FR-14

Dashboard/API; authentication/RBAC

Dashboard acceptance test; TC-11

NFR-01, NFR-02, NFR-07, NFR-09

Async workers, bounded jobs, Prometheus metrics

TC-09, TC-10

NFR-04–NFR-06

MLflow metadata, pinned dependencies, Docker/CI

TC-05, TC-15

SR-01–SR-04, SR-06

Auth middleware, validation, secret management, network policy

SEC-01–SEC-04, SEC-06

6. Deployment and DevOps Design

Developer opens a pull request to the GitHub repository.

GitHub Actions runs formatting/lint checks, unit tests, dependency checks, and API contract tests.

CI builds the Docker image and runs a smoke test.

On merge, a versioned image/artifact is created; deployment to the demo environment requires the configured approval gate.

Prometheus scrapes metrics; Grafana displays service and model-health panels.

MLflow tracks model experiments and candidate versions; a rollback procedure remains documented and tested.

7. Limitations and Future Enhancements

Initial project demonstrates controlled tabular drift rather than all production failure modes.

Ground-truth delay limits immediate confirmation of predictive-quality loss.

QML is a benchmark and may be slower or less accurate than classical baselines.

Future work may add richer lineage, Kubernetes deployment, notification integrations, canary evaluation, and real-world longitudinal datasets.