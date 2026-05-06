"""Repo-local Gateway status payloads for the Q19 skeleton."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "aide.gateway-status.v0"
GATEWAY_VERSION = "q19.gateway-skeleton.v0"
SERVICE_NAME = "aide-gateway-skeleton"

GATEWAY_POLICY_PATH = ".aide/policies/gateway.yaml"
GATEWAY_STATUS_JSON_PATH = ".aide/gateway/latest-gateway-status.json"
GATEWAY_STATUS_MD_PATH = ".aide/gateway/latest-gateway-status.md"
ROUTE_DECISION_JSON_PATH = ".aide/routing/latest-route-decision.json"
ROUTE_DECISION_MD_PATH = ".aide/routing/latest-route-decision.md"
TOKEN_SUMMARY_PATH = ".aide/reports/token-savings-summary.md"
VERIFICATION_REPORT_PATH = ".aide/verification/latest-verification-report.md"
GOLDEN_RUN_JSON_PATH = ".aide/evals/runs/latest-golden-tasks.json"
CACHE_KEYS_JSON_PATH = ".aide/cache/latest-cache-keys.json"
RECOMMENDATIONS_PATH = ".aide/controller/latest-recommendations.md"
LOCAL_STATE_POLICY_PATH = ".aide/policies/local-state.yaml"
CACHE_POLICY_PATH = ".aide/policies/cache.yaml"
PROFILE_PATH = ".aide/profile.yaml"

SUMMARY_REFS = {
    "task_packet": ".aide/context/latest-task-packet.md",
    "context_packet": ".aide/context/latest-context-packet.md",
    "review_packet": ".aide/context/latest-review-packet.md",
    "verification_report": VERIFICATION_REPORT_PATH,
    "token_summary": TOKEN_SUMMARY_PATH,
    "golden_task_report": GOLDEN_RUN_JSON_PATH,
    "outcome_recommendations": RECOMMENDATIONS_PATH,
    "cache_keys": CACHE_KEYS_JSON_PATH,
    "route_decision": ROUTE_DECISION_JSON_PATH,
    "gateway_policy": GATEWAY_POLICY_PATH,
}

READINESS_GROUPS = {
    "token_survival": [
        ".aide/policies/token-budget.yaml",
        ".aide/context/latest-task-packet.md",
        ".aide/prompts/compact-task.md",
    ],
    "context_compiler": [
        ".aide/context/repo-map.json",
        ".aide/context/test-map.json",
        ".aide/context/context-index.json",
        ".aide/context/latest-context-packet.md",
    ],
    "verifier": [
        ".aide/policies/verification.yaml",
        VERIFICATION_REPORT_PATH,
    ],
    "evidence_review": [
        ".aide/prompts/evidence-review.md",
        ".aide/context/latest-review-packet.md",
    ],
    "token_ledger": [
        ".aide/policies/token-ledger.yaml",
        ".aide/reports/token-ledger.jsonl",
        TOKEN_SUMMARY_PATH,
    ],
    "golden_tasks": [
        ".aide/policies/evals.yaml",
        ".aide/evals/golden-tasks/catalog.yaml",
        GOLDEN_RUN_JSON_PATH,
    ],
    "outcome_controller": [
        ".aide/policies/controller.yaml",
        ".aide/controller/latest-outcome-report.md",
        RECOMMENDATIONS_PATH,
    ],
    "router_profile": [
        ".aide/policies/routing.yaml",
        ROUTE_DECISION_JSON_PATH,
        ROUTE_DECISION_MD_PATH,
    ],
    "cache_boundary": [
        CACHE_POLICY_PATH,
        LOCAL_STATE_POLICY_PATH,
        CACHE_KEYS_JSON_PATH,
    ],
    "gateway_skeleton": [
        GATEWAY_POLICY_PATH,
        ".aide/gateway/endpoints.yaml",
        ".aide/gateway/lifecycle.yaml",
        ".aide/gateway/security-boundary.md",
    ],
}

ENDPOINTS = ["/health", "/status", "/route/explain", "/summaries", "/version"]


def repo_root_from(start: Path | None = None) -> Path:
    """Find the repository root by walking upward from start or cwd."""

    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".aide/profile.yaml").exists() and (candidate / ".aide/queue/index.yaml").exists():
            return candidate
    return current


def read_text(path: Path, max_chars: int | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    return text[:max_chars] if max_chars is not None else text


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def approx_tokens_for_chars(chars: int) -> int:
    return (chars + 3) // 4


def rel_stats(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_root / rel_path
    if not path.exists() or not path.is_file():
        return {"path": rel_path, "exists": False}
    try:
        text = read_text(path)
    except (OSError, UnicodeDecodeError):
        return {"path": rel_path, "exists": True, "readable": False}
    return {
        "path": rel_path,
        "exists": True,
        "readable": True,
        "chars": len(text),
        "lines": len(text.splitlines()),
        "approx_tokens": approx_tokens_for_chars(len(text)),
        "sha256": sha256_file(path)[:16],
    }


def parse_yaml_scalar(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def policy_metadata(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_root / rel_path
    if not path.exists():
        return {"path": rel_path, "exists": False}
    try:
        text = read_text(path, max_chars=20000)
    except OSError:
        return {"path": rel_path, "exists": True, "readable": False}
    return {
        "path": rel_path,
        "exists": True,
        "schema_version": parse_yaml_scalar(text, "schema_version"),
        "policy_id": parse_yaml_scalar(text, "policy_id"),
        "status": parse_yaml_scalar(text, "status"),
    }


def git_commit(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        return "unavailable"
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "unavailable"


def git_dirty(repo_root: Path) -> bool | str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--short"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        return "unavailable"
    if result.returncode != 0:
        return "unavailable"
    return bool(result.stdout.strip())


def readiness_for(repo_root: Path, rel_paths: list[str]) -> dict[str, Any]:
    missing = [rel for rel in rel_paths if not (repo_root / rel).exists()]
    return {
        "status": "ready" if not missing else "missing",
        "present": [rel for rel in rel_paths if (repo_root / rel).exists()],
        "missing": missing,
    }


def parse_verifier_status(repo_root: Path) -> str:
    path = repo_root / VERIFICATION_REPORT_PATH
    if not path.exists():
        return "unknown"
    text = read_text(path, max_chars=12000)
    match = re.search(r"result:\s*(PASS|WARN|FAIL)", text)
    if match:
        return match.group(1)
    for value in ["PASS", "WARN", "FAIL"]:
        if value in text[:2000]:
            return value
    return "unknown"


def parse_golden_status(repo_root: Path) -> str:
    data = read_json(repo_root / GOLDEN_RUN_JSON_PATH)
    if not data:
        return "unknown"
    result = data.get("result")
    return str(result) if result in {"PASS", "WARN", "FAIL"} else "unknown"


def parse_route_status(repo_root: Path) -> dict[str, Any]:
    data = read_json(repo_root / ROUTE_DECISION_JSON_PATH)
    if not data:
        return {"status": "unknown", "present": False}
    return {
        "status": "present",
        "present": True,
        "route_class": data.get("route_class", "unknown"),
        "task_class": data.get("task_class", "unknown"),
        "risk_class": data.get("risk_class", "unknown"),
        "blocked": bool(data.get("blocked", False)),
        "quality_gate_status": data.get("quality_gate_status", "unknown"),
        "token_budget_status": data.get("token_budget_status", "unknown"),
    }


def parse_cache_status(repo_root: Path) -> dict[str, Any]:
    data = read_json(repo_root / CACHE_KEYS_JSON_PATH)
    if not data:
        return {"status": "unknown", "present": False}
    keys = data.get("keys", {})
    boundary = data.get("local_state_boundary", {})
    return {
        "status": "present",
        "present": True,
        "key_count": len(keys) if isinstance(keys, dict) else 0,
        "local_state_ignored": bool(boundary.get("local_state_ignored", False)) if isinstance(boundary, dict) else False,
        "contents_inline": data.get("contents_inline"),
    }


def build_gateway_status(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    readiness = {name: readiness_for(root, refs) for name, refs in READINESS_GROUPS.items()}
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": GATEWAY_VERSION,
        "service": SERVICE_NAME,
        "mode": "local_skeleton_report_only",
        "provider_calls_enabled": False,
        "model_calls_enabled": False,
        "outbound_network_enabled": False,
        "raw_prompt_storage": False,
        "raw_response_storage": False,
        "repo_state": {
            "git_commit": git_commit(root),
            "dirty_state": git_dirty(root),
        },
        "policy": policy_metadata(root, GATEWAY_POLICY_PATH),
        "readiness": readiness,
        "signals": {
            "verifier_status": parse_verifier_status(root),
            "golden_task_status": parse_golden_status(root),
            "route": parse_route_status(root),
            "cache": parse_cache_status(root),
        },
        "summaries": {name: rel_stats(root, rel) for name, rel in SUMMARY_REFS.items()},
        "notes": [
            "Q19 exposes compact repo-local metadata only.",
            "Provider/model calls and proxy forwarding remain disabled.",
            "Runtime state remains outside committed .aide/ under gitignored .aide.local/.",
        ],
    }


def health_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "provider_calls_enabled": False,
        "model_calls_enabled": False,
        "outbound_network_enabled": False,
    }


def status_payload(repo_root: Path | None = None) -> dict[str, Any]:
    status = build_gateway_status(repo_root)
    readiness = status["readiness"]
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "gateway_policy_present": readiness["gateway_skeleton"]["status"] == "ready",
        "route_decision_present": status["signals"]["route"].get("present", False),
        "verifier_report_present": (repo_root_from(repo_root) / VERIFICATION_REPORT_PATH).exists(),
        "golden_tasks_status_present": status["signals"]["golden_task_status"] != "unknown",
        "token_summary_present": (repo_root_from(repo_root) / TOKEN_SUMMARY_PATH).exists(),
        "cache_boundary_present": status["signals"]["cache"].get("present", False),
        "local_state_boundary_present": (repo_root_from(repo_root) / LOCAL_STATE_POLICY_PATH).exists(),
        "readiness": readiness,
        "signals": status["signals"],
    }


def route_explain_payload(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    data = read_json(root / ROUTE_DECISION_JSON_PATH)
    if not data:
        return {
            "status": "warning",
            "service": SERVICE_NAME,
            "schema_version": SCHEMA_VERSION,
            "route_decision_present": False,
            "message": "No latest route decision exists; run aide_lite.py route explain.",
        }
    compact_keys = [
        "schema_version",
        "route_id",
        "task_source",
        "task_class",
        "risk_class",
        "route_class",
        "fallback_route_class",
        "hard_floor_applied",
        "blocked",
        "blocked_reason",
        "rationale",
        "evidence_sources",
        "required_checks",
        "token_budget_status",
        "verifier_status",
        "golden_task_status",
        "outcome_recommendation_status",
        "quality_gate_status",
        "notes",
    ]
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "route_decision_present": True,
        "route_decision": {key: data.get(key) for key in compact_keys if key in data},
        "provider_calls_enabled": False,
        "model_calls_enabled": False,
    }


def summaries_payload(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "summaries": {name: rel_stats(root, rel) for name, rel in SUMMARY_REFS.items()},
        "contents_inline": False,
    }


def version_payload(repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root_from(repo_root)
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "gateway_version": GATEWAY_VERSION,
        "gateway_policy": policy_metadata(root, GATEWAY_POLICY_PATH),
        "profile": policy_metadata(root, PROFILE_PATH),
        "provider_calls_enabled": False,
        "model_calls_enabled": False,
    }


def endpoint_payload(path: str, repo_root: Path | None = None) -> tuple[int, dict[str, Any]]:
    normalized = path.split("?", 1)[0].rstrip("/") or "/"
    if normalized == "/health":
        return 200, health_payload()
    if normalized == "/status":
        return 200, status_payload(repo_root)
    if normalized == "/route/explain":
        return 200, route_explain_payload(repo_root)
    if normalized == "/summaries":
        return 200, summaries_payload(repo_root)
    if normalized == "/version":
        return 200, version_payload(repo_root)
    return 404, {
        "status": "not_found",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "message": f"Unknown Q19 Gateway endpoint: {normalized}",
        "allowed_endpoints": ENDPOINTS,
    }


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def render_gateway_status_markdown(data: dict[str, Any]) -> str:
    readiness = data.get("readiness", {})
    signals = data.get("signals", {})
    route = signals.get("route", {}) if isinstance(signals, dict) else {}
    cache = signals.get("cache", {}) if isinstance(signals, dict) else {}
    lines = [
        "# Latest Gateway Status",
        "",
        f"- schema_version: `{data.get('schema_version', SCHEMA_VERSION)}`",
        f"- generated_by: `{data.get('generated_by', GATEWAY_VERSION)}`",
        f"- service: `{data.get('service', SERVICE_NAME)}`",
        f"- mode: `{data.get('mode', 'local_skeleton_report_only')}`",
        f"- provider_calls_enabled: `{str(data.get('provider_calls_enabled', False)).lower()}`",
        f"- model_calls_enabled: `{str(data.get('model_calls_enabled', False)).lower()}`",
        f"- outbound_network_enabled: `{str(data.get('outbound_network_enabled', False)).lower()}`",
        f"- raw_prompt_storage: `{str(data.get('raw_prompt_storage', False)).lower()}`",
        f"- raw_response_storage: `{str(data.get('raw_response_storage', False)).lower()}`",
        "",
        "## Readiness",
        "",
    ]
    if isinstance(readiness, dict):
        for name in sorted(readiness):
            item = readiness[name]
            if not isinstance(item, dict):
                continue
            missing = item.get("missing", [])
            missing_count = len(missing) if isinstance(missing, list) else 0
            lines.append(f"- {name}: {item.get('status', 'unknown')} (missing: {missing_count})")
    lines.extend(
        [
            "",
            "## Signals",
            "",
            f"- verifier_status: {signals.get('verifier_status', 'unknown') if isinstance(signals, dict) else 'unknown'}",
            f"- golden_task_status: {signals.get('golden_task_status', 'unknown') if isinstance(signals, dict) else 'unknown'}",
            f"- route_class: {route.get('route_class', 'unknown') if isinstance(route, dict) else 'unknown'}",
            f"- route_blocked: {str(route.get('blocked', 'unknown')).lower() if isinstance(route, dict) else 'unknown'}",
            f"- token_budget_status: {route.get('token_budget_status', 'unknown') if isinstance(route, dict) else 'unknown'}",
            f"- cache_key_count: {cache.get('key_count', 'unknown') if isinstance(cache, dict) else 'unknown'}",
            "",
            "## Endpoint Policy",
            "",
            "- `/health`: local liveness metadata only",
            "- `/status`: compact readiness metadata only",
            "- `/route/explain`: latest advisory route decision only",
            "- `/summaries`: repo-relative refs and short file stats only",
            "- `/version`: schema/policy/profile metadata only",
            "",
            "## Limits",
            "",
            "- No provider calls, model calls, outbound network calls, or proxy forwarding.",
            "- No raw prompt bodies, raw response bodies, secrets, or `.aide.local/` contents are stored or returned.",
            "- Q19 is not a production Gateway.",
            "",
        ]
    )
    return "\n".join(lines)


def write_gateway_status_files(repo_root: Path | None = None) -> tuple[Path, Path, dict[str, Any]]:
    root = repo_root_from(repo_root)
    data = build_gateway_status(root)
    json_path = root / GATEWAY_STATUS_JSON_PATH
    md_path = root / GATEWAY_STATUS_MD_PATH
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(stable_json(data), encoding="utf-8", newline="\n")
    md_path.write_text(render_gateway_status_markdown(data), encoding="utf-8", newline="\n")
    return json_path, md_path, data


def smoke_gateway(repo_root: Path | None = None) -> dict[str, Any]:
    results = []
    for endpoint in ENDPOINTS:
        status_code, payload = endpoint_payload(endpoint, repo_root)
        results.append(
            {
                "endpoint": endpoint,
                "status_code": status_code,
                "status": payload.get("status", "unknown"),
                "service": payload.get("service", SERVICE_NAME),
            }
        )
    not_found_code, not_found_payload = endpoint_payload("/unknown", repo_root)
    ok = all(item["status_code"] == 200 for item in results) and not_found_code == 404
    return {
        "schema_version": "aide.gateway-smoke.v0",
        "result": "PASS" if ok else "FAIL",
        "provider_calls_enabled": False,
        "model_calls_enabled": False,
        "outbound_network_enabled": False,
        "endpoints": results,
        "not_found_status_code": not_found_code,
        "not_found_status": not_found_payload.get("status"),
    }
