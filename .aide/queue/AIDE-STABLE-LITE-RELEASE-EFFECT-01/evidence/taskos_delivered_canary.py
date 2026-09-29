"""Check read-only Task OS inspection in exact delivered Lite ZIP bytes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    archive = Path(sys.argv[1]).resolve(strict=True)
    expected_zip, expected_cli = sys.argv[2:4]
    assert digest(archive.read_bytes()) == expected_zip
    scratch = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
    retained = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
    member = "aide-lite-pack-v0/files/.aide/scripts/aide_lite.py"
    with zipfile.ZipFile(archive) as zipped:
        cli_bytes = zipped.read(member)
    assert digest(cli_bytes) == expected_cli
    cli = scratch / "delivered-aide-lite.py"
    cli.write_bytes(cli_bytes)
    target = scratch / "consumer"
    report = target / ".aide/reports/task-os-next-plan.md"
    report.parent.mkdir(parents=True)
    sentinel = b"older retained report snapshot\n"
    report.write_bytes(sentinel)

    def invoke(*parts: str) -> str:
        result = subprocess.run(
            [sys.executable, "-I", "-B", str(cli), "--repo-root", str(target), "task", "next-plan", *parts],
            cwd=target,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
        )
        if result.returncode:
            raise AssertionError(f"delivered command exited {result.returncode}: {result.stderr[-300:]}")
        return result.stdout

    observed = invoke()
    assert "selected_next_workunit: No queued WorkUnit selected" in observed
    assert "non_mutating: true" in observed
    assert "lifecycle_apply_authorized: false" in observed
    assert "report:" not in observed
    assert report.read_bytes() == sentinel

    written = invoke("--write-report")
    assert "non_mutating: false" in written
    assert "report: .aide/reports/task-os-next-plan.md" in written
    assert report.read_bytes() != sentinel
    assert b"selected_next_workunit: No queued WorkUnit selected" in report.read_bytes()
    summary = {
        "schema": "aide.taskos-delivered-inspection-canary.v1",
        "status": "PASS",
        "zip_sha256": expected_zip,
        "delivered_cli_sha256": expected_cli,
        "default_report_unchanged": True,
        "explicit_report_changed": True,
        "lifecycle_apply_authorized": False,
    }
    (retained / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("delivered Task OS inspection: PASS")


if __name__ == "__main__":
    main()
