Software Requirements Specification (SRS)

Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery

Deliverable 1 — SRS

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

SRS - Self-Monitoring MLOps System

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

This Software Requirements Specification (SRS) defines the functional, non-functional, interface, and security requirements for the Self-Monitoring MLOps System. The system observes a deployed machine-learning model, detects potential input/prediction drift and service degradation, raises actionable alerts, and supports controlled evaluation of a replacement model. It is intended for student developers, testers, reviewers, and project stakeholders.

1.2 Scope

The system will provide a demonstrable monitoring workflow around a tabular classification model. It will collect prediction and service metrics; calculate drift and health indicators; use classical ML and a DL sequence/anomaly model as complementary experiments; and include an isolated QML benchmark for comparison. The QML component is experimental and will not control production recovery decisions in the initial release. Retraining and promotion will be gated by validation rules and human approval.

1.3 Intended audience

Project team and faculty evaluator.

Developers implementing the API, monitoring pipeline, model experiments, and dashboard.

Testers validating functional behavior, quality attributes, and security controls.

Users acting as ML engineers or system administrators.

1.4 Definitions, acronyms, and abbreviations

Term

Definition

MLOps

Practices and tooling for managing ML models across development, deployment, monitoring, and maintenance.

Drift

A change in input or prediction distributions relative to a reference period; it does not by itself prove accuracy loss.

Ground truth

Verified target labels used to evaluate actual predictive performance.

ML / DL / QML

Machine Learning / Deep Learning / Quantum Machine Learning.

CI/CD

Continuous Integration / Continuous Delivery or Deployment.

Model registry

Versioned store of model artifacts and associated metadata.

SLO

Service-level objective, such as an agreed latency or availability target.

1.5 References

IEEE 29148-style SRS organization (adapted for a student mini-project; institution-specific template takes precedence).

Project brief: Software Engineering Mini-Project Deliverables Part-1, supplied by the student.

Tool documentation to be consulted during implementation: FastAPI, scikit-learn, PyTorch, PennyLane/Qiskit, MLflow, Docker, GitHub Actions, Prometheus, Grafana, and Evidently AI.

1.6 Overview

Section 2 describes the product context. Section 3 lists external interfaces. Section 4 defines functional and non-functional requirements. Section 5 defines security objectives and requirements. Section 6 records assumptions and constraints. Section 7 provides a UML-style use-case view.

2. Overall Description

2.1 Product perspective

The system is a monitoring and lifecycle-control layer around an existing prediction service. It does not replace the underlying application or guarantee that detected drift causes accuracy degradation. It uses metrics and model outputs to decide when further investigation or controlled validation is appropriate.

2.2 Product functions

Register a baseline model version and reference data summary.

Collect prediction requests, latency, error counts, and input/prediction summaries.

Calculate drift indicators and model-health metrics.

Run ML and DL monitoring experiments and log QML benchmark results separately.

Display current health, trends, alerts, and audit events.

Create a retraining candidate when policy thresholds are met.

Validate a candidate against defined quality gates and require approval before promotion.

Retain the current stable version and support rollback if post-promotion checks fail.

2.3 User classes and characteristics

User class

Responsibilities

Access level

ML Engineer

Review health, investigate alerts, launch candidate evaluation, approve/reject a candidate.

Read monitoring; initiate and approve controlled model actions.

System Administrator

Configure service settings, manage users/secrets, review audit logs and service health.

Administrative configuration and audit access.

Automated pipeline

Collect metrics, calculate indicators, run tests, package and validate artifacts.

Service identity with least-privilege, non-interactive permissions.

2.4 Operating environment

Python 3.x; FastAPI service; scikit-learn and PyTorch; PennyLane or Qiskit simulator for experimental QML; MLflow for experiment/model tracking; Docker; GitHub Actions; Prometheus and Grafana; optional Evidently AI for drift reports. Initial development and testing may run on a local machine using synthetic or public tabular data.

2.5 Design and implementation constraints

QML runs on a simulator in the initial version; no real quantum hardware is required.

The initial scope uses tabular classification and controlled/synthetic drift so results are reproducible.

No automated production deployment without validation and explicit approval.

The prototype must not expose secrets, raw sensitive input records, or unrestricted model-management endpoints.

Resource-intensive DL/QML experiments must be isolated from the routine monitoring API.

