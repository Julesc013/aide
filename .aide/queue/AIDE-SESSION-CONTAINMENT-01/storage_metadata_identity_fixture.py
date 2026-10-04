"""Native identity regression in one owned job fixture; no target traversal."""
import importlib.util
import json
import os
from pathlib import Path

spec = importlib.util.spec_from_file_location("custody_probe", Path(__file__).with_name("storage_custody_probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
native_identity = probe.identity()
fixture = Path(os.environ["TMP"]) / "storage-metadata-identity"
fixture.mkdir()
(fixture / "a").write_bytes(b"abc")
(fixture / "b").write_bytes(b"abc")
os.link(fixture / "a", fixture / "a-link")
probe.TARGET = fixture
result = probe.metadata()
assert result["complete"] and result["file_identity_complete"], result
assert result["files"] == 3 and result["logical_bytes"] == 9, result
assert result["observed_unique_logical_bytes"] == 6, result
assert result["shared_file_entries"] == 2, result
assert result["allocated_or_reclaimable_bytes"] is None, result
record = {"status": "PASS", "worker_identity": native_identity,
          "metadata": result, "model_calls": 0, "target_reads": 0,
          "target_mutations": False, "disposable_proven": False}
(Path(os.environ["AIDE_JOB_OUTPUT"]) / "storage-identity-fixture.json").write_text(
    json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "files": 3, "logical_bytes": 9,
                  "unique_logical_bytes": 6, "shared_file_entries": 2}))
