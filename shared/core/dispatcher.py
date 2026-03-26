"""Top-level request dispatch and error handling for the shared-core runtime."""

from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Any, Mapping

from shared.config.boot_slice import PROTOCOL_VERSION, SUPPORTED_EXECUTION_MODES
from shared.core.boot_slice import dispatch_request
from shared.diagnostics import make_diagnostic
from shared.protocol.models import RequestEnvelope, RequestValidationError, ResponseEnvelope


def dispatch_request_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and dispatch one request payload."""

    request_id = _extract_request_id(payload)
    try:
        request = RequestEnvelope.from_dict(payload)
        if request.protocol_version != PROTOCOL_VERSION:
            raise RequestValidationError(
                "request.protocol_version",
                f"request.protocol_version must be {PROTOCOL_VERSION} for the bootstrap runtime.",
                machine_reason="unsupported-protocol",
            )
        if request.execution_mode not in SUPPORTED_EXECUTION_MODES:
            raise RequestValidationError(
                "request.execution_mode",
                "request.execution_mode is not supported by the bootstrap runtime.",
                machine_reason="execution-mode-mismatch",
            )
        return dispatch_request(request).to_dict()
    except RequestValidationError as exc:
        response = ResponseEnvelope(
            request_id=request_id,
            protocol_version=PROTOCOL_VERSION,
            status="rejected",
            diagnostics=[
                make_diagnostic(
                    diagnostic_id="request.malformed",
                    severity="error",
                    component="protocol-validation",
                    message=exc.message,
                    machine_reason=exc.machine_reason,
                    evidence={"field_path": exc.field_path},
                    action_summary="Provide the missing or corrected request field and retry.",
                )
            ],
            edits=[],
            actions=[],
            artifacts=[],
            follow_up_requirements=["Correct the request envelope before retrying the shared-core bootstrap runtime."],
            notes="The shared-core bootstrap runtime rejected the malformed request.",
            extensions={},
        )
        return response.to_dict()
    except Exception as exc:
        response = ResponseEnvelope(
            request_id=request_id,
            protocol_version=PROTOCOL_VERSION,
            status="failed",
            diagnostics=[
                make_diagnostic(
                    diagnostic_id="internal.processing-failure",
                    severity="error",
                    component="boot-slice-dispatcher",
                    message="Shared-core processing failed unexpectedly.",
                    machine_reason="internal-processing-failure",
                    evidence={"exception_type": type(exc).__name__},
                    action_summary="Inspect the shared-core bootstrap runtime and retry the same request.",
                )
            ],
            edits=[],
            actions=[],
            artifacts=[],
            follow_up_requirements=["Resolve the shared-core failure before retrying."],
            notes="Unexpected internal failure.",
            extensions={},
        )
        return response.to_dict()


def dispatch_json_text(payload_text: str) -> dict[str, Any]:
    """Parse a JSON request body and dispatch it."""

    try:
        payload = json.loads(payload_text)
    except JSONDecodeError as exc:
        response = ResponseEnvelope(
            request_id="unknown-request",
            protocol_version=PROTOCOL_VERSION,
            status="rejected",
            diagnostics=[
                make_diagnostic(
                    diagnostic_id="request.invalid-json",
                    severity="error",
                    component="transport",
                    message="Request body must be valid JSON.",
                    machine_reason="invalid-json",
                    evidence={"line": exc.lineno, "column": exc.colno},
                    action_summary="Provide a valid JSON request body and retry.",
                )
            ],
            edits=[],
            actions=[],
            artifacts=[],
            follow_up_requirements=["Correct the JSON syntax before retrying."],
            notes="JSON parsing failed before request validation could begin.",
            extensions={},
        )
        return response.to_dict()

    if not isinstance(payload, Mapping):
        return ResponseEnvelope(
            request_id="unknown-request",
            protocol_version=PROTOCOL_VERSION,
            status="rejected",
            diagnostics=[
                make_diagnostic(
                    diagnostic_id="request.malformed",
                    severity="error",
                    component="transport",
                    message="Request body must decode to a JSON object.",
                    machine_reason="malformed-request",
                    evidence={"decoded_type": type(payload).__name__},
                    action_summary="Wrap the request fields in a JSON object and retry.",
                )
            ],
            edits=[],
            actions=[],
            artifacts=[],
            follow_up_requirements=["Provide a JSON object request envelope before retrying."],
            notes="Decoded JSON did not match the request-envelope shape.",
            extensions={},
        ).to_dict()

    return dispatch_request_payload(payload)


def _extract_request_id(payload: Mapping[str, Any]) -> str:
    request_id = payload.get("request_id")
    if isinstance(request_id, str) and request_id:
        return request_id
    return "unknown-request"
