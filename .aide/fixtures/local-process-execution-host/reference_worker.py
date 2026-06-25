#!/usr/bin/env python3
"""Deterministic reference worker for LocalProcessExecutionHost v0.

The worker emits a small NDJSON event stream and writes one harmless artifact
inside its current working directory. It performs no repository writes, starts
no child processes, calls no network, and loads no provider or model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "aide.fixture-worker.events.v0"
FIXTURE_VERSION = "local-process-reference-worker-v0-repair-01"
DETERMINISTIC_TIMESTAMP = "2026-06-25T00:00:00+10:00"
ARTIFACT_MEMBER = "artifacts/result.json"


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def event(run_ref: str, sequence: int, event_kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_ref": run_ref,
        "sequence": sequence,
        "event_kind": event_kind,
        "timestamp": DETERMINISTIC_TIMESTAMP,
        "payload": payload,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIDE local-process reference worker.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workunit-ref", required=True)
    parser.add_argument("--event-stream", action="store_true")
    args = parser.parse_args(argv)
    if not args.event_stream:
        parser.error("--event-stream is required")

    artifact_payload = {
        "fixture_version": FIXTURE_VERSION,
        "result": "PASS",
        "run_ref": args.run_id,
        "workunit_ref": args.workunit_ref,
    }
    artifact_text = stable_json(artifact_payload)
    artifact_path = Path(ARTIFACT_MEMBER)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(artifact_text, encoding="utf-8", newline="\n")
    artifact_digest = sha256_text(artifact_text)
    artifact_size = len(artifact_text.encode("utf-8"))

    events = [
        event(args.run_id, 1, "run_created", {"workunit_ref": args.workunit_ref}),
        event(args.run_id, 2, "run_started", {"worker_kind": "local_reference_worker"}),
        event(args.run_id, 3, "worker_message", {"message": "fixture worker executed"}),
        event(
            args.run_id,
            4,
            "artifact_produced",
            {
                "path": ARTIFACT_MEMBER,
                "media_type": "application/json",
                "byte_count": artifact_size,
                "sha256": artifact_digest,
            },
        ),
        event(args.run_id, 5, "usage_updated", {"events": 6, "artifacts": 1, "processes": 1}),
        event(args.run_id, 6, "run_completed", {"result": "PASS"}),
    ]
    for item in events:
        print(json.dumps(item, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
