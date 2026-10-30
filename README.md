# Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery

[![CI Pipeline](https://github.com/anantha-bit/self-monitoring-mlops-system/actions/workflows/ci.yml/badge.svg)](https://github.com/anantha-bit/self-monitoring-mlops-system/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/Deep%20Learning-PyTorch-EE4C2C.svg)](https://pytorch.org/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg)](https://www.docker.com/)
[![Tests Passing](https://img.shields.io/badge/Test%20Suite-25%20Passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-86%25-brightgreen.svg)](docs/reports/CODE_COVERAGE_REPORT.md)
[![Release](https://img.shields.io/badge/Release-v1.1.0--sprint3-blue.svg)](https://github.com/anantha-bit/self-monitoring-mlops-system/releases/tag/v1.1.0-sprint3)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end, production-ready MLOps monitoring and automated recovery system designed for tabular machine learning models. Built in compliance with IEEE 29148 requirements specifications and Deliverables Part-1, Part-2, and Part-3 of the Software Engineering Mini-Project.

---

## 👥 Project Team & Contributors

| Name | USN | GitHub Profile | Project Responsibility |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [@anantha-bit](https://github.com/anantha-bit) | **Project Lead**, Core API, Recovery Orchestration, E2E Integration & Release Manager |
| **AKASH G K** | **PES1UG24AM022** | [@akashgkuradagi](https://github.com/akashgkuradagi) | **Contributor**, Metrics Collection, Statistical Drift Engine, Benchmarking & Tripwire |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [@prasadamith05-png](https://github.com/prasadamith05-png) | **Contributor**, DL Sequence Autoencoder, QML Benchmark, RBAC & Audit Verifier |

---

## 📑 Software Engineering Mini-Project Deliverables Part-3

In strict accordance with the **SE Mini-Project Deliverables Part-3** instructions:
1. **Test Cases Updation:**
   - Expanded from 18 to **25 automated test cases** covering newly developed Sprint-3 components (statistical sensitivity sweeps, autoencoder reconstruction attribution, continuous health tripwires, and SHA-256 audit chain verification).
   - Fully updated and executed in [**docs/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md**](docs/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md) and [**docs/02_Test_Plan_Self_Monitoring_MLOps_System.md**](docs/02_Test_Plan_Self_Monitoring_MLOps_System.md).
2. **Testing (2nd Nov to 6th Nov 2026):**
   - 100% test completion with **25/25 tests passing** in ~8.5 seconds.
   - **86% code coverage** achieved (88.8% statement coverage, 682/768 statements).
   - Generated and uploaded the 4 required test reports to the repository's `docs/` and `docs/reports/` directories:
     - 📘 [**Unit Test Report** (`docs/reports/UNIT_TEST_REPORT.md`)](docs/reports/UNIT_TEST_REPORT.md) | [Direct in docs/](docs/UNIT_TEST_REPORT.md)
     - 📗 [**System Validation Report** (`docs/reports/SYSTEM_VALIDATION_REPORT.md`)](docs/reports/SYSTEM_VALIDATION_REPORT.md) | [Direct in docs/](docs/SYSTEM_VALIDATION_REPORT.md)
     - 📙 [**Code Coverage Report** (`docs/reports/CODE_COVERAGE_REPORT.md`)](docs/reports/CODE_COVERAGE_REPORT.md) | [Direct in docs/](docs/CODE_COVERAGE_REPORT.md)
     - 📕 [**Branch Coverage Report** (`docs/reports/BRANCH_COVERAGE_REPORT.md`)](docs/reports/BRANCH_COVERAGE_REPORT.md) | [Direct in docs/](docs/BRANCH_COVERAGE_REPORT.md)
     - 🌐 [Interactive HTML Coverage Explorer (`docs/reports/htmlcov/index.html`)](docs/reports/htmlcov/index.html)
3. **Sprint-3 Parallel Activity (2nd Nov to 6th Nov 2026):**
   - Completed parallel development of Sprint-3 features and backlog items (#13 to #19).
   - Complete documentation in [**docs/SPRINT_3_DOCUMENTATION.md**](docs/SPRINT_3_DOCUMENTATION.md) and [**BACKLOG.md**](BACKLOG.md).
   - Code contributions authored across all three team members and release tagged [`v1.1.0-sprint3`](https://github.com/anantha-bit/self-monitoring-mlops-system/releases/tag/v1.1.0-sprint3).

---

## 🎥 Sprint Demonstration Videos

In accordance with the Software Engineering Mini-Project Deliverables, video demonstrations for each sprint have been recorded, verified, and committed to the repository:

| Sprint | Deliverable Description | Duration | Repository Path | Direct GitHub Link |
| :--- | :--- | :---: | :--- | :--- |
| **Sprint 1** | Functional MVP microservice demonstration: core prediction serving, automated telemetry metrics ingestion, two-sample KS & PSI statistical drift detection, PyTorch autoencoder, and isolated QML simulator benchmark. | ~1 min | [docs/evidence/videos/sprint1.mp4](docs/evidence/videos/sprint1.mp4) | [View sprint1.mp4 on GitHub](https://github.com/anantha-bit/self-monitoring-mlops-system/blob/main/docs/evidence/videos/sprint1.mp4) |
| **Sprint 2** | Complete working product walkthrough: real-time dashboard, synthetic drift injection, policy-triggered candidate retraining, automated validation quality gates, dual-key promotion, emergency rollback, and SHA-256 audit logs. | ~2 min | [docs/evidence/videos/sprint2.mp4](docs/evidence/videos/sprint2.mp4) | [View sprint2.mp4 on GitHub](https://github.com/anantha-bit/self-monitoring-mlops-system/blob/main/docs/evidence/videos/sprint2.mp4) |

> Detailed scripts, narration guides, and recording instructions are documented in [docs/SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md](docs/SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md).

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    Client["Client / Application"] -->|Inference Requests| API["FastAPI Prediction API (FR-01, FR-02)"]
    API -->|Telemetry Stream| Collector["Monitoring Collector (Prometheus Metrics)"]
    
    subgraph Monitoring & Detection
        Collector -->|Sliding Windows| DriftEngine["Statistical Drift Analyzer\n(KS-Test & PSI) (FR-03)"]
        DriftEngine -->|Threshold Exceeded| AlertMgr["Alert Manager (FR-08)"]
        Collector -->|Temporal Sequence| DLAutoencoder["PyTorch Sequence Autoencoder (FR-06)"]
        Benchmark["Statistical Sensitivity Benchmark (FR-03, NFR-03)"] -.->|Sensitivity Matrix| DriftEngine
        DLVisualizer["DL Latent Anomaly Attribution (FR-06)"] -.->|Per-Feature Loss| DLAutoencoder
        QML["QML Simulator Benchmark (FR-07)"] -.->|Isolated Reports| Registry
    end

    subgraph Autonomous Recovery & Safety Gates
        AlertMgr -->|Drift Signal| Policy["Recovery Policy Engine (FR-09)"]
        Policy -->|Trigger Retraining| Retrain["Candidate Retraining Worker"]
        Retrain -->|New Candidate| Registry["Model Registry Adapter"]
        Registry -->|Quality Checks| Validator["Automated Validator (FR-10, NFR-10)\n• Min Accuracy Gate\n• Latency SLO Gate\n• Regression Gate"]
        Validator -->|Dual Approval| HumanApproval["Authorized ML Engineer Approval (FR-14)"]
        HumanApproval -->|Promote| ActiveModel["Production Active Model"]
        ActiveModel -.->|Post-Promotion Anomaly| Rollback["Automated Rollback Engine (FR-12)"]
        Tripwire["Continuous Health Tripwire (FR-01, FR-12)"] -->|Consecutive Failures| Rollback
        Rollback -.->|Restore| StableModel["Last Known Stable Model"]
    end

    subgraph Security & Governance
        API & Policy & HumanApproval -->|Audit Events| AuditLogger["Tamper-Resistant Audit Logger\n(SHA-256 Hash Chain) (SR-05)"]
        Verifier["Audit Chain Verifier (FR-11, SR-05)"] -->|Integrity Check| AuditLogger
        RBAC["API Key & Role-Based Access Control (SR-01, SR-02)"] --> API
    end

    subgraph User Experience & Observability
        Dashboard["Interactive Web Dashboard (FR-13, NFR-08)"] <-->|REST API| API
        PromScraper["Prometheus Metrics Exporter (FR-02, NFR-07)"] <-->|/api/v1/metrics/prometheus| API
    end
```

---

## 🚀 Key Features

1. **Production Prediction Microservice (`FR-01`, `FR-02`):**
   - High-throughput asynchronous serving using FastAPI and Scikit-learn Random Forest baseline.
   - P95 latency sub-20ms ($18.4\text{ ms}$ verified) with automated telemetry capturing request counts, latencies, and input distributions.
2. **Multi-Method Drift Detection Engine (`FR-03`, `FR-08`):**
   - Two-sample **Kolmogorov-Smirnov (KS)** tests on numerical distributions.
   - **Population Stability Index (PSI)** quantile binned comparisons.
   - Real-time alert dispatching across severity levels (`WARNING`, `CRITICAL`).
   - Statistical sensitivity benchmark sweep testing shifts from $0.0\sigma$ to $3.0\sigma$.
3. **Multi-Paradigm Model Experiments (`FR-05`, `FR-06`, `FR-07`):**
   - **Classical ML:** Random Forest classifier on multidimensional tabular features with versioned hyperparameter logging.
   - **Deep Learning:** PyTorch Temporal Sequence Autoencoder detecting telemetry anomalies and attributing per-feature reconstruction errors.
   - **Quantum ML Benchmark:** Isolated 4-qubit parameterized variational quantum circuit (VQC) benchmark with angle embedding and CNOT entanglement.
4. **Automated Recovery Policy & Quality Gates (`FR-09`, `FR-10`, `NFR-10`):**
   - Policy evaluates drift severity, error rates, and latency SLOs before candidate retraining.
   - Strict candidate validation gate: accuracy >= 80%, latency <= 150ms, and zero regression vs stable baseline.
   - **Dual-key promotion:** Candidate can **never** be promoted without both passing validation and authorized human approval.
5. **Continuous Health Tripwire & Emergency Rollback (`FR-01`, `FR-12`):**
   - `ContinuousHealthTripwire` tracks consecutive telemetry spikes, triggering instant rollback after 3 failures.
   - Instant 1-click fallback to the last known stable model version if post-promotion anomalies are detected.
6. **Enterprise Security & Cryptographic Audit Verification (`SR-01` ~ `SR-06`, `FR-11`):**
   - Role-Based Access Control (`Admin`, `MLEngineer`, `Viewer`, `Service`).
   - Append-only audit logger using cryptographic **SHA-256 hash chaining** with independent chain verifier utility.
   - Request size sanitization and strict secret protection against credential leakage in error traces.
7. **Interactive Real-Time Dashboard & Live Prometheus Exporter (`FR-13`, `NFR-08`, `NFR-07`):**
   - Live metric gauges, telemetry simulators, drift monitors, candidate validation/promotion controls, and audit logs.
   - Scrapable Prometheus exposition endpoint at `/api/v1/metrics/prometheus`.

---

## ⚡ Quick Start

### 1. Environment Setup
```bash
git clone https://github.com/anantha-bit/self-monitoring-mlops-system.git
cd self-monitoring-mlops-system
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Launch Application
```bash
uvicorn app.main:app --reload --port 8000
```
- Open **`http://localhost:8000`** in your browser to launch the live dashboard.
- Open **`http://localhost:8000/docs`** for interactive Swagger API documentation.
- Open **`http://localhost:8000/api/v1/metrics/prometheus`** for live Prometheus exposition text.

---

## 🧪 Automated Test Execution (TC-01 through TC-25)

Run the complete 25-case test suite with line and branch coverage analysis:
```bash
python -m pytest tests/ --cov=app --cov-branch --cov-report=term-missing --cov-report=html:docs/reports/htmlcov --cov-report=json:docs/reports/coverage.json
```
**Results:** All 25 test cases pass in ~8.5 seconds with **86% code coverage**.

---

## 📁 Repository Structure

```
├── .github/workflows/
│   ├── ci.yml                             # Automated CI test execution & Docker build
│   └── pr-automation.yml                  # Automated PR labeling & checks
├── app/
│   ├── api/
│   │   └── routes.py                      # REST API endpoints (Health, Ingest, Drift, Candidates, Rollback, Prometheus)
│   ├── dashboard/
│   │   └── index.html                     # Real-time interactive UI dashboard
│   ├── models/
│   │   ├── ml_monitor.py                  # Classical ML baseline (Scikit-Learn Random Forest)
│   │   ├── dl_monitor.py                  # PyTorch Sequence Anomaly Autoencoder
│   │   ├── dl_visualizer.py               # Feature reconstruction error attribution visualizer
│   │   └── qml_benchmark.py               # Isolated 4-Qubit Variational Quantum Simulator
│   ├── monitoring/
│   │   ├── collector.py                   # Ingestion pipeline & Prometheus metrics
│   │   ├── drift.py                       # Statistical drift engine (KS-test & PSI)
│   │   └── benchmark.py                   # Stepwise variational shift sensitivity benchmark suite
│   ├── recovery/
│   │   ├── policy.py                      # Recovery policy engine & trigger rules
│   │   ├── validator.py                   # Automated quality gates & regression checks
│   │   └── health_checker.py              # Continuous health telemetry tripwire monitor
│   ├── registry/
│   │   └── mlflow_adapter.py              # Versioned model registry adapter
│   ├── security/
│   │   ├── auth.py                        # API key authentication & RBAC
│   │   ├── audit.py                       # Tamper-resistant SHA-256 hash-chained audit logger
│   │   └── verifier.py                    # Cryptographic audit ledger chain verifier
│   ├── config.py                          # Environment & threshold configuration
│   └── main.py                            # FastAPI application initialization & lifespan
├── docs/
│   ├── reports/                           # Formal Deliverables Part-3 Test Reports
│   │   ├── UNIT_TEST_REPORT.md            # Comprehensive Unit Test Report (25 tests)
│   │   ├── SYSTEM_VALIDATION_REPORT.md    # IEEE SRS System Validation Report
│   │   ├── CODE_COVERAGE_REPORT.md        # Line-by-line coverage analysis (86%)
│   │   ├── BRANCH_COVERAGE_REPORT.md      # Conditional branch coverage analysis
│   │   ├── coverage.json                  # Machine-readable coverage data
│   │   └── htmlcov/                       # Interactive HTML coverage report
│   ├── UNIT_TEST_REPORT.md                # Direct doc link for deliverable grading
│   ├── SYSTEM_VALIDATION_REPORT.md        # Direct doc link for deliverable grading
│   ├── CODE_COVERAGE_REPORT.md            # Direct doc link for deliverable grading
│   ├── BRANCH_COVERAGE_REPORT.md          # Direct doc link for deliverable grading
│   ├── 01_SRS_Self_Monitoring_MLOps_System.md
│   ├── 02_Test_Plan_Self_Monitoring_MLOps_System.md
│   ├── 03_Architecture_Design_Self_Monitoring_MLOps_System.md
│   ├── 04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md
│   ├── SPRINT_3_DOCUMENTATION.md          # Sprint 3 Agile planning, stories & velocity
│   ├── SPRINT_BACKLOG_AND_DEVIATIONS.md   # Backlog, Story Points, Velocity & Deviations
│   └── SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md # 1-min & 2-min video demonstration scripts
├── tests/                                 # 25 Automated Pytest Test Cases
│   ├── test_tc01_tc02_health_metrics.py
│   ├── test_tc03_tc04_tc06_drift.py
│   ├── test_tc05_tc16_experiments.py
│   ├── test_tc07_tc08_tc18_recovery_gates.py
│   ├── test_tc10_fault_tolerance.py
│   ├── test_tc11_tc12_security_audit.py
│   ├── test_tc13_tc14_payload_secrets.py
│   ├── test_tc15_container_smoke.py
│   ├── test_tc19_drift_sensitivity_benchmark.py
│   ├── test_tc20_dl_latent_attribution.py
│   ├── test_tc21_health_tripwire.py
│   ├── test_tc22_audit_chain_verification.py
│   ├── test_tc23_e2e_recovery_workflow.py
│   ├── test_tc24_prometheus_live_export.py
│   └── test_tc25_recovery_policy_coverage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── BACKLOG.md                             # Complete Agile Sprint Backlog (19 items, 106 SP)
└── README.md
```

---

## 📜 Deliverable Closure Note
In accordance with Part-1, Part-2, and Part-3 of the Software Engineering Mini-Project guidelines:
- **Part-1:** SRS, Test Plan, Architectural Design, and Test Case Specifications established.
- **Part-2:** Agile Backlog created in GitHub Projects, Sprints 1 and 2 completed, video artifacts verified, and release tagged `v1.0.0-sprint2`.
- **Part-3:** Parallel Sprint 3 completed, 25 test cases executed with 100% pass rate, 86% coverage achieved, 4 formal test reports generated in `docs/`, and release tagged `v1.1.0-sprint3`.
- Contributions committed and pushed across all three team members: **Anantha Krishna M A** ([`@anantha-bit`](https://github.com/anantha-bit)), **AKASH G K** ([`@akashgkuradagi`](https://github.com/akashgkuradagi)), and **AMIT PRASAD S G** ([`@prasadamith05-png`](https://github.com/prasadamith05-png)).
