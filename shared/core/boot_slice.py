"""Boot-slice request handling for the shared-core bootstrap runtime."""

from __future__ import annotations

from shared.config.boot_slice import BOOT_SLICE_ID, BOOT_SLICE_TITLE, EDITOR_MARKER_PREFIX, LanePolicy, SUPPORTED_FEATURES, get_lane_policy
from shared.diagnostics import make_diagnostic
from shared.protocol.models import (
    CapabilityAvailableFeature,
    CapabilityReport,
    CapabilityUnavailableFeature,
    RequestEnvelope,
    ResponseEnvelope,
)


def dispatch_request(request: RequestEnvelope) -> ResponseEnvelope:
    """Dispatch one boot-slice request."""

    if request.requested_feature.feature_id not in SUPPORTED_FEATURES:
        return _make_unavailable_feature_response(
            request=request,
            policy=get_lane_policy(request.host_identity.family, request.host_identity.technology),
            reason="not-implemented",
            message="Requested feature is outside the shared-core bootstrap slice.",
            follow_up="Use boot.slice.invoke or boot.slice.editor-marker for the current bootstrap runtime.",
        )

    policy = get_lane_policy(request.host_identity.family, request.host_identity.technology)
    if policy is None:
        return _make_unavailable_feature_response(
            request=request,
            policy=None,
            reason="not-implemented",
            message="The requested lane is not in the committed shared-core bootstrap map.",
            follow_up="Use a committed lane from the current boot-slice rollout plan.",
        )

    if request.requested_feature.feature_id == "boot.slice.invoke":
        return _handle_invoke(request, policy)
    return _handle_editor_marker(request, policy)


def _handle_invoke(request: RequestEnvelope, policy: LanePolicy) -> ResponseEnvelope:
    available, unavailable, current_capability = _feature_posture_for_request(
        active_text=request.selection_context.active_text,
        policy=policy,
    )
    capability_report = _build_capability_report(
        request=request,
        policy=policy,
        current_capability=current_capability,
        available=available,
        unavailable=unavailable,
    )
    artifact_report = _build_boot_slice_artifact(
        request=request,
        policy=policy,
        current_capability=current_capability,
        available=available,
        unavailable=unavailable,
        status="success",
        observable_output=(
            f"AIDE boot slice active for {request.host_identity.family}/{request.host_identity.technology} "
            f"via {request.execution_mode}."
        ),
        marker_preview=None,
    )
    return ResponseEnvelope(
        request_id=request.request_id,
        protocol_version=request.protocol_version,
        status="success",
        diagnostics=[],
        edits=[],
        actions=[],
        artifacts=[artifact_report, {"kind": "capability-report", "payload": capability_report.to_dict()}],
        follow_up_requirements=[],
        notes="Boot-slice invoke completed with deterministic report output.",
        extensions={},
    )


