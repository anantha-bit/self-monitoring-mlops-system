# Software Engineering Mini-Project — Sprint 3 Documentation

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Sprint Window:** 2nd November 2026 – 6th November 2026  
**Deliverable Context:** SE Mini-Project Deliverables Part-3 (Parallel Sprint-3 & Comprehensive Testing)  
**Version:** 1.1.0 (Release `v1.1.0-sprint3`)  
**Department:** Computer Science & Engineering (AI & ML), PES University  

---

## 1. Project Team & Sprint Allocation

| Team Member Name | USN | GitHub Username | Sprint 3 Role | Story Points Delivered |
| :--- | :--- | :--- | :--- | :---: |
| **Anantha Krishna M A** | **PES1UG24AM036** | [`@anantha-bit`](https://github.com/anantha-bit) | Lead Architect, E2E Integration, Prometheus Scraping, Test Orchestration & Release Manager | **18 SP** |
| **AKASH G K** | **PES1UG24AM022** | [`@akashgkuradagi`](https://github.com/akashgkuradagi) | Drift Sensitivity Benchmarks, Continuous Health Tripwire & Resiliency Testing | **10 SP** |
| **AMIT PRASAD S G** | **PES1UG24AM033** | [`@prasadamith05-png`](https://github.com/prasadamith05-png) | DL Autoencoder Latent Attribution, SHA-256 Audit Verification & Security Hardening | **10 SP** |

- **Sprint 3 Target Velocity:** **38 Story Points**
- **Sprint 3 Completed Velocity:** **38 Story Points (100% On-Time Delivery)**
- **Cumulative Project Velocity:** **106 Story Points (Sprint 1: 34 SP + Sprint 2: 34 SP + Sprint 3: 38 SP)**

---

## 2. Sprint 3 Objectives & Deliverable Alignment

Sprint 3 was executed as a parallel activity during **2nd Nov to 6th Nov 2026** in strict accordance with **Software Engineering Mini-Project Deliverables Part-3**:

1. **Statistical Drift Sensitivity Benchmarking:** Implement an automated benchmark suite to sweep covariate shift magnitudes ($0.0\sigma$ to $3.0\sigma$) and measure empirical sensitivity curves for the Kolmogorov-Smirnov test and Population Stability Index (PSI).
2. **Latent Space Reconstruction Attribution:** Enhance the PyTorch Autoencoder to compute per-feature reconstruction errors, enabling root-cause attribution when out-of-distribution drift occurs.
3. **Continuous Health Tripwire:** Implement a telemetry tripwire that monitors consecutive inference cycles and triggers an automated rollback upon sustained anomaly thresholds without human latency.
4. **Cryptographic Audit Ledger Verification:** Implement an independent chain verifier utility that recalculates SHA-256 block hashes from genesis to detect ledger tampering.
5. **Observability & Prometheus Standards:** Build a live Prometheus exposition format scraper endpoint (`/api/v1/metrics/prometheus`) compliant with standard metrics monitoring infrastructure.
6. **Comprehensive Test Automation & Reporting:** Expand test cases from 18 to 25, achieve $\ge 85\%$ test coverage, and author the four (4) required formal test reports in `docs/`:
   - Unit Test Report (`docs/reports/UNIT_TEST_REPORT.md` / `docs/UNIT_TEST_REPORT.md`)
   - System Validation Report (`docs/reports/SYSTEM_VALIDATION_REPORT.md` / `docs/SYSTEM_VALIDATION_REPORT.md`)
   - Code Coverage Report (`docs/reports/CODE_COVERAGE_REPORT.md` / `docs/CODE_COVERAGE_REPORT.md`)
   - Branch Coverage Report (`docs/reports/BRANCH_COVERAGE_REPORT.md` / `docs/BRANCH_COVERAGE_REPORT.md`)

---

## 3. Sprint 3 Backlog & User Stories

| Story ID | Backlog Item Summary | Assignee | Story Points | Traceability | Status | Key Deliverable |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- |
| **S3-1** | Statistical Sensitivity Benchmark Suite across Stepwise Shifts | `@akashgkuradagi` | **5 SP** | FR-03, FR-04, NFR-03, TC-19 | **Done** ✅ | `app/monitoring/benchmark.py`, `tests/test_tc19_drift_sensitivity_benchmark.py` |
| **S3-2** | DL Autoencoder Latent Reconstruction Attribution Visualizer | `@prasadamith05-png` | **5 SP** | FR-06, FR-07, TC-20 | **Done** ✅ | `app/models/dl_visualizer.py`, `tests/test_tc20_dl_latent_attribution.py` |
| **S3-3** | Continuous Telemetry Health Tripwire & Automated Rollback Monitor | `@akashgkuradagi` | **5 SP** | FR-01, FR-12, NFR-02, TC-21 | **Done** ✅ | `app/recovery/health_checker.py`, `tests/test_tc21_health_tripwire.py` |
| **S3-4** | Cryptographic SHA-256 Audit Chain Verifier & Tamper Detection | `@prasadamith05-png` | **5 SP** | FR-11, SR-03, SR-05, TC-22 | **Done** ✅ | `app/security/verifier.py`, `tests/test_tc22_audit_chain_verification.py` |
| **S3-5** | End-to-End Autonomous Model Recovery, Quarantine & Gate Promotion | `@anantha-bit` | **8 SP** | FR-08, FR-09, FR-10, FR-12, TC-23 | **Done** ✅ | `tests/test_tc23_e2e_recovery_workflow.py` |
| **S3-6** | Prometheus Live Telemetry Scraper & Recovery Policy Boundary Tests | `@anantha-bit` | **5 SP** | FR-02, FR-13, NFR-01, NFR-07, TC-24, TC-25 | **Done** ✅ | `tests/test_tc24_prometheus_live_export.py`, `tests/test_tc25_recovery_policy_coverage.py` |
| **S3-7** | Deliverables Part-3 Test Execution & 4 Formal Reports Generation | Team (`@anantha-bit`, `@akashgkuradagi`, `@prasadamith05-png`) | **5 SP** | Deliverables Part-3 Mandate | **Done** ✅ | 4 Formal Test Reports in `docs/` & `docs/reports/`, updated Test Plan & Catalogue |

---

## 4. Implementation & Engineering Highlights

### 4.1 Statistical Sensitivity Benchmark Suite (`app/monitoring/benchmark.py`)
- Sweeps shift magnitudes from $0.0\sigma$ (baseline) to $3.0\sigma$ in discrete steps.
- For each step, generates controlled sample matrices ($N=300$) with deterministic seeds.
- Verifies that Population Stability Index (PSI) stays below $0.25$ under normal baseline conditions and scales monotonically above $0.25$ once shifts reach severe thresholds ($\ge 2.0\sigma$).

### 4.2 DL Autoencoder Reconstruction Attribution (`app/models/dl_visualizer.py`)
- Employs a symmetric encoder-decoder PyTorch neural network ($D_{in} \to 16 \to 8 \to 16 \to D_{out}$).
- Computes element-wise squared reconstruction residual vector:
  $$\mathbf{r}_i = (x_i - \hat{x}_i)^2$$
- Ranks covariates by mean reconstruction error, isolating the root anomalous feature responsible for out-of-distribution drift without requiring manual data inspection.

### 4.3 Continuous Health Tripwire (`app/recovery/health_checker.py`)
- Tracks consecutive telemetry anomalies and health check failures across a sliding execution window.
- Eliminates false alarms caused by isolated network hiccups while guaranteeing fast failover: if $K \ge 3$ consecutive unhealthy responses occur, automated rollback is triggered immediately.

### 4.4 Cryptographic Audit Verifier (`app/security/verifier.py`)
- Implements an independent auditor service that traverses the SHA-256 hash-chained JSON ledger:
  $$\text{Hash}_i = \text{SHA-256}(\text{Block}_i \parallel \text{Hash}_{i-1})$$
- Detects unauthorized alterations to historical candidate approval or rollback decisions, ensuring compliance with IEEE 29148 security requirement SR-05.

---

## 5. Sprint 3 Quality Assurance & Verification Results

- **Automated Test Cases Executed:** **25 / 25 Passed**
- **Test Execution Speed:** **8.46 seconds**
- **Code Coverage Achieved:** **86% Combined Line + Branch Coverage (88.8% Statement Coverage)**
- **Defects Discovered:** 0 critical, 2 resolved during implementation (test client driver pinning and benchmark sample size calibration).
- **Formal Reports Uploaded to `docs/`:**
  1. `docs/reports/UNIT_TEST_REPORT.md` and `docs/UNIT_TEST_REPORT.md`
  2. `docs/reports/SYSTEM_VALIDATION_REPORT.md` and `docs/SYSTEM_VALIDATION_REPORT.md`
  3. `docs/reports/CODE_COVERAGE_REPORT.md` and `docs/CODE_COVERAGE_REPORT.md`
  4. `docs/reports/BRANCH_COVERAGE_REPORT.md` and `docs/BRANCH_COVERAGE_REPORT.md`

---

## 6. Sprint Retrospective

### What Went Well
- **Parallel Execution:** Development of Sprint-3 features and automated testing proceeded seamlessly in parallel, meeting all Part-3 deliverable deadlines.
- **Collaborative Contribution:** Clear division of responsibilities across Anantha Krishna, AKASH G K, and AMIT PRASAD S G with documented commit traces.
- **High Test Quality:** 25 automated test cases executed within 8.5 seconds with 86% coverage, exceeding the project's 80% threshold.

### Lessons Learned & Optimizations
- **Statistical Benchmark Calibration:** Synthetic drift benchmarks require a standardized sample size ($N \ge 300$) and explicit per-step random seed initialization to avoid small-sample binning noise in PSI calculations.
- **Decoupled Verification:** Isolating the cryptographic audit verifier into a standalone utility allowed rapid verification without slowing down production API inference loops.

---

## 7. Definition of Done (DoD) & Release Sign-Off

The Sprint-3 deliverable package has met all Definition of Done criteria:
- [x] All 7 Sprint-3 user stories implemented and reviewed.
- [x] All 25 test cases passing locally and on GitHub Actions CI.
- [x] Code coverage exceeds 80% threshold (86% achieved).
- [x] Four formal test reports generated and committed to `docs/`.
- [x] Test Case Catalogue and Test Plan documents updated.
- [x] Git commits distributed across all three team members.
- [x] Release tagged as `v1.1.0-sprint3`.

**Signed and Certified:**
- **Anantha Krishna M A** (PES1UG24AM036) — Lead Developer & Scrum Lead  
- **AKASH G K** (PES1UG24AM022) — Monitoring & Drift Systems Engineer  
- **AMIT PRASAD S G** (PES1UG24AM033) — Security & Model Quality Engineer  
Date: **6 November 2026**

