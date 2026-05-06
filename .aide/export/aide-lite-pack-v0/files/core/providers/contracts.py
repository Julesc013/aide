"""Small offline provider metadata contracts.

These dataclasses are intentionally inert. They describe provider families and
adapter expectations; they do not expose any live provider-call surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ProviderClass(str, Enum):
    DETERMINISTIC = "deterministic"
    HUMAN = "human"
    LOCAL_MODEL = "local_model"
    REMOTE_MODEL = "remote_model"
    AGGREGATOR = "aggregator"


class AdapterClass(str, Enum):
    DETERMINISTIC_TOOL = "deterministic_tool"
    HUMAN_REVIEW = "human_review"
    LOCAL_MODEL = "local_model"
    REMOTE_MODEL = "remote_model"
    AGGREGATOR = "aggregator"
    UNKNOWN = "unknown"


class PrivacyClass(str, Enum):
    LOCAL = "local"
    REMOTE = "remote"
    HUMAN = "human"
    UNKNOWN = "unknown"


class CapabilityStatus(str, Enum):
    SUPPORTED_BY_CONTRACT = "supported_by_contract"
    PLANNED = "planned"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"
    REQUIRES_FUTURE_PROBE = "requires_future_probe"


@dataclass(frozen=True)
class ProviderMetadata:
    provider_id: str
    display_name: str
    adapter_class: str
    provider_class: str
    privacy_class: str
    credentials_required: bool
    credentials_location: str
    live_calls_allowed_in_q20: bool
    status: str
    notes: str = ""


@dataclass(frozen=True)
class ProviderCapability:
    provider_id: str
    capabilities: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderStatus:
    provider_adapter_contract: str
    live_provider_calls: bool
    live_model_calls: bool
    credentials_configured: bool
    gateway_forwarding: bool
    local_model_setup: bool


@dataclass(frozen=True)
class AdapterContract:
    adapter_id: str
    provider_id: str
    adapter_class: str
    capabilities: tuple[str, ...]
    credential_requirements: tuple[str, ...]
    privacy_class: str
    call_policy: dict[str, bool]
    cache_policy: dict[str, bool]
    route_policy: dict[str, bool]
    health_policy: dict[str, bool]
    status_policy: dict[str, bool]
    no_call_boundary: dict[str, bool]
