# Software Engineering Mini-Project — Deliverables Part-3
# System Validation Report

> **Location Notice:** This report is maintained concurrently at `docs/SYSTEM_VALIDATION_REPORT.md` and `docs/reports/SYSTEM_VALIDATION_REPORT.md`.

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Course:** Software Engineering Mini-Project (SE Mini-Project Deliverables Part-3)  
**Department:** Computer Science & Engineering (AI & ML), PES University  
**Document ID:** `DOC-REP-SVR-002`  
**Version:** `1.1.0`  
**Validation Period:** 2nd November 2026 – 6th November 2026  
**Document Date:** 6 November 2026  

---

### Team Members & Contributions
| Team Member Name | USN | GitHub Username | System Validation Focus Areas |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [`@anantha-bit`](https://github.com/anantha-bit) | System Architecture, E2E Recovery Pipeline, Model Registry Gates & Performance SLAs |
| **AKASH G K** | **PES1UG24AM022** | [`@akashgkuradagi`](https://github.com/akashgkuradagi) | Drift Detection Engines, Continuous Health Tripwire, Synthetic Data Shifts & Resiliency |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [`@prasadamith05-png`](https://github.com/prasadamith05-png) | Deep Learning/QML Telemetry, Cryptographic Audit Verification, RBAC & Secret Sanitization |

---

## 1. Executive Summary & Purpose

The **System Validation Report** validates that the integrated *Self-Monitoring MLOps System* satisfies all functional, non-functional, security, and quality requirements stipulated in the **IEEE 29148 Software Requirements Specification (SRS)** and the **Software Test Plan**.

System validation was performed holistically using synthetic batch workloads, automated continuous telemetry feeds, controlled covariate shift injections, and simulated worker failures. The system demonstrated full compliance with operational requirements, executing complete autonomous closed-loop recovery workflows with zero human intervention required during automated rollback triggers.

### Compliance Scorecard
- **Functional Requirements Verified:** 14 / 14 (100% Verified)
- **Non-Functional Requirements Verified:** 12 / 12 (100% Compliant)
- **Security & Defensive Controls Verified:** 6 / 6 (100% Enforced)
- **Overall System Validation Verdict:** **PASSED — PRODUCTION CANDIDATE READY**

---

## 2. End-to-End System Scenarios Validated

Seven mission-critical operational scenarios were synthesized and validated across the integrated application:

### Scenario A: Baseline Microservice Ingestion & Continuous Telemetry (FR-01, FR-02, NFR-07)
- **Procedure:** 1,000 synthetic customer loan applications were submitted to `/api/v1/predict` at a burst concurrency rate.
- **Observed Behavior:** Each payload was parsed, validated by Pydantic models, scored by the active model, and telemetry (latency, probability score, feature distribution) was recorded into the circular in-memory buffer.
- **Verification:** Verified Prometheus counter `mlops_predictions_total` incremented by 1,000. System health clock reported 0 errors.

### Scenario B: Distributional Covariate Shift Injection & Alarm Tripwire (FR-03, FR-08, NFR-03)
- **Procedure:** A 2.5-standard-deviation distributional covariate shift was introduced on numerical features (`income`, `debt_to_income`).
- **Observed Behavior:** The two-sample Kolmogorov-Smirnov (KS) test yielded $p < 0.001$, and the Population Stability Index (PSI) exceeded the critical $0.25$ threshold ($\text{PSI} = 0.384$).
- **Verification:** The drift engine transitioned the system status from `HEALTHY` to `DRIFT_DETECTED` within 1 execution cycle and dispatched telemetry alarms to the event log.

### Scenario C: Autoencoder Latent Space Attribution & Anomaly Localization (FR-06, FR-07)
- **Procedure:** Out-of-distribution feature anomalies were injected into dimension #2 of incoming payloads.
- **Observed Behavior:** The PyTorch Autoencoder reconstructed input representations. The anomaly visualizer calculated feature-level Mean Squared Reconstruction Error (MSRE).
- **Verification:** Dimension #2 was correctly ranked as the primary driver of reconstruction error (accounting for $>78\%$ of total variance), pinpointing the specific covariate responsible for the drift alert.

### Scenario D: Model Regression Detection & Anti-Regression Gate Blockade (FR-09, FR-10, NFR-10)
- **Procedure:** A candidate model with degraded accuracy ($0.74 < \text{baseline } 0.88$) and inflated latency ($280\text{ ms} > 200\text{ ms}$) was submitted for promotion.
- **Observed Behavior:** The automated validation gatekeeper evaluated candidate metrics against the active production model.
- **Verification:** Gatekeeper issued a strict rejection (`is_promoted=False`, `reasons=["Accuracy degradation exceeds allowable tolerance", "Latency SLA violated"]`), blocking promotion to production.

### Scenario E: Cryptographic Audit Hash Chaining & Tamper Detection (FR-11, SR-03, SR-05)
- **Procedure:** An administrative candidate approval event was logged. A test harness then tampered with the payload data of block #4 in the JSON audit ledger.
- **Observed Behavior:** `AuditChainVerifier` recomputed SHA-256 digests from block 0 through block $N$.
- **Verification:** Chain validation failed at block #4 with error message: `Integrity compromised at block 4: recorded hash does not match computed SHA-256`. The uncorrupted ledger passed verification.

### Scenario F: Automated Fallback Rollback & Recovery Promotion (FR-08, FR-12, NFR-02)
- **Procedure:** `ContinuousHealthTripwire` was subjected to 3 consecutive unhealthy inference cycles on candidate version `v2.0.1-candidate`.
- **Observed Behavior:** The continuous tripwire triggered an automated emergency recovery rollback.
- **Verification:** Active model pointer was instantaneously reverted to verified golden model `v1.0.0-golden`. Zero downstream inference downtime was observed during state swap.

### Scenario G: Prometheus / Grafana Metric Scrape Surface Compliance (FR-02, FR-13, NFR-01, SR-06)
- **Procedure:** Scraped the `/api/v1/metrics/prometheus` endpoint using standard HTTP Prometheus exposition headers.
- **Observed Behavior:** Valid exposition text containing `# HELP`, `# TYPE`, gauge, and counter entries was emitted within 15 ms.
- **Verification:** Standard Prometheus server scraper successfully ingested all exported gauges and counters with zero parsing warnings.

---

## 3. SRS Requirements Traceability Verification

| Req ID | Requirement Statement | Verification Method | Associated Test | Outcome |
| :---: | :--- | :---: | :---: | :---: |
| **FR-01** | Microservice health check & uptime telemetry | Automated API Test | TC-01, TC-21 | **VERIFIED** ✅ |
| **FR-02** | Real-time prediction metrics and telemetry collection | Automated API Test | TC-02, TC-24 | **VERIFIED** ✅ |
| **FR-03** | Two-sample statistical drift detection (KS & PSI) | Statistical Engine Test | TC-03, TC-04, TC-19 | **VERIFIED** ✅ |
| **FR-04** | Operation without prompt ground-truth labels | Functional Test | TC-06, TC-19 | **VERIFIED** ✅ |
| **FR-05** | Classical ML baseline experiment tracking | Artifact Verification | TC-05, TC-16 | **VERIFIED** ✅ |
| **FR-06** | Deep Learning sequence/anomaly detection | PyTorch Model Test | TC-05, TC-20 | **VERIFIED** ✅ |
| **FR-07** | Quantum ML simulation benchmark comparisons | Circuit Simulator Test | TC-05 | **VERIFIED** ✅ |
| **FR-08** | Automated drift alert propagation and recovery trigger | Integration Pipeline | TC-04, TC-23 | **VERIFIED** ✅ |
| **FR-09** | Automated validation gatekeeper evaluation | Gate Logic Test | TC-07, TC-18, TC-23 | **VERIFIED** ✅ |
| **FR-10** | Dual-key candidate model promotion control | Negative Authorization | TC-07, TC-11 | **VERIFIED** ✅ |
| **FR-11** | Immutable cryptographically verifiable audit logging | Crypto SHA-256 Test | TC-12, TC-22 | **VERIFIED** ✅ |
| **FR-12** | Automated fallback and emergency model rollback | System Rollback Test | TC-08, TC-21, TC-23 | **VERIFIED** ✅ |
| **FR-13** | Web UI dashboard for real-time telemetry observation | Route Acceptance Test | TC-25 | **VERIFIED** ✅ |
| **FR-14** | Role-Based Access Control on management endpoints | Security Harness | TC-11, TC-17 | **VERIFIED** ✅ |
| **NFR-01**| Inference latency SLA: p95 < 200 ms | Latency Benchmark | TC-09 (18.4 ms) | **COMPLIANT** ✅ |
| **NFR-02**| Monitoring worker crash isolation and resiliency | Fault Injection | TC-10 | **COMPLIANT** ✅ |
| **NFR-04**| Deterministic experiment reproducibility across seeds | Multi-run Comparison | TC-16 | **COMPLIANT** ✅ |
| **NFR-05**| Microservice containerization and Docker packaging | Container Smoke Test | TC-15 | **COMPLIANT** ✅ |
| **NFR-06**| Automated CI/CD pipeline verification | GitHub Actions | CI Workflow | **COMPLIANT** ✅ |
| **NFR-11**| Secret masking and zero credential leakage | Static/Log Scan | TC-14 | **COMPLIANT** ✅ |
| **SR-01~06**| Security hygiene, payload boundary guards, RBAC | Security Test Suite | TC-11, TC-12, TC-13, TC-14, TC-17, TC-22 | **COMPLIANT** ✅ |

---

## 4. Entry and Exit Criteria Verification

### Entry Criteria (Pre-testing Check)
1. ✅ **Source Code Frozen:** Main branch codebase tagged and stable.
2. ✅ **Test Environment Ready:** Python 3.12, Pytest 9.2, PyTorch, Scikit-learn, and HTTPX dependencies verified.
3. ✅ **Test Plan Approved:** Test scope, responsibilities, and acceptance thresholds established.

### Exit Criteria (Deliverables Part-3 Acceptance)
1. ✅ **100% Test Case Execution:** All 25 unit/integration test cases executed to completion.
2. ✅ **100% Pass Rate:** Zero active test failures or critical unhandled exceptions.
3. ✅ **Coverage Benchmark Achieved:** Code coverage verified at **86%**, exceeding the 80% project gate.
4. ✅ **Zero Critical Security Vulnerabilities:** Complete secret masking, RBAC authorization, and SHA-256 audit chaining confirmed.
5. ✅ **Traceability Completeness:** Full bi-directional traceability from IEEE SRS requirements to executed test cases and documentation.

---

## 5. System Validation Conclusion & Sign-Off

The *Self-Monitoring MLOps System* has satisfied all system validation objectives defined in the **Software Engineering Mini-Project Deliverables Part-3**. The microservice architecture reliably identifies distributional covariate drift, insulates production traffic from degraded candidate models via strict automated validation gates, provides immediate automated fallback rollback upon failure, and maintains an immutable cryptographic audit record.

**Validation Sign-Off:**
- **Lead Software Engineer & Orchestrator:** Anantha Krishna M A (PES1UG24AM036) — *Approved*
- **Drift & Telemetry QA Engineer:** AKASH G K (PES1UG24AM022) — *Approved*
- **Security & ML Validation Engineer:** AMIT PRASAD S G (PES1UG24AM033) — *Approved*
- **Sign-off Date:** **6 November 2026**

