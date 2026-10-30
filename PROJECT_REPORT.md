# Comprehensive Project Report: Self-Monitoring MLOps System

**An Intelligent Framework for Machine Learning Model Drift Detection, Continuous Monitoring, and Autonomous Recovery**

- **Project Lead:** Anantha Krishna M A (USN: `PES1UG24AM036`)  
- **Team Members:**  
  - AKASH G K (USN: `PES1UG24AM022`)  
  - AMIT PRASAD S G (USN: `PES1UG24AM033`)  
- **Department:** Department of Computer Science & Engineering (AI & ML)  
- **Course:** Software Engineering Mini-Project (Deliverables Part-1 & Part-2)  
- **Repository:** [https://github.com/anantha-bit/self-monitoring-mlops-system](https://github.com/anantha-bit/self-monitoring-mlops-system)

---

## 1. Abstract
In production machine learning systems, statistical divergence between offline training distributions and real-world inference data—termed *data drift* and *concept drift*—causes silent predictive degradation. Traditional monitoring architectures rely on reactive manual intervention or external scheduled batch checks that introduce unacceptable latency and reliability risks. 

This project delivers an autonomous, self-monitoring MLOps framework tailored for real-time model telemetry, statistical drift diagnosis, and policy-driven recovery. By combining dual-sample **Kolmogorov-Smirnov (KS)** tests, **Population Stability Index (PSI)** quantile estimators, PyTorch-based **Deep Learning Sequence Anomaly Autoencoders**, and an isolated **Quantum Machine Learning (QML)** benchmark, the system detects distribution shifts sub-second. When degradation occurs, a strict policy engine orchestrates automated candidate retraining, enforces mandatory validation quality gates (minimum accuracy $\ge 80\%$, P95 latency $\le 150\text{ ms}$, zero regression vs. stable baseline), requires dual-key authorized promotion, and provides an instant one-click fallback rollback mechanism. A tamper-resistant cryptographic **SHA-256 hash-chain audit log** guarantees enterprise auditability.

---

## 2. Introduction & Problem Statement
### 2.1 The Silent Failure Problem in MLOps
Machine learning models, unlike conventional rule-based software, do not crash with syntax errors when the input distribution changes. Instead, they produce confident but incorrect inferences. In critical domains (healthcare diagnostics, fraud detection, credit scoring), undetected model drift leads to massive systemic risk.

### 2.2 Key Engineering Challenges
1. **Separation of Drift from Quality Loss (FR-04):** In production, ground-truth labels often arrive with substantial delays. The monitoring framework must detect distribution divergence without fabricating accuracy numbers.
2. **Safety of Automated Recovery (NFR-10, FR-10):** Completely unrestricted autonomous retraining can deploy corrupted or regressed models. Candidate promotion must require automated validation plus human authorization.
3. **Resilience & Fault Isolation (NFR-02):** Failures in heavy analytical or quantum benchmarking workers must never interrupt the primary low-latency prediction serving path.
4. **Accountability & Integrity (SR-05):** All model promotions, candidate rejections, and rollbacks must be immutably recorded in a verifiable audit trail.

---

## 3. Architecture & Technical Design

### 3.1 Layered Service Architecture
The system is architected as a modular, decoupled microservice:
1. **Inference & Telemetry Layer (`app/api/`):** High-throughput FastAPI endpoints (`/health`, `/api/v1/predict`, `/api/v1/events/prediction`) instrumented with microsecond latency timers and error collectors.
2. **Statistical Drift & Quality Engine (`app/monitoring/`):**
   - **Continuous Feature Drift:** Non-parametric two-sample Kolmogorov-Smirnov test assessing null hypothesis that current window and reference window are drawn from identical continuous distributions.
   - **Quantile Stability (PSI):** Quantile-based Population Stability Index calculation across binned frequencies:
     $$\text{PSI} = \sum_{i=1}^{k} (A_i - E_i) \times \ln\left(\frac{A_i}{E_i}\right)$$
3. **Multi-Paradigm Model Experiments (`app/models/`):**
   - **Classical ML Baseline:** Scikit-Learn Random Forest Classifier trained on multidimensional tabular features with versioned parameter logging.
   - **Deep Learning Sequence Anomaly Detector:** Multi-layer PyTorch Autoencoder ($6 \to 3 \to 2 \to 3 \to 6$) trained on normal telemetry sequences to flag temporal inference anomalies via reconstruction loss spikes.
   - **Isolated Quantum ML (QML) Benchmark:** 4-qubit Hardware-Efficient Variational Quantum Classifier (VQC) with Ry rotation angle embedding and CNOT entangling gates running in an isolated sandbox benchmark.
4. **Policy & Recovery Engine (`app/recovery/`):**
   - Evaluates trigger conditions against severity thresholds.
   - **Automated Validation Gates:** Enforces $\text{Accuracy} \ge 0.80$, $\text{P95 Latency} \le 150\text{ ms}$, $\text{F1-Score} \ge 0.75$, and regression boundary $\le 2\%$ below stable model.
   - **Dual-Key Promotion:** Blocks model promotion unless validation is `PASSED` and authorized ML Engineer decision is `APPROVED`.
5. **Security & Cryptographic Audit Logger (`app/security/`):**
   - Role-Based Access Control (`Admin`, `MLEngineer`, `Viewer`, `Service`).
   - Append-only audit logger using chained SHA-256 hashes ($H_i = \text{SHA256}(Payload_i \parallel H_{i-1})$) to ensure tamper-evidence.
6. **Executive Web Dashboard (`app/dashboard/`):** Real-time monitoring UI displaying live gauges, 1-click synthetic drift injection, candidate validation panels, emergency rollback, and streaming audit logs.

---

## 4. Agile Sprint Execution & Team Contributions

### Sprint 1: Foundation, Telemetry & Multi-Model Experiments (19–23 Oct 2026)
- **Anantha Krishna M A (Lead):** Core API routing, health probe, Pydantic data models, and automated GitHub Actions CI pipeline.
- **AKASH G K:** Ingestion telemetry collector, Prometheus exposition format, and two-sample KS & PSI drift engine.
- **AMIT PRASAD S G:** PyTorch deep learning sequence anomaly autoencoder and 4-qubit variational quantum classifier simulator benchmark.
- **Sprint 1 Outcome:** Functional prediction microservice with passing tests for TC-01 to TC-06, TC-09, TC-15, TC-16. Released as `v0.1.0-sprint1`.

### Sprint 2: Autonomous Recovery, Safety Gates, Security & UI (26–30 Oct 2026)
- **Anantha Krishna M A (Lead):** Recovery orchestrator, automated validation service, regression gatekeeper, and project closure documentation.
- **AKASH G K:** Automated emergency rollback mechanism, fallback policy, and monitoring worker fault isolation.
- **AMIT PRASAD S G:** RBAC authentication, secret hygiene guards, SHA-256 hash-chained audit logger, and real-time dashboard UI.
- **Sprint 2 Outcome:** 100% of functional requirements operational, 18 of 18 test cases verified in CI/CD, interactive web dashboard, and development freeze as `v1.0.0-sprint2`.

---

## 5. Verification & Test Summary (TC-01 through TC-18)
The test suite spans unit, integration, performance, resilience, and security tests:

| Test ID | Objective | Traceability | Result |
| :--- | :--- | :--- | :---: |
| **TC-01** | Verify health probe returns HTTP 200 and version metadata | `FR-01` | **PASS** |
| **TC-02** | Verify prediction count, latency, and error rate recording | `FR-02, NFR-07` | **PASS** |
| **TC-03** | Verify stable data produces NO_DRIFT status | `FR-03` | **PASS** |
| **TC-04** | Verify shifted features trigger DRIFT_DETECTED and CRITICAL alert | `FR-03, FR-08` | **PASS** |
| **TC-05** | Verify ML baseline, DL autoencoder, and isolated QML tracking | `FR-05, 06, 07` | **PASS** |
| **TC-06** | Verify measured accuracy is reported UNAVAILABLE when labels are absent | `FR-04` | **PASS** |
| **TC-07** | Verify promotion without validation is strictly blocked | `FR-10, NFR-10` | **PASS** |
| **TC-08** | Verify simulated post-promotion failure restores stable model | `FR-12` | **PASS** |
| **TC-09** | Verify throughput scaling for 1,000+ events and P95 latency < 500ms | `NFR-01, NFR-09` | **PASS** |
| **TC-10** | Verify analyzer fault injection does not crash prediction API | `NFR-02` | **PASS** |
| **TC-11** | Verify 401 unauthenticated and 403 viewer role enforcement | `FR-14, SR-01, 02` | **PASS** |
| **TC-12** | Verify audit log records actor, timestamp, version, and integrity hash | `FR-11, SR-05` | **PASS** |
| **TC-13** | Verify oversized (>5MB) and out-of-range payloads are rejected | `SR-04` | **PASS** |
| **TC-14** | Verify API keys and secrets are never leaked in error traces | `SR-03, NFR-11` | **PASS** |
| **TC-15** | Verify Dockerfile container configuration and compose healthcheck | `NFR-05, NFR-06` | **PASS** |
| **TC-16** | Verify exact reproducibility of metrics with fixed random seed | `NFR-04` | **PASS** |
| **TC-17** | Verify admin endpoints deny unauthenticated network access | `SR-06` | **PASS** |
| **TC-18** | Verify candidate regression gate blocks underperforming models | `FR-10, NFR-10` | **PASS** |

---

## 6. Conclusion
The Self-Monitoring MLOps System satisfies all criteria of the Software Engineering Mini-Project Deliverables Part-1 and Part-2. The codebase exhibits strict modularity, high performance, robust automated testing, clear contributor attribution across all three teammates, and a frozen, reproducible release.
