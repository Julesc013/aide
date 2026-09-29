"""One-use ordinary API-set loader observation in an admitted managed child.

This module prepares a separate effect from the unavailable L2 name query.
Importing it does not load an API-set DLL. A future exact effect manifest and
independent admission are required before invoking main on a native backend.
"""

from __future__ import annotations

import argparse
import ctypes as C
from dataclasses import dataclass
import json
import ntpath
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from core.runtime.continuous_worker.state import Refused
from core.runtime.continuous_worker import windows_system_observation as observation
import h2_api_query_effect as control

INVENTORY_REL = control.INVENTORY_REL
SOURCE_REL = control.SOURCE_REL
CONTROLLER_REL = ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2_api_query_effect.py"
DRIVER_REL = ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2_api_loader_effect.py"
RESULT_NAME = control.LOADER_RESULT_NAME
PENDING_MARKER = control.LOADER_PENDING_MARKER
FIELDS = {"schema", "request_id", "os_build", "api_name", "inventory_sha256",
          "source_sha256", "controller_sha256", "driver_sha256", "expires_at", "max_seconds"}


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Refused("duplicate loader effect JSON key")
        result[key] = value
    return result


def strict_json(content: bytes):
    try:
        return json.loads(content, object_pairs_hook=_unique_pairs)
    except (UnicodeError, ValueError, TypeError, RecursionError) as error:
        raise Refused("bounded unique-key loader effect JSON required") from error


@dataclass(frozen=True)
class LoaderPlan:
    request_id: str
    os_build: str
    api_names: tuple[str, ...]
    expires_at: float
    max_seconds: float
    fingerprint: str


class NativeLoaderBackend:
    """Add exact OS-build observation without changing the reviewed loader."""

    def __init__(self):
        self._loader = observation.NativeApiSetLoaderApi()
        self._rtl_get_version = observation.objects.bind(
            observation.objects.N, "RtlGetVersion",
            [C.POINTER(observation._RtlOsVersionInfoW)], C.c_long)

    def os_build(self):
        version = observation._RtlOsVersionInfoW()
        version.dwOSVersionInfoSize = C.sizeof(version)
        status = int(self._rtl_get_version(C.byref(version))) & 0xffffffff
        if (status or version.dwMajorVersion != 10 or version.dwMinorVersion != 0 or
                version.dwPlatformId != 2 or version.dwBuildNumber < 1):
            raise Refused("exact Windows OS build unavailable")
        return observation._os_build(
            f"{version.dwMajorVersion}.{version.dwMinorVersion}.{version.dwBuildNumber}")

    def load_and_identify(self, name):
        return self._loader.load_and_identify(name)


def load_plan(manifest: dict, root: Path, *, wall_clock=time.time) -> LoaderPlan:
    if (type(manifest) is not dict or set(manifest) != FIELDS or
            manifest["schema"] != "aide.host.api-set-loader-effect.v1"):
        raise Refused("exact one-name loader effect manifest required")
    request = manifest["request_id"]
    if type(request) is not str or not re.fullmatch(r"[0-9a-f]{32}", request):
        raise Refused("literal one-use loader request identity required")
    name = observation._name(manifest["api_name"])
    if name != manifest["api_name"] or not observation._api_name(name):
        raise Refused("literal admitted API-set loader contract required")
    os_build = observation._os_build(manifest["os_build"])
    expires, seconds = manifest["expires_at"], manifest["max_seconds"]
    if (not observation._finite(expires) or not observation._finite(seconds) or
            not 0 < seconds <= 30 or not 0 < expires - wall_clock() <= 3600):
        raise Refused("fresh finite loader effect expiry and duration required")
    for key, relative, maximum in (
            ("inventory_sha256", INVENTORY_REL, 256 * 1024),
            ("source_sha256", SOURCE_REL, 2 * 1024 * 1024),
            ("controller_sha256", CONTROLLER_REL, 256 * 1024),
            ("driver_sha256", DRIVER_REL, 256 * 1024)):
        expected = observation._digest(manifest[key])
        if control.sha256(control.pinned_file(root / relative, maximum)) != expected:
            raise Refused("pinned loader effect input changed: " + relative)
    inventory = strict_json(control.pinned_file(root / INVENTORY_REL, 256 * 1024))
    names = inventory.get("api_names") if type(inventory) is dict else None
    if type(names) is not list or len(names) != 180 or name not in names:
        raise Refused("exact retained API-set inventory membership required")
    return LoaderPlan(request, os_build, (name,), expires, seconds,
                      control.sha256(control.canonical(manifest)))


