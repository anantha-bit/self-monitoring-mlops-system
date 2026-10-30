# Developer Guide: Self-Monitoring MLOps System

This guide provides technical developers, testers, and evaluators with detailed documentation on the system architecture, component contracts, local setup, and extension points.

---

## 1. Directory Structure

```
├── .github/workflows/
│   ├── ci.yml                     # GitHub Actions CI (Lint, pytest TC-01~18, Docker build)
│   └── pr-automation.yml          # Automated PR labeling & checks
├── app/
│   ├── api/
│   │   └── routes.py              # REST API endpoints & route handlers
│   ├── dashboard/
│   │   └── index.html             # Real-time interactive UI dashboard
│   ├── models/
│   │   ├── ml_monitor.py          # Classical ML baseline (RandomForest)
│   │   ├── dl_monitor.py          # PyTorch Sequence Anomaly Autoencoder
│   │   └── qml_benchmark.py       # Isolated 4-Qubit Variational Quantum Simulator
│   ├── monitoring/
│   │   ├── collector.py           # Ingestion collector & Prometheus exporter
│   │   └── drift.py               # Statistical drift engine (Two-Sample KS & PSI)
│   ├── recovery/
│   │   ├── policy.py              # Recovery policy engine & trigger rules
│   │   └── validator.py           # Automated quality gates & regression checks
│   ├── registry/
│   │   └── mlflow_adapter.py      # Versioned model registry adapter
│   ├── security/
│   │   ├── auth.py                # API key authentication & RBAC
│   │   └── audit.py               # Tamper-resistant SHA-256 hash-chained audit logger
│   ├── config.py                  # Pydantic Settings & threshold configuration
│   └── main.py                    # FastAPI application initialization & lifespan
├── docs/
│   ├── evidence/                  # Deliverable screenshots and sprint demonstration videos
│   ├── deliverables_part1/        # Original Part-1 DOCX submissions
│   ├── 01_SRS_Self_Monitoring_MLOps_System.md
│   ├── 02_Test_Plan_Self_Monitoring_MLOps_System.md
│   ├── 03_Architecture_Design_Self_Monitoring_MLOps_System.md
│   ├── 04_Test_Case_Catalogue_Self_Monitoring_MLOps_System.md
│   ├── SPRINT_BACKLOG_AND_DEVIATIONS.md
│   └── SPRINT_1_AND_2_VIDEO_DEMO_GUIDE.md
├── tests/                         # All 18 Test Cases (TC-01 through TC-18)
├── Dockerfile                     # Multi-stage production container
├── docker-compose.yml             # Local microservice orchestration
├── pytest.ini                     # Pytest root configuration
├── requirements.txt               # Pinned dependencies
└── README.md                      # Executive overview & badges
```

---

## 2. Security Roles & Headers

All management endpoints require authentication via the `X-API-Key` header:

| Role | API Key (Demo) | Allowed Endpoints |
| :--- | :--- | :--- |
| **Admin** | `admin-secret-key-prod-demo` | Full access (validation, promotion, rollback, audit logs, configuration) |
| **ML Engineer** | `engineer-secret-key-prod-demo` | Experiment runs, drift analysis, candidate decision, validation |
| **Viewer** | `viewer-secret-key-prod-demo` | Read-only metrics summary, alerts, dashboard |
| **Service** | `service-secret-key-prod-demo` | High-frequency prediction telemetry submission (`/events/prediction`) |

---

## 3. Extending Drift Algorithms

To register a new drift detection metric (e.g. Wasserstein Distance or Jensen-Shannon Divergence), add the method to `app/monitoring/drift.py` and register it inside `compare_windows()`:

```python
from scipy.stats import wasserstein_distance

def calculate_wasserstein(expected: np.ndarray, actual: np.ndarray) -> float:
    return float(wasserstein_distance(expected, actual))
```

---

## 4. Running Tests & Linting

```bash
# Execute full test suite
python -m pytest tests/ -v

# Run linting
flake8 app tests --count --select=E9,F63,F7,F82 --show-source --statistics
```