def _handle_editor_marker(request: RequestEnvelope, policy: LanePolicy) -> ResponseEnvelope:
    if policy.editor_policy == "fallback":
        unavailable = [
            CapabilityUnavailableFeature(
                feature_id="boot.slice.editor-marker",
                reason="deferred",
                notes="This lane completes the first slice through report-first fallback proof.",
            )
        ]
        available = [
            CapabilityAvailableFeature(
                feature_id="boot.slice.invoke",
                notes="Report-first invocation is available for this lane.",
            )
        ]
        diagnostics = [
            make_diagnostic(
                diagnostic_id="capability.unavailable",
                severity="warning",
                component="capability-negotiation",
                message="Requested feature is unavailable on this lane.",
                machine_reason="deferred",
                evidence={"feature_id": "boot.slice.editor-marker", "lane_id": policy.lane_id},
                action_summary="Use boot.slice.invoke for the accepted fallback proof on this lane.",
                document_uri=request.document_context.document_uri,
                workspace_id=request.workspace_context.workspace_id,
            ),
            make_diagnostic(
                diagnostic_id="lane.deferred",
                severity="info",
                component="boot-slice-dispatcher",
                message="This lane uses a companion or fallback proof before native editor interaction.",
                machine_reason="deferred",
                evidence={"lane_id": policy.lane_id, "editor_policy": policy.editor_policy},
                action_summary="Promote this lane later when a native editor path becomes honest and stable.",
                document_uri=request.document_context.document_uri,
                workspace_id=request.workspace_context.workspace_id,
            ),
        ]
        capability_report = _build_capability_report(
            request=request,
            policy=policy,
            current_capability="L1",
            available=available,
            unavailable=unavailable,
        )
        artifact_report = _build_boot_slice_artifact(
            request=request,
            policy=policy,
            current_capability="L1",
            available=available,
            unavailable=unavailable,
            status="deferred",
            observable_output=(
                f"AIDE boot slice active for {request.host_identity.family}/{request.host_identity.technology} "
                f"via {request.execution_mode}."
            ),
            marker_preview=None,
        )
        return ResponseEnvelope(
            request_id=request.request_id,
            protocol_version=request.protocol_version,
            status="deferred",
            diagnostics=diagnostics,
            edits=[],
            actions=[],
            artifacts=[artifact_report, {"kind": "capability-report", "payload": capability_report.to_dict()}],
            follow_up_requirements=[
                "Use boot.slice.invoke as the accepted first proof for this lane.",
                "Record any native-lane blocker or promotion path outside the shared-core runtime.",
            ],
            notes="Editor-marker behavior is deferred for fallback-first lanes.",
            extensions={},
        )

    if request.selection_context.active_text is None:
        unavailable = [
            CapabilityUnavailableFeature(
                feature_id="boot.slice.editor-marker",
                reason="missing-context",
                notes="Provide selection_context.active_text to request the deterministic marker transform.",
            )
        ]
        available = [
            CapabilityAvailableFeature(
                feature_id="boot.slice.invoke",
                notes="Report-first invocation remains available without editor context.",
            )
        ]
        diagnostics = [
            make_diagnostic(
                diagnostic_id="context.missing-active-text",
                severity="warning",
                component="boot-slice-dispatcher",
                message="selection_context.active_text is required for the editor-marker request.",
                machine_reason="missing-context",
                evidence={"feature_id": "boot.slice.editor-marker"},
                action_summary="Provide selection_context.active_text and retry the editor-marker request.",
                document_uri=request.document_context.document_uri,
                workspace_id=request.workspace_context.workspace_id,
            )
        ]
        capability_report = _build_capability_report(
            request=request,
            policy=policy,
            current_capability="L1",
            available=available,
            unavailable=unavailable,
        )
        artifact_report = _build_boot_slice_artifact(
            request=request,
            policy=policy,
            current_capability="L1",
            available=available,
            unavailable=unavailable,
            status="deferred",
            observable_output=(
                f"AIDE boot slice active for {request.host_identity.family}/{request.host_identity.technology} "
                f"via {request.execution_mode}."
            ),
            marker_preview=None,
        )
        return ResponseEnvelope(
            request_id=request.request_id,
            protocol_version=request.protocol_version,
            status="deferred",
            diagnostics=diagnostics,
            edits=[],
            actions=[],
            artifacts=[artifact_report, {"kind": "capability-report", "payload": capability_report.to_dict()}],
            follow_up_requirements=[
                "Provide selection_context.active_text for the deterministic editor-marker operation."
            ],
            notes="Editor-marker request deferred because the required active text was not supplied.",
            extensions={},
        )

    marker_preview = f"{EDITOR_MARKER_PREFIX}{request.selection_context.active_text}"
    available = [
        CapabilityAvailableFeature(
            feature_id="boot.slice.invoke",
            notes="Report-first invocation is available for this lane.",
        ),
        CapabilityAvailableFeature(
            feature_id="boot.slice.editor-marker",
            notes="Deterministic marker preview is available for the supplied active text.",
        ),
    ]
    capability_report = _build_capability_report(
        request=request,
        policy=policy,
        current_capability="L2",
        available=available,
        unavailable=[],
    )
    artifact_report = _build_boot_slice_artifact(
        request=request,
        policy=policy,
        current_capability="L2",
        available=available,
        unavailable=[],
        status="success",
        observable_output=marker_preview,
        marker_preview=marker_preview,
    )
    return ResponseEnvelope(
        request_id=request.request_id,
        protocol_version=request.protocol_version,
        status="success",
        diagnostics=[],
        edits=[
            {
                "edit_id": "boot-slice-editor-marker-preview",
                "kind": "replace-selection-preview",
                "target": "selection.active_text",
                "document_uri": request.document_context.document_uri,
                "original_text": request.selection_context.active_text,
                "replacement_text": marker_preview,
            }
        ],
        actions=[],
        artifacts=[artifact_report, {"kind": "capability-report", "payload": capability_report.to_dict()}],
        follow_up_requirements=[],
        notes="Editor-marker preview generated deterministically by the shared core.",
        extensions={},
    )


