#!/usr/bin/env python3
"""Deterministic reference worker for LocalProcessExecutionHost v0 tests.

This fixture is intentionally narrow: it prints one JSON object, performs no
repository writes, calls no network, loads no provider or model, and starts no
child process of its own.
"""

from __future__ import annotations

import argparse
import json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIDE local-process reference worker.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workunit-ref", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.json:
        parser.error("--json is required")
    payload = {
        "schema_version": "aide.local-process-reference-worker-result.v0",
        "worker_kind": "local_reference_worker",
        "run_id": args.run_id,
        "workunit_ref": args.workunit_ref,
        "status": "PASS",
        "event_count": 3,
        "artifact_count": 1,
        "network_call_performed": False,
        "provider_or_model_called": False,
        "repository_mutation_performed": False,
        "preview_or_apply_performed": False,
        "release_or_promotion_performed": False,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
