"""Temporary fixture workspace helpers for DistributionApplyEngine v0.

Paths use the portable intersection of POSIX and Windows filename rules. These
checks reject static aliases and unsafe fixtures; they do not establish a
hostile-writer sandbox or authorize real target-repository mutation.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import unicodedata
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class FixturePathError(ValueError):
    """A fixture path cannot be handled with the declared portability rules."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$", "CLOCK$"}
_RESERVED_NAMES.update(prefix + number for prefix in ("COM", "LPT") for number in "123456789¹²³")
_REPARSE_POINT = 0x400


def canonical_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_path_refusal(value: object) -> str | None:
    """Classify a portable file locator without consulting the filesystem.

    Both separators are accepted for input locators; empty/dot components,
    drive-qualified paths (including C:relative), streams, device names and
    Windows-trimmed aliases are refused rather than silently reinterpreted.
    """
    if not isinstance(value, str) or not value:
        return "nonportable_path_refused"
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return "absolute_path_refused"
    parts = normalized.split("/")
    if ".." in parts:
        return "path_traversal_refused"
    if any(part in ("", ".") for part in parts):
        return "nonportable_path_refused"
    if any(ord(char) < 32 or ord(char) == 127 or char in '<>:"|?*' for char in normalized):
        return "nonportable_path_refused"
    try:
        normalized.encode("utf-8")
    except UnicodeEncodeError:
        return "nonportable_path_refused"
    for part in parts:
        if part.endswith((" ", ".")) or part.split(".", 1)[0].rstrip(" ").upper() in _RESERVED_NAMES:
            return "nonportable_path_refused"
    return None


def is_unsafe_relative_path(value: str) -> bool:
    return relative_path_refusal(value) is not None


def _normalized_path(value: str) -> str:
    reason = relative_path_refusal(value)
    if reason:
        raise FixturePathError(reason)
    return value.replace("\\", "/")


def _inspect(path: Path) -> os.stat_result | None:
    try:
        observed = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(observed.st_mode) or getattr(observed, "st_file_attributes", 0) & _REPARSE_POINT:
        raise FixturePathError("symlink_reparse_refused")
    if not (stat.S_ISREG(observed.st_mode) or stat.S_ISDIR(observed.st_mode)):
        raise FixturePathError("non_regular_path_refused")
    if stat.S_ISREG(observed.st_mode) and observed.st_nlink != 1:
        raise FixturePathError("hardlink_refused")
    return observed


def _workspace_root(root: Path) -> Path:
    observed = _inspect(root)
    if observed is not None and not stat.S_ISDIR(observed.st_mode):
        raise FixturePathError("workspace_not_directory")
    # The caller supplies a trusted fixture root. Platform aliases above that
    # root may resolve (e.g. macOS temp roots); relative child links never may.
    return root.resolve()


def safe_join(root: Path, relative_path: str) -> Path:
    normalized = _normalized_path(relative_path)
    resolved_root = _workspace_root(root)
    candidate = resolved_root
    parts = normalized.split("/")
    for index, part in enumerate(parts):
        parent_state = _inspect(candidate)
        entries: list[Path] = []
        if parent_state is not None:
            entries = list(candidate.iterdir())
            folded = unicodedata.normalize("NFC", part).casefold()
            for existing in entries:
                if unicodedata.normalize("NFC", existing.name).casefold() == folded and existing.name != part:
                    raise FixturePathError("path_collision_refused")
        candidate = candidate / part
        observed = _inspect(candidate)
        if observed is not None and not any(existing.name == part for existing in entries):
            # Case-insensitive filesystems can resolve aliases that directory
            # enumeration does not expose as entries, notably Windows 8.3
            # short names. Only the exact enumerated name is admissible.
            raise FixturePathError("path_collision_refused")
        if index < len(parts) - 1 and observed is not None and not stat.S_ISDIR(observed.st_mode):
            raise FixturePathError("parent_not_directory")
    return candidate


def _validated_paths(paths: list[str]) -> dict[str, str]:
    """Reject duplicate locators, case/Unicode aliases and file/parent overlap."""
    result: dict[str, str] = {}
    prefixes: dict[str, str] = {}
    leaves: set[str] = set()
    parents: set[str] = set()
    for raw in sorted(paths):
        normalized = _normalized_path(raw)
        components = normalized.split("/")
        for count in range(1, len(components) + 1):
            prefix = "/".join(components[:count])
            key = unicodedata.normalize("NFC", prefix).casefold()
            if key in prefixes and prefixes[key] != prefix:
                raise FixturePathError("path_collision_refused")
            if count < len(components):
                if key in leaves:
                    raise FixturePathError("path_collision_refused")
                parents.add(key)
            prefixes[key] = prefix
        leaf = unicodedata.normalize("NFC", normalized).casefold()
        if leaf in leaves or leaf in parents:
            raise FixturePathError("path_collision_refused")
        leaves.add(leaf)
        result[raw] = normalized
    return result


