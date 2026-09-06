"""Strict local paths, finite resource limits and bounded registered Git."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import uuid

from core.runtime.continuous_worker.state import Refused, canonical, digest
from core.runtime.continuous_worker.contract import require_path, beneath, file_hash
from core.runtime.continuous_worker.windows_job import WindowsJobHost

SHA = re.compile(r"[0-9a-f]{64}")
OID = re.compile(r"[0-9a-f]{40}")
MAX_FILES = 4096
MAX_FILE = 16 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
PROTECTED = (".git", ".aide", ".github", "release/index")
RESERVED = re.compile(r"(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", re.I)


def fields(value, names):
    if not isinstance(value, dict) or set(value) != set(names.split()):
        raise Refused("unexpected object fields")


def identity(value, pattern=SHA):
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise Refused("invalid content identity")
    return value


def relative(name):
    if not isinstance(name, str) or len(name) > 240:
        raise Refused("invalid relative path")
    parts = name.split("/")
    if any(not p or p in (".", "..") or p.endswith((".", " ")) or
           any(ord(c) < 32 or c in '\\:*?"<>|' for c in p) or
           RESERVED.fullmatch(p) or p.casefold() == ".git" for p in parts):
        raise Refused("unsafe relative path")
    return name


def allowed_paths(paths):
    if not isinstance(paths, list) or not paths:
        raise Refused("explicit allowed paths required")
    for name in paths:
        relative(name)
        low = name.casefold()
        if any(low == p or low.startswith(p + "/") or p.startswith(low + "/") for p in PROTECTED):
            raise Refused("protected path cannot be admitted")


def bounded_bytes(path, maximum=MAX_FILE):
    path = require_path(str(path))
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise Refused("artifact byte limit exceeded")
    return data


def parse_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise Refused("duplicate JSON key")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=unique)
    except (ValueError, UnicodeError) as exc:
        raise Refused("invalid JSON artifact") from exc


def object_json(path):
    return parse_json(bounded_bytes(path))

def create_exact(path, data):
    """Publish only into an exclusive new name; never delete a failed artifact."""
    path = require_path(str(path))
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


class Git:
    def __init__(self, executable, sha256):
        self.executable = require_path(str(executable))
        self.sha256 = identity(sha256)

    def run(self, root, *args, data=b""):
        if file_hash(self.executable) != self.sha256:
            raise Refused("registered Git executable drift")
        if len(data) > MAX_FILE:
            raise Refused("Git input budget")
        with tempfile.TemporaryDirectory(prefix="aide-broker-git-") as temporary:
            output = Path(temporary) / "streams"
            receipt = WindowsJobHost().run(
                [str(self.executable), "--no-optional-locks", "-c", "core.fsmonitor=false",
                 "-c", "core.hooksPath=" + os.devnull, "-c", "core.autocrlf=false",
                 "-c", "core.attributesFile=" + os.devnull, "-C", str(root), *args],
                cwd=root, input_bytes=data, output_dir=output, job_id=uuid.uuid4().hex,
                timeout=30, output_limit=MAX_FILE, memory_limit=536870912, process_limit=8)
            if receipt["exit_code"] or receipt["reason"] != "exited" or not receipt["quiescent"]:
                raise Refused("bounded Git operation failed")
            return bounded_bytes(output / "stdout")

    def tree(self, root, commit):
        identity(commit, OID)
        if self.run(root, "rev-parse", "--show-object-format").strip() != b"sha1":
            raise Refused("only SHA-1 Git repositories admitted in this slice")
        tree = self.run(root, "rev-parse", commit + "^{tree}").decode().strip()
        identity(tree, OID)
        result = {}
        for line in self.run(root, "ls-tree", "-r", "-z", commit).split(b"\0"):
            if not line:
                continue
            meta, raw = line.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            name = relative(raw.decode("utf-8"))
            if kind != "blob" or mode not in ("100644", "100755"):
                raise Refused("symlinks and gitlinks are not admitted")
            result[name] = {"mode": mode, "oid": oid}
        return tree, result
