# Video Demonstration Guide: Sprint-1 and Sprint-2 Outcomes

This document provides exact, timestamped walk-through scripts, talking points, and command sequences for recording the **1-minute Sprint-1 video** and the **2-minute Sprint-2 video** required by the mini-project deliverables.

---

## Part 1: Sprint-1 Outcome Video (1 Minute Demo)
- **Target Duration:** 60 seconds
- **Focus:** Working microservice, live prediction serving, telemetry metrics, and statistical drift detection.

### Timestamped Script

| Time | Screen Action | Narration Script |
| :--- | :--- | :--- |
| **0:00 - 0:15** | Open terminal / browser showing `GET http://localhost:8000/health` and Swagger UI (`/docs`). | *"Hello, this is Team PES1UG24AM presenting Sprint-1 of our Self-Monitoring MLOps System. We have established our FastAPI microservice with automated telemetry and health instrumentation."* |
| **0:15 - 0:35** | Trigger prediction requests via Swagger or curl (`POST /api/v1/predict`); show `/api/v1/metrics/summary` updating request counts and P95 latency. | *"Each prediction automatically streams latency, error rates, and feature summaries into our ingestion pipeline, adhering to FR-01 and FR-02."* |
| **0:35 - 0:50** | Run drift analysis endpoint (`POST /api/v1/drift/analyze`); show Kolmogorov-Smirnov test and PSI score calculation and alert generation (`FR-03`, `FR-08`). | *"When input distribution shifts, our statistical analyzer computes two-sample KS and PSI scores, triggering real-time drift alerts."* |
| **0:50 - 1:00** | Show terminal running PyTorch sequence autoencoder and QML benchmark, plus passing GitHub Actions CI pipeline. | *"We also completed baseline ML, deep learning sequence autoencoders, and isolated QML benchmarks with automated CI tests. Sprint-1 is complete!"* |

---

## Part 2: Sprint-2 Outcome Video (2 Minute Demo)
- **Target Duration:** 120 seconds
- **Focus:** End-to-end autonomous recovery cycle, quality validation gates, dual-key promotion, emergency rollback, tamper-evident audit logging, and full web dashboard.

### Timestamped Script

| Time | Screen Action | Narration Script |
| :--- | :--- | :--- |
| **0:00 - 0:20** | Open Dashboard at `http://localhost:8000/dashboard`. Point out Active Model Version (`v1.0.0`), P95 Latency, and Status Badges. | *"Welcome to the final Sprint-2 demonstration of our Self-Monitoring MLOps System by Anantha Krishna, Akash, and Amit Prasad. We are viewing the live interactive dashboard showing real-time operational telemetry."* |
| **0:20 - 0:45** | Click **"Inject +10 Shifted/Drift Data"**. Watch Drift Status turn red (`DRIFT_DETECTED`), alerts appear in the alerts table (`FR-08`), and recovery policy trigger candidate retraining (`FR-09`). | *"We inject synthetic drifted feature streams. The drift engine instantly detects distribution divergence, triggers a CRITICAL alert, and initiates an automated candidate retraining cycle under our recovery policy."* |
| **0:45 - 1:15** | In Candidates table: show candidate model. Click **"Validate"** to show automated quality gates (accuracy >= 80%, P95 latency <= 150ms, regression check vs baseline). Then click **"Approve"** (`FR-10`, `FR-14`). Active model updates to new candidate! | *"In accordance with FR-10 and NFR-10, promotion is strictly gated. Our automated validator tests the candidate against performance and regression gates. Once validated, an authorized ML Engineer approves the candidate, promoting it to active production."* |
| **1:15 - 1:40** | Click **"Emergency Rollback"** button (`FR-12`). Prompt pops up for reason; active model immediately reverts to `v1.0.0`! | *"If post-promotion anomalies emerge, our automated rollback mechanism instantly restores the last known stable baseline model, ensuring 99.9% service reliability."* |
| **1:40 - 2:00** | Scroll to **"Tamper-Resistant Audit Trail"**; show chained SHA-256 integrity hashes for each promotion, rollback, and approval (`SR-05`). Show terminal running all 18 passing test cases (`18 passed`). | *"Every lifecycle action is logged in our cryptographic SHA-256 audit log. All 18 test cases are verified in CI/CD. The development cycle is now complete and frozen. Thank you!"* |

---

## Recording Tips for the Team
1. Start the service with `python -m uvicorn app.main:app --port 8000` or `docker compose up`.
2. Navigate to `http://localhost:8000/dashboard` in Google Chrome or any modern browser.
3. Use OBS Studio or Windows Game Bar (`Win + G`) to record the screen and voiceover.
4. Export as MP4 and upload the demo video files directly to the `docs/videos/` directory in the repository or link the Google Drive / YouTube unlisted URL in the README!
