Test Case Catalogue and Traceability Supplement

Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery

Deliverable 4 — Test Case Update

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

Test Case Catalogue - Self-Monitoring MLOps System

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

1. Purpose and usage

This catalogue expands the test-case section of the Test Plan into execution-ready cases. The Test Plan remains the governing document; this supplement provides detailed preconditions, steps, expected results, and traceability. The cases are planned tests, not claims that the implementation has already passed.

2. Test execution conventions

Record actual result as Pass, Fail, Blocked, or Not Run.

Capture run date, tester, commit SHA, environment, logs/screenshots, and defect ID for each executed case.

Use synthetic data and test identities only.

Run expensive DL/QML tests separately from API performance tests.

Do not mark a case passed until evidence is recorded.

TC-01 — Health endpoint

Field

Specification

Requirement trace

FR-01

Test level/type

Integration

Preconditions

Service is running.

Test steps

1. Send GET /health. 2. Inspect status and response schema.

Expected result

HTTP 200; status indicates healthy; version and timestamp fields are present.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-02 — Prediction metrics collection

Field

Specification

Requirement trace

FR-02, NFR-07

Test level/type

Integration

Preconditions

Metrics exporter is enabled.

Test steps

1. Record initial counters. 2. Submit 20 successful and 2 failed synthetic events. 3. Query summary/metrics.

Expected result

Processed event count increases by 22; error count reflects 2 failures; latency observations are present.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-03 — Stable reference data

Field

Specification

Requirement trace

FR-03

Test level/type

System

Preconditions

Reference window and stable fixture are configured.

Test steps

1. Submit a sample from the same distribution. 2. Run window comparison. 3. Inspect status.

Expected result

No drift alert is emitted for the defined stable fixture under configured thresholds; summary is stored.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-04 — Shifted input data

Field

Specification

Requirement trace

FR-03, FR-08

Test level/type

System

Preconditions

Drift threshold and reference window are configured.

Test steps

1. Submit a controlled feature-shifted dataset. 2. Run analyzer. 3. Inspect alert.

Expected result

Configured drift condition is detected; alert includes metric, observed value, threshold, and timestamp.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-05 — ML/DL/QML experiment tracking

Field

Specification

Requirement trace

FR-05–FR-07, NFR-04

Test level/type

Integration

Preconditions

Experiment tools and small dataset are available.

Test steps

1. Run ML baseline. 2. Run DL experiment. 3. Run QML simulator benchmark. 4. Inspect metadata.

Expected result

Each run has method, data/version, config/seed where applicable, package version, metrics, runtime; QML run cannot promote a model.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-06 — No ground-truth labels

Field

Specification

Requirement trace

FR-04

Test level/type

Unit/Integration

Preconditions

Prediction events exist without labels.

Test steps

1. Query model-health summary before labels arrive. 2. Inspect accuracy field.

Expected result

Accuracy/performance is marked unavailable; system does not substitute drift score as accuracy.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-07 — Promotion without validation

Field

Specification

Requirement trace

FR-10, NFR-10

Test level/type

Negative/System

Preconditions

Candidate exists; validation status is failed or pending.

Test steps

1. Call candidate decision/promotion endpoint as authorized user. 2. Inspect active version and audit log.

Expected result

Promotion is rejected; active version is unchanged; failed attempt or decision is auditable.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-08 — Rollback on post-promotion failure

Field

Specification

Requirement trace

FR-12

Test level/type

System

Preconditions

Stable version A and candidate version B exist in test registry.

Test steps

1. Promote validated/approved B. 2. Simulate failed post-promotion health check. 3. Trigger rollback policy.

Expected result

Active version returns to A; rollback outcome and reason are logged.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-09 — API latency and event throughput

Field

Specification

Requirement trace

NFR-01, NFR-09

Test level/type

Performance

Preconditions

Performance environment is documented; QML worker idle.

Test steps

1. Run 10 concurrent clients against summary/health endpoints. 2. Submit 1,000 synthetic events. 3. collect report.

Expected result

p95 summary/health latency is under 500 ms in the agreed local configuration; all 1,000 events are accounted for.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-10 — Monitoring worker crash

Field

Specification

Requirement trace

NFR-02

Test level/type

Fault injection

Preconditions

API and worker run as separate processes/services.

Test steps

1. Stop or crash monitoring worker. 2. Call health endpoint. 3. Inspect logs/metrics.

Expected result

API remains responsive; worker failure is visible; no false success is reported for unfinished analysis.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-11 — Authorization for candidate decision

Field

Specification

