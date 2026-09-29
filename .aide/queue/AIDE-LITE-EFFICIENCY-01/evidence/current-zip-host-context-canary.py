"""Qualify the frozen Lite CLI against installed Codex prompt-input shape.

Run only as an admitted AIDE Python job. No model turn is requested or raw
prompt-input JSON retained.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[4]
ARCHIVE = ROOT / ".aide/release/stable/aide-lite-v1.0.0.zip"
PROMPT = ROOT / ".aide.local/efficiency-live-host-prompt.txt"
MEMBER = "aide-lite-pack-v0/files/.aide/scripts/aide_lite.py"
ZIP_SHA256 = "27948415530f260479c249b2d8cc956792eff4c77a524f0225f61f1f3f2ef7b1"
MAX_DEBUG_BYTES = 2 * 1024 * 1024
MAX_PROMPT_BYTES = 4096


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        raise ValueError("expected locally configured Codex path and SHA-256")
    codex = Path(sys.argv[1])
    codex_sha256 = sys.argv[2]
    if not codex.is_absolute() or not codex.is_file():
        raise ValueError("locally configured Codex executable is unavailable")
    if len(codex_sha256) != 64 or any(c not in "0123456789abcdef" for c in codex_sha256):
        raise ValueError("invalid locally configured Codex SHA-256")
    scratch = Path(os.environ["AIDE_JOB_TMP"])
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    if sha(ARCHIVE.read_bytes()) != ZIP_SHA256:
        raise ValueError("stable ZIP identity changed")
    if sha(codex.read_bytes()) != codex_sha256:
        raise ValueError("installed Codex executable changed")
    with PROMPT.open("rb") as prompt_file:
        prompt_bytes = prompt_file.read(MAX_PROMPT_BYTES + 1)
    if not 0 < len(prompt_bytes) <= MAX_PROMPT_BYTES:
        raise ValueError("local prompt changed or exceeds bound")
    prompt = prompt_bytes.decode("utf-8")

    with zipfile.ZipFile(ARCHIVE) as archive:
        info = archive.getinfo(MEMBER)
        if info.is_dir() or info.file_size > 4 * 1024 * 1024:
            raise ValueError("delivered CLI member is not bounded")
        cli_bytes = archive.read(info)

    with tempfile.TemporaryDirectory(prefix="lite-context-", dir=scratch) as temporary:
        consumer = Path(temporary) / "consumer"
        cli = consumer / ".aide/scripts/aide_lite.py"
        cli.parent.mkdir(parents=True)
        cli.write_bytes(cli_bytes)
        debugger = subprocess.run(
            [str(codex), "-c", "features.apps=false", "-c", "features.hooks=false",
             "-c", "features.multi_agent=false", "-c", "features.remote_plugin=false",
             "-c", "agents.enabled=false", "debug", "prompt-input", prompt],
            cwd=consumer, capture_output=True, timeout=60, check=False,
        )
        if debugger.returncode or not 0 < len(debugger.stdout) <= MAX_DEBUG_BYTES:
            raise ValueError("installed prompt-input debugger failed or exceeded bound")
        parsed = subprocess.run(
            [sys.executable, "-I", "-B", str(cli), "--repo-root", str(consumer),
             "job", "context"],
            cwd=consumer, input=debugger.stdout, capture_output=True,
            timeout=30, check=False,
        )
        if parsed.returncode or len(parsed.stdout) > 8192:
            raise ValueError("delivered context parser failed or exceeded bound")
        summary = json.loads(parsed.stdout)
        if (summary.get("status") != "COMPLETE"
                or summary.get("raw_prompt_or_response_retained") is not False
                or summary.get("model_requests_started_by_parser") != 0
                or summary.get("input_json_bytes") != len(debugger.stdout)
                or summary.get("effective_tokens") is not None
                or summary.get("tool_definitions") != "unknown"):
            raise ValueError("delivered context parser gave unsupported result")
        if consumer.joinpath("core").exists():
            raise ValueError("consumer unexpectedly contains source core")

    result = {
        "status": "PASS",
        "archive_sha256": ZIP_SHA256,
        "delivered_cli_sha256": sha(cli_bytes),
        "codex_cli_sha256": codex_sha256,
        "prompt_sha256": sha(prompt_bytes),
        "prompt_bytes": len(prompt_bytes),
        "host_command": "codex-cli 0.145.0 debug prompt-input",
        "debugger_json_bytes": len(debugger.stdout),
        "delivered_context": summary,
        "raw_debugger_json_retained": False,
        "actual_model_turn": False,
        "consumer_scratch_retired": True,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS current ZIP delivered context parser and installed debugger shape")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
