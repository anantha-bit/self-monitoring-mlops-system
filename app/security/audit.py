import os
import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.config import settings

class AuditLogger:
    def __init__(self, log_path: str = settings.AUDIT_LOG_PATH):
        self.log_path = log_path
        self._last_hash = "0" * 64
        self._memory_cache: List[Dict[str, Any]] = []
        self._load_existing()

    def _load_existing(self):
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            record = json.loads(line)
                            self._memory_cache.append(record)
                            if "integrity_hash" in record:
                                self._last_hash = record["integrity_hash"]
            except Exception:
                pass

    def record_event(
        self,
        actor: str,
        action: str,
        target_version: Optional[str],
        outcome: str,
        details: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Record a security or model-lifecycle event.
        Conforms to SR-05, FR-11, and TC-12.
        """
        event_id = f"evt-{uuid.uuid4().hex[:12]}"
        corr_id = correlation_id or f"corr-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        raw_payload = f"{event_id}|{timestamp}|{actor}|{action}|{target_version}|{outcome}|{self._last_hash}"
        integrity_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

        record = {
            "event_id": event_id,
            "correlation_id": corr_id,
            "timestamp": timestamp,
            "actor": actor,
            "action": action,
            "target_version": target_version or "N/A",
            "outcome": outcome,
            "details": details or {},
            "previous_hash": self._last_hash,
            "integrity_hash": integrity_hash
        }

        self._last_hash = integrity_hash
        self._memory_cache.append(record)

        # Append to disk
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        return record

    def query_events(
        self,
        action: Optional[str] = None,
        actor: Optional[str] = None,
        target_version: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        results = self._memory_cache
        if action:
            results = [r for r in results if r["action"] == action]
        if actor:
            results = [r for r in results if r["actor"] == actor]
        if target_version:
            results = [r for r in results if r["target_version"] == target_version]
        return results[-limit:]

audit_logger = AuditLogger()