Requirement trace

FR-14, SR-01, SR-02

Test level/type

Security/Integration

Preconditions

Read-only and ML Engineer test identities exist.

Test steps

1. Call decision endpoint without credentials. 2. Call as read-only user. 3. Call as authorized ML Engineer.

Expected result

Unauthenticated call is denied; read-only action is forbidden; authorized user can decide only when candidate passes required validation.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-12 — Audit record completeness

Field

Specification

Requirement trace

FR-11, SR-05

Test level/type

Integration

Preconditions

Audit logging is enabled.

Test steps

1. Reject a candidate. 2. Query audit events. 3. Inspect required fields.

Expected result

Event includes actor/service identity, timestamp, action, target, outcome, and correlation ID.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-13 — Invalid and oversized payload

Field

Specification

Requirement trace

SR-04

Test level/type

Negative/Security

Preconditions

API is running.

Test steps

1. Submit wrong field types and invalid ranges. 2. Submit oversized body. 3. Check service health.

Expected result

Invalid input is rejected with safe 4xx response; service remains available; no sensitive stack trace is returned.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-14 — Secret leakage

Field

Specification

Requirement trace

SR-03, NFR-11

Test level/type

Security

Preconditions

Synthetic secret marker is available for test only.

Test steps

1. Search repository for marker. 2. Trigger expected error path. 3. Search application logs.

Expected result

Marker is absent from committed source and logs; credentials are redacted.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-15 — Container build and CI smoke test

Field

Specification

Requirement trace

NFR-05, NFR-06

Test level/type

Build/Integration

Preconditions

Dockerfile and CI workflow exist.

Test steps

1. Run CI checks. 2. Build image. 3. Start container. 4. Call health endpoint.

Expected result

Lint/tests pass; image builds; service starts and health check succeeds.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-16 — Reproducibility of monitoring experiment

Field

Specification

Requirement trace

NFR-04

Test level/type

Experiment

Preconditions

Dataset version and random seed are recorded.

Test steps

1. Run same ML experiment twice with same configuration. 2. Compare metrics and metadata.

Expected result

Metadata matches; deterministic metrics match within the documented tolerance.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-17 — Metrics/admin surface restriction

Field

Specification

Requirement trace

SR-06

Test level/type

Security/Configuration

Preconditions

Trusted and untrusted test contexts are configured.

Test steps

1. Request metrics/admin endpoint from both contexts. 2. Inspect access logs.

Expected result

Trusted/authenticated access works as configured; untrusted access is denied.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

TC-18 — Candidate validation regression gate

Field

Specification

Requirement trace

FR-10, NFR-10

Test level/type

System/Negative

Preconditions

Stable model metrics and candidate evaluation fixtures exist.

Test steps

1. Submit candidate below minimum quality threshold. 2. Attempt approval/promotion.

Expected result

Candidate remains blocked despite approval attempt; stable version remains active; validation failures are visible.

Execution status

Not Run

Actual result / evidence

[Complete during execution: attach log, screenshot, report, or defect ID.]

3. Traceability matrix

SRS requirement

Mapped test cases

FR-01

TC-01

FR-02, NFR-07

TC-02

FR-03, FR-08

TC-03, TC-04

FR-04

TC-06

FR-05, FR-06, FR-07

TC-05

FR-09, FR-10, NFR-10

TC-07, TC-18

FR-11, SR-05

TC-12

FR-12

TC-08

FR-13

Dashboard acceptance walkthrough (add evidence in Test Plan)

FR-14, SR-01, SR-02

TC-11

NFR-01, NFR-09

TC-09

NFR-02

TC-10

NFR-04

TC-05, TC-16

NFR-05, NFR-06

TC-15

NFR-11, SR-03

TC-14

SR-04

TC-13

SR-06

TC-17

4. Execution record template

Test ID

Run date

Commit SHA

Tester

Status

Evidence / defect ID

[TC-xx]

[YYYY-MM-DD]

[commit]

[name]

[Pass/Fail/Blocked/Not Run]

[link/path/ID]

[TC-xx]

[YYYY-MM-DD]

[commit]

[name]

[Pass/Fail/Blocked/Not Run]

[link/path/ID]

[TC-xx]

[YYYY-MM-DD]

[commit]

[name]

[Pass/Fail/Blocked/Not Run]

[link/path/ID]

5. Submission note

The assignment brief requires at least 7–10 test cases covering functional and non-functional requirements. This catalogue includes 18 planned cases, including explicit security validation. These are test specifications; execution status must be updated after the implementation is run.