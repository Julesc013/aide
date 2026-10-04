"""Native identity regression in one owned job fixture; no target traversal."""
import importlib.util
import hashlib
import json
import os
import stat
from pathlib import Path

spec = importlib.util.spec_from_file_location("custody_probe", Path(__file__).with_name("storage_custody_probe.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
native_identity = probe.identity()
fixture = Path(os.environ["TMP"]) / "storage-metadata-identity"
fixture.mkdir()
fixture_identity = (fixture.stat().st_dev, fixture.stat().st_ino)
(fixture / "a").write_bytes(b"abc")
(fixture / "b").write_bytes(b"abc")
source_identity = ((fixture / "a").stat().st_dev, (fixture / "a").stat().st_ino)
alias = fixture / "a-link"
alias_created = False
try:
    os.link(fixture / "a", alias)
    alias_created = True
    probe.TARGET = fixture
    result = probe.metadata()
    assert result["complete"] and result["file_identity_complete"], result
    assert result["files"] == 3 and result["logical_bytes"] == 9, result
    assert result["observed_unique_logical_bytes"] == 6, result
    assert result["shared_file_entries"] == 2, result
    assert result["allocated_or_reclaimable_bytes"] is None, result
finally:
    if alias_created:
        # Only the exact fixture alias is retired, including assertion failure.
        probe.ordinary_directory(fixture)
        root_info = fixture.lstat()
        if (root_info.st_dev, root_info.st_ino) != fixture_identity:
            raise ValueError("owned fixture directory changed; cleanup refused")
        if not alias.resolve(strict=True).is_relative_to(fixture.resolve(strict=True)):
            raise ValueError("fixture alias escaped; cleanup refused")
        for path in (alias, fixture / "a"):
            info = path.lstat()
            if (not stat.S_ISREG(info.st_mode) or info.st_file_attributes & 1024
                    or (info.st_dev, info.st_ino) != source_identity
                    or info.st_nlink != 2 or info.st_size != 3
                    or hashlib.sha256(path.read_bytes()).digest()
                       != hashlib.sha256(b"abc").digest()):
                raise ValueError("owned fixture alias custody changed; cleanup refused")
        alias.unlink()
        if (fixture / "a").stat().st_nlink != 1:
            raise ValueError("fixture source link count did not retire")
record = {"status": "PASS", "worker_identity": native_identity,
          "metadata": result, "model_calls": 0, "target_reads": 0,
          "target_mutations": False, "disposable_proven": False}
(Path(os.environ["AIDE_JOB_OUTPUT"]) / "storage-identity-fixture.json").write_text(
    json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "files": 3, "logical_bytes": 9,
                  "unique_logical_bytes": 6, "shared_file_entries": 2}))