2.6 Assumptions and dependencies

A reference dataset and a trained baseline model are available.

Ground-truth labels may arrive later than predictions; accuracy monitoring is reported only when labels are available.

The project has access to a Docker-capable environment and GitHub repository.

Third-party tool versions and APIs may change; versions will be pinned in project configuration.

3. External Interface Requirements

3.1 User interface

A web dashboard will show service health, model version, recent prediction volume, latency/error metrics, drift status, model-quality metrics when labels are available, active alerts, candidate-model validation results, and audit history. Status must use text labels and not rely on color alone.

3.2 Software interfaces

Interface

Purpose

FastAPI REST API

Accept health, monitoring, alert, model-candidate, and approval requests.

Prediction service

Supplies input summaries, predictions, response times, and error status.

MLflow

Tracks runs, metrics, parameters, and candidate/stable model versions.

Prometheus

Scrapes service metrics and exposes operational telemetry.

Grafana

Visualizes metrics and alert trends.

GitHub Actions

Runs linting, tests, build, and controlled deployment workflow.

Docker

Packages API and worker components reproducibly.

3.3 Communications interfaces

REST communication uses HTTPS in any remotely accessible deployment. Local development may use HTTP only on loopback or an isolated network. Metrics scraping is restricted to the monitoring network. API requests use JSON and include request identifiers for correlation.

4. System Requirements

4.1 Functional requirements

ID

Requirement

Acceptance criterion

FR-01

The system shall expose a health endpoint that returns service status and application version.

GET /health returns HTTP 200 and required fields when service is healthy.

FR-02

The system shall record prediction count, response latency, and request error status for each processed request.

A test batch of N requests produces N corresponding count increments and measurable latency observations.

FR-03

The system shall compare current input/prediction statistics with a configured reference window and report drift status.

Given a known stable dataset, the analyzer returns a status and numeric/statistical summary; a shifted test dataset triggers the configured drift rule.

FR-04

The system shall calculate predictive performance only when valid ground-truth labels are available.

Without labels, the dashboard states that measured accuracy is unavailable rather than inventing a value.

FR-05

The system shall support an ML-based monitoring experiment and store its model version and evaluation metrics.

A run records algorithm, dataset split, metrics, timestamp, and artifact/version identifier.

FR-06

The system shall support a DL-based sequence or anomaly-monitoring experiment that can be evaluated against a baseline.

The run records evaluation metrics and can be reproduced from saved configuration.

FR-07

The system shall run QML only as an isolated benchmark in the initial release and record its results separately from production decisions.

A QML run records simulator/library version, feature encoding, seed, metrics, and runtime; it cannot promote a model.

FR-08

The system shall create an alert when configured drift, error-rate, latency, or quality thresholds are exceeded.

A controlled threshold breach creates an alert with timestamp, severity, metric, and observed value.

FR-09

The system shall initiate candidate retraining/evaluation only when the recovery policy allows it.

A policy-eligible event creates a candidate run; a policy-ineligible event does not start retraining.

FR-10

The system shall block candidate promotion until required validation checks pass and an authorized user approves it.

A candidate lacking either validation success or approval remains unpromoted.

FR-11

The system shall record model promotions, rejections, rollbacks, configuration changes, and security-relevant actions in an audit log.

Each action creates an event with actor/service identity, timestamp, action, target version, and outcome.

FR-12

The system shall support rollback to the last known stable model version when post-promotion checks fail.

A simulated failed post-promotion check restores the recorded stable version and creates an audit event.

FR-13

The system shall provide dashboard views for model health, alerts, model versions, and validation outcomes.

Authorized dashboard request displays the expected fields for seeded test records.

FR-14

The system shall provide an authenticated endpoint to approve or reject a candidate model.

Unauthenticated requests are denied; authorized decisions persist and are auditable.

4.2 Non-functional requirements

ID

Requirement

Verification

NFR-01 Performance

For the agreed local demo configuration, 95th-percentile health/summary API response time shall be under 500 ms at 10 concurrent clients, excluding model training.

Load test report records environment, concurrency, and p95.

NFR-02 Reliability

A monitoring worker failure shall not terminate the prediction API process.

Fault-injection test confirms API remains available and worker failure is logged.

NFR-03 Availability