def _check_time(plan: LoaderPlan, start: float, wall_start: float, clock, wall_clock) -> None:
    now, wall = clock(), wall_clock()
    if (not observation._finite(now) or not observation._finite(wall) or
            now < start or wall < wall_start or now - start >= plan.max_seconds or
            not 0 < plan.expires_at - wall <= 3600):
        raise Refused("loader effect clock, expiry or duration refused")


def _observation(value: object, name: str) -> dict:
    keys = {"api_name", "physical_name", "module_path", "loader_flags",
            "host_bytes_qualified", "restricted_loader_qualified"}
    if type(value) is not dict or set(value) != keys or value["api_name"] != name:
        raise Refused("exact loader observation required")
    host = observation._name(value["physical_name"])
    path = observation.NativeApiSetLoaderApi._directory(value["module_path"])
    if (observation._api_name(host) or host in observation.PRIVATE_NAMES or
            ntpath.basename(path) != host or
            value["loader_flags"] != observation.LOADER_SEARCH_SYSTEM32 or
            value["host_bytes_qualified"] is not False or
            value["restricted_loader_qualified"] is not False):
        raise Refused("bounded unqualified physical host observation required")
    return value


def reconcile_result(output: Path, journal_path: Path, plan: LoaderPlan) -> dict:
    result = control.reconcile_result(output, journal_path, plan,
                                      result_name=RESULT_NAME, pending_marker=PENDING_MARKER)
    if (result.get("schema") != "aide.host.api-set-loader-result.v1" or
            result.get("native_loads") != 1 or result.get("worker_activated") is not False):
        raise Refused("loader result schema or effect boundary changed")
    return result


def run_effect(manifest: dict, root: Path, control_root: Path, output: Path,
               api_factory, *, clock=time.monotonic, wall_clock=time.time) -> dict:
    plan = load_plan(manifest, root, wall_clock=wall_clock)
    control.safe_directory(output)
    journal = control.DurableJournal(control_root, plan,
                                     control.sha256(control.canonical(manifest)),
                                     namespace="api-loader")
    passed = False
    try:
        try:
            control.reserve_result(output, result_name=RESULT_NAME,
                                   pending_marker=PENDING_MARKER)
            api = api_factory()
            if (not callable(getattr(api, "os_build", None)) or
                    not callable(getattr(api, "load_and_identify", None))):
                raise Refused("exact loader backend required")
            start, wall_start = clock(), wall_clock()
            _check_time(plan, start, wall_start, clock, wall_clock)
            if journal.reserve(plan.fingerprint) != plan.fingerprint:
                raise Refused("loader journal reservation differs")
            journal.guard()
            if observation._os_build(api.os_build()) != plan.os_build:
                raise Refused("Windows build changed before API-set load")
            _check_time(plan, start, wall_start, clock, wall_clock)
            intent = {"schema": "aide.host.api-set-loader-intent.v1",
                      "request_id": plan.request_id, "plan_sha256": plan.fingerprint,
                      "sequence": 0, "api_name": plan.api_names[0],
                      "operation": "LoadLibraryExW"}
            journal.guard()
            acknowledgement = journal.intent(intent)
            if acknowledgement != control.sha256(control.canonical(intent)):
                raise Refused("journal did not acknowledge exact loader intent")
            _check_time(plan, start, wall_start, clock, wall_clock)
            observed = _observation(api.load_and_identify(plan.api_names[0]),
                                    plan.api_names[0])
            _check_time(plan, start, wall_start, clock, wall_clock)
            journal.guard()
            result = {"schema": "aide.host.api-set-loader-result.v1",
                      "request_id": plan.request_id, "plan_sha256": plan.fingerprint,
                      "os_build": plan.os_build, "native_loads": 1,
                      "intent_acknowledgement": acknowledgement,
                      "observation": observed, "host_bytes_qualified": False,
                      "restricted_loader_qualified": False,
                      "worker_activated": False}
            result_sha = control.stage_result(output, result, result_name=RESULT_NAME)
            journal.guard()
            journal.terminal("PASS", {"request_id": plan.request_id,
                                      "plan_sha256": plan.fingerprint,
                                      "result_sha256": result_sha,
                                      "native_loads": 1})
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
        raise Refused("task-owned loader effect manifest required")
    manifest = strict_json(control.pinned_file(manifest_path, 64 * 1024))
    result = run_effect(manifest, ROOT, Path(os.environ["AIDE_JOB_CONTROL"]),
                        Path(os.environ["AIDE_JOB_OUTPUT"]),
                        NativeLoaderBackend)
    print(json.dumps({"status": "PASS", "request_id": result["request_id"],
                      "native_loads": result["native_loads"]}, sort_keys=True))


if __name__ == "__main__":
    main()
