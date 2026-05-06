"""Provider status rendering for offline Q20 metadata."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .registry import (
    ADAPTER_CONTRACT_PATH,
    CAPABILITY_MATRIX_PATH,
    PROVIDER_CATALOG_PATH,
    PROVIDER_POLICY_PATH,
    PROVIDER_STATUS_PATH,
    capability_dimensions,
    load_provider_catalog,
    repo_root_from,
    validate_provider_files,
)


SCHEMA_VERSION = "aide.provider-status.v0"
PROVIDER_VERSION = "q20.provider-adapter.v0"
PROVIDER_STATUS_JSON_PATH = ".aide/providers/latest-provider-status.json"
PROVIDER_STATUS_MD_PATH = ".aide/providers/latest-provider-status.md"


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def counter_for(providers: list[Any], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(getattr(provider, field)) for provider in providers).items()))


def build_provider_status(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    providers = load_provider_catalog(root)
    validation = validate_provider_files(root)
    provider_ids = sorted(provider.provider_id for provider in providers)
    local_ids = sorted(provider.provider_id for provider in providers if provider.privacy_class == "local")
    remote_ids = sorted(provider.provider_id for provider in providers if provider.privacy_class == "remote")
    human_ids = sorted(provider.provider_id for provider in providers if provider.provider_class == "human")
    deterministic_ids = sorted(provider.provider_id for provider in providers if provider.provider_class == "deterministic")
    aggregator_ids = sorted(provider.provider_id for provider in providers if provider.provider_class == "aggregator")
    credential_required_ids = sorted(provider.provider_id for provider in providers if provider.credentials_required)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": PROVIDER_VERSION,
        "provider_adapter_contract": "implemented_metadata_only",
        "live_provider_calls": False,
        "live_model_calls": False,
        "network_calls": False,
        "provider_probe_calls": False,
        "credentials_configured": False,
        "gateway_forwarding": False,
        "local_model_setup": False,
        "raw_prompt_storage": False,
        "raw_response_storage": False,
        "no_credentials_in_status": True,
        "provider_family_count": len(providers),
        "provider_ids": provider_ids,
        "provider_class_counts": counter_for(providers, "provider_class"),
        "adapter_class_counts": counter_for(providers, "adapter_class"),
        "privacy_class_counts": counter_for(providers, "privacy_class"),
        "status_counts": counter_for(providers, "status"),
        "credential_required_count": len(credential_required_ids),
        "credential_required_provider_ids": credential_required_ids,
        "local_provider_ids": local_ids,
        "remote_provider_ids": remote_ids,
        "human_provider_ids": human_ids,
        "deterministic_provider_ids": deterministic_ids,
        "aggregator_provider_ids": aggregator_ids,
        "capability_dimension_count": len(capability_dimensions(root)),
        "metadata_paths": {
            "policy": PROVIDER_POLICY_PATH,
            "catalog": PROVIDER_CATALOG_PATH,
            "capability_matrix": CAPABILITY_MATRIX_PATH,
            "adapter_contract": ADAPTER_CONTRACT_PATH,
            "status": PROVIDER_STATUS_PATH,
        },
        "validation": validation,
        "notes": [
            "Q20 provider metadata is advisory and offline only.",
            "Credentials are not configured and must remain in future .aide.local/ state.",
            "Gateway forwarding, provider probes, model calls, and network calls remain disabled.",
        ],
    }


def render_provider_status_markdown(data: dict[str, Any]) -> str:
    validation = data.get("validation", {}) if isinstance(data.get("validation"), dict) else {}
    lines = [
        "# Latest Provider Status",
        "",
        f"- schema_version: `{data.get('schema_version', SCHEMA_VERSION)}`",
        f"- generated_by: `{data.get('generated_by', PROVIDER_VERSION)}`",
        f"- provider_adapter_contract: `{data.get('provider_adapter_contract', 'unknown')}`",
        f"- provider_family_count: {data.get('provider_family_count', 0)}",
        f"- live_provider_calls: `{str(data.get('live_provider_calls', False)).lower()}`",
        f"- live_model_calls: `{str(data.get('live_model_calls', False)).lower()}`",
        f"- network_calls: `{str(data.get('network_calls', False)).lower()}`",
        f"- provider_probe_calls: `{str(data.get('provider_probe_calls', False)).lower()}`",
        f"- credentials_configured: `{str(data.get('credentials_configured', False)).lower()}`",
        f"- gateway_forwarding: `{str(data.get('gateway_forwarding', False)).lower()}`",
        f"- raw_prompt_storage: `{str(data.get('raw_prompt_storage', False)).lower()}`",
        f"- raw_response_storage: `{str(data.get('raw_response_storage', False)).lower()}`",
        "",
        "## Provider Classes",
        "",
    ]
    for key, value in (data.get("provider_class_counts", {}) or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Privacy Classes", ""])
    for key, value in (data.get("privacy_class_counts", {}) or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            f"- result: {validation.get('result', 'unknown')}",
            f"- warnings: {len(validation.get('warnings', [])) if isinstance(validation.get('warnings', []), list) else 0}",
            f"- errors: {len(validation.get('errors', [])) if isinstance(validation.get('errors', []), list) else 0}",
            "",
            "## Boundary",
            "",
            "- live_calls_allowed_in_q20: false",
            "- credentials_location: future `.aide.local/` only",
            "- provider_or_model_calls: none",
            "- network_calls: none",
            "- raw_prompt_storage: false",
            "- raw_response_storage: false",
            "- gateway_forwarding: false",
            "",
        ]
    )
    return "\n".join(lines)


def write_provider_status_files(repo_root: Path | None = None) -> tuple[Path, Path, dict[str, Any]]:
    root = repo_root_from(repo_root)
    data = build_provider_status(root)
    json_path = root / PROVIDER_STATUS_JSON_PATH
    md_path = root / PROVIDER_STATUS_MD_PATH
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(stable_json(data), encoding="utf-8", newline="\n")
    md_path.write_text(render_provider_status_markdown(data), encoding="utf-8", newline="\n")
    return json_path, md_path, data


def contract_summary(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    contract_path = root / ADAPTER_CONTRACT_PATH
    text = contract_path.read_text(encoding="utf-8") if contract_path.exists() else ""
    required_fields: list[str] = []
    in_required = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == "required_fields:":
            in_required = True
            continue
        if in_required:
            if stripped.startswith("- "):
                required_fields.append(stripped[2:].strip())
                continue
            if stripped and not raw_line.startswith(" "):
                break
    return {
        "schema_version": "aide.provider-contract-summary.v0",
        "contract_path": ADAPTER_CONTRACT_PATH,
        "required_fields": required_fields,
        "live_calls_allowed_in_q20": False,
        "network_calls_allowed_in_q20": False,
        "model_calls_allowed_in_q20": False,
        "provider_probe_calls_allowed_in_q20": False,
        "raw_prompt_storage": False,
        "raw_response_storage": False,
    }


def offline_probe(repo_root: Path | None = None) -> dict[str, Any]:
    status = build_provider_status(repo_root)
    return {
        "schema_version": "aide.provider-offline-probe.v0",
        "result": status.get("validation", {}).get("result", "UNKNOWN"),
        "provider_family_count": status.get("provider_family_count", 0),
        "live_provider_calls": False,
        "live_model_calls": False,
        "network_calls": False,
        "provider_probe_calls": False,
        "credentials_configured": False,
        "future_credentials_location": ".aide.local/",
        "notes": [
            "Offline probe validates committed metadata only.",
            "No provider, model, network, credential, pricing, or availability probe was performed.",
        ],
    }
