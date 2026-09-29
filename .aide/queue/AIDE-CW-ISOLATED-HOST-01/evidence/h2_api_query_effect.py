"""One-use, controller-owned API-set query probe; never a worker launcher."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from core.runtime.continuous_worker.state import Refused
from core.runtime.continuous_worker import windows_system_observation as observation

SOURCE_REL = "core/runtime/continuous_worker/windows_system_observation.py"
INVENTORY_REL = ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2-delay-system-readonly-final.json"
RESULT_NAME = "api-query-result.json"
STAGED_NAME = RESULT_NAME + ".pending"
PENDING_MARKER = b"AIDE_API_QUERY_PENDING\n"
LOADER_RESULT_NAME = "api-loader-result.json"
LOADER_PENDING_MARKER = b"AIDE_API_LOADER_PENDING\n"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_directory(path: Path) -> Path:
    """The managed runner creates these exact, ordinary retained/control roots."""
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise Refused("ordinary owned output or control directory required")
    return path


def pinned_file(path: Path, maximum: int) -> bytes:
    before = path.lstat()
    if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
            getattr(before, "st_file_attributes", 0) & 0x400 or
            not 0 < before.st_size <= maximum):
        raise Refused("bounded ordinary API-set source input required")
    content = path.read_bytes()
    after = path.lstat()
    if (len(content) != before.st_size or
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) !=
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)):
        raise Refused("API-set source input changed during read")
    return content


def load_plan(manifest: dict, root: Path) -> observation.ApiSetQueryPlan:
    fields = {"schema", "request_id", "os_build", "api_names", "inventory_sha256",
              "source_sha256", "expires_at", "max_seconds"}
    if type(manifest) is not dict or set(manifest) != fields or manifest["schema"] != "aide.host.api-query-effect.v1":
        raise Refused("exact API-set effect manifest required")
    for key, relative, maximum in (("inventory_sha256", INVENTORY_REL, 256 * 1024),
                                   ("source_sha256", SOURCE_REL, 2 * 1024 * 1024)):
        if sha256(pinned_file(root / relative, maximum)) != observation._digest(manifest[key]):
            raise Refused("pinned API-set effect input changed: " + relative)
    inventory = json.loads(pinned_file(root / INVENTORY_REL, 256 * 1024))
    names = inventory.get("api_names") if type(inventory) is dict else None
    if type(names) is not list or len(names) != 180 or names != manifest["api_names"]:
        raise Refused("exact retained 180-name API-set inventory required")
    plan = observation.ApiSetQueryPlan.read({
        "schema": "aide.host.api-set-query.v1", "request_id": manifest["request_id"],
        "os_build": manifest["os_build"], "api_names": names,
        "expires_at": manifest["expires_at"], "max_seconds": manifest["max_seconds"],
    })
    if not 0 < plan.expires_at - time.time() <= 3600:
        raise Refused("fresh finite API-set effect expiry required")
    return plan


class DurableJournal:
    """Exclusive persistent reservation plus fsynced pre-call intents."""

    def __init__(self, control: Path, plan: observation.ApiSetQueryPlan,
                 manifest_sha256: str, *, namespace: str = "api-query"):
        if namespace not in ("api-query", "api-loader"):
            raise Refused("fixed API-set journal namespace required")
        self.path = safe_directory(control) / (namespace + "-" + plan.request_id + ".jsonl")
        self.plan = plan
        self.sequence = 0
        self.reserved = False
        self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_BINARY, 0o600)
        try:
            self._write({"kind": "exclusive_request", "request_id": plan.request_id,
                         "plan_sha256": plan.fingerprint, "manifest_sha256": manifest_sha256})
        except BaseException:
            os.close(self.fd)
            raise

    def _write(self, value: dict) -> None:
        encoded = canonical(value) + b"\n"
        if len(encoded) > 4096 or os.write(self.fd, encoded) != len(encoded):
            raise Refused("bounded complete journal row required")
        os.fsync(self.fd)

    def guard(self) -> bool:
        current, opened = self.path.lstat(), os.fstat(self.fd)
        if (not stat.S_ISREG(current.st_mode) or current.st_nlink != 1 or
                (current.st_dev, current.st_ino) != (opened.st_dev, opened.st_ino)):
            raise Refused("API-set journal identity changed")
        return True

    def reserve(self, fingerprint: str) -> str:
        if self.reserved or fingerprint != self.plan.fingerprint:
            raise Refused("API-set reservation differs or was consumed")
        self._write({"kind": "session_reservation", "plan_sha256": fingerprint})
        self.reserved = True
        return fingerprint

    def intent(self, value: dict) -> str:
        if (not self.reserved or self.sequence >= len(self.plan.api_names) or
                value.get("sequence") != self.sequence or
                value.get("api_name") != self.plan.api_names[self.sequence] or
                value.get("plan_sha256") != self.plan.fingerprint):
            raise Refused("API-set intent differs from exact sequence")
        acknowledgement = sha256(canonical(value))
        self._write({"kind": "pre_call_intent", "value": value,
                     "acknowledgement": acknowledgement})
        self.sequence += 1
        return acknowledgement

    def terminal(self, status: str, detail: dict) -> None:
        self._write({"kind": "terminal", "status": status, "detail": detail})

    def close(self) -> None:
        os.close(self.fd)


def _result_paths(output: Path, result_name: str) -> tuple[Path, Path]:
    if result_name not in (RESULT_NAME, LOADER_RESULT_NAME):
        raise Refused("fixed API-set result name required")
    root = safe_directory(output)
    return root / result_name, root / (result_name + ".pending")


def reserve_result(output: Path, *, result_name: str = RESULT_NAME,
                   pending_marker: bytes = PENDING_MARKER) -> None:
    """Occupy the final name before any native call; it is never success yet."""
    if pending_marker != (PENDING_MARKER if result_name == RESULT_NAME else LOADER_PENDING_MARKER):
        raise Refused("fixed API-set result reservation marker required")
    target, _ = _result_paths(output, result_name)
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_BINARY, 0o600)
    try:
        if os.write(fd, pending_marker) != len(pending_marker):
            raise Refused("complete API-set result reservation required")
        os.fsync(fd)
    finally:
        os.close(fd)


def stage_result(output: Path, value: dict, *, result_name: str = RESULT_NAME) -> str:
    _, target = _result_paths(output, result_name)
    encoded = canonical(value) + b"\n"
    if len(encoded) > observation.MAX_RESULT_BYTES:
        raise Refused("bounded API-set result required")
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_BINARY, 0o600)
    try:
        if os.write(fd, encoded) != len(encoded):
            raise Refused("complete API-set result write required")
        os.fsync(fd)
    finally:
        os.close(fd)
    return sha256(encoded)


def terminal_detail(journal_path: Path, plan: observation.ApiSetQueryPlan) -> dict:
    rows = pinned_file(journal_path, 2 * 1024 * 1024).splitlines()
    terminal = json.loads(rows[-1]) if rows else {}
    detail = terminal.get("detail", {})
    if (terminal.get("kind") != "terminal" or terminal.get("status") != "PASS" or
            detail.get("request_id") != plan.request_id or
            detail.get("plan_sha256") != plan.fingerprint):
        raise Refused("matching terminal PASS required for API-set result")
    return detail


def qualified_result(output: Path, journal_path: Path, plan: observation.ApiSetQueryPlan,
                     *, result_name: str = RESULT_NAME) -> dict:
    """A result is usable only with a matching terminal record and byte digest."""
    detail = terminal_detail(journal_path, plan)
    target, _ = _result_paths(output, result_name)
    encoded = pinned_file(target, observation.MAX_RESULT_BYTES)
    if sha256(encoded) != detail.get("result_sha256"):
        raise Refused("API-set result differs from terminal PASS")
    result = json.loads(encoded)
    if result.get("request_id") != plan.request_id or result.get("plan_sha256") != plan.fingerprint:
        raise Refused("API-set result differs from admitted plan")
    return result


def reconcile_result(output: Path, journal_path: Path, plan: observation.ApiSetQueryPlan,
                     *, result_name: str = RESULT_NAME,
                     pending_marker: bytes = PENDING_MARKER) -> dict:
    """Finish publication after a durable PASS, without replaying native calls."""
    if pending_marker != (PENDING_MARKER if result_name == RESULT_NAME else LOADER_PENDING_MARKER):
        raise Refused("fixed API-set result reconciliation marker required")
    detail = terminal_detail(journal_path, plan)
    target, staged = _result_paths(output, result_name)
    current = pinned_file(target, observation.MAX_RESULT_BYTES)
    if current == pending_marker:
        if sha256(pinned_file(staged, observation.MAX_RESULT_BYTES)) != detail.get("result_sha256"):
            raise Refused("staged API-set result differs from terminal PASS")
        os.replace(staged, target)
    return qualified_result(output, journal_path, plan, result_name=result_name)


def run_effect(manifest: dict, root: Path, control: Path, output: Path, api_factory) -> dict:
    plan = load_plan(manifest, root)
    safe_directory(output)
    journal = DurableJournal(control, plan, sha256(canonical(manifest)))
    passed = False
    try:
        try:
            reserve_result(output)
            api = api_factory()
            session = observation.ApiSetQuerySession(plan, api, journal, journal.guard)
            result = json.loads(session.run())
            if journal.sequence != len(plan.api_names):
                raise Refused("incomplete API-set query sequence")
            journal.guard()
            result_sha256 = stage_result(output, result)
            journal.guard()
            journal.terminal("PASS", {"native_calls": result["native_calls"],
                                      "query_attempts": result["query_attempts"],
                                      "request_id": plan.request_id,
                                      "plan_sha256": plan.fingerprint,
                                      "result_sha256": result_sha256})
            passed = True
            return reconcile_result(output, journal.path, plan)
        except Exception as error:
            if not passed:
                journal.terminal("REFUSED", {"error_type": type(error).__name__,
                                             "completed_intents": journal.sequence})
            raise
    finally:
        journal.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve(strict=True)
    if manifest_path.parent != ROOT / ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence":
        raise Refused("task-owned effect manifest required")
    manifest = json.loads(pinned_file(manifest_path, 64 * 1024))
    result = run_effect(manifest, ROOT, Path(os.environ["AIDE_JOB_CONTROL"]),
                        Path(os.environ["AIDE_JOB_OUTPUT"]), observation.NativeApiSetQueryApi)
    print(json.dumps({"status": "PASS", "request_id": result["request_id"],
                      "query_attempts": result["query_attempts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
