"""Registered bounded JSON bridge, without an installed operational provider.

The external qualifier must establish protected host/store and executable trust.
Windows Jobs provide process containment only. Client deadline monitoring cannot
supply the independently required server-side mutation predicate.
"""
from contextlib import closing
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import time
import uuid

from .common import Refused, fields, identity, canonical, digest, require_path, beneath, bounded_bytes, parse_json
from .bridge_store import BridgeStore
from .preparation import directory_lease
from .pr_observation import validate_plan
from core.runtime.continuous_worker.locking import supervisor_lock
from core.runtime.continuous_worker.windows_job import WindowsJobHost

MAX_INPUT = 1024 * 1024


def registration(path, pin, plan):
    identity(pin)
    raw = bounded_bytes(path, 65536)
    if hashlib.sha256(raw).hexdigest() != pin:
        raise Refused("registered bridge configuration changed")
    value = parse_json(raw)
    fields(value, "schema plan_digest argv inputs cwd limits")
    if value["schema"] != "aide.broker.bridge.v1" or value["plan_digest"] != digest(plan):
        raise Refused("bridge registration belongs to another plan")
    argv, inputs = value["argv"], value["inputs"]
    if (not isinstance(argv, list) or len(argv) not in (1, 4) or
            any(not isinstance(x, str) or not x or len(x) > 4096 or any(c in x for c in "\x00\r\n") for x in argv)):
        raise Refused("fixed registered bridge command required")
    executable = require_path(argv[0])
    if executable.suffix.lower() != ".exe":
        raise Refused("registered native executable required")
    if len(argv) == 4 and (not executable.name.lower().startswith("python") or argv[1:3] != ["-I", "-B"] or
                          require_path(argv[3]).suffix.lower() != ".py"):
        raise Refused("only explicit isolated Python script invocation is admitted")
    if not isinstance(inputs, dict) or not 1 <= len(inputs) <= 64:
        raise Refused("finite bridge input pins required")
    required = {argv[0]} | ({argv[3]} if len(argv) == 4 else set())
    if not required.issubset(inputs):
        raise Refused("actual bridge executable/script must be pinned")
    names, total = set(), 0
    for name, expected in inputs.items():
        path = require_path(name)
        identity(expected)
        normalized = str(path).casefold()
        if normalized in names:
            raise Refused("ambiguous registered input aliases")
        names.add(normalized)
        data = bounded_bytes(path)
        total += len(data)
        if total > 16 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != expected:
            raise Refused("bridge input source drift or byte budget")
    cwd = require_path(value["cwd"])
    if not cwd.is_dir():
        raise Refused("protected bridge working directory required")
    limits = value["limits"]
    fields(limits, "timeout_seconds output_bytes memory_bytes processes max_calls max_io_bytes minimum_free_bytes")
    if (type(limits["timeout_seconds"]) not in (int, float) or not math.isfinite(limits["timeout_seconds"]) or
            not .05 <= limits["timeout_seconds"] <= 30):
        raise Refused("finite bridge timeout required")
    bounds = {"output_bytes": (1, MAX_INPUT), "memory_bytes": (67108864, 1073741824),
              "processes": (1, 8), "max_calls": (1, min(132, plan["max_observations"] + 4)),
              "max_io_bytes": (1, 67108864), "minimum_free_bytes": (67108864, 17179869184)}
    for name, (low, high) in bounds.items():
        if type(limits[name]) is not int or not low <= limits[name] <= high:
            raise Refused("invalid registered bridge resource bound")
    return value


