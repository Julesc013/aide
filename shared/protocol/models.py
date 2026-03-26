"""Runtime protocol models aligned with the shared-core architecture docs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


class RequestValidationError(ValueError):
    """Raised when a request envelope is structurally invalid."""

    def __init__(self, field_path: str, message: str, machine_reason: str = "malformed-request") -> None:
        super().__init__(message)
        self.field_path = field_path
        self.message = message
        self.machine_reason = machine_reason


def _ensure_mapping(value: Any, field_path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RequestValidationError(field_path, f"{field_path} must be a mapping.")
    return value


def _ensure_list(value: Any, field_path: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise RequestValidationError(field_path, f"{field_path} must be a list.")
    return value


def _require_string(mapping: Mapping[str, Any], key: str, field_path: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or value == "":
        raise RequestValidationError(f"{field_path}.{key}", f"{field_path}.{key} must be a non-empty string.")
    return value


def _optional_string(mapping: Mapping[str, Any], key: str, field_path: str) -> str | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise RequestValidationError(f"{field_path}.{key}", f"{field_path}.{key} must be a string or null.")
    return value


def _optional_bool(mapping: Mapping[str, Any], key: str, field_path: str) -> bool | None:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise RequestValidationError(f"{field_path}.{key}", f"{field_path}.{key} must be a boolean or null.")
    return value


def _optional_mapping(mapping: Mapping[str, Any], key: str, field_path: str) -> dict[str, Any]:
    value = mapping.get(key)
    if value is None:
        return {}
    ensured = _ensure_mapping(value, f"{field_path}.{key}")
    return dict(ensured)


@dataclass(frozen=True)
class HostIdentity:
    family: str
    technology: str
    support_mode: str
    host_version_id: str | None = None


@dataclass(frozen=True)
class HostContext:
    product: str | None = None
    vendor: str | None = None
    process_id: str | int | None = None
    notes: str | None = None


@dataclass(frozen=True)
class DocumentContext:
    document_uri: str | None = None
    language_id: str | None = None
    is_dirty: bool | None = None
    content_ref: str | None = None


@dataclass(frozen=True)
class WorkspaceContext:
    workspace_id: str | None = None
    workspace_uri: str | None = None
    project_ids: list[Any] = field(default_factory=list)


@dataclass(frozen=True)
class SelectionContext:
    editor_id: str | None = None
    ranges: list[Any] = field(default_factory=list)
    active_text: str | None = None


@dataclass(frozen=True)
class RequestedFeature:
    feature_id: str
    arguments: dict[str, Any] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RequestEnvelope:
    request_id: str
    protocol_version: int
    execution_mode: str
    host_identity: HostIdentity
    host_context: HostContext = field(default_factory=HostContext)
    document_context: DocumentContext = field(default_factory=DocumentContext)
    workspace_context: WorkspaceContext = field(default_factory=WorkspaceContext)
    selection_context: SelectionContext = field(default_factory=SelectionContext)
    requested_feature: RequestedFeature = field(default_factory=lambda: RequestedFeature(feature_id="boot.slice.invoke"))
    extensions: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RequestEnvelope":
        request_id = _require_string(payload, "request_id", "request")
        protocol_version = payload.get("protocol_version")
        if not isinstance(protocol_version, int):
            raise RequestValidationError("request.protocol_version", "request.protocol_version must be an integer.")
        execution_mode = _require_string(payload, "execution_mode", "request")

        host_identity_payload = _ensure_mapping(payload.get("host_identity"), "request.host_identity")
        host_identity = HostIdentity(
            family=_require_string(host_identity_payload, "family", "request.host_identity"),
            technology=_require_string(host_identity_payload, "technology", "request.host_identity"),
            support_mode=_require_string(host_identity_payload, "support_mode", "request.host_identity"),
            host_version_id=_optional_string(host_identity_payload, "host_version_id", "request.host_identity"),
        )

        host_context_payload = _ensure_mapping(payload.get("host_context") or {}, "request.host_context")
        process_id = host_context_payload.get("process_id")
        if process_id is not None and not isinstance(process_id, (str, int)):
            raise RequestValidationError(
                "request.host_context.process_id",
                "request.host_context.process_id must be a string, integer, or null.",
            )
        host_context = HostContext(
            product=_optional_string(host_context_payload, "product", "request.host_context"),
            vendor=_optional_string(host_context_payload, "vendor", "request.host_context"),
            process_id=process_id,
            notes=_optional_string(host_context_payload, "notes", "request.host_context"),
        )

        document_payload = _ensure_mapping(payload.get("document_context") or {}, "request.document_context")
        document_context = DocumentContext(
            document_uri=_optional_string(document_payload, "document_uri", "request.document_context"),
            language_id=_optional_string(document_payload, "language_id", "request.document_context"),
            is_dirty=_optional_bool(document_payload, "is_dirty", "request.document_context"),
            content_ref=_optional_string(document_payload, "content_ref", "request.document_context"),
        )

        workspace_payload = _ensure_mapping(payload.get("workspace_context") or {}, "request.workspace_context")
        workspace_context = WorkspaceContext(
            workspace_id=_optional_string(workspace_payload, "workspace_id", "request.workspace_context"),
            workspace_uri=_optional_string(workspace_payload, "workspace_uri", "request.workspace_context"),
            project_ids=_ensure_list(workspace_payload.get("project_ids"), "request.workspace_context.project_ids"),
        )

        selection_payload = _ensure_mapping(payload.get("selection_context") or {}, "request.selection_context")
        selection_context = SelectionContext(
            editor_id=_optional_string(selection_payload, "editor_id", "request.selection_context"),
            ranges=_ensure_list(selection_payload.get("ranges"), "request.selection_context.ranges"),
            active_text=_optional_string(selection_payload, "active_text", "request.selection_context"),
        )

        feature_payload = _ensure_mapping(payload.get("requested_feature"), "request.requested_feature")
        requested_feature = RequestedFeature(
            feature_id=_require_string(feature_payload, "feature_id", "request.requested_feature"),
            arguments=_optional_mapping(feature_payload, "arguments", "request.requested_feature"),
            options=_optional_mapping(feature_payload, "options", "request.requested_feature"),
        )

        extensions = _optional_mapping(payload, "extensions", "request")

        return cls(
            request_id=request_id,
            protocol_version=protocol_version,
            execution_mode=execution_mode,
            host_identity=host_identity,
            host_context=host_context,
            document_context=document_context,
            workspace_context=workspace_context,
            selection_context=selection_context,
            requested_feature=requested_feature,
            extensions=extensions,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CapabilityAvailableFeature:
    feature_id: str
    notes: str | None = None


@dataclass(frozen=True)
class CapabilityUnavailableFeature:
    feature_id: str
    reason: str
    notes: str | None = None


@dataclass(frozen=True)
class CapabilityReport:
    family: str
    technology: str
    support_mode: str
    execution_modes: list[str]
    current_capability: str | None
    target_capability: str | None
    available_features: list[CapabilityAvailableFeature] = field(default_factory=list)
    unavailable_features: list[CapabilityUnavailableFeature] = field(default_factory=list)
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResponseEnvelope:
    request_id: str
    protocol_version: int
    status: str
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    edits: list[dict[str, Any]] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    follow_up_requirements: list[str] = field(default_factory=list)
    notes: str | None = None
    extensions: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
