import os
import time
from typing import Dict, Any, List, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from app.config import settings

class TemporalSequenceAutoencoder(nn.Module):
    """
    PyTorch Autoencoder for detecting anomalies in sequence telemetry.
    Conforms to FR-06 and TC-05.
    """
    def __init__(self, input_dim: int = 6, hidden_dim: int = 3):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class DeepLearningMonitor:
    def __init__(self, input_dim: int = 6, random_seed: int = 42):
        self.input_dim = input_dim
        self.random_seed = random_seed
        self.model: Optional[TemporalSequenceAutoencoder] = None
        self.anomaly_threshold: float = 0.5
        self.version: str = "dl-seq-ae-v1.0"

    def train_sequence_anomaly_model(
        self,
        training_data: np.ndarray,
        epochs: int = 30,
        lr: float = 0.01
    ) -> Dict[str, Any]:
        """
        Train temporal sequence autoencoder on normal baseline data.
        """
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)

        self.model = TemporalSequenceAutoencoder(input_dim=self.input_dim)
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        tensor_data = torch.tensor(training_data, dtype=torch.float32)

        self.model.train()
        losses = []
        for epoch in range(epochs):
            optimizer.zero_grad()
            reconstructed = self.model(tensor_data)
            loss = criterion(reconstructed, tensor_data)
            loss.backward()
            optimizer.step()
            losses.append(float(loss.item()))

        # Evaluate threshold on baseline
        self.model.eval()
        with torch.no_grad():
            reconstructed = self.model(tensor_data)
            sample_errors = torch.mean((reconstructed - tensor_data) ** 2, dim=1).numpy()
            self.anomaly_threshold = float(np.percentile(sample_errors, 95) * 1.5)

        artifact_path = os.path.join(settings.MODEL_REGISTRY_DIR, f"dl_autoencoder_{self.version}.pt")
        torch.save(self.model.state_dict(), artifact_path)

        metadata = {
            "model_type": "DeepLearning_Autoencoder",
            "model_version": self.version,
            "architecture": "MLP-Autoencoder [6 -> 3 -> 2 -> 3 -> 6]",
            "epochs": epochs,
            "learning_rate": lr,
            "final_train_loss": round(losses[-1], 6),
            "anomaly_threshold": round(self.anomaly_threshold, 4),
            "random_seed": self.random_seed,
            "environment": {
                "pytorch_version": torch.__version__
            },
            "artifact_path": artifact_path,
            "timestamp": time.time()
        }
        return metadata

    def score_window(self, window_data: np.ndarray) -> Dict[str, Any]:
        """
        Score a window of samples: calculate reconstruction loss and flag anomalies.
        """
        if self.model is None:
            # Fallback mock scoring if not yet trained
            return {"mean_reconstruction_error": 0.05, "anomaly_rate": 0.0}

        self.model.eval()
        with torch.no_grad():
            tensor_data = torch.tensor(window_data, dtype=torch.float32)
            reconstructed = self.model(tensor_data)
            errors = torch.mean((reconstructed - tensor_data) ** 2, dim=1).numpy()
            anomalies = errors > self.anomaly_threshold
            anomaly_rate = float(np.mean(anomalies))

            return {
                "mean_reconstruction_error": round(float(np.mean(errors)), 4),
                "max_reconstruction_error": round(float(np.max(errors)), 4),
                "anomaly_rate": round(anomaly_rate, 4),
                "anomaly_count": int(np.sum(anomalies)),
                "threshold": round(self.anomaly_threshold, 4)
            }

dl_monitor = DeepLearningMonitor()
