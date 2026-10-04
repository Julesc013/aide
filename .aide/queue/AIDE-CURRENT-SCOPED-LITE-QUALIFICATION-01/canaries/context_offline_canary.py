"""Exercise installed Lite context and evidence commands in disposable targets."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(argv: list[str], cwd: Path | None = None, timeout_seconds: int = 60) -> None:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout_seconds)
    if result.returncode:
        raise AssertionError(f"command failed {result.returncode}: {argv}: {result.stderr[-300:]}")


def offline_command(out: Path, label: str, script: Path, target: Path, parts: list[str]) -> dict[str, object]:
    guard = out / "offline-guard.py"
    argv = [sys.executable, "-I", "-B", str(guard), str(script), "--repo-root", str(target), *parts]
    result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
    record = {"argv": argv, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    path = out / f"{label}.json"
    path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if result.returncode:
        raise AssertionError(f"{label} failed with exit {result.returncode}; see {path}")
    if "OFFLINE_NETWORK_ATTEMPT" in result.stdout + result.stderr:
        raise AssertionError(f"{label} attempted Python socket access")
    return {"label": label, "exit_code": result.returncode, "log_sha256": sha(path), "stdout": result.stdout}


def evidence_text() -> str:
    return """# Disposable evidence packet

## Task

LOCAL-CONTEXT-CANARY-01: inspect installed Lite context.

## Objective

Generate a compact target-owned context packet and validate its structure.

## Scope

Only this disposable target; no external repositories or network effects.

## Changed Files

- `.aide/context/latest-context-packet.md` generated in the target.

## Validation Commands

- `python -I -B aide_lite.py context`: passed in the disposable target.

## Validation Results

Context packet exists; offline process socket guard recorded no attempt.

## Generated Artifacts

Target-owned `.aide/context/latest-context-packet.md` is generated output.

## Token Estimates

Compact packet uses the installed target policy; exact count is in the CLI log.

## Risks

Python socket audit does not observe native networking in child processes.

## Deferrals

Public downloaded-byte qualification belongs to the later release gate.

## Next Recommended Phase

Freeze exact release source and repeat on downloaded bytes.
"""


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: context_offline_canary.py ZIP ZIP_SHA HELPER_SHA")
    archive = Path(sys.argv[1]).resolve(strict=True)
    expected_zip, expected_helper = sys.argv[2:]
    root = Path(__file__).resolve().parent
    helper_path = root / "lifecycle_helper.py"
    if sha(archive) != expected_zip or sha(helper_path) != expected_helper:
        raise ValueError("archive or helper identity mismatch")
    spec = importlib.util.spec_from_file_location("aide_context_helper", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("helper cannot load")
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    out = Path(os.environ["AIDE_JOB_TMP"]) / "run-context"
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    out.mkdir()
    guard = out / "offline-guard.py"
    guard.write_text(
        "import runpy,socket,sys\n"
        "def blocked(*args,**kwargs): raise RuntimeError('OFFLINE_NETWORK_ATTEMPT')\n"
        "def audit(event,args):\n"
        "    if event in ('socket.connect','socket.bind'): blocked()\n"
        "sys.addaudithook(audit)\n"
        "socket.socket.connect=blocked\n"
        "socket.socket.connect_ex=blocked\n"
        "socket.getaddrinfo=blocked\n"
        "path=sys.argv[1]; sys.argv=sys.argv[1:]; runpy.run_path(path,run_name='__main__')\n",
        encoding="utf-8",
    )
    try:
        members = helper.extract_zip(archive, out / "candidate")
        pack = out / "candidate" / helper.PACK_NAME
        recorder = helper.Recorder(out)
        results = []
        for kind in ("fresh", "brownfield"):
            target = out / f"{kind}-target"
            target.mkdir()
            owned = target / "project-owned.txt"
            owned.write_bytes(b"Project owned; preserve.\r\n")
            if kind == "brownfield":
                (target / "README.md").write_bytes(b"# Authored project\n")
                run(["git", "init", "-q", str(target)])
                run(["git", "-C", str(target), "add", "README.md", "project-owned.txt"])
                run(["git", "-C", str(target), "-c", "user.name=AIDE canary", "-c",
                     "user.email=aide-canary@example.invalid", "commit", "-qm", "fixture baseline"])
            before = sha(owned)
            helper.install(recorder, f"{kind}-install", pack, target)
            installed = target / ".aide/scripts/aide_lite.py"
            if not installed.is_file() or sha(owned) != before:
                raise AssertionError(f"{kind} install changed project-owned bytes")
            if kind == "brownfield":
                run(["git", "-C", str(target), "add", ".aide", "AGENTS.md"], timeout_seconds=300)
                run(["git", "-C", str(target), "-c", "user.name=AIDE canary", "-c",
                     "user.email=aide-canary@example.invalid", "commit", "-qm", "fixture installed Lite"])
            context = offline_command(out, f"{kind}-context", installed, target, ["context"])
            packet = target / ".aide/context/latest-context-packet.md"
            if not packet.is_file() or "contents_inline: false" not in context["stdout"]:
                raise AssertionError(f"{kind} compact context missing")
            task = offline_command(out, f"{kind}-pack", installed, target,
                                   ["pack", "--task", "Inspect disposable target context offline"])
            if not (target / ".aide/context/latest-task-packet.md").is_file():
                raise AssertionError(f"{kind} task packet missing")
            evidence = target / ".aide/queue/LOCAL-CONTEXT-CANARY-01/evidence/validation.md"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(evidence_text(), encoding="utf-8")
            verify = offline_command(out, f"{kind}-verify", installed, target,
                                     ["verify", "--evidence", str(evidence.relative_to(target))])
            result = re.search(r"^result: (PASS|WARN|FAIL)$", verify["stdout"], re.M)
            errors = re.search(r"^errors: (\d+)$", verify["stdout"], re.M)
            if not result or result.group(1) == "FAIL" or not errors or errors.group(1) != "0":
                raise AssertionError(f"{kind} verifier failed")
            warnings = [line for line in verify["stdout"].splitlines() if line.startswith("- WARN ")]
            categories = sorted({line.split(":", 1)[0].split(" ", 2)[-1] for line in warnings})
            results.append({"kind": kind, "project_owned_sha256": before,
                            "context_sha256": sha(packet), "task_packet_sha256": sha(target / ".aide/context/latest-task-packet.md"),
                            "verify_result": result.group(1), "verify_warning_count": len(warnings),
                            "verify_warning_categories": categories,
                            "command_log_sha256": [context["log_sha256"], task["log_sha256"], verify["log_sha256"]]})
        summary = {"status": "PASS", "zip_sha256": expected_zip, "helper_sha256": expected_helper,
                   "script_sha256": sha(Path(__file__)), "offline_guard_sha256": sha(guard),
                   "member_count": len(members), "install_command_count": len(recorder.commands),
                   "targets": results,
                   "network_observation": "Python process socket guard only; native child traffic not observed"}
        (out / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", "summary_sha256": sha(out / "summary.json")}, sort_keys=True))
    finally:
        for path in out.glob("*.json"):
            shutil.copy2(path, retained / path.name)
        shutil.copy2(guard, retained / guard.name)


if __name__ == "__main__":
    main()
