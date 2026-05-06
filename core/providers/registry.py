"""Offline provider metadata registry helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .contracts import ProviderMetadata


PROVIDER_CATALOG_PATH = ".aide/providers/provider-catalog.yaml"
CAPABILITY_MATRIX_PATH = ".aide/providers/capability-matrix.yaml"
ADAPTER_CONTRACT_PATH = ".aide/providers/adapter-contract.yaml"
PROVIDER_POLICY_PATH = ".aide/policies/provider-adapters.yaml"
PROVIDER_STATUS_PATH = ".aide/providers/status.yaml"

REQUIRED_PROVIDER_FIELDS = [
    "provider_id",
    "display_name",
    "adapter_class",
    "provider_class",
    "privacy_class",
    "credentials_required",
    "credentials_location",
    "live_calls_allowed_in_q20",
    "status",
]

REQUIRED_PROVIDER_IDS = [
    "deterministic_tools",
    "human",
    "local_ollama",
    "local_lm_studio",
    "local_llama_cpp",
    "local_vllm",
    "local_sglang",
    "openai",
    "anthropic",
    "google_gemini",
    "deepseek",
    "openrouter",
    "other_remote_provider",
]

ADAPTER_CLASSES = {"deterministic_tool", "human_review", "local_model", "remote_model", "aggregator", "unknown"}
PROVIDER_CLASSES = {"deterministic", "human", "local_model", "remote_model", "aggregator"}
PRIVACY_CLASSES = {"local", "remote", "human", "unknown"}
STATUS_VALUES = {"metadata_only", "planned", "deferred"}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"sk-ant-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
]


def repo_root_from(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".aide/profile.yaml").exists() and (candidate / ".aide/queue/index.yaml").exists():
            return candidate
    return current


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"expected boolean value, got {value!r}")


def parse_catalog_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_records = False
    for raw_line in text.splitlines():
        if raw_line.strip() == "provider_families:":
            in_records = True
            continue
        if not in_records:
            continue
        if raw_line.startswith("  - provider_id:"):
            if current:
                records.append(current)
            current = {"provider_id": raw_line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        if raw_line.startswith("  - ") and "provider_id:" not in raw_line:
            if current:
                records.append(current)
            current = None
            continue
        if raw_line.startswith("    ") and ":" in raw_line:
            key, value = raw_line.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
            continue
        if raw_line and not raw_line.startswith(" ") and not raw_line.startswith("#"):
            break
    if current:
        records.append(current)
    return records


def metadata_from_record(record: dict[str, str]) -> ProviderMetadata:
    missing = [field for field in REQUIRED_PROVIDER_FIELDS if field not in record]
    if missing:
        raise ValueError(f"provider record missing fields for {record.get('provider_id', 'unknown')}: {', '.join(missing)}")
    return ProviderMetadata(
        provider_id=record["provider_id"],
        display_name=record["display_name"],
        adapter_class=record["adapter_class"],
        provider_class=record["provider_class"],
        privacy_class=record["privacy_class"],
        credentials_required=parse_bool(record["credentials_required"]),
        credentials_location=record["credentials_location"],
        live_calls_allowed_in_q20=parse_bool(record["live_calls_allowed_in_q20"]),
        status=record["status"],
        notes=record.get("notes", ""),
    )


def load_provider_catalog(repo_root: Path | None = None) -> list[ProviderMetadata]:
    root = repo_root_from(repo_root)
    path = root / PROVIDER_CATALOG_PATH
    if not path.exists():
        return []
    return [metadata_from_record(record) for record in parse_catalog_records(read_text(path))]


def parse_simple_list(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_list = False
    base_indent = 0
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == f"{key}:":
            in_list = True
            base_indent = len(raw_line) - len(raw_line.lstrip())
            continue
        if in_list:
            indent = len(raw_line) - len(raw_line.lstrip())
            if indent <= base_indent and not stripped.startswith("- "):
                break
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                if ":" in item:
                    item = item.split(":", 1)[1].strip()
                values.append(item.strip('"').strip("'"))
    return values


def capability_dimensions(repo_root: Path | None = None) -> list[str]:
    root = repo_root_from(repo_root)
    path = root / CAPABILITY_MATRIX_PATH
    if not path.exists():
        return []
    return parse_simple_list(read_text(path), "capability_dimensions")


def detect_secret_like_values(text: str) -> list[str]:
    findings: list[str] = []
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(match.group(0).splitlines()[0][:80])
    return findings


def validate_provider_files(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    required_paths = [
        PROVIDER_POLICY_PATH,
        PROVIDER_CATALOG_PATH,
        CAPABILITY_MATRIX_PATH,
        ADAPTER_CONTRACT_PATH,
        PROVIDER_STATUS_PATH,
    ]
    for rel in required_paths:
        if not (root / rel).exists():
            errors.append(f"missing provider file: {rel}")
    text_paths = [rel for rel in required_paths if (root / rel).exists()]
    for rel in text_paths:
        text = read_text(root / rel)
        if detect_secret_like_values(text):
            errors.append(f"secret-like value detected in {rel}")
        if "live_calls_allowed_in_q20: true" in text:
            errors.append(f"live calls enabled in {rel}")
        if "network_calls_allowed_in_q20: true" in text:
            errors.append(f"network calls enabled in {rel}")
        if "model_calls_allowed_in_q20: true" in text:
            errors.append(f"model calls enabled in {rel}")
    try:
        providers = load_provider_catalog(root)
    except ValueError as exc:
        providers = []
        errors.append(str(exc))
    ids = {provider.provider_id for provider in providers}
    for required_id in REQUIRED_PROVIDER_IDS:
        if required_id not in ids:
            errors.append(f"provider catalog missing family: {required_id}")
    for provider in providers:
        if provider.adapter_class not in ADAPTER_CLASSES:
            errors.append(f"{provider.provider_id} invalid adapter_class: {provider.adapter_class}")
        if provider.provider_class not in PROVIDER_CLASSES:
            errors.append(f"{provider.provider_id} invalid provider_class: {provider.provider_class}")
        if provider.privacy_class not in PRIVACY_CLASSES:
            errors.append(f"{provider.provider_id} invalid privacy_class: {provider.privacy_class}")
        if provider.status not in STATUS_VALUES:
            errors.append(f"{provider.provider_id} invalid status: {provider.status}")
        if provider.live_calls_allowed_in_q20:
            errors.append(f"{provider.provider_id} enables live calls in Q20")
        if provider.credentials_required and provider.credentials_location != ".aide.local/":
            errors.append(f"{provider.provider_id} credentials must be future .aide.local/ refs")
        if not provider.credentials_required and provider.credentials_location not in {"none", ".aide.local/"}:
            warnings.append(f"{provider.provider_id} has unusual credential location: {provider.credentials_location}")
    dimensions = capability_dimensions(root)
    for required in [
        "deterministic_transform",
        "file_system_local",
        "structured_output",
        "json_schema",
        "tool_use",
        "long_context",
        "local_execution",
        "privacy_sensitive",
        "cheap_bulk",
        "reasoning_heavy",
        "frontier_review",
        "human_judgement",
        "test_execution",
        "code_edit",
        "unavailable",
    ]:
        if required not in dimensions:
            errors.append(f"capability matrix missing dimension: {required}")
    return {
        "result": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "provider_count": len(providers),
    }


def provider_catalog_ids(repo_root: Path | None = None) -> list[str]:
    return [provider.provider_id for provider in load_provider_catalog(repo_root)]
