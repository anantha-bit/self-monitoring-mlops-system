from typing import Dict, Any, List
from app.config import settings

class CandidateValidator:
    """
    Automated Validation Service for Model Candidates.
    Conforms to FR-10, NFR-10, TC-07, TC-18.
    """
    def __init__(
        self,
        min_accuracy: float = settings.MIN_ACCURACY_THRESHOLD,
        max_latency_ms: float = settings.MAX_LATENCY_THRESHOLD_MS
    ):
        self.min_accuracy = min_accuracy
        self.max_latency_ms = max_latency_ms

    def validate_candidate(
        self,
        candidate_metrics: Dict[str, Any],
        stable_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate candidate model metrics against quality gates and stable baseline.
        """
        checks: List[Dict[str, Any]] = []
        all_passed = True

        # Gate 1: Absolute minimum accuracy
        cand_acc = candidate_metrics.get("accuracy", 0.0)
        gate1_pass = bool(cand_acc >= self.min_accuracy)
        checks.append({
            "gate": "MINIMUM_ACCURACY_THRESHOLD",
            "threshold": self.min_accuracy,
            "observed": cand_acc,
            "passed": gate1_pass,
            "message": f"Accuracy {cand_acc:.4f} vs threshold {self.min_accuracy:.4f}"
        })
        if not gate1_pass:
            all_passed = False

        # Gate 2: Latency SLO
        cand_lat = candidate_metrics.get("latency_p95_ms", 50.0)
        gate2_pass = bool(cand_lat <= self.max_latency_ms)
        checks.append({
            "gate": "MAX_LATENCY_SLO",
            "threshold": self.max_latency_ms,
            "observed": cand_lat,
            "passed": gate2_pass,
            "message": f"P95 Latency {cand_lat:.2f}ms vs SLO {self.max_latency_ms:.2f}ms"
        })
        if not gate2_pass:
            all_passed = False

        # Gate 3: Regression check vs Stable Baseline
        stable_acc = stable_metrics.get("accuracy", 0.85)
        # Regression margin allows max 0.02 drop
        min_allowed_vs_stable = stable_acc - 0.02
        gate3_pass = bool(cand_acc >= min_allowed_vs_stable)
        checks.append({
            "gate": "NO_PERFORMANCE_REGRESSION",
            "threshold": round(min_allowed_vs_stable, 4),
            "observed": cand_acc,
            "passed": gate3_pass,
            "message": f"Candidate accuracy {cand_acc:.4f} vs baseline allowable {min_allowed_vs_stable:.4f}"
        })
        if not gate3_pass:
            all_passed = False

        # Gate 4: F1 score threshold
        cand_f1 = candidate_metrics.get("f1_score", 0.75)
        gate4_pass = bool(cand_f1 >= 0.75)
        checks.append({
            "gate": "MINIMUM_F1_SCORE",
            "threshold": 0.75,
            "observed": cand_f1,
            "passed": gate4_pass,
            "message": f"F1-score {cand_f1:.4f} vs threshold 0.7500"
        })
        if not gate4_pass:
            all_passed = False

        return {
            "validation_status": "PASSED" if all_passed else "FAILED",
            "all_gates_passed": all_passed,
            "can_promote": all_passed,
            "checks": checks,
            "candidate_metrics": candidate_metrics,
            "stable_metrics": stable_metrics
        }

validator = CandidateValidator()
