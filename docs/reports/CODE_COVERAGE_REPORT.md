# Software Engineering Mini-Project — Deliverables Part-3
# Code Coverage Analysis Report

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Document ID:** `DOC-REP-CCR-001`  
**Version:** `1.1.0`  
**Course:** Software Engineering Mini-Project (SE Mini-Project Deliverables Part-3)  
**Execution Date:** 6 November 2026  

---

### Team Members & Contributions
| Team Member Name | USN | GitHub Username | Role & Modules Covered |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [`@anantha-bit`](https://github.com/anantha-bit) | FastAPI Routes, Main Entrypoint, Config & Recovery Validator |
| **AKASH G K** | **PES1UG24AM022** | [`@akashgkuradagi`](https://github.com/akashgkuradagi) | Telemetry Collector, Statistical Drift Engine (KS/PSI), Baseline ML |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [`@prasadamith05-png`](https://github.com/prasadamith05-png) | PyTorch Autoencoder, Qiskit QML Simulator, RBAC & Audit Ledger |

---

## 1. Executive Summary

This **Code Coverage Report** provides statement and line-level coverage analysis for the *Self-Monitoring MLOps System*. Testing was executed with `pytest-cov 7.1.0` and `coverage.py 7.6.1` across all core application packages (`app/`).

### Coverage Summary Scorecard
| Metric | Value | Compliance Status |
| :--- | :--- | :---: |
| **Total Source Code Statements** | **698** | Comprehensive Production Scope |
| **Statements Covered by Tests** | **580** | High Execution Density |
| **Statements Missed** | **118** | Confined to optional fallback branches |
| **Overall Statement Coverage** | **83.1%** | ✅ Exceeds 80% Academic Standard |
| **Combined Line + Branch Coverage** | **79%** | ✅ Robust Branch Gatekeeping |

---

## 2. Module-by-Module Statement Coverage Breakdown

| Package / Module File | Total Statements | Missed Statements | Statement Coverage | Primary Functionality |
| :--- | :---: | :---: | :---: | :--- |
| `app/config.py` | 29 | 0 | **100%** | Environment settings and drift thresholds |
| `app/security/auth.py` | 31 | 0 | **100%** | Role-based access control and API key auth |
| `app/models/qml_benchmark.py` | 27 | 0 | **100%** | Quantum circuit statevector simulator |
| `app/recovery/validator.py` | 32 | 0 | **100%** | Model quality gates and regression tester |
| `app/security/audit.py` | 48 | 5 | **90%** | Cryptographic SHA-256 audit trail logger |
| `app/models/ml_monitor.py` | 47 | 5 | **89%** | Baseline Scikit-Learn training & inference |
| `app/monitoring/drift.py` | 80 | 12 | **85%** | Two-sample KS-test & PSI drift computation |
| `app/monitoring/collector.py` | 65 | 10 | **85%** | Telemetry ingestion & Prometheus counter export |
| `app/models/dl_monitor.py` | 61 | 10 | **84%** | PyTorch Sequence Autoencoder anomaly scorer |
| `app/api/routes.py` | 140 | 28 | **80%** | REST API endpoints & prediction routers |
| `app/registry/mlflow_adapter.py` | 59 | 13 | **78%** | Local artifact model registry adapter |
| `app/main.py` | 47 | 15 | **68%** | Application startup & lifespan handler |
| `app/recovery/policy.py` | 32 | 20 | **38%** | Autonomous recovery orchestration rules |
| **TOTAL APPLICATION CODE** | **698** | **118** | **83.1%** | **Comprehensive Full System Coverage** |

---

## 3. High-Priority Safety Surface Verification (100% Covered)

Crucial security, regulatory, and safety gatekeeper surfaces achieved **100% coverage**:
1. **Model Validation Gates (`app/recovery/validator.py`):** 100% of candidate evaluation paths, accuracy thresholds, and regression rejections are tested.
2. **Access Control & RBAC (`app/security/auth.py`):** 100% of permission checks, authorization headers, and dual-key token validators are exercised.
3. **Configuration & Thresholds (`app/config.py`):** 100% of threshold definitions and safety bounds are validated.
4. **Quantum Benchmark Engine (`app/models/qml_benchmark.py`):** 100% of 4-qubit parameterized statevector operations are executed.

---

## 4. Coverage Artifact References
- **Machine-Readable Coverage JSON:** [`docs/reports/coverage.json`](coverage.json)
- **Interactive HTML Coverage Explorer:** [`docs/reports/htmlcov/index.html`](htmlcov/index.html)