class RegisteredBridge:
    """Internal adapter; never constructed from a worker command or CLI plugin.

    The qualifier's assert_current method must be a bounded local host check;
    provider network calls belong exclusively in the recorded child operation.
    A fixture no-op qualifier is not operational host or credential isolation.
    """
    def __init__(self, path, sha256, plan, *, qualifier=None, checkpoint=None):
        validate_plan(plan)
        self.path, self.pin = require_path(str(path)), identity(sha256)
        self._plan = canonical(plan)
        if len(self._plan.encode()) > 65536:
            raise Refused("registered bridge plan byte budget")
        self.config = registration(self.path, self.pin, plan)
        self.qualifier = qualifier
        self.checkpoint = checkpoint or (lambda phase: None)
        self.context = None
        self._context_identity = None

    @property
    def plan(self):
        return json.loads(self._plan)

    def assert_current(self, broker, request, plan, purpose):
        if self.qualifier is None:
            raise Refused("protected provider host qualification is absent")
        if plan != self.plan or digest(request) != plan["request_digest"]:
            raise Refused("registered bridge request identity changed")
        config = registration(self.path, self.pin, plan)
        if config != self.config:
            raise Refused("registered bridge configuration drift")
        cwd = require_path(config["cwd"])
        if any(beneath(cwd, other) or beneath(other, cwd) for other in
               (broker.root, broker.repository_root, broker.exchange)):
            raise Refused("bridge working directory overlaps protected data or worker roots")
        self.qualifier.assert_current(broker, json.loads(canonical(request)), self.plan, purpose)
        binding = (str(broker.root), str(broker.repository_root), str(broker.exchange),
                   digest(broker.authority), canonical(request))
        if self._context_identity is not None and self._context_identity != binding:
            raise Refused("bridge context cannot transfer to another authority/store")
        self._context_identity = binding
        self.context = broker, json.loads(canonical(request))

    def _current(self, purpose):
        if self.context is None:
            raise Refused("bridge has no qualified broker context")
        broker, request = self.context
        self.assert_current(broker, request, self.plan, purpose)
        if purpose != "observe":
            now = broker.now()
            if (type(now) not in (int, float) or not math.isfinite(now) or
                    now >= min(self.plan["expires_at"], broker.authority["expires_at"])):
                raise Refused("registered bridge mutation deadline expired")
        return broker, request

    def observe(self, plan, *, attempt):
        if plan != self.plan:
            raise Refused("bridge observation plan changed")
        return canonical(self._call("observe", attempt, None)).encode()

    def dispatch(self, operation, plan, prepared):
        if plan != self.plan:
            raise Refused("bridge mutation plan changed")
        broker, request = self._current(operation)
        fields(prepared, "directory request_digest tree generation directory_identity commit_bytes")
        generation = broker.ledger.preparation(digest(request))
        if (not generation or prepared["request_digest"] != plan["request_digest"] or
                prepared["generation"] != generation["generation"] or prepared["directory_identity"] != generation["identity"] or
                require_path(str(prepared["directory"])) != broker.root / generation["generation"] or
                prepared["tree"] != plan["candidate_tree"]):
            raise Refused("bridge mutation lacks exact prepared generation")
        raw = prepared["commit_bytes"]
        if type(raw) is not bytes or len(raw) > 65536:
            raise Refused("bridge commit input budget")
        oid = hashlib.sha1(b"commit " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if oid != plan["candidate_commit"]:
            raise Refused("bridge commit bytes differ from fixed plan")
        value = dict(prepared, directory=str(prepared["directory"]), commit_bytes=base64.b64encode(raw).decode("ascii"))
        result = self._call(operation, None, value)
        fields(result, "status")
        if result["status"] != "submitted":
            raise Refused("bridge mutation response is not an exact acknowledgement")
        # Acknowledgement is not integration proof; only a later checked provider
        # observation can complete the broker request.

    def _recover(self, store, host):
        for row in store.unfinished():
            observed = host.reconcile(row["id"])
            if observed.get("quiescent") is not True:
                raise Refused("prior registered provider Job is not quiescent")
            store.finish(row["id"], "uncertain", {"recovery": observed, "replay_allowed": False})

    def _call(self, operation, attempt, prepared):
        broker, request = self._current(operation)
        limits = self.config["limits"]
        call_id = uuid.uuid4().hex
        envelope = {"schema": "aide.broker.bridge-call.v1", "call_id": call_id,
                    "request_digest": self.plan["request_digest"], "operation": operation,
                    "attempt": attempt, "plan": self.plan, "prepared": prepared}
        payload = canonical(envelope).encode()
        if len(payload) > MAX_INPUT:
            raise Refused("bridge input byte budget")
        reserve_bytes = len(payload) + limits["output_bytes"] + 16384
        if shutil.disk_usage(broker.root).free < limits["minimum_free_bytes"] + reserve_bytes:
            raise Refused("bridge free-space floor refused")
        host = WindowsJobHost()
        with directory_lease(broker.root), supervisor_lock(broker.root, scope="provider-bridge"), closing(BridgeStore(broker.root)) as store:
            self._recover(store, host)
            registered = canonical({"path": str(self.path), "sha256": self.pin, "config": self.config})
            store.reserve(self.plan, registered, operation, attempt, call_id,
                          hashlib.sha256(payload).hexdigest(), reserve_bytes, limits)
            self.checkpoint("call_intent")
            folder = broker.root / ("provider-call-" + call_id)
            job_receipt, hashes, guard_failure = None, None, []
            last_checked = [float("-inf")]
            def guard(force=False):
                now = broker.now()
                if operation != "observe" and (type(now) not in (int, float) or not math.isfinite(now) or
                        now >= min(self.plan["expires_at"], broker.authority["expires_at"])):
                    raise Refused("registered bridge mutation deadline expired")
                if force or time.monotonic() - last_checked[0] >= .25:
                    self._current(operation)
                    store.authorized(self.plan, operation, attempt)
                    last_checked[0] = time.monotonic()
            def checkpoint(phase):
                self.checkpoint(phase)
                guard(True)
            def cancelled():
                try:
                    guard()
                    return False
                except (Refused, OSError, ValueError) as error:
                    guard_failure.append(type(error).__name__)
                    return True
            try:
                with directory_lease(folder, create=True) as owned, directory_lease(Path(self.config["cwd"])):
                    store.owned_directory(call_id, owned)
                    guard(True)
                    job_receipt = host.run(self.config["argv"], cwd=Path(self.config["cwd"]), input_bytes=payload,
                                           output_dir=folder / "streams", job_id=call_id,
                                           timeout=limits["timeout_seconds"], output_limit=limits["output_bytes"],
                                           memory_limit=limits["memory_bytes"], process_limit=limits["processes"],
                                           cancelled=cancelled, checkpoint=checkpoint)
                    hashes = {}
                    for name in ("stdin", "stdout", "stderr"):
                        path = folder / "streams" / name
                        # Persist the owned, quiescent streams before recording
                        # their successful return; retain all failure artifacts.
                        with path.open("r+b") as stream:
                            stream.flush()
                            os.fsync(stream.fileno())
                        hashes[name] = hashlib.sha256(bounded_bytes(path, MAX_INPUT)).hexdigest()
                    if hashes["stdin"] != hashlib.sha256(payload).hexdigest():
                        raise Refused("registered bridge input artifact changed")
                    guard(True)
                    if (guard_failure or job_receipt["exit_code"] != 0 or job_receipt["reason"] != "exited" or
                            job_receipt["quiescent"] is not True or job_receipt["io_errors"]):
                        raise Refused("registered bridge did not return a bounded successful result")
                    response = parse_json(bounded_bytes(folder / "streams" / "stdout", limits["output_bytes"]))
                    fields(response, "schema call_id request_digest operation result")
                    if (response["schema"] != "aide.broker.bridge-response.v1" or
                            any(response[k] != envelope[k] for k in ("call_id", "request_digest", "operation"))):
                        raise Refused("registered bridge returned an unrelated response")
                    store.finish(call_id, "returned", {"job": job_receipt, "hashes": hashes,
                                                       "response_digest": digest(response)})
                    return response["result"]
            except BaseException as error:
                quiescence = host.reconcile(call_id)
                store.finish(call_id, "uncertain", {"job": job_receipt, "hashes": hashes, "quiescence": quiescence,
                                                    "error_type": type(error).__name__, "replay_allowed": False})
                raise
