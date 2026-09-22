"""Strict admission and exact-source evidence helpers for the opt-in pilot."""
from __future__ import annotations

import hashlib
import json
import os
import math
import tempfile
import uuid
from pathlib import Path
import re
import subprocess

from .state import Refused, digest

SHA = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,119}$")
PROTECTED = (".git", ".aide/policies", ".aide/queue", ".github", "release/index")


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as src:
        while chunk := src.read(65536):
            h.update(chunk)
    return h.hexdigest()


def beneath(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def require_path(raw):
    path = Path(raw)
    if not path.is_absolute():
        raise Refused("paths must be absolute")
    # Reject junctions/symlinks through any existing ancestor.
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise Refused("symlink or junction in registered path")
    return path.resolve()


def registered_command(spec):
    if set(spec) != {"argv", "sha256", "inputs"} or not isinstance(spec["argv"], list) or not spec["argv"]:
        raise Refused("invalid registered command")
    if not all(isinstance(v, str) and "\0" not in v for v in spec["argv"]):
        raise Refused("command arguments must be literal strings")
    exe = require_path(spec["argv"][0])
    if not SHA.fullmatch(spec["sha256"]) or file_hash(exe) != spec["sha256"]:
        raise Refused("registered executable drift")
    if not isinstance(spec["inputs"], dict):
        raise Refused("registered input pins required")
    for name, pin in spec["inputs"].items():
        if file_hash(require_path(name)) != pin:
            raise Refused("registered command input drift")
    return list(spec["argv"])


def read_activation(path, expected_hash):
    raw = path.read_bytes()
    if not SHA.fullmatch(expected_hash) or hashlib.sha256(raw).hexdigest() != expected_hash:
        raise Refused("activation requires the exact operator-supplied file digest")
    data = json.loads(raw)
    required = {"schema", "runtime_files", "state_root", "expires_at", "limits", "codex",
                "git", "worker_models", "tasks", "qualification", "integration"}
    if set(data) != required or data["schema"] not in ("aide.continuous-worker.activation.v0", "aide.continuous-worker.activation.v1"):
        raise Refused("unknown activation fields or schema")
    state = require_path(data["state_root"])
    if beneath(state, Path(__file__).resolve().parents[3]):
        raise Refused("durable state must be outside the runtime checkout")
    if type(data["expires_at"]) not in (int, float) or not math.isfinite(data["expires_at"]):
        raise Refused("activation requires an absolute expiry timestamp")
    limits = data["limits"]
    bounds = {"max_attempts": (1, 2), "max_integration_queries": (3, 120), "max_processes": (1, 16), "max_sessions": (1, 4),
              "process_seconds": (1, 1800), "programme_seconds": (1, 7200),
              "output_bytes": (1024, 16777216), "memory_bytes": (134217728, 17179869184),
              "max_state_bytes": (1048576, 2147483648), "min_free_bytes": (1048576, 107374182400)}
    if set(limits) != set(bounds):
        raise Refused("all resource limits must be explicit")
    for key, (lo, hi) in bounds.items():
        if type(limits[key]) is not int or not lo <= limits[key] <= hi:
            raise Refused("invalid resource limit: " + key)
    qualification = data["qualification"]
    for key in ("isolated_worker_host", "credential_boundary", "integration_delegation"):
        record = qualification.get(key)
        if not record or set(record) != {"path", "sha256"}:
            raise Refused("missing externally reviewed qualification: " + key)
        source = require_path(record["path"])
        if file_hash(source) != record["sha256"]:
            raise Refused("qualification drift: " + key)
    runtime = Path(__file__).resolve().parent
    expected_files = {p.name for p in runtime.glob("*.py")}
    if set(data["runtime_files"]) != expected_files:
        raise Refused("runtime pin must enumerate every pilot Python source")
    for name, pin in data["runtime_files"].items():
        if file_hash(runtime / name) != pin:
            raise Refused("runtime source drift")
    if set(data["worker_models"]) != {"coding", "assurance"} or any(
            not isinstance(v, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", v)
            for v in data["worker_models"].values()):
        raise Refused("both worker models must be explicitly pinned")
    registered_command(data["codex"])
    registered_command(data["git"])
    if not isinstance(data["tasks"], list) or not 1 <= len(data["tasks"]) <= 2:
        raise Refused("pilot admits one or two tasks")
    ids = set()
    roots = []
    for task in data["tasks"]:
        fields = {"id", "source", "source_sha256", "workspace", "base", "allowed_paths", "depends_on",
                  "instructions", "test_commands", "repository"}
        if set(task) != fields or not ID.fullmatch(task["id"]) or task["id"] in ids:
            raise Refused("invalid or duplicate task")
        ids.add(task["id"])
        source = require_path(task["source"])
        if file_hash(source) != task["source_sha256"]:
            raise Refused("task admission source drift")
        workspace = require_path(task["workspace"])
        if not workspace.is_dir() or not (workspace / ".git").is_dir():
            raise Refused("pre-provisioned independent clone required")
        require_path(str(workspace / ".git"))
        # Linked worktrees share Git authority; this first host accepts independent clones only.
        if beneath(state, workspace) or beneath(workspace, state):
            raise Refused("workspace and durable state must be separate roots")
        if beneath(path, workspace) or beneath(runtime, workspace) or beneath(source, workspace):
            raise Refused("workers cannot own their activation/runtime/admission source")
        if any(beneath(workspace, old) or beneath(old, workspace) for old in roots):
            raise Refused("overlapping writer workspaces")
        roots.append(workspace)
        if not task["allowed_paths"] or not 1 <= len(task["test_commands"]) <= 16:
            raise Refused("allowed paths and independent test commands required")
        for allowed in task["allowed_paths"]:
            if (not isinstance(allowed, str) or allowed.startswith(("/", "\\")) or "\\" in allowed
                    or any(part in ("", ".", "..") for part in allowed.split("/"))):
                raise Refused("invalid allowed path")
            if any(allowed == p or allowed.startswith(p + "/") or p.startswith(allowed + "/") for p in PROTECTED):
                raise Refused("pilot cannot edit policy, queue, CI or release acceptance")
        for command in task["test_commands"]:
            registered_command(command)
    for task in data["tasks"]:
        if any(dep not in ids or dep == task["id"] for dep in task["depends_on"]):
            raise Refused("unknown or self dependency")
    if len(data["tasks"]) == 2 and all(t["depends_on"] for t in data["tasks"]):
        raise Refused("cyclic pilot dependencies")
    if not data["integration"]:
        raise Refused("live activation requires a registered legitimate integration broker")
    v1 = data["schema"] == "aide.continuous-worker.activation.v1"
    integration_fields = {"query", "apply", "cwd"}
    operations = ["query", "apply"]
    if v1:
        integration_fields |= {"authority", "reconcile", "exchange_root", "broker_runtime_files"}
        operations.extend(("authority", "reconcile"))
        exchange = require_path(data["integration"]["exchange_root"])
        if exchange == state or not beneath(exchange, state):
            raise Refused("v1 exchange must be a dedicated child of budgeted coordinator state")
        broker_sources = runtime.parent / "integration_broker"
        expected_broker = {p.name for p in broker_sources.glob("*.py")}
        if set(data["integration"]["broker_runtime_files"]) != expected_broker:
            raise Refused("v1 broker runtime pin must enumerate every source")
        for name, pin in data["integration"]["broker_runtime_files"].items():
            if file_hash(broker_sources / name) != pin:
                raise Refused("broker runtime source drift")
        if len(data["git"]["argv"]) != 1:
            raise Refused("v1 candidate handoff requires the exact registered Git executable")
    if set(data["integration"]) != integration_fields:
        raise Refused("unknown integration fields")
    for kind in operations:
        broker = data["integration"][kind]
        registered_command(broker)
        exe_name = Path(broker["argv"][0]).name.lower()
        if exe_name.startswith("python"):
            args = broker["argv"]
            if len(args) < 5 or args[1:3] != ["-I", "-B"]:
                raise Refused("Python brokers require an isolated pinned script entrypoint")
            entrypoint = str(require_path(args[3]))
            if entrypoint not in broker["inputs"] or Path(entrypoint).suffix != ".py":
                raise Refused("actual broker entrypoint must be explicitly pinned")
        elif Path(exe_name).suffix != ".exe":
            raise Refused("broker must be a standalone executable or isolated Python script")
        for arg in broker["argv"][1:]:
            if Path(arg).is_absolute():
                if str(require_path(arg)) not in broker["inputs"]:
                    raise Refused("broker file argument lacks an input pin")
        for raw in [broker["argv"][0], *broker["inputs"]]:
            entry = require_path(raw)
            if any(beneath(entry, root) for root in roots):
                raise Refused("integration broker must be outside worker clones")
        if not isinstance(data["integration"].get("cwd"), str):
            raise Refused("integration requires a protected working directory")
        broker_cwd = require_path(data["integration"]["cwd"])
        if any(beneath(broker_cwd, root) for root in roots):
            raise Refused("integration must not execute in a worker clone")
    protected = [path, runtime, state]
    protected += [require_path(t["source"]) for t in data["tasks"]]
    protected += [require_path(v["path"]) for v in qualification.values()]
    for command in [data["codex"], data["git"], *(data["integration"][kind] for kind in operations)]:
        protected += [require_path(command["argv"][0]), *(require_path(p) for p in command["inputs"])]
    if any(beneath(p, root) for p in protected for root in roots):
        raise Refused("worker clone contains programme authority or executable inputs")
    return data


def git(command, workspace, *args):
    from .windows_job import WindowsJobHost
    argv = [*command, "--no-optional-locks", "-c", "core.fsmonitor=false",
            "-c", "core.hooksPath=" + os.devnull, "-C", str(workspace), *args]
    with tempfile.TemporaryDirectory(prefix="aide-continuous-git-") as folder:
        output = Path(folder) / "observation"
        receipt = WindowsJobHost().run(
            argv, cwd=workspace, input_bytes=b"", output_dir=output, job_id=uuid.uuid4().hex,
            timeout=30, output_limit=16777216, memory_limit=536870912, process_limit=8)
        if receipt["exit_code"] or receipt["reason"] != "exited" or not receipt["quiescent"]:
            raise Refused("bounded Git observation failed")
        return (output / "stdout").read_bytes()


def snapshot(command, workspace):
    workspace = Path(workspace)
    git_dir = require_path(str(workspace / ".git"))
    metadata = {}
    for path in [git_dir / "config", git_dir / "HEAD", *(git_dir / "hooks").glob("*"), *(git_dir / "info").glob("*")]:
        if path.is_file():
            metadata[str(path.relative_to(git_dir))] = file_hash(require_path(str(path)))
    head = git(command, workspace, "rev-parse", "HEAD").decode().strip()
    index = git(command, workspace, "ls-files", "--stage", "-z")
    raw = git(command, workspace, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    files = {}
    total = 0
    for name in sorted(set(raw.decode("utf-8").split("\0")) - {""}):
        target = require_path(str(workspace / name))
        if not beneath(target, workspace) or name.startswith(".git/"):
            raise Refused("unsafe snapshot path")
        if target.exists():
            if not target.is_file():
                raise Refused("unsupported snapshot entry")
            total += target.stat().st_size
            if total > 1073741824:
                raise Refused("pilot snapshot size limit")
            files[name] = file_hash(target)
        else:
            files[name] = None
    # File mode / index effects are part of the evidence as well as byte contents.
    diff = git(command, workspace, "diff", "--binary", "--no-ext-diff", "--no-textconv", "HEAD")
    names = git(command, workspace, "diff", "--name-only", "-z", "--no-renames", "HEAD").decode().split("\0")
    observation = {"head": head, "files": files, "diff_sha256": hashlib.sha256(diff).hexdigest(),
                   "index_sha256": hashlib.sha256(index).hexdigest(), "metadata": metadata,
                   "git_changed": sorted(set(names) - {""})}
    return observation | {"identity": digest(observation)}


def changed(before, after, allowed):
    if before["head"] != after["head"]:
        raise Refused("worker moved the approved Git base")
    if before["index_sha256"] != after["index_sha256"] or before["metadata"] != after["metadata"]:
        raise Refused("worker mutated Git index or control metadata")
    names = sorted(set(after["git_changed"]) | {
        name for name in set(before["files"]) | set(after["files"])
        if before["files"].get(name) != after["files"].get(name)})
    for name in names:
        if not any(name == p or name.startswith(p + "/") for p in allowed):
            raise Refused("patch escaped admitted paths: " + name)
    if not names:
        raise Refused("no content progress")
    return sorted(names)

