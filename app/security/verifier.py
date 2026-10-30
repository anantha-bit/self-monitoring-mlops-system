import hashlib
from typing import List, Dict, Any, Tuple
from app.security.audit import audit_logger

class AuditChainVerifier:
    """
    Cryptographic SHA-256 audit log integrity validator.
    Developed by AMIT PRASAD S G (PES1UG24AM033) - Sprint 2.
    """
    @staticmethod
    def verify_chain(events: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Walk the audit trail and verify that each integrity hash matches its predecessor.
        """
        if not events:
            return True, "Audit log is empty; chain is valid."

        for i, evt in enumerate(events):
            expected_prev = evt.get("previous_hash", "0" * 64)
            if i > 0:
                prev_hash = events[i - 1].get("integrity_hash")
                if expected_prev != prev_hash:
                    return False, f"Tamper detected at event index {i} (id: {evt.get('event_id')}). Previous hash mismatch."

            raw_payload = f"{evt['event_id']}|{evt['timestamp']}|{evt['actor']}|{evt['action']}|{evt['target_version']}|{evt['outcome']}|{expected_prev}"
            computed_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()
            if computed_hash != evt.get("integrity_hash"):
                return False, f"Integrity check failed at event {evt.get('event_id')}. Hash mismatch."

        return True, f"All {len(events)} audit records cryptographically verified."

audit_verifier = AuditChainVerifier()
