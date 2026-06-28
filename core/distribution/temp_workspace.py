"""Temporary fixture workspace helpers for DistributionApplyEngine v0."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


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


def is_unsafe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    if not normalized or normalized.startswith("/") or normalized.startswith("//"):
        return True
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] == "/":
        return True
    parts = [part for part in normalized.split("/") if part]
    return any(part == ".." for part in parts)


def safe_join(root: Path, relative_path: str) -> Path:
    if is_unsafe_relative_path(relative_path):
        raise ValueError(f"unsafe fixture path: {relative_path}")
    candidate = (root / relative_path).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(f"fixture path escapes workspace: {relative_path}")
    return candidate


def write_initial_files(workspace_root: Path, files: dict[str, str]) -> None:
    for rel, content in sorted(files.items()):
        target = safe_join(workspace_root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def snapshot_tree(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    if not root.exists():
        return snapshot
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            snapshot[rel] = sha256_bytes(path.read_bytes())
    return snapshot


def restore_snapshot(root: Path, snapshot: dict[str, str], contents: dict[str, str]) -> None:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    for rel in sorted(snapshot):
        write_text(safe_join(root, rel), contents[rel])


def tree_digest(root: Path) -> str:
    payload = json.dumps(snapshot_tree(root), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def directory_digest(root: Path) -> str:
    entries: dict[str, str] = {}
    if root.exists():
        for path in sorted(root.rglob("*")):
            if path.is_file():
                entries[path.relative_to(root).as_posix()] = sha256_bytes(path.read_bytes())
    payload = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


@contextmanager
def temporary_fixture_workspace(scenario_id: str) -> Iterator[Path]:
    prefix = "aide-distribution-apply-" + scenario_id.replace("_", "-") + "-"
    with tempfile.TemporaryDirectory(prefix=prefix) as temp:
        root = Path(temp) / "target"
        root.mkdir(parents=True, exist_ok=True)
        yield root
