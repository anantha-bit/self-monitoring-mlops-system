# Software Engineering Mini-Project — Deliverables Part-3
# System Validation Report

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Document ID:** `DOC-REP-SVR-001`  
**Version:** `1.1.0`  
**Course:** Software Engineering Mini-Project (SE Mini-Project Deliverables Part-3)  
**Execution Date:** 6 November 2026  

---

### Team Members & Contributions
| Team Member Name | USN | GitHub Username | Role & System Validation Responsibilities |
| :--- | :--- | :--- | :--- |
| **Anantha Krishna M A** | **PES1UG24AM036** | [`@anantha-bit`](https://github.com/anantha-bit) | Lead Architect & Evaluator; API, Core Telemetry, Validation Gates & Rollback Scenarios |
| **AKASH G K** | **PES1UG24AM022** | [`@akashgkuradagi`](https://github.com/akashgkuradagi) | Drift Specialist; KS-Test & PSI Sensitivity, Worker Isolation & Containerization Smoke |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [`@prasadamith05-png`](https://github.com/prasadamith05-png) | Security & Deep Learning Lead; Autoencoder, Quantum Benchmarks, RBAC & SHA-256 Audit |

---

## 1. Executive Summary

This **System Validation Report** presents the formal validation of the *Self-Monitoring MLOps System* against its complete system specification, comprising **14 Functional Requirements (FR-01 to FR-14)**, **11 Non-Functional Requirements (NFR-01 to NFR-11)**, and **6 Security Requirements (SR-01 to SR-06)**.

Validation was conducted using black-box system evaluation, simulated operational stress scenarios, and automated Pytest harnesses.

### System Verification Summary
| Verification Scope | Total Requirements | Verified & Compliant | Verification Pass Rate |
| :--- | :---: | :---: | :---: |
| **Functional Requirements (FR)** | **14** | **14** | **100%** ✅ |
| **Non-Functional Requirements (NFR)** | **11** | **11** | **100%** ✅ |
| **Security Requirements (SR)** | **6** | **6** | **100%** ✅ |
| **End-to-End Operational Scenarios** | **5** | **5** | **100%** ✅ |

---

## 2. Requirements Compliance Matrix

| Requirement ID | Specification Summary | Validation Evidence | Result |
| :---: | :--- | :--- | :---: |
| **FR-01** | Microservice Health & Uptime Status | Verified via `GET /health` returning HTTP 200 and uptime timestamp (TC-01). | **PASSED** ✅ |
| **FR-02** | Prometheus Metric Ingestion & Exposition | Latency histogram and prediction counters exposed conforming to Prometheus text format (TC-02). | **PASSED** ✅ |
| **FR-03** | Two-Sample Statistical Drift Detection | Two-sample Kolmogorov-Smirnov test and Population Stability Index (PSI) computed on sliding windows (TC-03, TC-04). | **PASSED** ✅ |
| **FR-04** | Operation in Absence of Ground-Truth Labels | Drift computed entirely on input feature distribution without requiring delayed labels (TC-06). | **PASSED** ✅ |
| **FR-05** | Classical ML Experiment Tracking | Baseline Scikit-Learn Random Forest models tracked with deterministic evaluation (TC-05, TC-16). | **PASSED** ✅ |
| **FR-06** | Deep Learning Autoencoder Anomaly Scoring | PyTorch sequence autoencoder detects reconstruction loss anomalies on shifted sequences (TC-05). | **PASSED** ✅ |
| **FR-07** | Quantum ML (QML) Circuit Simulation Benchmark | Parameterized 4-qubit variational circuit simulated via statevector backend (TC-05). | **PASSED** ✅ |
| **FR-08** | Drift Alert Propagation & Recovery Trigger | Exceeding PSI >= 0.25 triggers automated quarantine and retraining workflow (TC-04). | **PASSED** ✅ |
| **FR-09** | Automated Validation Gatekeeper | Candidate models evaluated against accuracy (>= 0.85) and latency constraints (TC-07, TC-18). | **PASSED** ✅ |
| **FR-10** | Dual-Key Candidate Model Promotion | Administrative promotion strictly requires dual authorization keys (TC-07, TC-11). | **PASSED** ✅ |
| **FR-11** | Cryptographic Audit Log Ledger | All administrative actions chained with SHA-256 block hashes (TC-12). | **PASSED** ✅ |
| **FR-12** | Automated Emergency Model Rollback | Substandard candidate triggers immediate rollback to stable baseline version (TC-08). | **PASSED** ✅ |
| **FR-13** | Web UI Dashboard Telemetry Route | Real-time monitoring metrics and drift indicators exposed for visualization (TC-01, TC-02). | **PASSED** ✅ |
| **FR-14** | Role-Based Access Control on Administrative Surfaces | Unauthorized API keys rejected with HTTP 401/403 (TC-11, TC-17). | **PASSED** ✅ |

---

## 3. Operational Scenario Validation

1. **Scenario 1 — Normal Traffic Steady State:** 1,000 requests served at 18.4 ms mean latency; drift metrics remain PSI < 0.05.
2. **Scenario 2 — Abrupt Concept Drift & Recovery:** Synthetic shift injected; drift engine triggers alert within 2 evaluation cycles; candidate retrained and verified.
3. **Scenario 3 — Regression Quality Gate Block:** Degraded model candidate injected; gatekeeper rejects promotion with reason logged in audit trail.
4. **Scenario 4 — Worker Crash Isolation:** Monitoring thread exception injected; inference serving continues without downtime (TC-10).
5. **Scenario 5 — Security & Credential Leakage Guard:** Malformed and oversized requests rejected; environment variables and secret keys redacted (TC-13, TC-14).

---

## 4. Final System Sign-Off

The *Self-Monitoring MLOps System* meets all functional, non-functional, and security specifications. The system is certified complete, production-ready, and compliant with all SE Mini-Project Deliverables.
