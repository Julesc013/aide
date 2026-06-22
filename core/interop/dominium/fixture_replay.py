"""Replayable negative fixtures for the Dominium read-only seam."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import integrity, models


class FixtureReplayError(ValueError):
    """Raised when a negative fixture patch cannot be replayed."""


ALLOWED_OPERATIONS = {"add", "remove", "replace", "append"}
FORBIDDEN_OPERATION_KEYS = {"callable", "module", "command", "shell", "eval", "exec", "python", "entrypoint", "script"}


def _pointer_parts(pointer: str) -> list[str]:
    if not isinstance(pointer, str):
        raise FixtureReplayError("JSON pointer path must be a string")
    if not pointer.startswith("/"):
        raise FixtureReplayError(f"JSON pointer must start with /: {pointer}")
    parts = pointer.split("/")[1:]
    decoded: list[str] = []
    for part in parts:
        index = 0
        while index < len(part):
            if part[index] == "~" and (index + 1 >= len(part) or part[index + 1] not in {"0", "1"}):
                raise FixtureReplayError(f"malformed JSON pointer escape: {pointer}")
            index += 1
        decoded.append(part.replace("~1", "/").replace("~0", "~"))
    return decoded


def _canonical_index(value: str, *, allow_dash: bool, limit: int, allow_end: bool) -> int:
    if value == "-":
        if allow_dash:
            return limit
        raise FixtureReplayError("'-' array index is only allowed for add or append")
    if not isinstance(value, str) or value == "":
        raise FixtureReplayError("array index must be a canonical non-negative decimal string")
    if not value.isdecimal():
        raise FixtureReplayError(f"array index is not canonical decimal: {value}")
    if len(value) > 1 and value.startswith("0"):
        raise FixtureReplayError(f"array index must not contain leading zeroes: {value}")
    index = int(value)
    maximum = limit if allow_end else limit - 1
    if index < 0 or index > maximum:
        raise FixtureReplayError(f"array index out of range: {value}")
    return index


def _resolve_parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = _pointer_parts(pointer)
    if not parts:
        raise FixtureReplayError("operation requires a non-root target")
    current = document
    for part in parts[:-1]:
        if isinstance(current, list):
            current = current[_canonical_index(part, allow_dash=False, limit=len(current), allow_end=False)]
        elif isinstance(current, dict):
            if part not in current:
                raise FixtureReplayError(f"missing intermediate object key: {part}")
            current = current[part]
        else:
            raise FixtureReplayError(f"cannot traverse through non-container at {part}")
    return current, parts[-1]


def apply_operations(document: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = deepcopy(document)
    for op in operations:
        if not isinstance(op, dict):
            raise FixtureReplayError("operation must be an object")
        if FORBIDDEN_OPERATION_KEYS & set(op):
            raise FixtureReplayError("operation contains forbidden executable field")
        kind = op.get("op")
        if kind not in ALLOWED_OPERATIONS:
            raise FixtureReplayError(f"unsupported operation: {kind}")
        parent, key = _resolve_parent(candidate, op.get("path"))
        if isinstance(parent, list):
            if kind == "remove":
                index = _canonical_index(key, allow_dash=False, limit=len(parent), allow_end=False)
                parent.pop(index)
            elif kind == "add":
                index = _canonical_index(key, allow_dash=True, limit=len(parent), allow_end=True)
                parent.insert(index, deepcopy(op.get("value")))
            elif kind == "replace":
                index = _canonical_index(key, allow_dash=False, limit=len(parent), allow_end=False)
                parent[index] = deepcopy(op.get("value"))
            elif kind == "append":
                if key != "-":
                    _canonical_index(key, allow_dash=False, limit=len(parent), allow_end=True)
                parent.append(deepcopy(op.get("value")))
            else:
                raise FixtureReplayError(f"unsupported list operation: {kind}")
        elif isinstance(parent, dict):
            if kind == "remove":
                if key not in parent:
                    raise FixtureReplayError(f"remove target object key does not exist: {key}")
                parent.pop(key)
            elif kind == "add":
                if key in parent:
                    raise FixtureReplayError(f"add target object key already exists: {key}")
                parent[key] = deepcopy(op.get("value"))
            elif kind == "replace":
                if key not in parent:
                    raise FixtureReplayError(f"replace target object key does not exist: {key}")
                parent[key] = deepcopy(op.get("value"))
            elif kind == "append":
                if key not in parent or not isinstance(parent[key], list):
                    raise FixtureReplayError("append operation requires an array target")
                parent[key].append(deepcopy(op.get("value")))
            else:
                raise FixtureReplayError(f"unsupported object operation: {kind}")
        else:
            raise FixtureReplayError("operation target parent is not a container")
    return candidate


def fixture(name: str, expected_codes: list[str], operations: list[dict[str, Any]], base_bundle: dict[str, Any]) -> dict[str, Any]:
    invalid = apply_operations(base_bundle, operations)
    return {
        "schema_version": "aide.dominium-readonly-seam.negative-fixture.v1",
        "name": name,
        "base_bundle_ref": base_bundle["manifest"]["bundle_ref"],
        "base_bundle_sha256": integrity.stable_digest(base_bundle),
        "expected_error_codes": expected_codes,
        "operations": operations,
        "invalid_bundle_sha256": integrity.stable_digest(invalid),
        "validation_mode": "replay operations against base bundle and validate the resulting bundle",
    }


def materialize_fixture(case: dict[str, Any], base_bundle: dict[str, Any]) -> dict[str, Any]:
    return apply_operations(base_bundle, case["operations"])


def negative_fixture_cases(base_bundle: dict[str, Any]) -> list[dict[str, Any]]:
    rev = base_bundle["manifest"]["source_revision"]
    other_rev = ("0" * 40) if rev != ("0" * 40) else ("1" * 40)
    return [
        fixture("wrong_repository_identity", ["repository.identity"], [{"op": "replace", "path": "/source_snapshot/repository_identity/canonical_identity", "value": "github.com/example/dominium-shadow"}], base_bundle),
        fixture("stale_revision", ["revision.binding"], [{"op": "replace", "path": "/manifest/source_revision", "value": other_rev}], base_bundle),
        fixture("missing_required_contract", ["selected_files.exact_set"], [{"op": "remove", "path": "/source_snapshot/selected_files/0"}], base_bundle),
        fixture("invalid_reference_id", ["reference.syntax"], [{"op": "replace", "path": "/records/event_envelopes/0/spec/correlation_ref", "value": "not-a-reference"}], base_bundle),
        fixture("duplicate_identity", ["identity.duplicate"], [{"op": "replace", "path": "/records/artifact_references/1/metadata/id", "value": base_bundle["records"]["artifact_references"][0]["metadata"]["id"]}], base_bundle),
        fixture("wrong_authority_role", ["authority.role"], [{"op": "replace", "path": "/records/host_manifest/metadata/authority_role", "value": "canonical_truth"}], base_bundle),
        fixture("generated_projection_marked_canonical", ["authority.canonical_overclaim"], [{"op": "replace", "path": "/status/generated_projection_marked_canonical", "value": True}], base_bundle),
        fixture("path_traversal", ["path.traversal"], [{"op": "replace", "path": "/source_snapshot/selected_files/0/path", "value": "../AGENTS.md"}], base_bundle),
        fixture("absolute_path_escape", ["path.absolute"], [{"op": "replace", "path": "/source_snapshot/selected_files/0/path", "value": "/tmp/AGENTS.md"}], base_bundle),
        fixture("digest_mismatch", ["digest.source"], [{"op": "replace", "path": "/source_snapshot/selected_files/0/sha256", "value": "sha256:" + "0" * 64}], base_bundle),
        fixture("unknown_required_capability", ["compat.required_capability"], [{"op": "replace", "path": "/metadata/compatibility/requiredCapabilities", "value": [models.FEATURE_FLAG, "future.required"]}], base_bundle),
        fixture("unsupported_version", ["schema.version"], [{"op": "replace", "path": "/records/host_manifest/metadata/schema_version", "value": "future"}], base_bundle),
        fixture("conflicting_ownership", ["ownership.semantic"], [{"op": "replace", "path": "/records/host_manifest/metadata/semantic_owner", "value": "Workbench"}], base_bundle),
        fixture("workbench_authority_overclaim", ["workbench.authority"], [{"op": "replace", "path": "/records/workspace_descriptor/status/workbench_started", "value": True}], base_bundle),
        fixture("private_tool_bypass_declaration", ["command.invocation"], [{"op": "replace", "path": "/records/dominium_bridge_manifest/spec/command_mapping/command_invocation_implemented", "value": True}], base_bundle),
        fixture("mutation_capability_claim", ["capability.mutation"], [{"op": "add", "path": "/records/host_capability_set/spec/capabilities/-", "value": {"id": "dominium.source.write", "side_effect_class": "read_only", "implemented_in_this_slice": True, "requires_future_policy_decision": False}}], base_bundle),
        fixture("provider_network_worker_claim", ["status.false_boundary"], [{"op": "replace", "path": "/status/network_call_performed", "value": True}], base_bundle),
        fixture("invalid_refusal_mapping", ["refusal.registry"], [{"op": "replace", "path": "/records/refusal_projections/0/spec/code", "value": "dominium.refusal.invented"}], base_bundle),
        fixture("invalid_diagnostic_severity", ["diagnostic.registry"], [{"op": "replace", "path": "/records/diagnostic_projections/0/spec/severity", "value": "critical"}], base_bundle),
        fixture("broken_evidence_ref", ["reference.closure"], [{"op": "add", "path": "/records/evidence_reference_set/spec/evidence_refs/-", "value": "aide://artifact/missing"}], base_bundle),
        fixture("event_correlation_mismatch", ["event.correlation"], [{"op": "replace", "path": "/records/event_envelopes/0/spec/correlation_ref", "value": "aide://seam-bundle/wrong"}], base_bundle),
        fixture("non_deterministic_ordering", ["event.sequence"], [{"op": "replace", "path": "/records/event_envelopes/0/spec/sequence", "value": 99}], base_bundle),
        fixture("mixed_record_revision", ["revision.binding"], [{"op": "replace", "path": "/records/host_manifest/metadata/source_revision", "value": other_rev}], base_bundle),
        fixture("snapshot_digest_not_validated", ["digest.snapshot"], [{"op": "replace", "path": "/source_snapshot/snapshot_digest", "value": "sha256:" + "1" * 64}], base_bundle),
        fixture("second_host_capability_set", ["cardinality.singleton"], [{"op": "replace", "path": "/records/host_capability_set", "value": [base_bundle["records"]["host_capability_set"], base_bundle["records"]["host_capability_set"]]}], base_bundle),
        fixture("dangling_artifact_reference", ["reference.closure"], [{"op": "add", "path": "/records/context_descriptor/spec/artifact_refs/-", "value": "aide://artifact/dangling"}], base_bundle),
        fixture("wrong_semantic_owner", ["ownership.semantic"], [{"op": "replace", "path": "/records/artifact_references/0/metadata/semantic_owner", "value": "AIDE"}], base_bundle),
        fixture("mutation_capability_labeled_readonly", ["capability.mutation"], [{"op": "replace", "path": "/records/host_capability_set/spec/capabilities/0/id", "value": "dominium.patch.apply"}], base_bundle),
        fixture("duplicate_event_sequence", ["event.sequence"], [{"op": "replace", "path": "/records/event_envelopes/1/spec/sequence", "value": 1}], base_bundle),
        fixture("arbitrary_diagnostic_severity", ["diagnostic.registry"], [{"op": "replace", "path": "/records/diagnostic_projections/0/spec/severity", "value": "notice"}], base_bundle),
        fixture("invented_refusal", ["refusal.registry"], [{"op": "replace", "path": "/records/refusal_projections/0/spec/refusal_id", "value": "dominium.refusal.invented"}], base_bundle),
        fixture("missing_host_id", ["spec.required"], [{"op": "remove", "path": "/records/host_manifest/spec/host_id"}], base_bundle),
    ]
