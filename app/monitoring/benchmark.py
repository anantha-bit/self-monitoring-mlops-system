from typing import Dict, Any, List
import numpy as np
from app.monitoring.drift import calculate_psi, DriftAnalyzer

class DriftBenchmarkSuite:
    """
    Sensitivity and robustness benchmark suite for Kolmogorov-Smirnov and PSI estimators.
    Developed by AKASH G K (PES1UG24AM022) - Sprint 1.
    """
    def __init__(self, sample_size: int = 100):
        self.sample_size = sample_size

    def evaluate_sensitivity(self, shift_magnitudes: List[float] = [0.0, 0.5, 1.0, 2.0, 3.0]) -> List[Dict[str, Any]]:
        baseline = np.random.normal(0, 1, self.sample_size)
        results = []
        for shift in shift_magnitudes:
            shifted = np.random.normal(shift, 1, self.sample_size)
            psi = calculate_psi(baseline, shifted)
            results.append({
                "shift_magnitude_std": shift,
                "psi_score": round(psi, 4),
                "drift_indicated": psi >= 0.25
            })
        return results

drift_benchmark = DriftBenchmarkSuite()
