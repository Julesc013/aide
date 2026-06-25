"""Filesystem content-addressed artifact store for local Service fixtures."""

from __future__ import annotations

import hashlib
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


class ArtifactStoreError(ValueError):
    """Raised for fail-closed artifact store refusals."""


@dataclass(frozen=True)
class ArtifactWrite:
    digest: str
    size: int
    path: Path
    deduplicated: bool


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validate_digest(digest: str) -> str:
    if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
        raise ArtifactStoreError("artifact_digest_invalid")
    hex_part = digest.removeprefix("sha256:")
    if any(ch not in "0123456789abcdef" for ch in hex_part):
        raise ArtifactStoreError("artifact_digest_invalid")
    return hex_part


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.payload_root = self.root / "artifacts" / "sha256"
        self.temp_root = self.root / "temp"
        self.payload_root.mkdir(parents=True, exist_ok=True)
        self.temp_root.mkdir(parents=True, exist_ok=True)

    def payload_path(self, digest: str) -> Path:
        hex_part = validate_digest(digest)
        return self.payload_root / hex_part[:2] / hex_part

    def write(self, payload: bytes, *, expected_digest: str | None = None) -> ArtifactWrite:
        actual_digest = sha256_bytes(payload)
        if expected_digest is not None and expected_digest != actual_digest:
            raise ArtifactStoreError("artifact_digest_mismatch")
        target = self.payload_path(actual_digest)
        if target.exists():
            if not target.is_file() or target.is_symlink():
                raise ArtifactStoreError("artifact_payload_not_regular")
            if sha256_bytes(target.read_bytes()) != actual_digest:
                raise ArtifactStoreError("artifact_existing_payload_mismatch")
            return ArtifactWrite(actual_digest, len(payload), target, True)
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix="artifact-", suffix=".tmp", dir=self.temp_root)
        temp_path = Path(temp_name)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            if sha256_bytes(temp_path.read_bytes()) != actual_digest:
                raise ArtifactStoreError("artifact_temp_digest_mismatch")
            os.replace(temp_path, target)
            if sha256_bytes(target.read_bytes()) != actual_digest:
                raise ArtifactStoreError("artifact_persisted_digest_mismatch")
            return ArtifactWrite(actual_digest, len(payload), target, False)
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def read(self, digest: str) -> bytes:
        target = self.payload_path(digest)
        if not target.exists():
            raise ArtifactStoreError("artifact_missing")
        if target.is_symlink() or not target.is_file():
            raise ArtifactStoreError("artifact_payload_not_regular")
        payload = target.read_bytes()
        if sha256_bytes(payload) != digest:
            raise ArtifactStoreError("artifact_digest_mismatch")
        return payload
