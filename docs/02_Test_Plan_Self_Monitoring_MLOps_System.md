Software Test Plan

Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery

Deliverable 2 — Test Plan (Deliverables Part-3 Updated)

Version 1.1.0

Prepared on: 10 October 2026 | Updated on: 6 November 2026

Team Members:

Anantha Krishna M A — PES1UG24AM036

AKASH G K — PES1UG24AM022

AMIT PRASAD S G — PES1UG24AM033

Department: CSE (AI & ML), PES University

Document Control

Field

Value

Document title

Test Plan - Self-Monitoring MLOps System

Version

Version 1.1.0

Status

Approved & Executed (Deliverables Part-3)

Date

6 November 2026

Owner

Anantha Krishna M A, AKASH G K, AMIT PRASAD S G

Review note

Replace bracketed identity fields and confirm institution-specific template requirements before submission.

1. Introduction

1.1 Purpose

This test plan defines the strategy, scope, resources, schedule approach, entry/exit criteria, and test activities for the Self-Monitoring MLOps System. It covers functional behavior, model-monitoring experiments, DevOps workflows, quality attributes, security validation, and traceability to the SRS.

1.2 Scope

In scope: REST API, metric collection, drift detection, ML/DL experiments, isolated QML benchmark logging, alerts, candidate validation, authorization, audit logs, rollback, Docker build, CI workflow, and dashboard data.

Out of scope for Part-1: production-scale cloud deployment, real quantum hardware, guaranteed accuracy improvement under arbitrary drift, and unrestricted autonomous production retraining.

1.3 References

SRS — Self-Monitoring MLOps System, Version 1.0.

Software Engineering Mini-Project Deliverables Part-1 brief supplied by the student.

Repository test configuration, API schema, and pinned dependency files (to be created/maintained during implementation).

1.4 Test objectives

Verify that monitoring data and drift statuses are produced correctly for controlled inputs.

Verify the system distinguishes drift warnings from measured predictive-quality degradation.

Verify model promotion is gated by validation and authorized approval.

Verify ML, DL, and QML experiments produce traceable, comparable metadata.

Verify performance, reliability, packaging, observability, privacy, and security requirements.

2. Test Items and Test Approach

2.1 Test items

Item

Test focus

FastAPI endpoints

Schemas, status codes, validation, authentication, authorization.

Monitoring collector and metrics

Event counts, latency, error status, missing/late labels.

Drift analyzer

Stable vs shifted distributions, threshold behavior, reproducibility.

ML/DL experiment workers

Training/evaluation split, metrics, saved configuration, repeatability.

QML benchmark

Simulator-only execution, separate result tracking, runtime and seed metadata.

Recovery orchestrator and registry

Candidate eligibility, validation gates, approval, promotion, rollback.

Dashboard and audit log

Required fields, correct status, access restriction, action traceability.

CI/CD and Docker

Lint, tests, build, smoke test, configuration and secret handling.

2.2 Test levels

Unit testing: individual metric, schema, threshold, policy, and utility functions.

Integration testing: API + collector + analyzer + metrics store/model registry.

System testing: end-to-end drift alert and candidate evaluation workflow.

Acceptance testing: faculty/user walkthrough against requirements and dashboard needs.

Security testing: authentication, authorization, input validation, secret leakage, and audit logging.

2.3 Test types and techniques

Black-box tests for endpoint contracts and user-visible behavior.

White-box tests for recovery policy branches and exception handling.

Boundary-value tests for thresholds, empty windows, missing labels, invalid payloads, and resource limits.

Negative tests for unauthorized actions and invalid model candidates.

Reproducibility tests using fixed seeds and pinned dataset/configuration versions.

Load/fault-injection tests for event throughput, worker failure, and API latency.

3. Test Environment

3.1 Hardware and software

Category

Planned environment

Hardware

Developer laptop/desktop; CPU is sufficient for the initial tabular ML/DL demo; GPU optional.

OS/runtime

Linux, macOS, or Windows with Docker support; Python 3.x pinned in project setup.

Application

FastAPI, scikit-learn, PyTorch, MLflow, optional Evidently AI.

QML

PennyLane or Qiskit simulator; pinned library versions; no quantum hardware requirement.

DevOps/observability

GitHub Actions, Docker/Compose, Prometheus, Grafana.

Test tools

pytest, coverage tool, lint/format checks, HTTP test client, load tool selected by team.

3.2 Test data

Use a public or synthetic tabular classification dataset with documented license/source.

Create a stable reference window and controlled shifted windows (feature distribution shift and, where possible, label/relationship shift).

Keep train/validation/test partitions separate to avoid data leakage.

Use synthetic test credentials and synthetic sensitive values for security tests.