During a 30-minute controlled demo, the health endpoint shall achieve at least 99% successful responses, excluding planned restarts.

Automated probe report meets threshold.

NFR-04 Reproducibility

Each experiment shall record a dataset/version identifier, random seed where applicable, configuration, software versions, and metrics.

Reviewer can rerun the experiment and locate the matching metadata.

NFR-05 Maintainability

The codebase shall separate API, monitoring, model experiments, recovery policy, and persistence modules.

Code review verifies module boundaries and automated tests cover core modules.

NFR-06 Portability

The application shall build and run using the documented Docker Compose configuration on a Docker-capable host.

Clean-environment build and smoke test pass.

NFR-07 Observability

The service shall expose request count, error count, and latency metrics for Prometheus scraping.

Metrics endpoint exposes all three metric categories.

NFR-08 Usability

A first-time evaluator shall be able to locate health, alerts, and candidate status within three navigation actions.

Short usability walkthrough confirms each target view.

NFR-09 Scalability

Monitoring collection shall support at least 1,000 synthetic prediction events in a test run without losing event counts.

Load test compares submitted and processed counts.

NFR-10 Safety of automation

No candidate shall become stable unless validation gates and authorization both pass.

Negative tests prove promotion is blocked when either condition is absent.

NFR-11 Privacy

Logs shall not store raw sensitive feature values by default; request identifiers and aggregated summaries shall be used where possible.

Log inspection finds no configured sensitive test values.

NFR-12 Security

All model-management endpoints shall require authentication and role-based authorization.

Unauthorized/forbidden test cases are denied and logged.

5. Security Requirements

5.1 Security objectives

SO-01 — Confidentiality: protect credentials, configuration secrets, and any sensitive input data from unauthorized disclosure.

SO-02 — Integrity: prevent unauthorized alteration of model artifacts, monitoring configuration, audit records, and promotion decisions.

SO-03 — Access control: ensure only authenticated and authorized users can approve, reject, promote, or roll back models.

SO-04 — Accountability: record security-relevant and model-lifecycle actions so they can be reviewed.

5.2 Security requirements

ID

Requirement

Verification

SR-01

The system shall require authentication for all model-management and approval endpoints.

Unauthenticated requests receive 401 or equivalent denial.

SR-02

The system shall enforce role-based authorization for approval, configuration, and rollback actions.

A read-only user cannot perform administrative actions; the attempt is logged.

SR-03

The system shall store secrets outside source control and shall not print secret values in logs.

Repository scan and seeded-secret log test show no exposed values.

SR-04

The system shall validate request schema, field types, allowed ranges, and payload size before processing.

Malformed, oversized, or out-of-range inputs are rejected safely.

SR-05

The system shall record model lifecycle actions with actor, timestamp, target, outcome, and correlation ID.

Audit-log test checks all required fields.

SR-06

The system shall restrict metrics and administrative interfaces to trusted networks or authenticated access.

Network/configuration review confirms restriction.

6. Requirements Traceability

Requirement group

Architecture component

Primary test IDs

FR-01–FR-02; NFR-01, NFR-03

API and Metrics Collector

TC-01, TC-02, TC-09

FR-03–FR-08; NFR-07, NFR-09

Drift Analyzer, ML/DL/QML experiment workers, Alert Manager

TC-03, TC-04, TC-05, TC-06, TC-10

FR-09–FR-12; NFR-10

Recovery Orchestrator, Validator, Model Registry

TC-07, TC-08, TC-11

FR-13–FR-14; SR-01–SR-06; NFR-12

Dashboard, Auth/RBAC, Audit Logger

TC-12, TC-13, TC-14

NFR-04–NFR-06, NFR-08, NFR-11

Experiment Tracker, Packaging, UI and Logging

TC-05, TC-09, TC-15

7. UML Use-Case Diagram

The diagram is a simplified use-case view for the initial prototype. The user roles and use cases are also specified in Sections 2.3 and 4.

Figure 1. Use-case overview.

8. Acceptance Criteria and Open Items

The prototype is acceptable when all critical functional requirements and security requirements pass their tests, and no candidate can be promoted without both validation and approval.

Threshold values are configuration parameters for the demo and must be documented in the repository; the default values are not universal production recommendations.

Student identity, institution-specific cover details, dataset selection, and exact performance environment must be completed before submission.