def _feature_posture_for_request(
    *,
    active_text: str | None,
    policy: LanePolicy,
) -> tuple[list[CapabilityAvailableFeature], list[CapabilityUnavailableFeature], str]:
    available = [
        CapabilityAvailableFeature(
            feature_id="boot.slice.invoke",
            notes="Shared-core report-first invocation is implemented for the committed lane map.",
        )
    ]
    unavailable: list[CapabilityUnavailableFeature] = []
    current_capability = "L1"

    if policy.editor_policy == "fallback":
        unavailable.append(
            CapabilityUnavailableFeature(
                feature_id="boot.slice.editor-marker",
                reason="deferred",
                notes="This lane completes the first slice through fallback proof instead of native editor interaction.",
            )
        )
        return available, unavailable, current_capability

    if active_text is None:
        unavailable.append(
            CapabilityUnavailableFeature(
                feature_id="boot.slice.editor-marker",
                reason="missing-context",
                notes="Provide selection_context.active_text to expose the deterministic marker preview.",
            )
        )
        return available, unavailable, current_capability

    available.append(
        CapabilityAvailableFeature(
            feature_id="boot.slice.editor-marker",
            notes="Deterministic marker preview is available when active_text is supplied.",
        )
    )
    return available, unavailable, "L2"


def _build_capability_report(
    *,
    request: RequestEnvelope,
    policy: LanePolicy | None,
    current_capability: str | None,
    available: list[CapabilityAvailableFeature],
    unavailable: list[CapabilityUnavailableFeature],
) -> CapabilityReport:
    target_capability = policy.target_capability if policy is not None else None
    notes = "Shared-core bootstrap runtime only. Host adapters remain unimplemented in this phase."
    return CapabilityReport(
        family=request.host_identity.family,
        technology=request.host_identity.technology,
        support_mode=request.host_identity.support_mode,
        execution_modes=[request.execution_mode],
        current_capability=current_capability,
        target_capability=target_capability,
        available_features=available,
        unavailable_features=unavailable,
        notes=notes,
    )


def _build_boot_slice_artifact(
    *,
    request: RequestEnvelope,
    policy: LanePolicy | None,
    current_capability: str | None,
    available: list[CapabilityAvailableFeature],
    unavailable: list[CapabilityUnavailableFeature],
    status: str,
    observable_output: str,
    marker_preview: str | None,
) -> dict[str, object]:
    return {
        "kind": "boot-slice-report",
        "payload": {
            "boot_slice_id": BOOT_SLICE_ID,
            "title": BOOT_SLICE_TITLE,
            "feature_id": request.requested_feature.feature_id,
            "status": status,
            "lane": {
                "family": request.host_identity.family,
                "technology": request.host_identity.technology,
                "support_mode": request.host_identity.support_mode,
                "host_version_id": request.host_identity.host_version_id,
            },
            "execution_mode": request.execution_mode,
            "current_capability": current_capability,
            "target_capability": policy.target_capability if policy is not None else None,
            "available_behaviors": [item.feature_id for item in available],
            "unavailable_behaviors": [
                {"feature_id": item.feature_id, "reason": item.reason, "notes": item.notes}
                for item in unavailable
            ],
            "observable_output": observable_output,
            "marker_preview": marker_preview,
            "notes": "Shared-core bootstrap report only. Host adapters remain out of scope in P10.",
        },
    }


def _make_unavailable_feature_response(
    *,
    request: RequestEnvelope,
    policy: LanePolicy | None,
    reason: str,
    message: str,
    follow_up: str,
) -> ResponseEnvelope:
    unavailable = [
        CapabilityUnavailableFeature(
            feature_id=request.requested_feature.feature_id,
            reason=reason,
            notes=message,
        )
    ]
    capability_report = _build_capability_report(
        request=request,
        policy=policy,
        current_capability="L1" if policy is not None else None,
        available=[],
        unavailable=unavailable,
    )
    diagnostics = [
        make_diagnostic(
            diagnostic_id="capability.unavailable",
            severity="warning",
            component="capability-negotiation",
            message=message,
            machine_reason=reason,
            evidence={
                "feature_id": request.requested_feature.feature_id,
                "family": request.host_identity.family,
                "technology": request.host_identity.technology,
            },
            action_summary=follow_up,
            document_uri=request.document_context.document_uri,
            workspace_id=request.workspace_context.workspace_id,
        )
    ]
    artifact_report = _build_boot_slice_artifact(
        request=request,
        policy=policy,
        current_capability="L1" if policy is not None else None,
        available=[],
        unavailable=unavailable,
        status="deferred",
        observable_output=(
            f"AIDE boot slice active for {request.host_identity.family}/{request.host_identity.technology} "
            f"via {request.execution_mode}."
        ),
        marker_preview=None,
    )
    return ResponseEnvelope(
        request_id=request.request_id,
        protocol_version=request.protocol_version,
        status="deferred",
        diagnostics=diagnostics,
        edits=[],
        actions=[],
        artifacts=[artifact_report, {"kind": "capability-report", "payload": capability_report.to_dict()}],
        follow_up_requirements=[follow_up],
        notes=message,
        extensions={},
    )
