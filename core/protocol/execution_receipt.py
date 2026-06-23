"""Neutral execution receipt and outcome protocol records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def digest_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_json(data: Any) -> str:
    return digest_text(stable_json(data))


def stream_summary(text: str, *, limit: int = 800) -> dict[str, Any]:
    encoded = text.encode("utf-8")
    return {
        "byte_count": len(encoded),
        "sha256": "sha256:" + hashlib.sha256(encoded).hexdigest(),
        "excerpt": text[:limit],
    }


@dataclass(frozen=True)
class CapabilityOutcome:
    transport_outcome: str
    process_outcome: str
    decoder_outcome: str
    domain_outcome: str
    validation_outcome: str
    evidence_completeness: str
    reason_code: str = ""
    message: str = ""
    domain_result: Mapping[str, Any] | None = None
    refusal: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "transport_outcome": self.transport_outcome,
            "process_outcome": self.process_outcome,
            "decoder_outcome": self.decoder_outcome,
            "domain_outcome": self.domain_outcome,
            "validation_outcome": self.validation_outcome,
            "evidence_completeness": self.evidence_completeness,
            "reason_code": self.reason_code,
            "message": self.message,
            "domain_result": dict(self.domain_result or {}),
            "refusal": dict(self.refusal or {}),
        }


@dataclass(frozen=True)
class ProcessExecutionReceipt:
    capability_ref: str
    invocation_ref: str
    provider_ref: str
    launcher_call_count: int
    executable_identity: str
    executable_digest: str
    argv_digest: str
    redacted_environment_manifest_digest: str
    return_code: int | None
    timed_out: bool
    cancelled: bool
    stdout: Mapping[str, Any]
    stderr: Mapping[str, Any]
    decoder_ref: str
    before_state_ref: str
    after_state_ref: str
    mutation_observation: str
    probe_coverage: list[str]
    started_at: str
    ended_at: str
    shell: bool = False
    working_directory_ref: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_ref": self.capability_ref,
            "invocation_ref": self.invocation_ref,
            "provider_ref": self.provider_ref,
            "launcher_call_count": self.launcher_call_count,
            "executable_identity": self.executable_identity,
            "executable_digest": self.executable_digest,
            "argv_digest": self.argv_digest,
            "redacted_environment_manifest_digest": self.redacted_environment_manifest_digest,
            "return_code": self.return_code,
            "timed_out": self.timed_out,
            "cancelled": self.cancelled,
            "stdout": dict(self.stdout),
            "stderr": dict(self.stderr),
            "decoder_ref": self.decoder_ref,
            "before_state_ref": self.before_state_ref,
            "after_state_ref": self.after_state_ref,
            "mutation_observation": self.mutation_observation,
            "probe_coverage": list(self.probe_coverage),
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "shell": self.shell,
            "working_directory_ref": self.working_directory_ref,
            "metadata": dict(self.metadata),
        }
