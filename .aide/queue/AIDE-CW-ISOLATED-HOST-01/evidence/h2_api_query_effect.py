"""One-use, bounded ordinary-host API-set query effect.

This measures only this host's supported API-set name mapping. It does not
qualify a protected controller, physical host bytes, or a restricted loader.
Run only through the AIDE managed Windows job after exact effect review.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys

REPO = Path(__file__).resolve().parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from core.runtime.continuous_worker.windows_system_observation import (
    ApiSetQueryPlan, ApiSetQuerySession, NativeApiSetQueryApi, _canonical,
)

INVENTORY = ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2-delay-system-readonly-final.json"
INVENTORY_SHA256 = "a9fef62f0e1431c12b4743cbc42f2039790625dd6ea8e769991512467b6ccce3"
SOURCE_FILES = (
    ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2_api_query_effect.py",
    "core/runtime/continuous_worker/__init__.py",
    "core/runtime/continuous_worker/state.py",
    "core/runtime/continuous_worker/windows_pe.py",
    "core/runtime/continuous_worker/windows_python_contract.py",
    "core/runtime/continuous_worker/windows_security_objects.py",
    "core/runtime/continuous_worker/windows_system_observation.py",
)
MAX_EFFECT_BYTES = 16384
MAX_INVENTORY_BYTES = 131072
MAX_RESULT_BYTES = 2 * 1024 * 1024
MAX_JOURNAL_BYTES = 262144


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bounded(path: Path, limit: int) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("bounded input exceeded")
    return data


def load_effect(path: Path, expected: str) -> tuple[dict, ApiSetQueryPlan]:
    raw = bounded(path, MAX_EFFECT_BYTES)
    if digest(raw) != expected:
        raise ValueError("reviewed effect bytes changed")
    value = json.loads(raw)
    if type(value) is not dict or set(value) != {
        "schema", "inventory_sha256", "source_files", "plan", "effects"
    } or value["schema"] != "aide.host.api-set-native-effect.v1":
        raise ValueError("exact native query effect required")
    if value["inventory_sha256"] != INVENTORY_SHA256:
        raise ValueError("inventory identity changed")
    if type(value["source_files"]) is not dict or set(value["source_files"]) != set(SOURCE_FILES):
        raise ValueError("exact source input set required")
    for relative in SOURCE_FILES:
        expected_file = value["source_files"][relative]
        if type(expected_file) is not str or len(expected_file) != 64:
            raise ValueError("source digest missing")
        if digest(bounded(REPO / relative, 2 * 1024 * 1024)) != expected_file:
            raise ValueError("reviewed source input changed: " + relative)
    required_effects = {
        "native_api_set_queries": 180,
        "api_query_library_loads": 1,
        "physical_host_reads": 0,
        "file_copies": 0,
        "grants": 0,
        "profiles": 0,
        "network_calls": 0,
        "operational_activation": False,
    }
    if value["effects"] != required_effects or any(
        type(value["effects"][key]) is not type(required)
        for key, required in required_effects.items()
    ):
        raise ValueError("exact effect ceiling required")
    inventory_raw = bounded(REPO / INVENTORY, MAX_INVENTORY_BYTES)
    if digest(inventory_raw) != INVENTORY_SHA256:
        raise ValueError("retained inventory changed")
    inventory = json.loads(inventory_raw)
    plan = ApiSetQueryPlan.read(value["plan"])
    if (
        type(inventory) is not dict
        or type(inventory.get("api_names")) is not list
        or len(inventory["api_names"]) != 180
        or plan.api_names != tuple(sorted(inventory["api_names"]))
    ):
        raise ValueError("exact 180-name inventory required")
    return value, plan


class Journal:
    def __init__(self, output: Path, effect_sha256: str, job_id: str):
        mode = os.lstat(output).st_mode
        if not stat.S_ISDIR(mode) or output.is_symlink():
            raise ValueError("ordinary managed output directory required")
        self.path = output / "api-query-journal.jsonl"
        self.stream = self.path.open("xb")
        self.bytes = 0
        self.effect_sha256 = effect_sha256
        self.job_id = job_id

    def write(self, row: dict) -> str:
        raw = _canonical(row) + b"\n"
        if self.bytes + len(raw) > MAX_JOURNAL_BYTES:
            raise ValueError("journal bound exceeded")
        if self.stream.write(raw) != len(raw):
            raise ValueError("journal write incomplete")
        self.stream.flush()
        os.fsync(self.stream.fileno())
        self.bytes += len(raw)
        return digest(_canonical(row))

    def reserve(self, fingerprint: str) -> str:
        self.write({
            "schema": "aide.host.api-set-native-reservation.v1",
            "effect_sha256": self.effect_sha256,
            "job_id": self.job_id,
            "plan_sha256": fingerprint,
            "consumed": True,
            "replay_permitted": False,
        })
        return fingerprint

    def intent(self, row: dict) -> str:
        return self.write(row)

    def close(self) -> None:
        self.stream.close()


class DeferredNativeApi:
    """Do not load the API-query DLL until the session's reservation is durable."""
    def __init__(self):
        self.native = None

    def _ensure(self):
        if self.native is None:
            self.native = NativeApiSetQueryApi()
        return self.native

    def os_build(self):
        return self._ensure().os_build()

    def api_set_host(self, name):
        return self._ensure().api_set_host(name)


def output_file(output: Path, name: str, value: dict) -> None:
    raw = _canonical(value) + b"\n"
    if len(raw) > MAX_RESULT_BYTES:
        raise ValueError("bounded output exceeded")
    with (output / name).open("xb") as stream:
        if stream.write(raw) != len(raw):
            raise ValueError("result write incomplete")
        stream.flush()
        os.fsync(stream.fileno())


def run(effect_path: Path, expected_sha256: str, output: Path, job_id: str) -> int:
    effect, plan = load_effect(effect_path, expected_sha256)
    journal = Journal(output, expected_sha256, job_id)
    session = None
    try:
        # The session writes a durable reservation before DeferredNativeApi
        # loads the supported query library. It journals each query first.
        api = DeferredNativeApi()
        session = ApiSetQuerySession(plan, api, journal, lambda: None)
        raw = session.run()
        result = json.loads(raw)
        journal.write({
            "schema": "aide.host.api-set-native-terminal.v1",
            "result_sha256": digest(raw),
            "native_calls": result["native_calls"],
            "query_attempts": result["query_attempts"],
        })
        output_file(output, "api-query-result.json", result)
        return 0
    except Exception as error:
        failure = {
            "schema": "aide.host.api-set-native-failure.v1",
            "effect_sha256": expected_sha256,
            "job_id": job_id,
            "plan_sha256": plan.fingerprint,
            "error_type": type(error).__name__,
            "session_failure": session.failure if session is not None else None,
            "replay_permitted": False,
        }
        journal.write(failure)
        output_file(output, "api-query-failure.json", failure)
        return 2
    finally:
        journal.close()


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] != "--effect":
        raise ValueError("exact effect invocation required")
    expected = sys.argv[3]
    if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
        raise ValueError("literal effect SHA-256 required")
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    job_id = os.environ["AIDE_JOB_ID"]
    if len(job_id) != 32 or any(ch not in "0123456789abcdef" for ch in job_id):
        raise ValueError("managed job identity required")
    return run(Path(sys.argv[2]), expected, output, job_id)


if __name__ == "__main__":
    raise SystemExit(main())
