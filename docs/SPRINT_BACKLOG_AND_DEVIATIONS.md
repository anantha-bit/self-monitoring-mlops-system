# Software Engineering Mini-Project Deliverables Part-2: Agile Sprint & Backlog Documentation

## Project Control & Identity
- **Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery
- **Repository:** [`https://github.com/anantha-bit/self-monitoring-mlops-system`](https://github.com/anantha-bit/self-monitoring-mlops-system)
- **Department:** CSE (Artificial Intelligence & Machine Learning)
- **Course:** Software Engineering Mini-Project

### Team Members & Roles
| Name | USN | GitHub Handle | Role in Project |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | PES1UG24AM036 | [`anantha-bit`](https://github.com/anantha-bit) | Repo Owner, Project Lead, API & Orchestration Architect |
| **AKASH G K** | PES1UG24AM022 | [`akashgkuradagi`](https://github.com/akashgkuradagi) | Contributor, Telemetry & Statistical Drift Lead |
| **AMIT PRASAD S G** | PES1UG24AM033 | [`prasadamith05-png`](https://github.com/prasadamith05-png) | Contributor, Deep Learning / QML & Security Lead |

---

## 1. Backlog Creation in GitHub (ETA: 12th Oct 2026)
All Functional Requirements (FR) and Non-Functional Requirements (NFR) from Deliverable 1 (SRS) were decomposed into Agile User Stories and logged as tracked GitHub Issues with Story Points (SP) and Team Assignments.

### Backlog Mapping & Estimation Table

| Issue # | Sprint | Assignee | Story Summary | Traceability | Story Points |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **#1** | Sprint-1 | Anantha Krishna M A | Core Prediction API & Health Monitoring Endpoint | FR-01, FR-02, NFR-01, NFR-03 | **5** |
| **#2** | Sprint-1 | AKASH G K | Ingestion Pipeline & Prometheus Metrics Collector | FR-02, NFR-07, NFR-09 | **5** |
| **#3** | Sprint-1 | AKASH G K | Drift Detection Engine & Statistical Window Comparison | FR-03, FR-08, TC-03, TC-04 | **8** |
| **#4** | Sprint-1 | AKASH G K | Classical ML Baseline & Drift Monitoring Experiments | FR-05, NFR-04, TC-05, TC-16 | **5** |
| **#5** | Sprint-1 | AMIT PRASAD S G | Deep Learning Sequence/Anomaly Detector (PyTorch) | FR-06, TC-05 | **8** |
| **#6** | Sprint-1 | AMIT PRASAD S G | Experimental Quantum Machine Learning (QML) Simulator | FR-07, TC-05 | **5** |
| **#7** | Sprint-1 | Anantha Krishna M A | CI/CD GitHub Actions & Multi-Stage Docker Packaging | NFR-05, NFR-06, TC-15 | **3** |
| **#8** | Sprint-2 | Anantha Krishna M A | Recovery Orchestration & Automated Validation Gatekeeper | FR-09, FR-10, NFR-10, TC-07, TC-18 | **8** |
| **#9** | Sprint-2 | AKASH G K | Automated Rollback Mechanism & Stable Fallback Policy | FR-12, TC-08 | **5** |
| **#10** | Sprint-2 | AMIT PRASAD S G | RBAC, Tamper-Resistant Audit Logging & Security Controls | FR-11, FR-14, SR-01~06, TC-11, TC-12 | **8** |
| **#11** | Sprint-2 | AMIT PRASAD S G | Interactive Web Dashboard & Real-Time Monitoring UI | FR-13, NFR-08 | **5** |
| **#12** | Sprint-2 | Anantha Krishna M A | Deliverable Closure: Documentation, Traceability & Demo | Deliverable Part-2 Closure | **3** |

- **Total Story Points:** 68 SP (Sprint 1: 34 SP, Sprint 2: 34 SP)
- **Team Velocity:** 34 SP per sprint (balanced evenly across all three members).

---

## 2. Sprint-1 Execution [19th Oct to 23rd Oct 2026]
- **Goal:** Establish core prediction serving, automated telemetry collection, statistical drift analyzer (KS-test & PSI), baseline ML model, PyTorch sequence anomaly autoencoder, isolated QML benchmark, and GitHub Actions CI.
- **Workflow & Branching Strategy:**
  - Feature branches created by assigned team members:
    - `feature/sprint1-metrics-and-drift` (Akash G K)
    - `feature/sprint1-dl-qml-experiments` (Amit Prasad S G)
    - `feature/sprint1-api-and-cicd` (Anantha Krishna M A)
  - Pull Requests submitted, automated CI checks verified, reviewed and committed to `main` by Repo Owner.
- **Sprint 1 Outcome:**
  - Fully working FastAPI prediction and monitoring microservice.
  - Automated tests passing for TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-09, TC-15, TC-16.
  - Outcome demonstrated in a 1-minute working product demo video (see demo guide).

---

## 3. Sprint-2 Execution [26th Oct to 30th Oct 2026]
- **Goal:** Complete automated recovery policy, validation gates, dual-key candidate promotion, emergency fallback rollback, role-based security, SHA-256 audit chaining, and interactive web dashboard.
- **Workflow & Branching Strategy:**
  - Feature branches created and PRs submitted:
    - `feature/sprint2-recovery-and-rollback` (Akash G K)
    - `feature/sprint2-security-audit-dashboard` (Amit Prasad S G)
    - `feature/sprint2-orchestration-and-docs` (Anantha Krishna M A)
  - Pull Requests merged into `main`.
- **Sprint 2 Outcome:**
  - 100% of functional requirements (FR-01 to FR-14) and security requirements (SR-01 to SR-06) operational.
  - All 18 Test Cases (TC-01 through TC-18) fully verified and passing.
  - Outcome demonstrated in a 2-minute comprehensive working product video.
  - Development cycle frozen as of 30th October 2026 (Tagged `v1.0.0-sprint2`).

---

## 4. Documented Deviations from Submitted Part-1 Design (Deliverable 2.i)
In accordance with Section 2.i of Deliverables Part-2, the following technical refinements and deviations from initial preliminary sketches are documented:

1. **Self-Contained In-Process Telemetry & SQLite Metric Store vs External Prometheus Agent:**
   - *Original Plan:* Assumed an external Prometheus server daemon required on the host.
   - *Implemented Improvement:* Implemented an internal high-performance telemetry aggregator (`MonitoringCollector`) with on-demand `/api/v1/metrics/prometheus` exposition and SQLite metadata persistence. This guarantees zero external system dependency while satisfying NFR-07 and TC-02.
2. **QML Benchmark Parameterized Simulation:**
   - *Original Plan:* Explored PennyLane cloud simulators.
   - *Implemented Improvement:* Built an in-process 4-qubit hardware-efficient variational quantum circuit simulator (`QuantumVariationalSimulator`) with angle embedding and CNOT entanglement. As strictly mandated by FR-07 and TC-05, this QML component is isolated from automated recovery decisions.
3. **Audit Log Tamper-Resistance Enhancement:**
   - *Original Plan:* Flat file log of candidate approvals.
   - *Implemented Improvement:* Designed a SHA-256 cryptographic hash-chaining audit logger (`app/security/audit.py`), where each record chains the previous record's hash, providing verifiable tamper-evidence (SR-05, TC-12).
