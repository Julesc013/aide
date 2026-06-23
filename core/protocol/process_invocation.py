"""Generic capability invocation and binding protocol records."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


VALID_ARGUMENT_KINDS = {
    "literal",
    "workspace_path",
    "artifact_path",
    "bounded_invocation_value",
}


@dataclass(frozen=True)
class ArgumentToken:
    kind: str
    value: str

    def __post_init__(self) -> None:
        if self.kind not in VALID_ARGUMENT_KINDS:
            raise ValueError(f"unsupported argument kind: {self.kind}")
        if not isinstance(self.value, str) or self.value == "":
            raise ValueError("argument token value must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "value": self.value}


@dataclass(frozen=True)
class CapabilityInvocation:
    invocation_ref: str
    capability_ref: str
    values: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.invocation_ref:
            raise ValueError("invocation_ref is required")
        if not self.capability_ref:
            raise ValueError("capability_ref is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "invocation_ref": self.invocation_ref,
            "capability_ref": self.capability_ref,
            "values": dict(self.values),
        }


@dataclass(frozen=True)
class CapabilityBinding:
    capability_ref: str
    provider_id: str
    provider_spec_ref: str = ""
    provider_spec: Any = None
    decoder_id: str = ""
    state_probe_id: str = ""
    scrubber_id: str = ""
    conformance_profile_ref: str = ""

    def __post_init__(self) -> None:
        if not self.capability_ref:
            raise ValueError("capability_ref is required")
        if not self.provider_id:
            raise ValueError("provider_id is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_ref": self.capability_ref,
            "provider_id": self.provider_id,
            "provider_spec_ref": self.provider_spec_ref,
            "decoder_id": self.decoder_id,
            "state_probe_id": self.state_probe_id,
            "scrubber_id": self.scrubber_id,
            "conformance_profile_ref": self.conformance_profile_ref,
        }
