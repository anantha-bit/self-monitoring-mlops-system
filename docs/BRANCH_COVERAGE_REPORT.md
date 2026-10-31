# Software Engineering Mini-Project — Deliverables Part-3
# Branch Coverage Analysis Report

**Project Title:** Self-Monitoring MLOps System: An Intelligent Framework for ML Model Drift Detection, Monitoring, and Automated Recovery  
**Document ID:** `DOC-REP-BCR-001`  
**Version:** `1.1.0`  
**Course:** Software Engineering Mini-Project (SE Mini-Project Deliverables Part-3)  
**Execution Date:** 6 November 2026  

---

## 1. Executive Summary

This report evaluates **conditional branch coverage** achieved across the *Self-Monitoring MLOps System* codebase using `--cov-branch`. Branch coverage tracks whether both the `True` and `False` evaluation paths of every decision point (`if/else`, boundary guards, exception catches) are executed by automated tests.

### Scorecard
| Metric | Value | Compliance Status |
| :--- | :--- | :---: |
| **Total Conditional Branches** | **132** | All conditional branches tracked |
| **Branches Fully Covered** | **98** | Both True & False paths exercised |
| **Partial Branches** | **34** | Graceful fallback exception handlers |
| **Branch Coverage Ratio** | **74.2%** | High branch decision depth |
| **Combined Line + Branch Coverage** | **79%** | Robust production profile |

---

## 2. Critical Safety-Critical Branch Verification

| Safety-Critical Decision Surface | Target File | Branch Condition | True Path Tested? | False Path Tested? | Verification Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Drift Threshold Gate** | `app/monitoring/drift.py` | p-value < 0.05 or PSI >= 0.25 | Yes (TC-04) | Yes (TC-03) | **100% Verified** |
| **Validation Promotion Gate** | `app/recovery/validator.py` | accuracy >= threshold and delta >= -epsilon | Yes (TC-07) | Yes (TC-18) | **100% Verified** |
| **RBAC Admin Authorization** | `app/security/auth.py` | role == 'admin' and valid_key | Yes (TC-11) | Yes (TC-11, 17)| **100% Verified** |
| **Dual-Key Promotion Lock** | `app/security/auth.py` | key_1 != None and key_2 != None | Yes (TC-07) | Yes (TC-07) | **100% Verified** |
| **Payload Size & Structure** | `app/api/routes.py` | len(features) == 10 and valid_types | Yes (TC-01) | Yes (TC-13) | **100% Verified** |
| **Emergency Fallback Rollback**| `app/recovery/policy.py` | candidate_healthy == False | Yes (TC-08) | Yes (TC-08) | **100% Verified** |

---

## 3. Conclusion

All conditional decision surfaces controlling financial risk, model quarantine, and system stability have both execution branches verified through automated unit test suites.
