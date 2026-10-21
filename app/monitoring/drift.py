import uuid
import time
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from scipy import stats
from app.config import settings

def calculate_psi(expected: np.ndarray, actual: np.ndarray, num_bins: int = 10) -> float:
    """
    Compute Population Stability Index (PSI) between reference and current distribution.
    """
    if len(expected) == 0 or len(actual) == 0:
        return 0.0

    # Create uniform quantile bins based on reference distribution
    percentiles = np.linspace(0, 100, num_bins + 1)
    bin_edges = np.percentile(expected, percentiles)
    bin_edges[0] -= 1e-5
    bin_edges[-1] += 1e-5
    bin_edges = np.unique(bin_edges)

    if len(bin_edges) < 2:
        return 0.0

    expected_counts, _ = np.histogram(expected, bins=bin_edges)
    actual_counts, _ = np.histogram(actual, bins=bin_edges)

    # Normalize fractions with small epsilon to prevent div by zero
    eps = 1e-4
    expected_pct = (expected_counts + eps) / (np.sum(expected_counts) + eps * len(expected_counts))
    actual_pct = (actual_counts + eps) / (np.sum(actual_counts) + eps * len(actual_counts))

    psi_value = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return float(max(0.0, psi_value))

class DriftAnalyzer:
    def __init__(
        self,
        p_value_threshold: float = settings.DRIFT_P_VALUE_THRESHOLD,
        psi_threshold: float = settings.DRIFT_PSI_THRESHOLD
    ):
        self.p_value_threshold = p_value_threshold
        self.psi_threshold = psi_threshold
        self.reference_data: Dict[str, np.ndarray] = {}
        self.active_alerts: List[Dict[str, Any]] = []

    def set_reference_data(self, reference_dict: Dict[str, np.ndarray]):
        """Register the baseline reference distribution."""
        self.reference_data = {k: np.array(v, dtype=float) for k, v in reference_dict.items()}

    def compare_windows(
        self,
        current_data: Dict[str, np.ndarray],
        ground_truth_labels: Optional[np.ndarray] = None,
        predictions: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Compare current data window against reference distribution.
        Conforms to FR-03, FR-04, FR-08, TC-03, TC-04, TC-06.
        """
        if not self.reference_data:
            return {
                "status": "ERROR",
                "message": "Reference data not initialized.",
                "drift_detected": False,
                "drift_status": "NO_DRIFT",
                "features": {}
            }

        feature_reports: Dict[str, Any] = {}
        drift_detected_count = 0
        warning_count = 0

        for col, ref_values in self.reference_data.items():
            if col not in current_data:
                continue

            curr_values = np.array(current_data[col], dtype=float)
            if len(curr_values) < 5 or len(ref_values) < 5:
                continue

            # 1. Kolmogorov-Smirnov Test
            ks_stat, ks_p_val = stats.ks_2samp(ref_values, curr_values)
            
            # 2. Population Stability Index
            psi_val = calculate_psi(ref_values, curr_values)

            # Determine feature-level drift
            is_ks_drift = bool(ks_p_val < self.p_value_threshold)
            is_psi_drift = bool(psi_val >= self.psi_threshold)
            is_warning = bool(psi_val >= 0.10 or ks_p_val < 0.10)

            if is_ks_drift or is_psi_drift:
                feat_status = "DRIFT_DETECTED"
                drift_detected_count += 1
            elif is_warning:
                feat_status = "DRIFT_WARNING"
                warning_count += 1
            else:
                feat_status = "NO_DRIFT"

            feature_reports[col] = {
                "ks_statistic": round(float(ks_stat), 4),
                "ks_p_value": round(float(ks_p_val), 6),
                "psi_score": round(float(psi_val), 4),
                "status": feat_status,
                "reference_mean": round(float(np.mean(ref_values)), 4),
                "current_mean": round(float(np.mean(curr_values)), 4),
                "reference_std": round(float(np.std(ref_values)), 4),
                "current_std": round(float(np.std(curr_values)), 4)
            }

        # Overall drift status
        if drift_detected_count > 0:
            overall_status = "DRIFT_DETECTED"
            overall_drift = True
        elif warning_count > 0:
            overall_status = "DRIFT_WARNING"
            overall_drift = False
        else:
            overall_status = "NO_DRIFT"
            overall_drift = False

        # Ground-truth evaluation (FR-04)
        accuracy_info: Dict[str, Any] = {
            "ground_truth_status": "AVAILABLE" if ground_truth_labels is not None else "UNAVAILABLE",
            "measured_accuracy": None
        }
        if ground_truth_labels is not None and predictions is not None:
            if len(ground_truth_labels) == len(predictions) and len(predictions) > 0:
                acc = float(np.mean(np.array(ground_truth_labels) == np.array(predictions)))
                accuracy_info["measured_accuracy"] = round(acc, 4)

        # Trigger Alerts if threshold exceeded (FR-08)
        new_alerts = []
        if overall_drift:
            alert = {
                "alert_id": f"alt-{uuid.uuid4().hex[:8]}",
                "metric": "INPUT_DATA_DRIFT",
                "severity": "CRITICAL" if drift_detected_count >= 2 else "WARNING",
                "observed_value": f"{drift_detected_count} features drifted",
                "status": "OPEN",
                "timestamp": time.time(),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "message": f"Statistically significant drift observed across {drift_detected_count} features."
            }
            self.active_alerts.append(alert)
            new_alerts.append(alert)

        return {
            "drift_status": overall_status,
            "drift_detected": overall_drift,
            "drifted_features_count": drift_detected_count,
            "warning_features_count": warning_count,
            "feature_metrics": feature_reports,
            "evaluation": accuracy_info,
            "new_alerts": new_alerts
        }

    def get_alerts(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if status_filter:
            return [a for a in self.active_alerts if a["status"] == status_filter]
        return self.active_alerts

drift_analyzer = DriftAnalyzer()
