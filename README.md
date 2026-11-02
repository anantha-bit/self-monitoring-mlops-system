# Self-Monitoring MLOps System: Intelligent Drift Detection, Monitoring & Automated Recovery

[![Self-Monitoring MLOps CI Pipeline](https://github.com/anantha-bit/self-monitoring-mlops-system/actions/workflows/ci.yml/badge.svg)](https://github.com/anantha-bit/self-monitoring-mlops-system/actions/workflows/ci.yml)
[![Tests Passing](https://img.shields.io/badge/tests-18%20passed-success.svg)](tests/)
[![Statement Coverage](https://img.shields.io/badge/statement--coverage-83.1%25-brightgreen.svg)](docs/reports/CODE_COVERAGE_REPORT.md)
[![Branch Coverage](https://img.shields.io/badge/branch--coverage-79%25-blue.svg)](docs/reports/BRANCH_COVERAGE_REPORT.md)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.4.1-EE4C2C.svg)](https://pytorch.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.2.4-6929C4.svg)](https://qiskit.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)
[![Release](https://img.shields.io/badge/release-v1.0.0-purple.svg)](https://github.com/anantha-bit/self-monitoring-mlops-system/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end, production-ready MLOps microservice framework designed for mission-critical financial transaction risk scoring, continuous unsupervised drift detection, deep learning anomaly identification, and closed-loop autonomous model self-healing.

---

## 📑 Table of Contents
1. [Project Overview & Problem Statement](#-project-overview--problem-statement)
2. [Student Team & Academic Identity](#-student-team--academic-identity)
3. [Course Deliverables Breakdown (Deliverables 1, 2, and 3)](#-course-deliverables-breakdown)
   - [Deliverable Part-1: Specifications, Architecture & Planning](#deliverable-part-1--specifications-architecture--planning)
   - [Deliverable Part-2: Agile Sprints Execution & Complete Working Product](#deliverable-part-2--agile-sprints-execution--complete-working-product)
   - [Deliverable Part-3: Testing Updation, Execution & Formal Test Reports](#deliverable-part-3--testing-updation-execution--formal-test-reports)
4. [System Architecture & Component Structure](#-system-architecture--component-structure)
5. [Repository Directory Structure](#-repository-directory-structure)
6. [Comprehensive Setup & Installation Guide](#-comprehensive-setup--installation-guide)
7. [Automated Test Execution & Quality Gates](#-automated-test-execution--quality-gates)
8. [Interactive Live Walkthrough & Operational Demonstration](#-interactive-live-walkthrough--operational-demonstration)
9. [CI/CD Pipeline & DevOps Automation](#-cicd-pipeline--devops-automation)
10. [Academic Integrity & License](#-academic-integrity--license)

---

## 🌟 Project Overview & Problem Statement

### The Problem in Production ML
Machine learning models deployed in production inevitably degrade due to **concept drift** (changes in underlying statistical relationships between features and targets) and **data drift** (shifts in the input feature distribution caused by economic changes, seasonality, consumer behavior, or sensor anomalies). In high-throughput domains like financial fraud detection and credit risk assessment:
- Traditional monitoring fails because **ground-truth labels are delayed** by weeks or months (chargebacks, default events).
- Manual model retraining, validation, and deployment introduces human latency and high operational costs.
- Silent model failures lead to catastrophic financial risk, compliance violations, and severe customer impact.

### The Solution: Self-Monitoring MLOps System
This system introduces an intelligent, autonomous framework that continuously monitors real-time telemetry, detects distribution shifts without requiring ground-truth labels, and executes an automated, safe recovery lifecycle:
- **Real-Time Prediction & Telemetry Serving:** High-performance asynchronous FastAPI microservice with Prometheus telemetry scraping.
- **Unsupervised Two-Sample Statistical Drift Engine:** Computes Kolmogorov-Smirnov (KS-test) and Population Stability Index (PSI) over sliding telemetry windows.
- **Deep Learning Sequence Anomaly Scorer:** PyTorch Sequence Autoencoder that detects reconstruction loss anomalies on complex input vectors.
- **Quantum Machine Learning (QML) Benchmark:** Parameterized 4-qubit variational circuit benchmark running on a quantum statevector backend for advanced algorithmic benchmarking.
- **Closed-Loop Autonomous Recovery:** Dynamic policy triggers candidate model retraining upon drift alerts.
- **Strict Validation Quality Gates:** Candidate models must satisfy rigorous accuracy ($\ge 0.85$) and latency constraints before promotion.
- **Defensive Dual-Key Administrative Promotion:** Prevents unauthorized or rogue deployments.
- **Emergency Automated Rollback:** Automatically reverts to a certified stable model snapshot if degradation is detected.
- **Immutable Cryptographic Audit Ledger:** SHA-256 block hash-chained ledger logging all administrative operations, model promotions, and rollback events.
- **Interactive Web Dashboard:** Real-time visual monitoring of drift metrics, model states, prediction throughput, and system health.

---

## 👥 Student Team & Academic Identity

| Team Member Name | USN | GitHub Profile | Project Contributions & Primary Responsibilities |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [@anantha-bit](https://github.com/anantha-bit) | **Project Lead**, FastAPI Architecture, Validation Gatekeeper, Automated Retraining, Rollback & E2E Orchestration |
| **AKASH G K** | **PES1UG24AM022** | [@akashgkuradagi](https://github.com/akashgkuradagi) | **Contributor**, Telemetry Metrics Collection, Statistical Drift Detection Engine (KS & PSI), Sensitivity Benchmarks |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [@prasadamith05-png](https://github.com/prasadamith05-png) | **Contributor**, PyTorch Sequence Autoencoder, Qiskit Quantum Simulator Benchmark, RBAC & SHA-256 Audit Ledger |

- **Department:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Institution:** PES University, Bengaluru
- **Course:** Software Engineering Mini-Project

---

## 📑 Course Deliverables Breakdown

This project fulfills all requirements specified across the three evaluation phases of the Software Engineering Mini-Project curriculum:

```
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                               SE MINI-PROJECT DELIVERABLES                                │
├───────────────────────────┬───────────────────────────────┬───────────────────────────────┤
│    DELIVERABLE PART-1     │      DELIVERABLE PART-2       │      DELIVERABLE PART-3       │
│  Specifications & Design  │   Agile Sprints & Product     │  Testing Updation & Reports   │
├───────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ • IEEE SRS Specification  │ • Sprint 1: MVP Microservice  │ • Updated Test Suite (18 TCs) │
│ • Software Test Plan      │ • Sprint 2: Full Recovery Sys │ • 100% Pass Rate (0 Defects)  │
│ • Architecture & Design   │ • 68 Story Points Delivered   │ • 83.1% Statement Coverage    │
│ • Test Case Catalogue     │ • 2 Verified Video Demos      │ • 4 Formal IEEE Test Reports  │
│ • Traceability Matrix     │ • GitHub CI & Projects Board  │ • Interactive HTML Coverage   │
└───────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

### Deliverable Part-1 — Specifications, Architecture & Planning

Deliverable Part-1 established the engineering foundation, technical requirements, testing philosophy, and system architecture for the project:

| Document ID | Deliverable Artifact | Description & Contents | View Markdown | View Document (.docx) |
| :---: | :--- | :--- | :---: | :---: |
| **DOC-01** | **Software Requirements Specification (SRS)** | IEEE 830 standard SRS defining 14 Functional Requirements (FR-01 to FR-14), 11 Non-Functional Requirements (NFR-01 to NFR-11), and 6 Security Requirements (SR-01 to SR-06). | [**`docs/01_SRS...md`**](docs/01_SRS_Self_Monitoring_MLOps_System.md) | [**`docs/deliverables_part1/01_SRS...docx`**](docs/deliverables_part1/01_SRS_Self_Monitoring_MLOps_System.docx) |
| **DOC-02** | **Software Test Plan** | IEEE 829 test plan outlining testing strategy, test levels, pass/fail thresholds, defect severity triage, and hardware/software harness configuration. | [**`docs/02_Test_Plan...md`**](docs/02_Test_Plan_Self_Monitoring_MLOps_System.md) | [**`docs/deliverables_part1/02_Test_Plan...docx`**](docs/deliverables_part1/02_Test_Plan_Self_Monitoring_MLOps_System.docx) |
| **DOC-03** | **Architecture & Design Document** | Modular microservice architecture, component topology, sequence flows, data contracts, and UML architectural diagrams. | [**`docs/03_Architecture...md`**](docs/03_Architecture_Design_Self_Monitoring_MLOps_System.md) | [**`docs/deliverables_part1/03_Architecture...docx`**](docs/deliverables_part1/03_Architecture_Design_Self_Monitoring_MLOps_System.docx) |
| **DOC-04** | **Test Case Catalogue** | Comprehensive test case definitions mapping business requirements to automated test procedures (TC-01 to TC-18). | [**`docs/04_Test_Case...md`**](docs/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md) | [**`docs/deliverables_part1/04_Test_Case...docx`**](docs/deliverables_part1/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.docx) |

---

### Deliverable Part-2 — Agile Sprints Execution & Complete Working Product

Deliverable Part-2 tracked agile sprint execution across two structured development cycles, resulting in a fully working, tested, and containerized production system:

#### 1. Agile Sprint Breakdown & Velocity
- **Sprint 1 — Foundation, Drift Detection & Experimental Models (19th – 23rd Oct 2026):**
  - **Delivered Velocity:** **34 Story Points** across 7 user stories (US-01 through US-07).
  - **Features:** Core FastAPI prediction engine, sliding-window telemetry collector, two-sample KS-test and PSI statistical drift engine, baseline Random Forest model, PyTorch Sequence Autoencoder, isolated 4-qubit Qiskit quantum benchmark, and GitHub Actions CI workflow.
  - **Release Tag:** [`v0.1.0-sprint1`](https://github.com/anantha-bit/self-monitoring-mlops-system/releases/tag/v0.1.0-sprint1).
- **Sprint 2 — Autonomous Recovery, Safety Gatekeeper, Security & Web Dashboard (26th – 30th Oct 2026):**
  - **Delivered Velocity:** **34 Story Points** across 7 user stories (US-08 through US-14).
  - **Features:** Multi-modal synthetic drift injection, autonomous candidate retraining pipeline, automated model validation quality gates (accuracy $\ge 0.85$, latency regression checks), dual-key administrative promotion lock, emergency rollback trigger, SHA-256 chained audit ledger, and real-time dashboard UI.
  - **Release Tag:** [`v1.0.0-sprint2`](https://github.com/anantha-bit/self-monitoring-mlops-system/releases/tag/v1.0.0-sprint2).
- **Total Project Velocity:** **68 Story Points** across 14 user stories (100% completed on schedule, zero spillovers).
- **Agile Backlog Traceability:** Full details documented in [**`BACKLOG.md`**](BACKLOG.md) and [**`docs/SPRINT_BACKLOG_AND_DEVIATIONS.md`**](docs/SPRINT_BACKLOG_AND_DEVIATIONS.md).

#### 2. Sprint Demonstration Videos (Verified H.264 MP4)
Video demonstrations were recorded, encoded in standard **H.264 (AVC) / MP4** with `+faststart` streaming metadata, committed directly to git, and verified for direct browser playback:

| Sprint | Deliverable Description | Target Duration | Repo File Path | Direct GitHub Video Link |
| :---: | :--- | :---: | :--- | :--- |
| **Sprint 1** | Functional MVP microservice demonstration: core prediction serving, automated telemetry metrics ingestion, two-sample KS & PSI statistical drift detection, PyTorch autoencoder, and isolated QML simulator benchmark. | **60s** (1 min) | [`docs/evidence/videos/sprint1.mp4`](docs/evidence/videos/sprint1.mp4) | [**▶️ Play sprint1.mp4 on GitHub**](https://github.com/anantha-bit/self-monitoring-mlops-system/blob/main/docs/evidence/videos/sprint1.mp4) |
| **Sprint 2** | Complete working product walkthrough: real-time dashboard, synthetic drift injection, policy-triggered candidate retraining, automated validation quality gates, dual-key promotion, emergency rollback, and SHA-256 audit logs. | **120s** (2 min) | [`docs/evidence/videos/sprint2.mp4`](docs/evidence/videos/sprint2.mp4) | [**▶️ Play sprint2.mp4 on GitHub**](https://github.com/anantha-bit/self-monitoring-mlops-system/blob/main/docs/evidence/videos/sprint2.mp4) |

> Complete walk-through scripts, narration guides, and timestamped sequences are documented in [**`docs/SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md`**](docs/SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md).

#### 3. Deliverable Verification Evidence & Screenshots

| Evidence Artifact | Description | Direct File Link |
| :--- | :--- | :---: |
| **GitHub Actions CI/CD Benchmark** | Automated CI pipeline workflow runs passing on `main` and feature branches across all three contributors with green checkmarks. | [**`docs/evidence/01_github_actions_ci_runs_benchmark.png`**](docs/evidence/01_github_actions_ci_runs_benchmark.png) |
| **GitHub Projects Agile Board** | 14 completed user stories mapped across Sprint-1 and Sprint-2 with Assignees and Story Points (68 SP total, 100% completed). | [**`docs/evidence/02_github_projects_board_benchmark.png`**](docs/evidence/02_github_projects_board_benchmark.png) |

---

### Deliverable Part-3 — Testing Updation, Execution & Formal Test Reports

In strict accordance with the **SE Mini-Project Deliverables Part-3** instructions:

#### 1. Test Cases Updation
- The test suite was updated and aligned with all components delivered across Sprint 1 and Sprint 2, establishing **18 automated test cases (TC-01 through TC-18)**.
- Formally updated in [**`docs/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md`**](docs/04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md) (Version 1.1.0) and [**`docs/02_Test_Plan_Self_Monitoring_MLOps_System.md`**](docs/02_Test_Plan_Self_Monitoring_MLOps_System.md).

#### 2. Testing Execution (2nd Nov to 6th Nov 2026)
- **100% Pass Rate:** All **18 of 18 test cases passing** with zero defects.
- **Coverage Achieved:** **83.1% statement coverage** (580/698 statements) and **79% combined line + branch coverage** across application packages.
- **Four Required Formal Test Reports Uploaded:**
  - 📘 [**Unit Test Report (`docs/reports/UNIT_TEST_REPORT.md`)**](docs/reports/UNIT_TEST_REPORT.md) | [Direct in docs/](docs/UNIT_TEST_REPORT.md): Matrix of TC-01 to TC-18, execution timings, and defect triage.
  - 📗 [**System Validation Report (`docs/reports/SYSTEM_VALIDATION_REPORT.md`)**](docs/reports/SYSTEM_VALIDATION_REPORT.md) | [Direct in docs/](docs/SYSTEM_VALIDATION_REPORT.md): System compliance against 14 FRs, 11 NFRs, 6 SRs, and 5 operational scenarios.
  - 📙 [**Code Coverage Report (`docs/reports/CODE_COVERAGE_REPORT.md`)**](docs/reports/CODE_COVERAGE_REPORT.md) | [Direct in docs/](docs/CODE_COVERAGE_REPORT.md): Detailed module-by-module statement coverage breakdown.
  - 📕 [**Branch Coverage Report (`docs/reports/BRANCH_COVERAGE_REPORT.md`)**](docs/reports/BRANCH_COVERAGE_REPORT.md) | [Direct in docs/](docs/BRANCH_COVERAGE_REPORT.md): Analysis of 132 conditional branches and safety gate decision surfaces.
  - 🌐 [**Interactive HTML Coverage Explorer (`docs/reports/htmlcov/index.html`)**](docs/reports/htmlcov/index.html): Line-by-line interactive browser visualization.

#### 3. Sprint Scope Note (Zero Spillovers)
- As specified in Section 3 of the SE Mini-Project Deliverables Part-3 brief, Sprint-3 is an *Optional Parallel Activity* reserved exclusively for teams requiring spillover development.
- Because 100% of user stories, functional modules, and safety controls were completed and verified within Sprints 1 and 2, no Sprint 3 development was conducted. The team transitioned directly into Deliverables Part-3 testing and system verification.

---

## 🏛️ System Architecture & Component Structure

### Architecture Flowchart

```mermaid
flowchart TD
    Client["Client Application / Traffic Generator"] -->|1. POST /api/v1/predict| API["FastAPI Prediction Microservice (FR-01, FR-02)"]
    API -->|2. Ingest Stream| Collector["Monitoring Collector (Prometheus Metrics)"]
    
    subgraph Monitoring & Anomaly Detection
        Collector -->|3. Sliding Windows| DriftEngine["Statistical Drift Analyzer\n(Two-Sample KS-Test & PSI) (FR-03, FR-04)"]
        Collector -->|Feature Sequence| DLAutoencoder["PyTorch Sequence Autoencoder\n(Reconstruction Error) (FR-06)"]
        QML["Qiskit 4-Qubit Quantum Simulator\n(Variational Benchmark) (FR-07)"] -.->|Isolated Benchmark| Registry["Model Registry Adapter"]
    end
    
    subgraph Autonomous Self-Healing & Safety Gates
        DriftEngine -->|4. Drift Detected (PSI >= 0.25)| AlertMgr["Alert Manager (FR-08)"]
        AlertMgr -->|5. Trigger Retraining| PolicyEngine["Recovery Policy Engine (FR-08, FR-09)"]
        PolicyEngine -->|6. Retrain on Fresh Data| Retrainer["Automated Model Retrainer"]
        Retrainer -->|7. Candidate Model| Gatekeeper["Validation Gatekeeper (FR-09, FR-10)"]
        Gatekeeper -->|8a. Pass Acc >= 0.85 & Latency| DualKey["Dual-Key Promotion Lock (FR-10, FR-14)"]
        DualKey -->|9. Authorized Promotion| Registry
        Gatekeeper -->|8b. Fail Validation Gate| Rollback["Emergency Rollback Trigger (FR-12)"]
        Rollback -->|Revert Active Pointer| Registry
    end
    
    subgraph Security & Audit Ledger
        API -.->|Request Auth| RBAC["RBAC / API Key Filter (FR-14)"]
        PolicyEngine -.->|Audit Record| AuditLedger["SHA-256 Chained Audit Ledger (FR-11)"]
        Gatekeeper -.->|Promotion Audit| AuditLedger
        Rollback -.->|Rollback Audit| AuditLedger
    end
    
    Registry -->|Serve Active Model Weights| API
```

### Core Subsystems & Components

1. **Prediction Microservice (`app/main.py`, `app/api/routes.py`):**
   - High-throughput asynchronous REST API built with FastAPI.
   - Serves prediction inference (`POST /api/v1/predict`) with latency SLAs ($p95 < 200\text{ ms}$).
   - Exposes system health checks (`GET /health`) and Prometheus scraping metrics (`GET /api/v1/metrics/prometheus`).
2. **Monitoring & Drift Engine (`app/monitoring/drift.py`, `app/monitoring/collector.py`):**
   - Ingests sliding windows of inference feature vectors.
   - Computes two-sample Kolmogorov-Smirnov (KS-test) p-values and Population Stability Index (PSI) without requiring delayed ground-truth labels.
   - Classifies drift: Stable ($\text{PSI} < 0.1$), Moderate Warning ($0.1 \le \text{PSI} < 0.25$), and Severe Drift ($\text{PSI} \ge 0.25$).
3. **Deep Learning & Quantum Experimental Models (`app/models/`):**
   - `dl_monitor.py`: PyTorch Autoencoder computing per-feature reconstruction error for multi-variate anomaly identification.
   - `ml_monitor.py`: Scikit-Learn baseline Random Forest classifier trained on financial risk features.
   - `qml_benchmark.py`: Isolated 4-qubit parameterized quantum circuit running on Qiskit's statevector backend.
4. **Autonomous Recovery & Quality Gatekeeper (`app/recovery/`):**
   - `policy.py`: Evaluates severity rules and dispatches candidate retraining workflows.
   - `validator.py`: Automated safety gatekeeper evaluating accuracy ($\ge 0.85$), latency, and performance regressions. Rejects defective models and blocks unauthorized promotion.
5. **Security & Cryptographic Audit Ledger (`app/security/`):**
   - `auth.py`: Role-Based Access Control (RBAC) enforcing admin, tester, and guest roles.
   - `audit.py`: Tamper-resistant audit trail with cryptographic SHA-256 block hash chaining.
6. **Model Registry Adapter (`app/registry/mlflow_adapter.py`):**
   - Maintains versioned model snapshots, active pointers, candidate quarantines, and rollback archives.

---

## 📂 Repository Directory Structure

```
self-monitoring-mlops-system/
├── .github/
│   └── workflows/
│       └── ci.yml                         # Automated GitHub Actions CI/CD Pipeline
├── app/
│   ├── api/
│   │   └── routes.py                      # FastAPI REST endpoints & prediction router
│   ├── models/
│   │   ├── ml_monitor.py                  # Scikit-Learn Random Forest baseline
│   │   ├── dl_monitor.py                  # PyTorch Sequence Autoencoder anomaly detector
│   │   └── qml_benchmark.py               # Isolated 4-Qubit Variational Quantum Simulator
│   ├── monitoring/
│   │   ├── collector.py                   # Ingestion pipeline & Prometheus metrics
│   │   ├── drift.py                       # Statistical drift engine (KS-test & PSI)
│   │   └── benchmark.py                   # Shift sensitivity benchmark suite
│   ├── recovery/
│   │   ├── policy.py                      # Recovery policy engine & trigger rules
│   │   └── validator.py                   # Automated quality gates & regression checks
│   ├── registry/
│   │   └── mlflow_adapter.py              # Versioned model registry adapter
│   ├── security/
│   │   ├── auth.py                        # API key authentication & RBAC
│   │   └── audit.py                       # Tamper-resistant SHA-256 hash-chained audit logger
│   ├── config.py                          # Environment & threshold configuration
│   └── main.py                            # FastAPI application initialization & lifespan
├── docs/
│   ├── deliverables_part1/                # Official Deliverables Part-1 Word Documents
│   │   ├── 01_SRS_Self_Monitoring_MLOps_System.docx
│   │   ├── 02_Test_Plan_Self_Monitoring_MLOps_System.docx
│   │   ├── 03_Architecture_Design_Self_Monitoring_MLOps_System.docx
│   │   └── 04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.docx
│   ├── evidence/                          # Deliverable Verification Evidence & Screenshots
│   │   ├── 01_github_actions_ci_runs_benchmark.png # Passing CI runs benchmark
│   │   ├── 02_github_projects_board_benchmark.png  # Agile Projects board (14 backlog items)
│   │   └── videos/                        # Playable Demonstration MP4 Videos
│   │       ├── sprint1.mp4                # 60s Sprint-1 MVP demo video
│   │       ├── sprint2.mp4                # 120s Sprint-2 product demo video
│   │       └── README.md                  # Video guide & script references
│   ├── reports/                           # Formal Deliverables Part-3 Test Reports
│   │   ├── UNIT_TEST_REPORT.md            # Comprehensive Unit Test Report (18 tests)
│   │   ├── SYSTEM_VALIDATION_REPORT.md    # IEEE SRS System Validation Report
│   │   ├── CODE_COVERAGE_REPORT.md        # Line-by-line coverage analysis (83.1%)
│   │   ├── BRANCH_COVERAGE_REPORT.md      # Conditional branch coverage analysis (79%)
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
│   ├── SPRINT_BACKLOG_AND_DEVIATIONS.md   # Backlog, Story Points, Velocity & Deviations
│   └── SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md # 1-min & 2-min video demonstration scripts
├── tests/                                 # 18 Automated Pytest Test Cases
│   ├── test_tc01_tc02_health_metrics.py   # TC-01 (Health), TC-02 (Metrics), TC-09 (Latency)
│   ├── test_tc03_tc04_tc06_drift.py       # TC-03 (Baseline), TC-04 (Drift Alert), TC-06 (No Labels)
│   ├── test_tc05_tc16_experiments.py      # TC-05 (ML/DL/QML), TC-16 (Reproducibility)
│   ├── test_tc07_tc08_tc18_recovery_gates.py # TC-07 (Validation Gate), TC-08 (Rollback), TC-18 (Regression)
│   ├── test_tc10_fault_tolerance.py       # TC-10 (Worker Isolation)
│   ├── test_tc11_tc12_security_audit.py   # TC-11 (RBAC), TC-12 (Audit Log), TC-17 (Surface Lock)
│   ├── test_tc13_tc14_payload_secrets.py  # TC-13 (Input Guard), TC-14 (Secret Redaction)
│   └── test_tc15_container_smoke.py       # TC-15 (Docker Build Smoke)
├── Dockerfile                             # Production container specification
├── docker-compose.yml                     # Multi-container orchestration specification
├── pytest.ini                             # Pytest harness configuration
├── requirements.txt                       # Production & test dependencies
├── BACKLOG.md                             # Complete Agile Backlog with 14 User Stories
└── README.md                              # Master project documentation
```

---

## 🚀 Comprehensive Setup & Installation Guide

Follow these steps to set up, run, and test the system locally or inside Docker containers:

### 1. Prerequisites
- **Python:** Version `3.12+` (64-bit)
- **Git:** Version `2.30+`
- **Docker & Docker Compose:** (Optional, for containerized deployment)

### 2. Clone Repository & Setup Virtual Environment

#### On Windows (PowerShell):
```powershell
# 1. Clone the repository
git clone https://github.com/anantha-bit/self-monitoring-mlops-system.git
cd self-monitoring-mlops-system

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### On Linux / macOS (Bash):
```bash
# 1. Clone the repository
git clone https://github.com/anantha-bit/self-monitoring-mlops-system.git
cd self-monitoring-mlops-system

# 2. Create Python virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Running the Microservice Locally

Start the FastAPI application with live reloading using Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Once running, access the services:
- 🌐 **Real-Time Web Dashboard:** [`http://localhost:8000/`](http://localhost:8000/)
- 🩺 **Microservice Health Check:** [`http://localhost:8000/health`](http://localhost:8000/health)
- 📖 **Interactive Swagger UI:** [`http://localhost:8000/docs`](http://localhost:8000/docs)
- 📑 **ReDoc Documentation:** [`http://localhost:8000/redoc`](http://localhost:8000/redoc)
- 📊 **Prometheus Metrics Exposition:** [`http://localhost:8000/api/v1/metrics/prometheus`](http://localhost:8000/api/v1/metrics/prometheus)
- 🔒 **Cryptographic Audit Ledger:** [`http://localhost:8000/api/v1/audit/logs`](http://localhost:8000/api/v1/audit/logs)

---

### 4. Running with Docker & Docker Compose

To run the complete system in an isolated container:
```bash
# Build and run container in detached mode
docker compose up --build -d

# Check running container status
docker compose ps

# View container logs
docker compose logs -f

# Stop container
docker compose down
```

---

## 🧪 Automated Test Execution & Quality Gates

The test harness is implemented in Pytest with strict coverage and quality gates.

### 1. Run the Full Test Suite (18 Automated Test Cases)
```bash
python -m pytest tests/ -v
```

### 2. Run with Statement & Branch Coverage
```bash
python -m pytest tests/ --cov=app --cov-branch --cov-report=term-missing --cov-report=json:docs/reports/coverage.json --cov-report=html:docs/reports/htmlcov
```

### 3. Summary of Test Verification Results
- **Total Tests Executed:** **18**
- **Passed:** **18 (100% Pass Rate)**
- **Failed:** **0**
- **Total Execution Time:** **~17.8 seconds**
- **Statement Coverage:** **83.1% (580 / 698 statements)**
- **Branch Coverage:** **79% combined**

---

## 🎮 Interactive Live Walkthrough & Operational Demonstration

You can test the entire self-monitoring and recovery lifecycle interactively:

### 1. Submit a Real-Time Prediction Request
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [0.12, -0.45, 1.23, 0.05, -0.89, 0.34, 0.67, -0.12, 0.44, -0.21]}'
```
*Expected Response:* HTTP 200 with prediction probability, risk classification (`LOW_RISK`), model version, and inference latency.

### 2. Inject Synthetic Concept Drift
```bash
curl -X POST "http://localhost:8000/api/v1/monitoring/inject-drift" \
     -H "Content-Type: application/json" \
     -d '{"magnitude": 2.5, "feature_indices": [0, 1, 2]}'
```
*Expected Response:* HTTP 200 confirming synthetic shift applied to feature distributions.

### 3. Trigger Drift Evaluation & Observe Quarantine Alert
```bash
curl -X GET "http://localhost:8000/api/v1/monitoring/drift"
```
*Expected Response:* Drift engine reports $\text{PSI} \ge 0.25$, flags `alert_triggered: true`, and initiates autonomous recovery quarantine.

### 4. Inspect the Immutable SHA-256 Audit Ledger
```bash
curl -X GET "http://localhost:8000/api/v1/audit/logs"
```
*Expected Response:* Cryptographically chained audit blocks showing all events, previous block hashes, timestamps, and SHA-256 integrity tokens.

---

## 🔄 CI/CD Pipeline & DevOps Automation

The repository includes a fully automated GitHub Actions CI/CD pipeline defined in [**`.github/workflows/ci.yml`**](.github/workflows/ci.yml):

```yaml
name: Self-Monitoring MLOps CI Pipeline

on:
  push:
    branches: [ "main", "feature/*" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt && pip install httpx flake8 pytest-cov coverage
      - run: flake8 app tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - run: python -m pytest tests/ --cov=app --cov-branch --cov-report=term-missing -v
      - run: docker build -t self-monitoring-mlops:latest .
```

Every push and pull request triggers linting, test execution (TC-01 through TC-18), coverage checks, and a Docker container build smoke test.

---

## 📜 Academic Integrity & License

This project was developed for the **Software Engineering Mini-Project** course at **PES University**, Bengaluru.

- **License:** Distributed under the [**MIT License**](LICENSE).
- **Academic Declaration:** All code, models, tests, reports, and documentation were authored collaboratively by the team members listed above in full compliance with university academic integrity standards.
