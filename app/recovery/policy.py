from typing import Dict, Any, Tuple
from app.config import settings

class RecoveryPolicyEngine:
    """
    Automated Recovery & Promotion Policy Engine.
    Conforms to FR-09, FR-10, FR-12, NFR-10, TC-07, TC-08, TC-18.
    """
    def __init__(
        self,
        error_rate_threshold: float = settings.ERROR_RATE_ALERT_THRESHOLD,
        auto_retrain_enabled: bool = settings.AUTO_RETRAIN_ENABLED
    ):
        self.error_rate_threshold = error_rate_threshold
        self.auto_retrain_enabled = auto_retrain_enabled

    def evaluate_retraining_trigger(
        self,
        drift_status: str,
        error_rate: float,
        p95_latency_ms: float
    ) -> Dict[str, Any]:
        """
        Evaluate if recovery / candidate retraining is eligible.
        Conforms to FR-09.
        """
        is_drift_severe = drift_status == "DRIFT_DETECTED"
        is_error_high = error_rate >= self.error_rate_threshold
        is_latency_breached = p95_latency_ms >= settings.P95_LATENCY_ALERT_THRESHOLD_MS

        eligible = bool(self.auto_retrain_enabled and (is_drift_severe or is_error_high or is_latency_breached))
        reasons = []
        if is_drift_severe:
            reasons.append("Severe input feature drift detected.")
        if is_error_high:
            reasons.append(f"Error rate {error_rate:.4f} exceeded threshold {self.error_rate_threshold:.4f}.")
        if is_latency_breached:
            reasons.append(f"P95 latency {p95_latency_ms:.2f}ms breached SLO.")

        return {
            "retraining_eligible": eligible,
            "reasons": reasons if eligible else ["Telemetry operating within acceptable policy boundaries."],
            "policy_parameters": {
                "auto_retrain_enabled": self.auto_retrain_enabled,
                "error_rate_threshold": self.error_rate_threshold,
                "p95_latency_threshold_ms": settings.P95_LATENCY_ALERT_THRESHOLD_MS
            }
        }

    def can_promote_candidate(
        self,
        validation_status: str,
        human_approval_status: str
    ) -> Tuple[bool, str]:
        """
        Enforce dual-key gate for candidate promotion.
        Conforms to FR-10 and NFR-10:
        Candidate MUST have PASSED validation AND be APPROVED by authorized user.
        """
        if validation_status != "PASSED":
            return False, f"Promotion blocked: candidate validation status is '{validation_status}', required 'PASSED'."
        if human_approval_status != "APPROVED":
            return False, f"Promotion blocked: human approval status is '{human_approval_status}', required 'APPROVED'."
        return True, "Promotion authorized: validation gates passed and authorized approval confirmed."

    def evaluate_post_promotion_health(
        self,
        post_promotion_error_rate: float,
        post_promotion_p95_latency: float
    ) -> Tuple[bool, str]:
        """
        Evaluate post-promotion health check for rollback triggering.
        Conforms to FR-12 and TC-08.
        """
        if post_promotion_error_rate > 0.10:
            return False, f"Post-promotion failure: error rate {post_promotion_error_rate:.2f} exceeded allowable 0.10 threshold."
        if post_promotion_p95_latency > 600.0:
            return False, f"Post-promotion failure: latency {post_promotion_p95_latency:.2f}ms breached allowable 600ms boundary."
        return True, "Post-promotion health check passed."

recovery_policy = RecoveryPolicyEngine()
