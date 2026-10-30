import pytest
import numpy as np
from app.models.dl_monitor import dl_monitor
from app.models.dl_visualizer import latent_analyzer

def test_tc20_dl_latent_attribution():
    """
    TC-20: Verify Deep Learning Autoencoder per-feature reconstruction error attribution.
    Traceability: FR-06.
    """
    # Baseline train if not yet initialized
    normal_data = np.random.normal(0, 1, (50, 6))
    if dl_monitor.model is None:
        dl_monitor.train_sequence_anomaly_model(normal_data, epochs=5)

    sample = np.zeros(6)
    errors = latent_analyzer.compute_feature_reconstruction_errors(sample)
    assert len(errors) == 6
    for i in range(6):
        assert f"feat_{i}" in errors
        assert isinstance(errors[f"feat_{i}"], float)
