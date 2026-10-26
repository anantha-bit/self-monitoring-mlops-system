import time
from typing import Dict, Any, List, Optional
from app.recovery.policy import recovery_policy
from app.recovery.validator import validator
from app.security.audit import audit_logger

class ModelRegistryAdapter:
    """
    Model Registry Adapter supporting MLflow-compatible metadata and lifecycle states.
    Conforms to FR-09, FR-10, FR-12, TC-07, TC-08, TC-18.
    """
    def __init__(self):
        self.active_version = "v1.0.0"
        self.last_stable_version = "v1.0.0"
        self.stable_metrics = {
            "accuracy": 0.9231,
            "precision": 0.9125,
            "recall": 0.9412,
            "f1_score": 0.9266,
            "latency_p95_ms": 42.5
        }
        self.candidates: Dict[str, Dict[str, Any]] = {}

    def register_candidate(
        self,
        candidate_id: str,
        model_type: str,
        metrics: Dict[str, Any],
        artifact_path: str,
        author: str
    ) -> Dict[str, Any]:
        candidate_record = {
            "candidate_id": candidate_id,
            "model_type": model_type,
            "metrics": metrics,
            "artifact_path": artifact_path,
            "registered_by": author,
            "registered_at": time.time(),
            "validation_status": "PENDING",
            "validation_report": None,
            "approval_status": "PENDING",
            "lifecycle_state": "REGISTERED"
        }
        self.candidates[candidate_id] = candidate_record
        return candidate_record

    def validate_candidate(self, candidate_id: str) -> Dict[str, Any]:
        if candidate_id not in self.candidates:
            raise KeyError(f"Candidate '{candidate_id}' not found.")

        cand = self.candidates[candidate_id]
        report = validator.validate_candidate(cand["metrics"], self.stable_metrics)
        cand["validation_status"] = report["validation_status"]
        cand["validation_report"] = report
        cand["lifecycle_state"] = "VALIDATED" if report["all_gates_passed"] else "VALIDATION_FAILED"
        return report

    def record_decision(
        self,
        candidate_id: str,
        decision: str,
        actor: str,
        comment: str = ""
    ) -> Dict[str, Any]:
        """
        Record approval or rejection decision.
        Conforms to FR-10, FR-14, TC-11.
        """
        if candidate_id not in self.candidates:
            raise KeyError(f"Candidate '{candidate_id}' not found.")

        cand = self.candidates[candidate_id]
        decision_upper = decision.upper()

        if decision_upper not in ["APPROVED", "REJECTED"]:
            raise ValueError("Decision must be either 'APPROVED' or 'REJECTED'.")

        cand["approval_status"] = decision_upper
        cand["decision_by"] = actor
        cand["decision_comment"] = comment

        # If approved, evaluate promotion gate
        if decision_upper == "APPROVED":
            can_promote, reason = recovery_policy.can_promote_candidate(
                validation_status=cand["validation_status"],
                human_approval_status=cand["approval_status"]
            )
            if can_promote:
                # Promote candidate to active
                old_active = self.active_version
                self.last_stable_version = old_active
                self.active_version = candidate_id
                self.stable_metrics = cand["metrics"]
                cand["lifecycle_state"] = "PROMOTED"

                audit_logger.record_event(
                    actor=actor,
                    action="CANDIDATE_PROMOTED",
                    target_version=candidate_id,
                    outcome="SUCCESS",
                    details={
                        "previous_version": old_active,
                        "metrics": cand["metrics"],
                        "comment": comment
                    }
                )
                return {
                    "status": "PROMOTED",
                    "active_version": self.active_version,
                    "previous_version": old_active,
                    "message": "Candidate successfully promoted to production active version."
                }
            else:
                cand["lifecycle_state"] = "PROMOTION_BLOCKED"
                audit_logger.record_event(
                    actor=actor,
                    action="PROMOTION_ATTEMPT_DENIED",
                    target_version=candidate_id,
                    outcome="BLOCKED",
                    details={"reason": reason, "comment": comment}
                )
                return {
                    "status": "BLOCKED",
                    "active_version": self.active_version,
                    "message": reason
                }
        else:
            cand["lifecycle_state"] = "REJECTED"
            audit_logger.record_event(
                actor=actor,
                action="CANDIDATE_REJECTED",
                target_version=candidate_id,
                outcome="REJECTED",
                details={"comment": comment}
            )
            return {
                "status": "REJECTED",
                "active_version": self.active_version,
                "message": f"Candidate '{candidate_id}' was rejected by {actor}."
            }

    def rollback(self, actor: str, reason: str) -> Dict[str, Any]:
        """
        Rollback to last known stable model.
        Conforms to FR-12 and TC-08.
        """
        previous_active = self.active_version
        target_version = self.last_stable_version

        self.active_version = target_version
        audit_record = audit_logger.record_event(
            actor=actor,
            action="MODEL_ROLLBACK",
            target_version=target_version,
            outcome="SUCCESS",
            details={
                "rolled_back_from": previous_active,
                "restored_version": target_version,
                "reason": reason
            }
        )
        return {
            "status": "ROLLED_BACK",
            "active_version": self.active_version,
            "rolled_back_from": previous_active,
            "audit_event_id": audit_record["event_id"],
            "reason": reason
        }

    def list_candidates(self) -> List[Dict[str, Any]]:
        return list(self.candidates.values())

model_registry = ModelRegistryAdapter()