def _validated_contents(files: dict[str, str]) -> dict[str, str]:
    if not isinstance(files, dict) or any(not isinstance(key, str) for key in files):
        raise ValueError("invalid fixture file map")
    paths = _validated_paths(list(files))
    result = {}
    for raw, normalized in paths.items():
        text = files[raw]
        if not isinstance(text, str):
            raise ValueError("fixture content must be text")
        text.encode("utf-8")
        result[normalized] = text
    return result


def write_initial_files(workspace_root: Path, files: dict[str, str]) -> None:
    planned = _validated_contents(files)
    targets = {rel: safe_join(workspace_root, rel) for rel in planned}
    # Complete preflight before the first directory or file write.
    if any(target.exists() for target in targets.values()):
        raise ValueError("initial fixture target already exists")
    for rel, content in planned.items():
        target = safe_join(workspace_root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)


def _file_digest(path: Path) -> str:
    before = _inspect(path)
    if before is None or not stat.S_ISREG(before.st_mode):
        raise FixturePathError("snapshot_file_missing")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns)
        if identity(opened) != identity(before):
            raise FixturePathError("snapshot_changed")
        digest = hashlib.sha256()
        remaining = before.st_size
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                raise FixturePathError("snapshot_changed")
            digest.update(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1) or identity(os.fstat(descriptor)) != identity(before):
            raise FixturePathError("snapshot_changed")
        after = _inspect(path)
        if after is None or identity(after) != identity(before):
            raise FixturePathError("snapshot_changed")
        return "sha256:" + digest.hexdigest()
    finally:
        os.close(descriptor)


def snapshot_tree(root: Path) -> dict[str, str]:
    resolved_root = _workspace_root(root)
    if not resolved_root.exists():
        return {}
    snapshot: dict[str, str] = {}
    directories = [resolved_root]
    observed_names: dict[str, str] = {}
    while directories:
        current = directories.pop()
        _inspect(current)
        for path in sorted(current.iterdir()):
            rel = path.relative_to(resolved_root).as_posix()
            if _normalized_path(rel) != rel:
                raise FixturePathError("nonportable_path_refused")
            key = unicodedata.normalize("NFC", rel).casefold()
            if key in observed_names and observed_names[key] != rel:
                raise FixturePathError("path_collision_refused")
            observed_names[key] = rel
            observed = _inspect(path)
            if observed is None:
                raise FixturePathError("snapshot_changed")
            if stat.S_ISDIR(observed.st_mode):
                directories.append(path)
            else:
                snapshot[rel] = _file_digest(path)
    return dict(sorted(snapshot.items()))


def restore_snapshot(root: Path, snapshot: dict[str, str], contents: dict[str, str]) -> None:
    planned = _validated_contents(contents)
    if not isinstance(snapshot, dict) or set(snapshot) != set(contents) or set(snapshot) != set(planned):
        raise ValueError("rollback snapshot/content keys do not match")
    for raw, expected in snapshot.items():
        if expected != sha256_text(contents[raw]):
            raise ValueError("rollback content digest mismatch")
    resolved_root = _workspace_root(root)
    if resolved_root == Path(resolved_root.anchor):
        raise ValueError("cannot restore a filesystem root")
    # Targets are validated lexically above. The old fixture may intentionally
    # contain a file where the restored snapshot needs a directory (or vice versa).
    # Refuse unreadable/linked/special existing trees before destructive cleanup.
    # This remains a fixture reset, NOT crash-atomic production rollback.
    snapshot_tree(root)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    write_initial_files(root, planned)


def tree_digest(root: Path) -> str:
    payload = json.dumps(snapshot_tree(root), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def directory_digest(root: Path) -> str:
    return tree_digest(root)


@contextmanager
def temporary_fixture_workspace(scenario_id: str) -> Iterator[Path]:
    if not isinstance(scenario_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", scenario_id):
        raise ValueError("invalid fixture scenario identifier")
    prefix = "aide-distribution-apply-" + scenario_id.replace("_", "-") + "-"
    with tempfile.TemporaryDirectory(prefix=prefix) as temp:
        root = Path(temp) / "target"
        root.mkdir(parents=True, exist_ok=True)
        yield root
