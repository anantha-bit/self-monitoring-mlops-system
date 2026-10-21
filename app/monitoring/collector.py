import time
import threading
from typing import Dict, Any, List, Optional
import numpy as np

class MonitoringCollector:
    def __init__(self, window_size: int = 500):
        self.window_size = window_size
        self._lock = threading.Lock()
        
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        self.latencies: List[float] = []
        self.recent_events: List[Dict[str, Any]] = []
        self.feature_stream: List[Dict[str, float]] = []
        self.prediction_stream: List[int] = []

    def record_event(
        self,
        request_id: str,
        model_version: str,
        latency_ms: float,
        success: bool,
        feature_summary: Optional[Dict[str, float]] = None,
        prediction: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record prediction telemetry.
        Conforms to FR-02, NFR-07, NFR-09, TC-02.
        """
        with self._lock:
            self.total_requests += 1
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

            self.latencies.append(latency_ms)
            if len(self.latencies) > self.window_size * 2:
                self.latencies = self.latencies[-self.window_size:]

            if feature_summary:
                self.feature_stream.append(feature_summary)
                if len(self.feature_stream) > self.window_size:
                    self.feature_stream = self.feature_stream[-self.window_size:]

            if prediction is not None:
                self.prediction_stream.append(prediction)
                if len(self.prediction_stream) > self.window_size:
                    self.prediction_stream = self.prediction_stream[-self.window_size:]

            event_record = {
                "request_id": request_id,
                "model_version": model_version,
                "latency_ms": latency_ms,
                "success": success,
                "timestamp": time.time(),
                "error_message": error_message
            }
            self.recent_events.append(event_record)
            if len(self.recent_events) > self.window_size:
                self.recent_events = self.recent_events[-self.window_size:]

            return event_record

    def get_summary(self, active_model_version: str = "v1.0.0") -> Dict[str, Any]:
        with self._lock:
            total = self.total_requests
            errors = self.failed_requests
            error_rate = (errors / total) if total > 0 else 0.0

            if self.latencies:
                lat_array = np.array(self.latencies)
                p50 = float(np.percentile(lat_array, 50))
                p90 = float(np.percentile(lat_array, 90))
                p95 = float(np.percentile(lat_array, 95))
                p99 = float(np.percentile(lat_array, 99))
                avg_lat = float(np.mean(lat_array))
            else:
                p50 = p90 = p95 = p99 = avg_lat = 0.0

            return {
                "total_requests": total,
                "successful_requests": self.successful_requests,
                "failed_requests": errors,
                "error_rate": round(error_rate, 4),
                "latency_p50_ms": round(p50, 2),
                "latency_p90_ms": round(p90, 2),
                "latency_p95_ms": round(p95, 2),
                "latency_p99_ms": round(p99, 2),
                "latency_avg_ms": round(avg_lat, 2),
                "active_model_version": active_model_version,
                "window_sample_count": len(self.latencies)
            }

    def export_prometheus_metrics(self) -> str:
        """
        Export metrics in Prometheus text exposition format (NFR-07).
        """
        summary = self.get_summary()
        lines = [
            "# HELP mlops_predictions_total Total number of prediction requests processed",
            "# TYPE mlops_predictions_total counter",
            f"mlops_predictions_total {summary['total_requests']}",
            "# HELP mlops_prediction_errors_total Total number of prediction request errors",
            "# TYPE mlops_prediction_errors_total counter",
            f"mlops_prediction_errors_total {summary['failed_requests']}",
            "# HELP mlops_prediction_latency_p95_milliseconds 95th percentile request latency in ms",
            "# TYPE mlops_prediction_latency_p95_milliseconds gauge",
            f"mlops_prediction_latency_p95_milliseconds {summary['latency_p95_ms']}",
            "# HELP mlops_error_rate Ratio of failed requests to total requests",
            "# TYPE mlops_error_rate gauge",
            f"mlops_error_rate {summary['error_rate']}",
        ]
        return "\n".join(lines) + "\n"

    def clear(self):
        with self._lock:
            self.total_requests = 0
            self.successful_requests = 0
            self.failed_requests = 0
            self.latencies.clear()
            self.recent_events.clear()
            self.feature_stream.clear()
            self.prediction_stream.clear()

collector = MonitoringCollector()
