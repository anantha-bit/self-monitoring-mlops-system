from typing import Dict, Any, Tuple
from app.recovery.policy import recovery_policy

class ContinuousHealthTripwire:
    """
    Automated continuous health monitor and tripwire for instant emergency rollback.
    Developed by AKASH G K (PES1UG24AM022) - Sprint 2.
    """
    def __init__(self, max_consecutive_failures: int = 3):
        self.max_failures = max_consecutive_failures
        self.consecutive_failures = 0

    def check_telemetry(self, error_rate: float, p95_latency: float) -> Tuple[bool, str]:
        healthy, reason = recovery_policy.evaluate_post_promotion_health(error_rate, p95_latency)
        if not healthy:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.max_failures:
                return False, f"TRIPWIRE_ACTIVATED: {self.consecutive_failures} consecutive failures. {reason}"
        else:
            self.consecutive_failures = 0
        return True, "Health checks operating normally."

health_tripwire = ContinuousHealthTripwire()
