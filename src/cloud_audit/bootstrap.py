from __future__ import annotations

from cloud_audit.generate_snapshots import generate_snapshots
from cloud_audit.health import assert_outputs, required_exports
from cloud_audit.scan import scan_snapshots


def ensure_demo_outputs() -> bool:
    if all(path.exists() for path in required_exports().values()):
        assert_outputs()
        return False
    generate_snapshots()
    scan_snapshots(source="snapshots")
    assert_outputs()
    return True
