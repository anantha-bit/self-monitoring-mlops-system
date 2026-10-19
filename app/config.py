import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Self-Monitoring MLOps System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Security Keys
    ADMIN_API_KEY: str = "admin-secret-key-prod-demo"
    ML_ENGINEER_API_KEY: str = "engineer-secret-key-prod-demo"
    VIEWER_API_KEY: str = "viewer-secret-key-prod-demo"
    SERVICE_API_KEY: str = "service-secret-key-prod-demo"

    # Monitoring & Drift Thresholds
    DRIFT_P_VALUE_THRESHOLD: float = 0.05
    DRIFT_PSI_THRESHOLD: float = 0.25
    ERROR_RATE_ALERT_THRESHOLD: float = 0.05
    P95_LATENCY_ALERT_THRESHOLD_MS: float = 500.0

    # Recovery & Validation Gates
    MIN_ACCURACY_THRESHOLD: float = 0.80
    MAX_LATENCY_THRESHOLD_MS: float = 150.0
    AUTO_RETRAIN_ENABLED: bool = True
    REQUIRE_DUAL_APPROVAL: bool = True

    # Storage
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    DATABASE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "monitoring_store.db")
    MODEL_REGISTRY_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "models")
    AUDIT_LOG_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "audit_log.jsonl")

settings = Settings()
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.MODEL_REGISTRY_DIR, exist_ok=True)