Store dataset version/hash and random seed for reproducibility.

3.3 Environment controls

Pin dependencies and use the same container image for repeatable integration tests.

Keep QML jobs separate from API latency tests because simulator execution can be expensive.

Do not use real production credentials or sensitive data.

Capture commit SHA, container tag, run ID, and environment details with test reports.

4. Test Strategy and Test Cases

4.1 Entry criteria

SRS and API contracts reviewed and versioned.

Test environment builds successfully from documented instructions.

Baseline model, reference dataset, and drift test fixtures are available.

Authentication roles and candidate promotion policy are configured.

Test data does not contain unapproved sensitive information.

4.2 Exit criteria

All critical functional and security tests pass.

At least 90% of planned test cases pass; all failures are triaged and documented.

No open critical/high security defect remains for the submitted prototype.

Traceability exists from each test to one or more SRS requirements.

Test report records environment, commit, results, defects, and known limitations.

4.3 Test case summary

Test ID

Scenario

Requirement trace

Expected result

TC-01

Health endpoint

FR-01

Healthy response returns 200 and version/status fields.

TC-02

Prediction metrics collection

FR-02, NFR-07

Counts, latency, and error metrics reflect submitted events.

TC-03

Stable reference window

FR-03

No drift alert when configured stable fixture remains within rule thresholds.

TC-04

Shifted input window

FR-03, FR-08

Configured drift rule raises a drift alert with metric/value/time.

TC-05

ML/DL/QML experiment metadata

FR-05–FR-07, NFR-04

Each experiment logs its model/method, versions, seed/configuration, metrics, and runtime; QML remains non-promoting.

TC-06

Missing ground-truth labels

FR-04

Accuracy is shown as unavailable; no fabricated metric is emitted.

TC-07

Promotion without validation

FR-10, NFR-10

Promotion is rejected and audit event is recorded.

TC-08

Rollback after failed health check

FR-12

Stable model version is restored and rollback is logged.

TC-09

API performance/load

NFR-01, NFR-09

At target load, p95 is under 500 ms for summary/health endpoints and 1,000 events are accounted for.

TC-10

Worker fault isolation

NFR-02

Worker failure is logged; API remains responsive.

TC-11

Approval authorization

FR-14, SR-01, SR-02

Unauthorized approval denied; authorized user can approve/reject.

TC-12

Audit completeness

FR-11, SR-05

Lifecycle event contains actor, timestamp, target, outcome, and correlation ID.

TC-13

Invalid/oversized request

SR-04

Request is rejected safely without crash or sensitive stack trace.

TC-14

Secret leakage check

SR-03, NFR-11

Seeded secret is absent from source-controlled files and logs.

TC-15

Container/CI smoke test

NFR-05, NFR-06

CI tests pass, image builds, and container health check succeeds.


TC-16

Experiment reproducibility check

NFR-04

Identical model metrics and loss curves obtained across independent runs with identical random seed.

TC-17

Metrics/admin network restriction

SR-06

Access to internal metrics and administrative endpoints without proper authorization is denied with HTTP 403.

TC-18

Candidate validation regression gate

FR-10, NFR-10

Candidate model with substandard accuracy or excessive latency is automatically blocked from promotion.

TC-19

Drift sensitivity benchmark suite

FR-03, FR-04, NFR-03

Stepwise shift sweep (0.0 to 3.0 std) demonstrates monotonic PSI scaling from baseline (<0.25) to significant drift (>=0.25).

TC-20

DL autoencoder latent attribution

FR-06, FR-07

Per-feature reconstruction error correctly pinpoints the exact anomalous feature responsible for drift.

TC-21

Continuous health tripwire

FR-01, FR-12, NFR-02

Continuous telemetry monitor triggers automated fallback rollback after consecutive failure threshold is breached.

TC-22

Audit chain cryptographic verification

FR-11, SR-03, SR-05

SHA-256 hash chaining validates intact audit ledgers and raises tamper alarm upon modified historical entries.

TC-23

End-to-end recovery pipeline

FR-08, FR-09, FR-10, FR-12

Full autonomous loop from prediction, drift alert, gate validation, to live promotion completes without regression.

TC-24

Prometheus live metrics export

FR-02, NFR-01, NFR-07

Metrics endpoint (/api/v1/metrics/prometheus) emits valid exposition text scrapeable by monitoring servers.

TC-25

Recovery policy boundary and routes

FR-13, NFR-08, NFR-10

Dynamic recovery policies and dashboard status routes return consistent state without unhandled exceptions.

4.4 Defect severity and priority

Severity

Definition

Handling

Critical

Unauthorized model promotion, data/secret exposure, data corruption, or core system unusable.

Stop release; fix and retest.

High

Core monitoring, validation gate, or rollback fails with no safe workaround.

