"""Reference, path, and digest helpers for the Dominium seam."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any


SHA256_PREFIX = "sha256:"
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SAFE_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._~@+=:, -]+$")
AIDE_REF_RE = re.compile(r"^aide://(?P<kind>[A-Za-z0-9._~-]+)/(?P<object_id>[A-Za-z0-9._~@+=:,-]+)$")


def sha256_bytes(payload: bytes) -> str:
    return SHA256_PREFIX + hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return SHA256_PREFIX + digest.hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def stable_id(prefix: str, value: str, *, length: int = 16) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]
    return f"{prefix}-{digest}"


def stable_ref(kind: str, object_id: str) -> str:
    return f"aide://{kind}/{object_id}"


def parse_stable_ref(value: Any) -> tuple[str, str]:
    if not isinstance(value, str):
        raise ValueError("ReferenceID must be a string")
    if "?" in value or "#" in value or "\\" in value:
        raise ValueError(f"invalid ReferenceID syntax: {value}")
    match = AIDE_REF_RE.match(value)
    if not match:
        raise ValueError(f"invalid ReferenceID syntax: {value}")
    kind = match.group("kind")
    object_id = match.group("object_id")
    if ".." in object_id or "/" in object_id:
        raise ValueError(f"invalid ReferenceID object id: {value}")
    return kind, object_id


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(SHA256_PREFIX) and bool(HEX_RE.match(value[len(SHA256_PREFIX) :]))


def is_commit_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(COMMIT_RE.match(value))


def normalize_repo_path(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("repo-relative path must be a non-empty string")
    raw = value.replace("\\", "/")
    if "\x00" in raw:
        raise ValueError("repo-relative path must not contain NUL")
    if raw.startswith("/") or raw.startswith("//"):
        raise ValueError(f"absolute path is not allowed: {value}")
    if re.match(r"^[A-Za-z]:", raw):
        raise ValueError(f"drive-qualified path is not allowed: {value}")
    parts = [part for part in raw.split("/") if part]
    if not parts or any(part in {".", ".."} for part in parts):
        raise ValueError(f"path traversal is not allowed: {value}")
    for part in parts:
        if not SAFE_SEGMENT_RE.match(part):
            raise ValueError(f"unsupported path segment: {part}")
    return "/".join(parts)


def assert_inside_root(root: Path, child: Path) -> None:
    root_resolved = root.resolve()
    child_resolved = child.resolve()
    try:
        child_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"path escapes root: {child}") from exc


def local_path_for_repo_rel(root: Path, rel: str) -> Path:
    normalized = normalize_repo_path(rel)
    path = root / Path(normalized)
    assert_inside_root(root, path)
    return path


def path_has_symlink_escape(root: Path, rel: str) -> bool:
    try:
        path = local_path_for_repo_rel(root, rel)
    except ValueError:
        return True
    root_resolved = root.resolve()
    current = root_resolved
    for part in Path(rel.replace("\\", "/")).parts:
        current = current / part
        if current.exists() and os.path.islink(current):
            try:
                current.resolve().relative_to(root_resolved)
            except ValueError:
                return True
    try:
        path.resolve().relative_to(root_resolved)
    except ValueError:
        return True
    return False
