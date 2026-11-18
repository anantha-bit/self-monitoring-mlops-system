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

    def ensure_model_ready(self):
        """Ensure autoencoder model weights are loaded and ready for inference."""
        if self.model is None:
            artifact_path = os.path.join(settings.MODEL_REGISTRY_DIR, f"dl_autoencoder_{self.version}.pt")
            if os.path.exists(artifact_path):
                try:
                    self.model = TemporalSequenceAutoencoder(input_dim=self.input_dim)
                    self.model.load_state_dict(torch.load(artifact_path, map_location=torch.device('cpu')))
                    self.model.eval()
                    from app.models.ml_monitor import ml_monitor
                    if not ml_monitor.reference_data:
                        ml_monitor.train_baseline()
                    train_matrix = np.column_stack(list(ml_monitor.reference_data.values()))
                    with torch.no_grad():
                        t_data = torch.tensor(train_matrix, dtype=torch.float32)
                        rec = self.model(t_data)
                        sample_errors = torch.mean((rec - t_data) ** 2, dim=1).numpy()
                        self.anomaly_threshold = float(np.percentile(sample_errors, 95) * 1.5)
                    return
                except Exception:
                    pass
            from app.models.ml_monitor import ml_monitor
            if not ml_monitor.reference_data:
                ml_monitor.train_baseline()
            train_matrix = np.column_stack(list(ml_monitor.reference_data.values()))
            self.train_sequence_anomaly_model(train_matrix, epochs=20)

    def score_sample(self, sample: np.ndarray) -> Dict[str, Any]:
        """
        Score a single sample vector: returns reconstructed vector, 2D latent coordinates,
        per-feature reconstruction errors, MSE, and anomaly classification.
        """
        self.ensure_model_ready()
        self.model.eval()
        with torch.no_grad():
            tensor = torch.tensor(sample.reshape(1, -1), dtype=torch.float32)
            encoded = self.model.encoder(tensor)
            reconstructed = self.model.decoder(encoded)
            recon_np = reconstructed.squeeze().numpy()
            sample_np = sample.flatten()
            feature_errors = (recon_np - sample_np) ** 2
            mse = float(np.mean(feature_errors))
            is_anomaly = bool(mse > self.anomaly_threshold)
            return {
                "reconstructed": [round(float(v), 4) for v in recon_np],
                "latent_2d": [round(float(v), 4) for v in encoded.squeeze().numpy()],
                "feature_errors": [round(float(v), 4) for v in feature_errors],
                "reconstruction_error": round(mse, 4),
                "anomaly_threshold": round(self.anomaly_threshold, 4),
                "is_anomaly": is_anomaly,
                "anomaly_score": round(mse / (self.anomaly_threshold if self.anomaly_threshold > 0 else 1.0), 4)
            }

dl_monitor = DeepLearningMonitor()
