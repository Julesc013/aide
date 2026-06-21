"""Read-only Dominium Git snapshot reader."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - retained for portability.
    tomllib = None  # type: ignore[assignment]

from . import identity, integrity, models, operations
from .references import is_commit_sha, normalize_repo_path, path_has_symlink_escape, sha256_bytes, stable_id


class SnapshotError(ValueError):
    """Raised when a Dominium snapshot cannot be read safely."""


def _run_git(root: Path, args: list[str], *, text: bool = True) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    ledger = operations.active_ledger()
    family, allowed = operations.classify_git_args(args)
    command = ["git", "-C", str(root), *args]
    operation = "git " + " ".join(args)
    if ledger is not None and not allowed:
        ledger.record(
            operation,
            family=family,
            target="Dominium",
            classification="forbidden_git_refused_before_execution",
            allowed=False,
            source="snapshot.git_runner",
            observation_method=operations.COVERAGE_METHODS.get(family, "git_command_denylist"),
            return_code=None,
        )
        raise SnapshotError(f"forbidden git operation refused before execution: {operation}")
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=text,
    )
    if ledger is not None:
        ledger.record(
            operation,
            family=family,
            target="Dominium",
            classification="read_only_git_observation" if allowed else "forbidden_git_observation",
            allowed=allowed,
            source="snapshot.git_runner",
            observation_method=operations.COVERAGE_METHODS.get(family, "command_wrapper_observation"),
            return_code=result.returncode,
        )
    if result.returncode != 0:
        stderr = result.stderr if isinstance(result.stderr, str) else result.stderr.decode("utf-8", errors="replace")
        raise SnapshotError(f"git {' '.join(args)} failed: {stderr.strip()}")
    return result


def _git_text(root: Path, args: list[str]) -> str:
    result = _run_git(root, args, text=True)
    return str(result.stdout).strip()


def _git_bytes(root: Path, args: list[str]) -> bytes:
    result = _run_git(root, args, text=False)
    return bytes(result.stdout)


def assert_git_repo(root: Path) -> None:
    if not root.exists() or not root.is_dir():
        raise SnapshotError(f"Dominium root is not a directory: {root}")
    top = _git_text(root, ["rev-parse", "--show-toplevel"])
    if Path(top).resolve() != root.resolve():
        raise SnapshotError(f"ambiguous source root: {root} resolves to {top}")


def remote_url(root: Path) -> str:
    try:
        return _git_text(root, ["remote", "get-url", "origin"])
    except SnapshotError:
        return ""


def resolve_revision(root: Path, revision: str | None = None) -> str:
    rev = revision or "HEAD"
    resolved = _git_text(root, ["rev-parse", f"{rev}^{{commit}}"])
    if not is_commit_sha(resolved):
        raise SnapshotError(f"revision did not resolve to a commit SHA: {revision or 'HEAD'}")
    return resolved


def worktree_status(root: Path) -> str:
    return _git_text(root, ["status", "--short", "--branch"])


def porcelain_status(root: Path) -> str:
    return _git_text(root, ["status", "--porcelain"])


def current_branch(root: Path) -> str:
    return _git_text(root, ["branch", "--show-current"])


def local_head(root: Path) -> str:
    return resolve_revision(root, "HEAD")


def local_origin_main(root: Path) -> str | None:
    try:
        return resolve_revision(root, "origin/main")
    except SnapshotError:
        return None


def count_ahead_behind(root: Path, left: str, right: str) -> int | None:
    try:
        return int(_git_text(root, ["rev-list", "--count", f"{left}..{right}"]))
    except SnapshotError:
        return None


def git_object_bytes(root: Path, revision: str, rel_path: str) -> bytes:
    rel = normalize_repo_path(rel_path)
    return _git_bytes(root, ["show", f"{revision}:{rel}"])


def git_object_text(root: Path, revision: str, rel_path: str) -> str:
    return git_object_bytes(root, revision, rel_path).decode("utf-8")


def git_object_json(root: Path, revision: str, rel_path: str) -> dict[str, Any]:
    try:
        data = json.loads(git_object_text(root, revision, rel_path))
    except json.JSONDecodeError as exc:
        raise SnapshotError(f"Dominium JSON input failed to parse: {rel_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SnapshotError(f"Dominium JSON input root must be object: {rel_path}")
    return data


def git_object_toml(root: Path, revision: str, rel_path: str) -> dict[str, Any]:
    text = git_object_text(root, revision, rel_path)
    if tomllib is None:
        return _fallback_toml(text)
    data = tomllib.loads(text)
    return data if isinstance(data, dict) else {}


def _fallback_toml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    section: dict[str, Any] = data
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            key = line.strip("[]")
            section = data.setdefault(key, {})
            continue
        if "=" not in line:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        section[key] = value.strip('"')
    return data


def _tree_metadata(root: Path, revision: str, rel_path: str) -> dict[str, Any]:
    rel = normalize_repo_path(rel_path)
    output = _git_text(root, ["ls-tree", revision, rel])
    if not output:
        raise SnapshotError(f"required source missing at revision {revision}: {rel}")
    meta, _tab, _path = output.partition("\t")
    parts = meta.split()
    return {
        "mode": parts[0] if len(parts) > 0 else "",
        "object_type": parts[1] if len(parts) > 1 else "",
        "git_object": parts[2] if len(parts) > 2 else "",
    }


def git_object_metadata(root: Path, revision: str, rel_path: str) -> dict[str, Any]:
    return _tree_metadata(root, revision, rel_path)


def _queue_summary(root: Path, revision: str) -> dict[str, Any]:
    data = git_object_toml(root, revision, ".aide/queue/current.toml")
    current = data.get("current", {}) if isinstance(data.get("current"), dict) else {}
    return {
        "schema_version": data.get("schema_version", ""),
        "status": data.get("status", ""),
        "current_task": current.get("current_task") or current.get("task") or "",
        "result": current.get("result", ""),
        "next_task": current.get("next_task", ""),
        "alternate_next_task": current.get("alternate_next_task", ""),
    }


def build_source_snapshot(
    dominium_root: str | Path,
    *,
    revision: str | None = None,
    expected_revision: str | None = None,
    expected_repo_identity: str | None = identity.DEFAULT_DOMINIUM_IDENTITY,
    require_clean: bool = True,
) -> dict[str, Any]:
    root = Path(dominium_root).resolve()
    assert_git_repo(root)
    url = remote_url(root)
    parsed_identity = (
        identity.assert_expected_repository_identity(url, expected_identity=expected_repo_identity)
        if expected_repo_identity
        else identity.parse_repository_identity(url)
    )
    dirty = porcelain_status(root)
    if require_clean and dirty:
        raise SnapshotError("dirty authoritative input rejected by read-only seam")
    resolved = resolve_revision(root, revision)
    if expected_revision and resolved != expected_revision:
        raise SnapshotError(f"revision mismatch: expected {expected_revision}, got {resolved}")

    selected: list[dict[str, Any]] = []
    for item in models.SELECTED_DOMINIUM_INPUTS:
        rel = normalize_repo_path(str(item["path"]))
        if path_has_symlink_escape(root, rel):
            raise SnapshotError(f"symlink escape detected for source path: {rel}")
        meta = _tree_metadata(root, resolved, rel)
        payload = git_object_bytes(root, resolved, rel)
        selected.append(
            {
                "path": rel,
                "role": item["role"],
                "authority": item["authority"],
                "required": bool(item.get("required", False)),
                "mode": meta["mode"],
                "object_type": meta["object_type"],
                "git_object": meta["git_object"],
                "sha256": sha256_bytes(payload),
                "size_bytes": len(payload),
                "artifact_ref": f"aide://artifact/{stable_id('dominium-artifact', rel)}",
            }
        )

    origin_main = local_origin_main(root)
    head = local_head(root)
    freshness = {
        "branch": current_branch(root),
        "worktree_status": worktree_status(root),
        "local_head": head,
        "selected_revision": resolved,
        "local_origin_main": origin_main,
        "behind_origin_main": count_ahead_behind(root, "HEAD", "origin/main") if origin_main else 0,
        "selected_revision_is_local_head": resolved == head,
        "remote_ref_updated": False,
        "fetch_performed": False,
        "pull_performed": False,
        "checkout_performed": False,
    }
    snapshot = {
        "schema_version": "aide.dominium-readonly-seam.source-snapshot.v0",
        "repository_identity": {
            "root_name": root.name,
            "remote_url": url,
            "expected_identity": expected_repo_identity or "",
            **parsed_identity.as_dict(),
        },
        "source_revision": resolved,
        "source_ref": revision or "HEAD",
        "selected_file_count": len(selected),
        "selected_files": selected,
        "contract_inventory": [item for item in selected if str(item["path"]).startswith("contracts/")],
        "authority_input_inventory": [
            {
                "path": item["path"],
                "role": item["role"],
                "authority": item["authority"],
                "sha256": item["sha256"],
            }
            for item in selected
        ],
        "queue_status": _queue_summary(root, resolved),
        "freshness": freshness,
        "read_only_operations": {
            "git_fetch": False,
            "git_pull": False,
            "git_checkout": False,
            "remote_ref_update": False,
            "dominium_command_invocation": False,
            "dominium_file_write": False,
        },
    }
    integrity.finalize_source_snapshot(snapshot)
    return snapshot