Fix before submission/release unless formally waived.

Medium

Feature partially incorrect or non-critical metric/UI issue.

Prioritize and document; retest after fix.

Low

Cosmetic issue or minor usability concern.

Fix when practical; record known issue.

5. Test Deliverables and Responsibilities

5.1 Security validation

Security validation is performed in an isolated test environment using synthetic users and credentials. The tester verifies authentication on management endpoints, role-based denial, input validation, secret handling, audit completeness, and restriction of metrics/admin surfaces. These tests are mapped to SRS SR-01 through SR-06 and NFR-11/NFR-12.

Security test

Procedure

Pass criteria

Trace

SEC-01 Authentication bypass

Call approval/promotion endpoint without credentials.

Request denied (401 or equivalent); no state change.

SR-01, FR-14

SEC-02 Role escalation

Authenticate as read-only role and attempt approval/rollback.

Request denied (403 or equivalent); state unchanged; event logged.

SR-02

SEC-03 Secret leakage

Place a synthetic secret in test config and trigger normal/error logs; scan repository.

Secret absent from committed files and output logs.

SR-03, NFR-11

SEC-04 Malformed payload

Send invalid types, unexpected fields, oversized body, and out-of-range threshold.

Request rejected with safe error; process remains available.

SR-04

SEC-05 Audit tampering/completeness

Perform candidate rejection/promotion attempt and inspect audit record.

Required fields present; ordinary application user cannot edit/delete records.

SR-05

SEC-06 Metrics exposure

Attempt to access metrics/admin interface from an untrusted test context.

Access restricted by configured network/auth policy.

SR-06

5.2 Test deliverables (Deliverables Part-3 Formal Reports)

Automated unit and integration test suite (25 test cases across tests/ directory).

Unit Test Report (docs/reports/UNIT_TEST_REPORT.md and docs/UNIT_TEST_REPORT.md).

System Validation Report (docs/reports/SYSTEM_VALIDATION_REPORT.md and docs/SYSTEM_VALIDATION_REPORT.md).

Code Coverage Report (docs/reports/CODE_COVERAGE_REPORT.md and docs/CODE_COVERAGE_REPORT.md) with 86% overall coverage.

Branch Coverage Report (docs/reports/BRANCH_COVERAGE_REPORT.md and docs/BRANCH_COVERAGE_REPORT.md) with 69.3% branch coverage.

Interactive HTML Coverage Explorer (docs/reports/htmlcov/index.html).

Traceability matrix linking all 14 FRs, 12 NFRs, and 6 SRs to test cases TC-01 through TC-25.

5.3 Roles and responsibilities

Role

Responsibility

Developer

Implement testable components, fix defects, maintain unit tests and CI configuration.

Tester / student team member

Execute planned tests, record evidence, triage failures, maintain traceability.

ML Engineer role

Review drift thresholds, model-quality metrics, and candidate evaluation.

Reviewer / faculty evaluator

Review requirements, test evidence, limitations, and acceptance criteria.

6. Traceability Matrix

SRS requirement

Test case(s)

Test level

FR-01

TC-01

Integration/System

FR-02, NFR-07

TC-02

Unit/Integration

FR-03, FR-08

TC-03, TC-04

System

FR-04

TC-06

Unit/Integration

FR-05–FR-07, NFR-04

TC-05

Integration/Experiment

FR-09–FR-10, NFR-10

TC-07 plus candidate-eligibility branch tests

System/Negative

FR-11, SR-05

TC-12, SEC-05

Integration/Security

FR-12

TC-08

System/Recovery

FR-13

Dashboard walkthrough / seeded-view test

Acceptance

FR-14, SR-01, SR-02

TC-11, SEC-01, SEC-02

Security/Integration

NFR-01, NFR-09

TC-09

Performance/Load

NFR-02

TC-10

Fault injection

NFR-05, NFR-06

TC-15

Build/Smoke

NFR-11, SR-03

TC-14, SEC-03

Security

SR-04

TC-13, SEC-04

Security/Negative

SR-06

SEC-06

Security/Configuration

7. Risks and Mitigations

Risk

Impact

Mitigation

No ground-truth labels available promptly

Cannot verify actual accuracy degradation.

Display accuracy as unavailable; use drift as a warning only.

QML simulation is slow

Test suite and demo become slow.

Use small feature sets/subsamples and run QML benchmark asynchronously.

Synthetic drift does not represent all real-world drift

Limited external validity.

Document controlled scenarios and avoid broad claims.

Automatic retraining worsens quality

Regression or unsafe model promotion.

Use validation gates, human approval, stable version and rollback.

Environment differences

Non-reproducible results.

Pin dependencies, containerize and record versions/seeds.