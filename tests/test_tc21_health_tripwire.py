import pytest
from app.recovery.health_checker import ContinuousHealthTripwire

def test_tc21_health_tripwire():
    """
    TC-21: Continuous telemetry tripwire and consecutive failure rollback triggers.
    Traceability: FR-12, NFR-02.
    """
    tripwire = ContinuousHealthTripwire(max_consecutive_failures=3)

    # 1. Normal telemetry
    healthy, msg = tripwire.check_telemetry(error_rate=0.01, p95_latency=45.0)
    assert healthy is True
    assert tripwire.consecutive_failures == 0

    # 2. Degraded telemetry step 1 & 2
    h1, _ = tripwire.check_telemetry(error_rate=0.15, p95_latency=700.0)
    assert h1 is True  # not yet tripped
    assert tripwire.consecutive_failures == 1

    h2, _ = tripwire.check_telemetry(error_rate=0.15, p95_latency=700.0)
    assert h2 is True
    assert tripwire.consecutive_failures == 2

    # 3. Third failure triggers tripwire
    h3, trip_msg = tripwire.check_telemetry(error_rate=0.15, p95_latency=700.0)
    assert h3 is False
    assert "TRIPWIRE_ACTIVATED" in trip_msg
    assert tripwire.consecutive_failures == 3

    # 4. Recovery resets counter
    h_rec, _ = tripwire.check_telemetry(error_rate=0.02, p95_latency=40.0)
    assert h_rec is True
    assert tripwire.consecutive_failures == 0
