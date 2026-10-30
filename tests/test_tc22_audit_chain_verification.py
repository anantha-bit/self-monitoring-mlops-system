import pytest
import copy
from app.security.audit import audit_logger
from app.security.verifier import audit_verifier

def test_tc22_audit_chain_verification():
    """
    TC-22: Cryptographic SHA-256 audit log chain verification and tamper detection.
    Traceability: FR-11, SR-05.
    """
    # Record test events
    e1 = audit_logger.record_event(
        actor="test_user_1",
        action="TEST_ACTION_ALPHA",
        target_version="v1.0.0",
        outcome="SUCCESS"
    )
    e2 = audit_logger.record_event(
        actor="test_user_2",
        action="TEST_ACTION_BETA",
        target_version="v1.0.1",
        outcome="SUCCESS"
    )

    events = [e1, e2]
    # 1. Clean verification must pass
    valid, msg = audit_verifier.verify_chain(events)
    assert valid is True
    assert "cryptographically verified" in msg

    # 2. Tampered record must be detected
    tampered_events = copy.deepcopy(events)
    tampered_events[0]["target_version"] = "v_HACKED_9.9.9"  # Alter payload without updating hash
    tampered_valid, tamper_msg = audit_verifier.verify_chain(tampered_events)
    assert tampered_valid is False
    assert "Integrity check failed" in tamper_msg or "Tamper detected" in tamper_msg
