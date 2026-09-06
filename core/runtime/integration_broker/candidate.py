"""Frozen regular-file content handoff, independently reproducible as a Git tree."""
from __future__ import annotations

import hashlib
from pathlib import Path
import uuid

from .common import (Refused, MAX_FILES, MAX_FILE, MAX_TOTAL, OID, fields, identity,
                     relative, allowed_paths, bounded_bytes, object_json, create_exact,
                     require_path, beneath, canonical, digest)


def blob_oid(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def tree_oid(entries):
    root = {}
    for name, entry in entries.items():
        cursor = root
        parts = relative(name).split("/")
        for part in parts[:-1]:
            previous = cursor.setdefault(part, {})
            if not isinstance(previous, dict):
                raise Refused("file/directory collision")
            cursor = previous
        if parts[-1] in cursor:
            raise Refused("file/directory collision")
        cursor[parts[-1]] = (entry["mode"], entry["oid"])

    def visit(node):
        body = bytearray()
        for name, item in sorted(node.items(), key=lambda pair:
                                 (pair[0] + ("/" if isinstance(pair[1], dict) else "")).encode()):
            mode, oid = ("40000", visit(item)) if isinstance(item, dict) else item
            body.extend(mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(oid))
        return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()
    return visit(root)


def validate_manifest(manifest):
    fields(manifest, "schema repository base base_tree candidate_tree allowed_paths files")
    if manifest["schema"] not in ("aide.broker.candidate.v1", "aide.broker.candidate.v2"):
        raise Refused("unknown candidate schema")
    for name in ("base", "base_tree", "candidate_tree"):
        identity(manifest[name], OID)
    allowed_paths(manifest["allowed_paths"])
    files = manifest["files"]
    if not isinstance(files, dict) or not 1 <= len(files) <= MAX_FILES:
        raise Refused("candidate entry budget")
    total = 0
    names = set()
    for name, entry in files.items():
        relative(name)
        folded = name.casefold()
        if folded in names:
            raise Refused("case-colliding candidate paths")
        names.add(folded)
        if entry is None and manifest["schema"] == "aide.broker.candidate.v2":
            continue
        fields(entry, "mode oid sha256 size")
        if entry["mode"] not in ("100644", "100755"):
            raise Refused("unsupported file mode")
        identity(entry["oid"], OID)
        identity(entry["sha256"])
        if type(entry["size"]) is not int or not 0 <= entry["size"] <= MAX_FILE:
            raise Refused("file byte budget")
        total += entry["size"]
    if total > MAX_TOTAL:
        raise Refused("candidate total byte budget")
    # Directory case aliases must also be refused on Windows.
    prefixes = {}
    for name in files:
        parts = name.split("/")
        for end in range(1, len(parts) + 1):
            prefix = "/".join(parts[:end])
            if prefixes.setdefault(prefix.casefold(), prefix) != prefix:
                raise Refused("case-colliding directory paths")
    if manifest["schema"] == "aide.broker.candidate.v1" and tree_oid(files) != manifest["candidate_tree"]:
        raise Refused("candidate Git tree mismatch")


def verify_changes(manifest, base_files):
    current = manifest["files"]
    if manifest["schema"] == "aide.broker.candidate.v2":
        merged = dict(base_files)
        for name, entry in current.items():
            value = None if entry is None else {k: entry[k] for k in ("mode", "oid")}
            if value == base_files.get(name):
                raise Refused("redundant or unknown deletion in change-set")
            if value is None:
                merged.pop(name)
            else:
                merged[name] = value
        prefixes = {}
        for name in merged:
            parts = name.split("/")
            for end in range(1, len(parts) + 1):
                prefix = "/".join(parts[:end])
                if prefixes.setdefault(prefix.casefold(), prefix) != prefix:
                    raise Refused("case-colliding base overlay paths")
        if tree_oid(merged) != manifest["candidate_tree"]:
            raise Refused("candidate base overlay tree mismatch")
        changes = list(current)
    else:
        changes = [name for name in set(current) | set(base_files)
                   if ({k: current[name][k] for k in ("mode", "oid")} if name in current else None)
                   != base_files.get(name)]
    if not changes:
        raise Refused("candidate makes no content progress")
    for name in changes:
        if not any(name == p or name.startswith(p + "/") for p in manifest["allowed_paths"]):
            raise Refused("candidate escaped allowed paths")
    return sorted(changes)


def literal_checkout(git, workspace, base):
    """Pre-coding admission: only literal Git blob bytes, never filter evaluation."""
    workspace = require_path(str(workspace))
    if git.run(workspace, "rev-parse", "HEAD").decode().strip() != base:
        raise Refused("moved literal checkout base")
    tree, files = git.tree(workspace, base)
    for name, entry in files.items():
        if blob_oid(bounded_bytes(workspace / name)) != entry["oid"]:
            raise Refused("worker clone must contain literal Git blob bytes; transformed checkout refused")
    return {"schema": "aide.broker.literal-checkout.v1", "base": base,
            "base_tree": tree, "file_count": len(files), "files_digest": digest(files)}


def freeze_candidate(git, workspace, exchange, *, repository, base, allowed, checkout, max_total=MAX_TOTAL):
    workspace, exchange = require_path(str(workspace)), require_path(str(exchange))
    if beneath(exchange, workspace) or beneath(workspace, exchange):
        raise Refused("handoff must be outside the worker workspace")
    allowed_paths(allowed)
    if type(max_total) is not int or not 1 <= max_total <= MAX_TOTAL:
        raise Refused("invalid candidate byte reservation")
    if git.run(workspace, "rev-parse", "HEAD").decode().strip() != base:
        raise Refused("moved worker base")
    base_tree, base_files = git.tree(workspace, base)
    expected_checkout = {"schema": "aide.broker.literal-checkout.v1", "base": base,
                         "base_tree": base_tree, "file_count": len(base_files), "files_digest": digest(base_files)}
    if checkout != expected_checkout:
        raise Refused("exact pre-coding literal checkout evidence required")
    if git.run(workspace, "diff", "--cached", "--no-ext-diff", "--no-textconv", "--name-only", base).strip():
        raise Refused("worker Git index differs from admitted base")
    index_before = git.run(workspace, "ls-files", "--stage", "-z")
    names_before = git.run(workspace, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    names = sorted(set(names_before.decode("utf-8").split("\0")) - {""})
    files, blobs, observed, total = {}, {}, {}, 0
    merged = dict(base_files)
    for name in names:
        relative(name)
        path = require_path(str(workspace / name))
        if not beneath(path, workspace):
            raise Refused("candidate path escaped workspace")
        if not path.exists():
            if name not in base_files:
                raise Refused("new file vanished")
            files[name] = None
            observed[name] = None
            merged.pop(name)
            continue
        data = bounded_bytes(path)
        oid = blob_oid(data)
        pin = hashlib.sha256(data).hexdigest()
        observed[name] = pin
        if base_files.get(name, {}).get("oid") == oid:
            continue
        total += len(data)
        if total > max_total:
            raise Refused("candidate total byte budget")
        blobs[pin] = data
        files[name] = {"mode": base_files.get(name, {}).get("mode", "100644"),
                       "oid": oid, "sha256": pin, "size": len(data)}
        merged[name] = {k: files[name][k] for k in ("mode", "oid")}
        if len(files) > MAX_FILES:
            raise Refused("candidate entry budget")
    manifest = {"schema": "aide.broker.candidate.v2", "repository": repository,
                "base": base, "base_tree": base_tree, "candidate_tree": tree_oid(merged),
                "allowed_paths": allowed, "files": files}
    validate_manifest(manifest)
    verify_changes(manifest, base_files)
    # Re-read every byte and metadata input before publishing a coherent handoff.
    if (git.run(workspace, "rev-parse", "HEAD").decode().strip() != base or
            git.run(workspace, "ls-files", "--stage", "-z") != index_before or
            git.run(workspace, "ls-files", "-z", "--cached", "--others", "--exclude-standard") != names_before):
        raise Refused("workspace changed during freeze")
    for name in names:
        path = workspace / name
        if observed[name] is None:
            if path.exists():
                raise Refused("deleted file reappeared")
        elif hashlib.sha256(bounded_bytes(path)).hexdigest() != observed[name]:
            raise Refused("candidate changed during freeze")
    # All validation above precedes publication effects; partial bundles are retained.
    folder = exchange / uuid.uuid4().hex
    folder.mkdir()
    (folder / "blobs").mkdir()
    for pin, data in blobs.items():
        create_exact(folder / "blobs" / pin, data)
    create_exact(folder / "manifest.json", canonical(manifest).encode())
    return {"bundle": folder.name, "manifest_sha256": digest(manifest)}


def read_candidate(exchange, ref):
    fields(ref, "bundle manifest_sha256")
    if not isinstance(ref["bundle"], str) or len(ref["bundle"]) != 32 or any(
            c not in "0123456789abcdef" for c in ref["bundle"]):
        raise Refused("invalid bundle reference")
    identity(ref["manifest_sha256"])
    folder = require_path(str(exchange / ref["bundle"]))
    manifest = object_json(folder / "manifest.json")
    if digest(manifest) != ref["manifest_sha256"]:
        raise Refused("manifest changed")
    validate_manifest(manifest)
    blobs = {}
    for entry in manifest["files"].values():
        if entry is None:
            continue
        pin = entry["sha256"]
        if pin not in blobs:
            blobs[pin] = bounded_bytes(folder / "blobs" / pin)
        data = blobs[pin]
        if len(data) != entry["size"] or hashlib.sha256(data).hexdigest() != pin or blob_oid(data) != entry["oid"]:
            raise Refused("candidate blob changed")
    return manifest, blobs


def materialize(git, directory, manifest, blobs, *, base_repository=None):
    """Fill an exclusively owned empty directory, reading trusted base objects only."""
    git.run(directory, "init", "--bare", "--object-format=sha1")
    if manifest["schema"] == "aide.broker.candidate.v2":
        if base_repository is None:
            raise Refused("trusted base repository required for delta handoff")
        base_repository = require_path(str(base_repository))
        git.validate_store(base_repository, manifest["base"])
        base_tree, base_files = git.tree(base_repository, manifest["base"])
        if base_tree != manifest["base_tree"]:
            raise Refused("trusted base tree changed")
        verify_changes(manifest, base_files)
        raw = git.run(base_repository, "rev-parse", "--git-path", "objects").decode().strip()
        objects = require_path(str(base_repository / raw))
        if not beneath(objects, base_repository) or not objects.is_dir():
            raise Refused("trusted base object directory escaped admitted repository")
        # Only the protected broker repository supplies unchanged objects. The
        # mutable worker object database is never an alternate or import source.
        create_exact(directory / "objects" / "info" / "alternates",
                     (str(objects).replace("\\", "/") + "\n").encode())
        git.run(directory, "read-tree", manifest["base_tree"])
    lines = []
    for name, entry in sorted(manifest["files"].items()):
        if entry is None:
            lines.append(("0 " + "0" * 40 + "\t" + name).encode() + b"\0")
            continue
        oid = git.run(directory, "hash-object", "-w", "--stdin", data=blobs[entry["sha256"]]).decode().strip()
        if oid != entry["oid"]:
            raise Refused("materialized blob identity mismatch")
        lines.append((entry["mode"] + " " + oid + "\t" + name).encode() + b"\0")
    git.run(directory, "update-index", "-z", "--index-info", data=b"".join(lines))
    tree = git.run(directory, "write-tree").decode().strip()
    if tree != manifest["candidate_tree"]:
        raise Refused("materialized candidate tree mismatch")
    return tree
