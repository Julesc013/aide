from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Sequence


LANE_PROOF = {
    "lane_id": "microsoft.visual-studio.vsix-v1",
    "proof_kind": "degraded-runnable",
    "execution_mode": "cli-bridge",
    "boot_slice_notes": "P11 degraded lane proof. Shared-core behavior is reused through a thin cli-bridge wrapper; native VSIX packaging and shell loading remain deferred.",
    "capability_notes": "P11 lane-local capability report for a degraded cli-bridge proof. Native VSIX packaging and richer editor wiring remain deferred.",
    "top_level_notes": "Lane-local cli-bridge boot-slice proof completed with deterministic report output.",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AIDE boot-slice proof for the Visual Studio VSIX v1 lane.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the shared-core response.")
    parser.add_argument("--verify", action="store_true", help="Compare the live response with boot_slice_response.json.")
    return parser


def annotate_response(response: dict[str, object]) -> dict[str, object]:
    annotated = dict(response)
    annotated["notes"] = LANE_PROOF["top_level_notes"]
    extensions = dict(annotated.get("extensions") or {})
    extensions["lane_proof"] = {
        "lane_id": LANE_PROOF["lane_id"],
        "proof_kind": LANE_PROOF["proof_kind"],
        "execution_mode": LANE_PROOF["execution_mode"],
        "shared_behavior_source": "shared.cli",
        "host_wrapper_scope": "request-shaping and deterministic result serialization",
    }
    annotated["extensions"] = extensions
    artifacts = []
    for artifact in annotated.get("artifacts", []):
        current = dict(artifact)
        payload = current.get("payload")
        if isinstance(payload, dict):
            payload = dict(payload)
            if current.get("kind") == "boot-slice-report":
                payload["notes"] = LANE_PROOF["boot_slice_notes"]
            if current.get("kind") == "capability-report":
                payload["notes"] = LANE_PROOF["capability_notes"]
            current["payload"] = payload
        artifacts.append(current)
    annotated["artifacts"] = artifacts
    return annotated


def render_response(response: dict[str, object], pretty: bool) -> str:
    if pretty:
        return json.dumps(response, indent=2) + "\n"
    return json.dumps(response) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    lane_dir = Path(__file__).resolve().parent
    repo_root = Path(__file__).resolve().parents[4]
    command = [sys.executable, "-m", "shared.cli", "--request", str(lane_dir / "boot_slice_request.json")]
    if args.pretty:
        command.append("--pretty")
    completed = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    if completed.returncode != 0:
        if completed.stdout:
            sys.stdout.write(completed.stdout)
        return completed.returncode
    actual = annotate_response(json.loads(completed.stdout))
    sys.stdout.write(render_response(actual, args.pretty))
    if not args.verify:
        return 0
    expected = json.loads((lane_dir / "boot_slice_response.json").read_text(encoding="utf-8-sig"))
    if actual != expected:
        sys.stderr.write("boot_slice_response.json does not match live output.\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
