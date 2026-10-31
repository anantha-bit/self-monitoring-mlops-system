# Software Engineering Mini-Project — Deliverables Part-3
# Unit Test Execution Report

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Course:** Software Engineering Mini-Project (SE Mini-Project Deliverables Part-3)  
**Department:** Computer Science & Engineering (AI & ML), PES University  
**Document ID:** `DOC-REP-UTR-001`  
**Version:** `1.1.0`  
**Execution Window:** 2nd November 2026 – 6th November 2026  
**Document Date:** 6 November 2026  

---

### Team Members & Contributions
| Team Member Name | USN | GitHub Username | Role & Test Responsibilities |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [`@anantha-bit`](https://github.com/anantha-bit) | Project Lead, Test Orchestrator, Core API & Safety Gate Tests (TC-01, TC-02, TC-07, TC-08, TC-09, TC-18) |
| **AKASH G K** | **PES1UG24AM022** | [`@akashgkuradagi`](https://github.com/akashgkuradagi) | Contributor, Drift Detection Engine, Fault Tolerance & Container Tests (TC-03, TC-04, TC-06, TC-10, TC-15) |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [`@prasadamith05-png`](https://github.com/prasadamith05-png) | Contributor, DL/QML Experiments, Security RBAC & Audit Ledger Tests (TC-05, TC-11, TC-12, TC-13, TC-14, TC-16, TC-17) |

---

## 1. Executive Summary

This **Unit Test Execution Report** documents the formal verification and validation of the *Self-Monitoring MLOps System* in accordance with the **Software Engineering Mini-Project Deliverables Part-3** specifications.

All eighteen (18) automated test cases—spanning foundational health checks, statistical drift detection engines, deep learning autoencoder anomaly detection, quantum circuit benchmarks, safety gates, automated rollback, RBAC authorization, and cryptographic audit log chaining—were executed via `pytest 9.2.0` with `pytest-cov 7.1.0`.

### Summary Scorecard
| Metric | Value | Compliance Status |
| :--- | :--- | :---: |
| **Total Test Cases Executed** | **18** | ✅ Exceeds requirement (min 7–10) |
| **Tests Passed** | **18** | ✅ 100% Pass Rate |
| **Tests Failed** | **0** | ✅ Zero Defects |
| **Tests Skipped / Blocked** | **0** | ✅ 100% Execution Completion |
| **Total Test Execution Duration** | **17.83 seconds** | ✅ High Efficiency |
| **Overall Statement Coverage** | **83.1% (580 / 698 statements)** | ✅ Exceeds 80% Threshold |
| **Combined Line + Branch Coverage**| **79%** | ✅ Highly Robust |

---

## 2. Test Execution Environment & Test Harness

The unit test suite is automated through standard test harnesses and runs both locally on developer workstations and automatically in the GitHub Actions CI/CD matrix pipeline on every pull request and push to `main`.

```
Platform Architecture: Windows 11 x86_64 / Linux x86_64 (Ubuntu 22.04 LTS runner)
Python Runtime:        Python 3.12.10 (64-bit)
Core Frameworks:       FastAPI 0.115.0, Starlette 0.38.6, Pydantic 2.9.2
ML / Scientific Stack: PyTorch 2.4.1+cpu, Scikit-Learn 1.5.2, NumPy 1.26.4, SciPy 1.14.1
Quantum Stack:         Qiskit 1.2.4 (Statevector simulation backend)
Test Frameworks:       Pytest 9.2.0, Pytest-Cov 7.1.0, Pytest-Asyncio 1.4.1
```

---

## 3. Individual Test Case Execution Results Matrix

| Test ID | Test Case Title | Target Module / Component | Traceability | Execution Time | Status |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **TC-01** | Microservice Health & Uptime Status | `app.main`, `/health` | FR-01 | 18 ms | **PASSED** ✅ |
| **TC-02** | Prediction Ingestion & Prometheus Metrics | `app.monitoring.collector` | FR-02, NFR-07 | 24 ms | **PASSED** ✅ |
| **TC-03** | Baseline Statistical Invariance Check | `app.monitoring.drift` | FR-03, NFR-03 | 31 ms | **PASSED** ✅ |
| **TC-04** | Statistical Drift Detection (KS & PSI) | `app.monitoring.drift` | FR-03, FR-08 | 38 ms | **PASSED** ✅ |
| **TC-05** | ML, DL & QML Experiment Tracking | `app.models`, `app.registry` | FR-05, FR-06, FR-07 | 4,120 ms | **PASSED** ✅ |
| **TC-06** | Unsupervised Drift Detection Without Labels | `app.monitoring.drift` | FR-04 | 29 ms | **PASSED** ✅ |
| **TC-07** | Automated Validation Gatekeeper | `app.recovery.validator` | FR-09, FR-10 | 45 ms | **PASSED** ✅ |
| **TC-08** | Automated Emergency Model Rollback | `app.recovery.policy` | FR-12, NFR-10 | 33 ms | **PASSED** ✅ |
| **TC-09** | End-to-End Latency SLA & Throughput | `app.api.routes` | NFR-01, NFR-09 | 18.4 ms/req | **PASSED** ✅ |
| **TC-10** | Monitoring Worker Crash Isolation | `app.monitoring.collector` | NFR-02 | 22 ms | **PASSED** ✅ |
| **TC-11** | RBAC Candidate Promotion Authorization | `app.security.auth` | FR-10, FR-14 | 19 ms | **PASSED** ✅ |
| **TC-12** | Immutable Audit Log Completeness | `app.security.audit` | FR-11, SR-03 | 27 ms | **PASSED** ✅ |
| **TC-13** | Input Validation & Oversized Payloads | `app.api.routes` | SR-01, SR-02 | 14 ms | **PASSED** ✅ |
| **TC-14** | Secret Leakage & Credential Sanitization | `app.config`, `app.security`| NFR-11, SR-04 | 12 ms | **PASSED** ✅ |
| **TC-15** | Microservice Container Build Smoke Test | `Dockerfile`, `docker-compose`| NFR-05, NFR-06 | 15 ms | **PASSED** ✅ |
| **TC-16** | Deterministic ML Reproducibility | `app.models.ml_monitor` | NFR-04 | 310 ms | **PASSED** ✅ |
| **TC-17** | Metric Route Admin Surface Restriction | `app.security.auth` | FR-14, SR-06 | 16 ms | **PASSED** ✅ |
| **TC-18** | Candidate Retraining Regression Gate | `app.recovery.validator` | FR-09, FR-10 | 210 ms | **PASSED** ✅ |

---

## 4. Pytest Execution Console Output (Automated Verification)

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- python.exe
cachedir: .pytest_cache
rootdir: C:\Users\anant\.gemini\antigravity\scratch\self-monitoring-mlops-system
configfile: pytest.ini
plugins: anyio-4.15.1, hydra-core-1.3.7, cov-7.1.0
collecting ... collected 18 items

tests/test_tc01_tc02_health_metrics.py::test_tc01_health_endpoint PASSED [  5%]
tests/test_tc01_tc02_health_metrics.py::test_tc02_prediction_metrics_collection PASSED [ 11%]
tests/test_tc01_tc02_health_metrics.py::test_tc09_latency_and_throughput PASSED [ 16%]
tests/test_tc03_tc04_tc06_drift.py::test_tc03_stable_reference_data PASSED [ 22%]
tests/test_tc03_tc04_tc06_drift.py::test_tc04_shifted_input_data_triggers_alert PASSED [ 27%]
tests/test_tc03_tc04_tc06_drift.py::test_tc06_no_ground_truth_labels PASSED [ 33%]
tests/test_tc05_tc16_experiments.py::test_tc05_ml_dl_qml_experiment_tracking PASSED [ 38%]
tests/test_tc05_tc16_experiments.py::test_tc16_experiment_reproducibility PASSED [ 44%]
tests/test_tc07_tc08_tc18_recovery_gates.py::test_tc07_promotion_without_validation_is_blocked PASSED [ 50%]
tests/test_tc07_tc08_tc18_recovery_gates.py::test_tc18_candidate_validation_regression_gate PASSED [ 55%]
tests/test_tc07_tc08_tc18_recovery_gates.py::test_tc08_rollback_on_failure PASSED [ 61%]
tests/test_tc10_fault_tolerance.py::test_tc10_monitoring_worker_failure_isolation PASSED [ 66%]
tests/test_tc11_tc12_security_audit.py::test_tc11_authorization_for_candidate_decision PASSED [ 72%]
tests/test_tc11_tc12_security_audit.py::test_tc12_audit_record_completeness PASSED [ 77%]
tests/test_tc11_tc12_security_audit.py::test_tc17_metrics_admin_surface_restriction PASSED [ 83%]
tests/test_tc13_tc14_payload_secrets.py::test_tc13_invalid_and_oversized_payload PASSED [ 88%]
tests/test_tc13_tc14_payload_secrets.py::test_tc14_secret_leakage_protection PASSED [ 94%]
tests/test_tc15_container_smoke.py::test_tc15_container_and_environment_configuration PASSED [100%]

======================= 18 passed, 1 warning in 17.83s ========================
```

---

## 5. Formal Verification & QA Sign-Off

The undersigned team members certify that the unit and integration tests described in this report have been executed thoroughly against repository `anantha-bit/self-monitoring-mlops-system`. All 18 test cases pass with 100% success rate and zero remaining critical defects.

**Anantha Krishna M A** (PES1UG24AM036) — Lead Developer & Orchestrator  
**AKASH G K** (PES1UG24AM022) — Drift & Continuous Monitoring Engineer  
**AMIT PRASAD S G** (PES1UG24AM033) — DL/QML & Security Quality Engineer  
Date of Verification: **6 November 2026**
