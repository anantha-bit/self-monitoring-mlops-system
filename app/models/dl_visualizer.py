from typing import Dict, Any, List
import numpy as np
import torch
from app.models.dl_monitor import dl_monitor

class AutoencoderLatentAnalyzer:
    """
    Latent space representation and reconstruction error attribution module.
    Developed by AMIT PRASAD S G (PES1UG24AM033) - Sprint 1.
    """
    def __init__(self):
        pass

    def compute_feature_reconstruction_errors(self, sample: np.ndarray) -> Dict[str, float]:
        """Compute per-feature reconstruction error to identify which feature drives the anomaly."""
        if dl_monitor.model is None:
            return {f"feature_{i}": 0.01 for i in range(len(sample))}

        dl_monitor.model.eval()
        with torch.no_grad():
            tensor = torch.tensor(sample.reshape(1, -1), dtype=torch.float32)
            recon = dl_monitor.model(tensor)
            diff = (recon - tensor).squeeze().numpy() ** 2
            return {f"feat_{i}": round(float(diff[i]), 4) for i in range(len(diff))}

latent_analyzer = AutoencoderLatentAnalyzer()
