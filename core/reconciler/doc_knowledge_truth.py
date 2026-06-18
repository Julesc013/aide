"""Report-only documentation and knowledge truth reconciliation.

This module observes selected AIDE documentation, OKF, queue, evidence,
protocol, report, and projection surfaces. It emits report-convention
GovernanceFinding records and never repairs, rewrites, regenerates, moves, or
normalizes source artifacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


TASK_ID = "AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01"
ACCEPTED_PREDECESSOR = "AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01"
RECOMMENDED_NEXT_TASK = "AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01"
SECONDARY_FUTURE_TASK = "AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01"
DETERMINISTIC_TIMESTAMP = "2026-06-18T00:00:00+10:00"

REPORT_ROOT = Path(".aide/reports/self-management")
REPORT_JSON = REPORT_ROOT / "doc-knowledge-truth-reconciler.json"
REPORT_MD = REPORT_ROOT / "doc-knowledge-truth-reconciler.md"
FINDINGS_JSON = REPORT_ROOT / "doc-knowledge-truth-reconciler.findings.json"

TRUTH_PRECEDENCE = [
    "accepted governance and policy",
    "canonical protocol/schema definitions",
    ".aide/queue/index.yaml and queue task status",
    "build/check/accept evidence",
    "accepted capability/conformance records",
    "generated reports and indexes",
    "OKF knowledge projections",
    "human-facing documentation",
    "generated context/tool-specific projections",
]

EXPLICIT_NON_CAPABILITIES = [
    "automatic_doc_repair",
    "automatic_okf_regeneration",
    "automatic_queue_repair",
    "automatic_evidence_repair",
    "file_moves",
    "file_renames",
    "reference_rewrites",
    "migration_apply",
    "generated_output_ledger",
    "runtime",
    "provider_calls",
    "network_calls",
    "github_mutation",
    "branch_worktree_automation",
    "release_behavior",
    "target_repo_mutation",
]

ALLOWED_SEVERITIES = {"info", "warning", "error", "blocker"}
ALLOWED_SURFACES = {
    "documentation",
    "okf_knowledge",
    "queue_state",
    "protocol",
    "capability",
    "evidence",
    "generated_report",
    "context_projection",
    "interop_projection",
    "policy",
    "acceptance_state",
}
ALLOWED_TAXONOMY = {
    "stale_claim",
    "missing_evidence",
    "queue_drift",
    "schema_drift",
    "generated_truth_risk",
    "authority_overlap",
    "reference_break_risk",
    "unsupported_capability_claim",
    "status_mismatch",
    "explicit_non_capability_omitted",
    "projection_drift",
    "truth_alignment_confirmed",
}

TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".toml"}
CODE_SUFFIXES = {".py"}
MAX_TEXT_BYTES = 2_000_000

ROOT_DOCS = [
    "README.md",
    "AGENTS.md",
    "ROADMAP.md",
    "PLANS.md",
    "IMPLEMENT.md",
    "DOCUMENTATION.md",
    "CHANGELOG.md",
]

SCAN_ROOTS = [
    ("governance", "policy"),
    ("docs", "documentation"),
    (".aide/policies", "policy"),
    (".aide/protocol", "protocol"),
    ("core/protocol", "protocol"),
    (".aide/reports", "generated_report"),
    (".aide/knowledge/okf", "okf_knowledge"),
    (".aide/context", "context_projection"),
    (".agents", "interop_projection"),
    (".codex", "interop_projection"),
]

SELECTED_QUEUE_TASKS = [
    "AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01",
    "AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01",
    "AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01",
    "AIDE-ACCEPT-RECONCILER-REPORTS-01",
    "AIDE-BUILD-CAPABILITY-MANIFEST-01",
    "AIDE-CHECK-CAPABILITY-MANIFEST-01",
    "AIDE-ACCEPT-CAPABILITY-MANIFEST-01",
]

OUTPUT_PATHS = {
    REPORT_JSON.as_posix(),
    REPORT_MD.as_posix(),
    FINDINGS_JSON.as_posix(),
}


@dataclass(frozen=True)
class SourceRecord:
    path: str
    surface: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class GovernanceFinding:
    id: str
    severity: str
    surface: str
    taxonomy: str
    claim: str
    expected: str
    observed: str
    evidence_refs: list[str]
    affected_paths: list[str]
    recommendation: str
    next_task: str


def stable_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(data), encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_text_optional(path: Path) -> str:
    try:
        return read_text(path)
    except OSError:
        return ""


def read_json_optional(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(read_text(path))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def rel_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_output_path(rel: str) -> bool:
    return rel in OUTPUT_PATHS or rel.startswith(f".aide/queue/{TASK_ID}/")


def _clean_scalar(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[0] in {"'", '"'} and stripped[-1:] == stripped[0]:
        return stripped[1:-1]
    return stripped


def parse_top_level_scalars(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line or raw_line.startswith((" ", "\t", "-")):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key:
            values[key] = _clean_scalar(value)
    return values


def parse_simple_list(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_list = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == f"{key}:":
            in_list = True
            continue
        if not in_list:
            continue
        if stripped.startswith("- "):
            values.append(_clean_scalar(stripped[2:]))
            continue
        if stripped and not raw_line.startswith((" ", "\t")):
            break
    return values


def parse_queue_index(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_items = False
    key_value = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "items:":
            in_items = True
            continue
        if not in_items:
            continue
        if stripped.startswith("- id:"):
            if current is not None:
                items.append(current)
            current = {"id": _clean_scalar(stripped.split(":", 1)[1])}
            continue
        if current is None:
            continue
        match = key_value.match(raw_line.rstrip())
        if match:
            key, value = match.groups()
            current[key] = _clean_scalar(value)
    if current is not None:
        items.append(current)
    return items


def git_ref(repo_root: Path, ref: str = "HEAD") -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", ref],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError:
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def path_surface(rel: str) -> str:
    if rel.startswith(".aide/knowledge/okf/"):
        return "okf_knowledge"
    if rel.startswith(".aide/context/"):
        return "context_projection"
    if rel.startswith(".aide/reports/"):
        return "generated_report"
    if rel.startswith(".aide/protocol/") or rel.startswith("core/protocol/"):
        return "protocol"
    if rel.startswith(".aide/policies/") or rel.startswith("governance/"):
        return "policy"
    if rel.startswith(".aide/queue/"):
        return "queue_state"
    if rel.startswith(".agents/") or rel.startswith(".codex/"):
        return "interop_projection"
    return "documentation"


def iter_candidate_files(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for rel in ROOT_DOCS:
        path = repo_root / rel
        if path.exists() and path.is_file():
            paths.append(path)
    for task_id in SELECTED_QUEUE_TASKS:
        for name in ["task.yaml", "status.yaml"]:
            path = repo_root / ".aide/queue" / task_id / name
            if path.exists() and path.is_file():
                paths.append(path)
        evidence_dir = repo_root / ".aide/queue" / task_id / "evidence"
        if evidence_dir.exists():
            paths.extend(sorted(path for path in evidence_dir.glob("*.md") if path.is_file()))
    paths.append(repo_root / ".aide/queue/index.yaml")
    for rel_root, _surface in SCAN_ROOTS:
        root = repo_root / rel_root
        if not root.exists():
            continue
        if root.is_file():
            paths.append(root)
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            suffixes = TEXT_SUFFIXES | (CODE_SUFFIXES if rel_root in {".aide/protocol", "core/protocol"} else set())
            if path.suffix.lower() not in suffixes:
                continue
            paths.append(path)
    unique: dict[str, Path] = {}
    for path in paths:
        rel = rel_path(path, repo_root)
        if is_output_path(rel):
            continue
        if "__pycache__" in path.parts or ".git" in path.parts or ".aide.local" in path.parts:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > MAX_TEXT_BYTES:
            continue
        unique[rel] = path
    return [unique[key] for key in sorted(unique)]


def collect_sources(repo_root: str | Path) -> list[SourceRecord]:
    root = Path(repo_root)
    records: list[SourceRecord] = []
    for path in iter_candidate_files(root):
        rel = rel_path(path, root)
        records.append(
            SourceRecord(
                path=rel,
                surface=path_surface(rel),
                sha256=sha256_file(path),
                size_bytes=path.stat().st_size,
            )
        )
    return records


def read_sources(repo_root: Path, sources: list[SourceRecord]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for record in sources:
        path = repo_root / record.path
        try:
            texts[record.path] = read_text(path)
        except UnicodeDecodeError:
            continue
        except OSError:
            continue
    return texts


def counts_by_key(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def report_result(findings: list[GovernanceFinding]) -> str:
    severities = {finding.severity for finding in findings}
    if "blocker" in severities:
        return "BLOCKED"
    if "error" in severities:
        return "PASS_WITH_WARNINGS"
    if "warning" in severities:
        return "PASS_WITH_WARNINGS"
    return "PASS"


def new_finding(
    findings: list[GovernanceFinding],
    *,
    severity: str,
    surface: str,
    taxonomy: str,
    claim: str,
    expected: str,
    observed: str,
    evidence_refs: list[str],
    affected_paths: list[str],
    recommendation: str,
    next_task: str = RECOMMENDED_NEXT_TASK,
) -> None:
    if severity not in ALLOWED_SEVERITIES:
        raise ValueError(f"unsupported severity: {severity}")
    if surface not in ALLOWED_SURFACES:
        raise ValueError(f"unsupported surface: {surface}")
    if taxonomy not in ALLOWED_TAXONOMY:
        raise ValueError(f"unsupported taxonomy: {taxonomy}")
    findings.append(
        GovernanceFinding(
            id=f"DKT-{len(findings) + 1:03d}",
            severity=severity,
            surface=surface,
            taxonomy=taxonomy,
            claim=claim,
            expected=expected,
            observed=observed,
            evidence_refs=sorted(set(evidence_refs)),
            affected_paths=sorted(set(affected_paths)),
            recommendation=recommendation,
            next_task=next_task,
        )
    )


def queue_facts(repo_root: Path) -> dict[str, Any]:
    index_path = repo_root / ".aide/queue/index.yaml"
    items = parse_queue_index(read_text_optional(index_path))
    by_id = {item.get("id", ""): item for item in items if item.get("id")}
    statuses: dict[str, dict[str, str]] = {}
    for task_id in SELECTED_QUEUE_TASKS + [TASK_ID]:
        status_path = repo_root / ".aide/queue" / task_id / "status.yaml"
        if status_path.exists():
            statuses[task_id] = parse_top_level_scalars(read_text_optional(status_path))
    return {
        "items": items,
        "by_id": by_id,
        "statuses": statuses,
        "task_ids": sorted(by_id),
    }


def source_hash_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_hashes = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped == "source_hashes:":
            in_hashes = True
            continue
        if not in_hashes:
            continue
        if stripped.startswith("- path:"):
            if current is not None:
                records.append(current)
            current = {"path": _clean_scalar(stripped.split(":", 1)[1])}
            continue
        if current is not None and stripped.startswith("sha256:"):
            current["sha256"] = _clean_scalar(stripped.split(":", 1)[1])
            continue
        if stripped and not raw_line.startswith((" ", "\t")):
            break
    if current is not None:
        records.append(current)
    return records


def collect_okf_hash_gaps(repo_root: Path, texts: dict[str, str]) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    for rel, text in texts.items():
        if not rel.startswith(".aide/knowledge/okf/"):
            continue
        for record in source_hash_records(text):
            source_rel = record.get("path", "")
            recorded = record.get("sha256", "")
            source = repo_root / source_rel
            if not source_rel or not recorded or not source.exists() or not source.is_file():
                continue
            current = sha256_file(source)
            if current != recorded:
                gaps.append(
                    {
                        "page": rel,
                        "source": source_rel,
                        "recorded": recorded,
                        "current": current,
                    }
                )
    return sorted(gaps, key=lambda item: (item["page"], item["source"]))


PATH_REF_PATTERN = re.compile(r"`([^`]+)`")


def normalize_ref(ref: str) -> str | None:
    value = ref.strip().strip(".,:;()[]")
    if not value or " " in value or value.startswith(("http://", "https://", "aide://")):
        return None
    if "*" in value or "<" in value or ">" in value or "$" in value:
        return None
    value = value.replace("\\", "/")
    if "#L" in value:
        value = value.split("#L", 1)[0]
    if not (
        value.startswith(".")
        or value.startswith("docs/")
        or value.startswith("governance/")
        or value.startswith("core/")
        or value.startswith("scripts/")
        or value.startswith("shared/")
        or value.startswith("hosts/")
        or value.startswith("bridges/")
        or value.startswith("inventory/")
        or value.startswith("matrices/")
        or value.startswith("evals/")
        or value.startswith("packaging/")
        or value in ROOT_DOCS
    ):
        return None
    return value


def collect_missing_path_refs(repo_root: Path, texts: dict[str, str]) -> list[dict[str, str]]:
    missing: list[dict[str, str]] = []
    for source_rel, text in texts.items():
        if source_rel.startswith(".aide/reports/self-management/doc-knowledge-truth-reconciler"):
            continue
        for match in PATH_REF_PATTERN.finditer(text):
            ref = normalize_ref(match.group(1))
            if not ref:
                continue
            path = repo_root / ref
            if path.exists():
                continue
            missing.append({"source": source_rel, "ref": ref})
    return sorted({(item["source"], item["ref"]) for item in missing})


def _contains_implemented_claim(text: str, name: str) -> bool:
    lowered = text.lower()
    name_lower = name.lower()
    for match in re.finditer(re.escape(name_lower), lowered):
        start = max(0, match.start() - 100)
        end = min(len(lowered), match.end() + 100)
        window = lowered[start:end]
        if any(term in window for term in ["implemented", "complete", "accepted"]):
            if not any(term in window for term in ["not implemented", "not complete", "not accepted", "planned", "deferred"]):
                return True
    return False


def collect_findings(repo_root: str | Path) -> list[GovernanceFinding]:
    root = Path(repo_root)
    sources = collect_sources(root)
    texts = read_sources(root, sources)
    queue = queue_facts(root)
    findings: list[GovernanceFinding] = []

    accepted = read_json_optional(root / ".aide/reports/self-management/accept-self-management-charter.json")
    accepted_next = str(accepted.get("recommended_next_task") or "")
    if accepted_next == TASK_ID:
        new_finding(
            findings,
            severity="info",
            surface="acceptance_state",
            taxonomy="truth_alignment_confirmed",
            claim="Accepted self-management charter routes Track B to the doc/knowledge truth reconciler.",
            expected=f"`{ACCEPTED_PREDECESSOR}` recommends `{TASK_ID}`.",
            observed=f"accepted report recommended_next_task is `{accepted_next}`.",
            evidence_refs=[".aide/reports/self-management/accept-self-management-charter.json"],
            affected_paths=[".aide/reports/self-management/accept-self-management-charter.json"],
            recommendation="Use the accepted predecessor as the authority for this build task.",
        )
    else:
        new_finding(
            findings,
            severity="error",
            surface="acceptance_state",
            taxonomy="queue_drift",
            claim="Accepted self-management charter should route to this reconciler build task.",
            expected=f"`recommended_next_task` should be `{TASK_ID}`.",
            observed=f"`recommended_next_task` is `{accepted_next or 'missing'}`.",
            evidence_refs=[".aide/reports/self-management/accept-self-management-charter.json"],
            affected_paths=[".aide/reports/self-management/accept-self-management-charter.json"],
            recommendation="Do not proceed beyond report generation until next-task routing is reviewed.",
        )

    if TASK_ID in queue["by_id"]:
        new_finding(
            findings,
            severity="info",
            surface="queue_state",
            taxonomy="truth_alignment_confirmed",
            claim="The current build task is registered in the canonical queue index.",
            expected=f"`.aide/queue/index.yaml` includes `{TASK_ID}`.",
            observed=f"`{TASK_ID}` is present in queue index.",
            evidence_refs=[".aide/queue/index.yaml"],
            affected_paths=[".aide/queue/index.yaml"],
            recommendation="Stop this build at needs_review and route to the independent check task.",
        )

    policy_text = texts.get(".aide/policies/self-management.yaml", "")
    required_sequence = parse_simple_list(policy_text, "required_sequence")
    if "AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01" in required_sequence and TASK_ID in required_sequence:
        root_index = required_sequence.index("AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01")
        current_index = required_sequence.index(TASK_ID)
        if root_index < current_index and accepted_next == TASK_ID:
            new_finding(
                findings,
                severity="warning",
                surface="policy",
                taxonomy="status_mismatch",
                claim="The original self-management policy sequence still routes RootAuthorityManifest before the doc/knowledge truth reconciler.",
                expected="Accepted predecessor routing should be reflected or explicitly superseded by future policy/docs updates.",
                observed="Policy required_sequence lists AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01 before AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01, while the accepted charter acceptance routes this reconciler next.",
                evidence_refs=[
                    ".aide/policies/self-management.yaml",
                    ".aide/reports/self-management/accept-self-management-charter.json",
                ],
                affected_paths=[".aide/policies/self-management.yaml"],
                recommendation="Keep this as a report-only drift finding for the check/accept gate; do not edit policy in this build task.",
            )

    self_doc_text = texts.get("docs/reference/aide-self-management.md", "")
    if "AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01" in self_doc_text and accepted_next == TASK_ID:
        new_finding(
            findings,
            severity="warning",
            surface="documentation",
            taxonomy="stale_claim",
            claim="The self-management reference still documents the earlier initial queue sequence.",
            expected="Human docs should either match accepted next-task routing or explicitly mark older sequence text as superseded.",
            observed="`docs/reference/aide-self-management.md` lists RootAuthorityManifest before DocKnowledgeTruthReconciler, while acceptance routes DocKnowledgeTruthReconciler next.",
            evidence_refs=[
                "docs/reference/aide-self-management.md",
                ".aide/reports/self-management/accept-self-management-charter.json",
            ],
            affected_paths=["docs/reference/aide-self-management.md"],
            recommendation="Report the drift now; repair should be a future docs-truth task after check/accept.",
        )

    latest_text = texts.get(".aide/context/latest-task-packet.md", "")
    if latest_text and TASK_ID not in latest_text:
        phase = "unknown"
        match = re.search(r"^## PHASE\s+(.+?)$", latest_text, flags=re.MULTILINE)
        if match:
            phase = match.group(1).strip()
        new_finding(
            findings,
            severity="warning",
            surface="context_projection",
            taxonomy="projection_drift",
            claim="The latest generated task packet is stale relative to accepted Track B routing.",
            expected=f"Generated context should mention `{TASK_ID}` after accepted routing, or remain clearly non-canonical.",
            observed=f"Latest task packet phase is `{phase}` and does not mention `{TASK_ID}`.",
            evidence_refs=[
                ".aide/context/latest-task-packet.md",
                ".aide/reports/self-management/accept-self-management-charter.json",
            ],
            affected_paths=[".aide/context/latest-task-packet.md"],
            recommendation="Do not regenerate context in this task; keep as a projection drift finding.",
        )

    okf_next = texts.get(".aide/knowledge/okf/current-state/next-work.md", "")
    if okf_next and TASK_ID not in okf_next:
        new_finding(
            findings,
            severity="warning",
            surface="okf_knowledge",
            taxonomy="stale_claim",
            claim="OKF next-work projection is stale relative to accepted Track B routing.",
            expected=f"OKF next-work should explain `{TASK_ID}` or clearly indicate it predates the accepted charter acceptance.",
            observed="OKF next-work still recommends AIDE-CHECK-OKF-KNOWLEDGE-BUNDLE-01 and says not to recommend Reconciler directly from that older build slice.",
            evidence_refs=[
                ".aide/knowledge/okf/current-state/next-work.md",
                ".aide/reports/self-management/accept-self-management-charter.json",
            ],
            affected_paths=[".aide/knowledge/okf/current-state/next-work.md"],
            recommendation="Report only; OKF regeneration remains deferred.",
        )

    okf_queue = texts.get(".aide/knowledge/okf/current-state/queue.md", "")
    if okf_queue and "AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01" in okf_queue:
        new_finding(
            findings,
            severity="warning",
            surface="okf_knowledge",
            taxonomy="projection_drift",
            claim="OKF queue current-state projection still describes the older OKF build slice.",
            expected="OKF current-state pages should not be mistaken for current queue truth when their source hash or task text is stale.",
            observed="OKF queue page names AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01 as the current slice.",
            evidence_refs=[
                ".aide/knowledge/okf/current-state/queue.md",
                ".aide/queue/index.yaml",
            ],
            affected_paths=[".aide/knowledge/okf/current-state/queue.md"],
            recommendation="Report projection drift; do not hand-edit or regenerate OKF in this task.",
        )

    hash_gaps = collect_okf_hash_gaps(root, texts)
    if hash_gaps:
        affected = sorted({gap["page"] for gap in hash_gaps})
        observed = "; ".join(f"{gap['page']} -> {gap['source']}" for gap in hash_gaps[:8])
        if len(hash_gaps) > 8:
            observed += f"; plus {len(hash_gaps) - 8} more"
        new_finding(
            findings,
            severity="warning",
            surface="okf_knowledge",
            taxonomy="projection_drift",
            claim="Some OKF pages record source hashes that no longer match their source files.",
            expected="OKF source hashes should match the current source file when the projection is fresh.",
            observed=observed,
            evidence_refs=affected[:12],
            affected_paths=affected,
            recommendation="Keep as OKF drift evidence for a future authorized incremental OKF projection task.",
        )

    readme = texts.get("README.md", "")
    reconciler_accept_status = queue["statuses"].get("AIDE-ACCEPT-RECONCILER-REPORTS-01", {})
    if "Reconciler reports | Planned" in readme and reconciler_accept_status.get("result") == "ACCEPTED_WITH_WARNINGS":
        new_finding(
            findings,
            severity="warning",
            surface="documentation",
            taxonomy="stale_claim",
            claim="README implementation status still describes Reconciler reports as planned.",
            expected="Human documentation should reflect that minimal Reconciler reports were accepted with warnings, while runtime repair remains deferred.",
            observed="README table says `Reconciler reports | Planned`; queue status says AIDE-ACCEPT-RECONCILER-REPORTS-01 result ACCEPTED_WITH_WARNINGS.",
            evidence_refs=[
                "README.md",
                ".aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/status.yaml",
            ],
            affected_paths=["README.md"],
            recommendation="Report now; any README refresh should be a separate docs-truth repair task.",
        )

    if "Reconciler, CapabilityManifest, ConformanceProfile" in texts.get("DOCUMENTATION.md", ""):
        new_finding(
            findings,
            severity="warning",
            surface="documentation",
            taxonomy="stale_claim",
            claim="DOCUMENTATION current status groups Reconciler and CapabilityManifest with future phases.",
            expected="Documentation should distinguish accepted report-only Reconciler, built/checked CapabilityManifest, and truly future Track A objects.",
            observed="DOCUMENTATION.md still says Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 remain future phases.",
            evidence_refs=[
                "DOCUMENTATION.md",
                ".aide/queue/AIDE-ACCEPT-RECONCILER-REPORTS-01/status.yaml",
                ".aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/status.yaml",
            ],
            affected_paths=["DOCUMENTATION.md"],
            recommendation="Keep as stale documentation finding; do not edit DOCUMENTATION.md in this build.",
        )

    missing_refs = collect_missing_path_refs(root, texts)
    if missing_refs:
        observed = "; ".join(f"{source} -> {ref}" for source, ref in missing_refs[:12])
        if len(missing_refs) > 12:
            observed += f"; plus {len(missing_refs) - 12} more"
        new_finding(
            findings,
            severity="warning",
            surface="documentation",
            taxonomy="reference_break_risk",
            claim="Some inspected documentation or reports reference paths that are absent from the current worktree.",
            expected="Path references used as evidence or documentation links should resolve, be glob placeholders, or be explicitly marked as examples.",
            observed=observed,
            evidence_refs=sorted({source for source, _ref in missing_refs[:12]}),
            affected_paths=sorted({source for source, _ref in missing_refs}),
            recommendation="Review path references in a future doc-truth repair/check task; no references are rewritten here.",
        )

    status_paths = [
        root / ".aide/queue/AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01/status.yaml",
        root / ".aide/queue/AIDE-CHECK-CAPABILITY-MANIFEST-01/status.yaml",
    ]
    missing_evidence: list[str] = []
    for status_path in status_paths:
        status_text = read_text_optional(status_path)
        for evidence_ref in parse_simple_list(status_text, "evidence"):
            if evidence_ref and not (root / evidence_ref).exists():
                missing_evidence.append(f"{rel_path(status_path, root)} -> {evidence_ref}")
    if missing_evidence:
        new_finding(
            findings,
            severity="error",
            surface="evidence",
            taxonomy="missing_evidence",
            claim="Some selected queue status files reference missing evidence.",
            expected="Evidence refs in selected build/check/accept status files should exist.",
            observed="; ".join(missing_evidence[:12]),
            evidence_refs=[rel_path(path, root) for path in status_paths],
            affected_paths=[item.split(" -> ", 1)[0] for item in missing_evidence],
            recommendation="Block acceptance until missing evidence refs are repaired or dispositioned.",
        )
    else:
        new_finding(
            findings,
            severity="info",
            surface="evidence",
            taxonomy="truth_alignment_confirmed",
            claim="Selected acceptance/check status evidence references resolve.",
            expected="Evidence refs in selected status files exist.",
            observed="No missing evidence refs found for accepted self-management charter or CapabilityManifest check status.",
            evidence_refs=[rel_path(path, root) for path in status_paths if path.exists()],
            affected_paths=[rel_path(path, root) for path in status_paths if path.exists()],
            recommendation="Preserve this evidence check in the independent check task.",
        )

    explanatory_surfaces = {"documentation", "okf_knowledge", "context_projection", "interop_projection"}
    for rel, text in texts.items():
        if rel.startswith((".aide/reports/", ".aide/queue/")) or path_surface(rel) not in explanatory_surfaces:
            continue
        for capability in ["ConformanceProfile", "PatchTransaction", "AdapterManifest", "ContextPack v2"]:
            if _contains_implemented_claim(text, capability):
                new_finding(
                    findings,
                    severity="warning",
                    surface=path_surface(rel),
                    taxonomy="unsupported_capability_claim",
                    claim=f"`{capability}` appears near implemented/accepted wording in an explanatory surface.",
                    expected=f"`{capability}` should remain planned/deferred unless accepted evidence exists.",
                    observed=f"Potential implemented/accepted wording around `{capability}` in `{rel}`.",
                    evidence_refs=[rel],
                    affected_paths=[rel],
                    recommendation="Review the wording in a future docs-truth repair task; this build does not edit it.",
                )

    return findings


def build_findings_payload(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    findings = [asdict(finding) for finding in collect_findings(root)]
    result = report_result([GovernanceFinding(**finding) for finding in findings])
    return {
        "task_id": TASK_ID,
        "checked_predecessor": ACCEPTED_PREDECESSOR,
        "result": result,
        "report_convention": "GovernanceFinding",
        "report_convention_only": True,
        "schema_implemented": False,
        "cli_implemented": False,
        "findings": findings,
    }


def build_report(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    sources = collect_sources(root)
    findings_payload = build_findings_payload(root)
    findings = findings_payload["findings"]
    result = str(findings_payload["result"])
    source_hashes = {record.path: record.sha256 for record in sources}
    scanned_paths = [record.path for record in sources]
    return {
        "task_id": TASK_ID,
        "result": result,
        "scan_mode": "full",
        "repository_ref": git_ref(root, "HEAD"),
        "baseline_ref": ACCEPTED_PREDECESSOR,
        "baseline_commit_ref": git_ref(root, "HEAD"),
        "generated_at": DETERMINISTIC_TIMESTAMP,
        "source_count": len(sources),
        "finding_count": len(findings),
        "counts_by_severity": counts_by_key(findings, "severity"),
        "counts_by_surface": counts_by_key(findings, "surface"),
        "counts_by_taxonomy": counts_by_key(findings, "taxonomy"),
        "truth_precedence": list(TRUTH_PRECEDENCE),
        "scanned_paths": scanned_paths,
        "excluded_paths": sorted(OUTPUT_PATHS | {f".aide/queue/{TASK_ID}/**", ".git/**", ".aide.local/**", "**/__pycache__/**"}),
        "source_hashes": source_hashes,
        "explicit_non_capabilities": list(EXPLICIT_NON_CAPABILITIES),
        "report_only": True,
        "mutation_performed": False,
        "automatic_doc_repair": False,
        "automatic_okf_regeneration": False,
        "automatic_queue_repair": False,
        "automatic_evidence_repair": False,
        "file_moves": False,
        "file_renames": False,
        "reference_rewrites": False,
        "migration_apply": False,
        "generated_output_ledger": False,
        "runtime": False,
        "provider_calls": False,
        "network_calls": False,
        "github_mutation": False,
        "branch_worktree_automation": False,
        "release_behavior": False,
        "target_repo_mutation": False,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
        "secondary_future_task": SECONDARY_FUTURE_TASK,
    }


def render_markdown(report: dict[str, Any], findings_payload: dict[str, Any]) -> str:
    lines = [
        "# Doc/Knowledge Truth Reconciler",
        "",
        f"- task_id: {report.get('task_id')}",
        f"- result: {report.get('result')}",
        f"- scan_mode: {report.get('scan_mode')}",
        f"- repository_ref: {report.get('repository_ref')}",
        f"- baseline_ref: {report.get('baseline_ref')}",
        f"- source_count: {report.get('source_count')}",
        f"- finding_count: {report.get('finding_count')}",
        "- report_only: true",
        "- mutation_performed: false",
        f"- recommended_next_task: {report.get('recommended_next_task')}",
        "",
        "## Truth Precedence",
        "",
    ]
    for index, item in enumerate(report.get("truth_precedence", []), start=1):
        lines.append(f"{index}. {item}")
    lines.extend(["", "## Counts By Severity", ""])
    for key, value in report.get("counts_by_severity", {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Counts By Surface", ""])
    for key, value in report.get("counts_by_surface", {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Counts By Taxonomy", ""])
    for key, value in report.get("counts_by_taxonomy", {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Findings", ""])
    for finding in findings_payload.get("findings", []):
        lines.extend(
            [
                f"### {finding.get('id')}",
                "",
                f"- severity: {finding.get('severity')}",
                f"- surface: {finding.get('surface')}",
                f"- taxonomy: {finding.get('taxonomy')}",
                f"- claim: {finding.get('claim')}",
                f"- expected: {finding.get('expected')}",
                f"- observed: {finding.get('observed')}",
                f"- next_task: {finding.get('next_task')}",
                "",
            ]
        )
    lines.extend(["## Explicit Non-Capabilities", ""])
    for item in report.get("explicit_non_capabilities", []):
        lines.append(f"- {item}")
    return "\n".join(lines).rstrip() + "\n"


def write_doc_knowledge_truth_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    findings_payload = build_findings_payload(root)
    report = build_report(root)
    write_json(root / REPORT_JSON, report)
    write_json(root / FINDINGS_JSON, findings_payload)
    write_text(root / REPORT_MD, render_markdown(report, findings_payload))
    return report


def validate_doc_knowledge_truth_reports(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    errors: list[str] = []
    warnings: list[str] = []
    report = read_json_optional(root / REPORT_JSON)
    findings_payload = read_json_optional(root / FINDINGS_JSON)
    markdown = read_text_optional(root / REPORT_MD)

    for rel in [REPORT_JSON, FINDINGS_JSON, REPORT_MD]:
        if not (root / rel).exists():
            errors.append(f"missing report: {rel.as_posix()}")

    required_report_fields = {
        "task_id",
        "result",
        "scan_mode",
        "repository_ref",
        "baseline_ref",
        "source_count",
        "finding_count",
        "counts_by_severity",
        "counts_by_surface",
        "counts_by_taxonomy",
        "scanned_paths",
        "excluded_paths",
        "source_hashes",
        "explicit_non_capabilities",
        "recommended_next_task",
    }
    if report and not required_report_fields.issubset(report):
        errors.append("report JSON is missing required metadata fields")

    findings = findings_payload.get("findings", []) if isinstance(findings_payload.get("findings"), list) else []
    required_finding_fields = {
        "id",
        "severity",
        "surface",
        "taxonomy",
        "claim",
        "expected",
        "observed",
        "evidence_refs",
        "affected_paths",
        "recommendation",
        "next_task",
    }
    for finding in findings:
        if not isinstance(finding, dict):
            errors.append("finding is not an object")
            continue
        missing = sorted(required_finding_fields - set(finding))
        if missing:
            errors.append(f"finding {finding.get('id', '<unknown>')} missing fields: {', '.join(missing)}")
        if finding.get("severity") not in ALLOWED_SEVERITIES:
            errors.append(f"finding {finding.get('id')} has unsupported severity")
        if finding.get("surface") not in ALLOWED_SURFACES:
            errors.append(f"finding {finding.get('id')} has unsupported surface")
        if finding.get("taxonomy") not in ALLOWED_TAXONOMY:
            errors.append(f"finding {finding.get('id')} has unsupported taxonomy")
        if finding.get("severity") != "info" and not finding.get("next_task"):
            errors.append(f"finding {finding.get('id')} has no next_task")
        if finding.get("severity") != "info" and not finding.get("evidence_refs"):
            errors.append(f"finding {finding.get('id')} has no evidence_refs")
        if finding.get("severity") != "info" and not finding.get("affected_paths"):
            errors.append(f"finding {finding.get('id')} has no affected_paths")

    if report and report.get("finding_count") != len(findings):
        errors.append("report finding_count does not match findings payload")
    if report and report.get("recommended_next_task") != RECOMMENDED_NEXT_TASK:
        errors.append("report recommended_next_task is incorrect")
    if report and report.get("report_only") is not True:
        errors.append("report_only boundary is not true")
    for key in EXPLICIT_NON_CAPABILITIES:
        if report and report.get(key, False) is not False:
            errors.append(f"non-capability flag not false: {key}")

    missing_markdown_ids = [str(finding.get("id")) for finding in findings if str(finding.get("id")) not in markdown]
    if missing_markdown_ids:
        errors.append(f"Markdown missing finding ids: {', '.join(missing_markdown_ids)}")

    if findings:
        warnings.append("GovernanceFinding records are observations only; no repair was attempted.")
    status = "FAILED_VALIDATION" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS"
    return {
        "task_id": TASK_ID,
        "validation_status": status,
        "validated": status in {"PASS", "PASS_WITH_WARNINGS"},
        "reports_present": not any(error.startswith("missing report:") for error in errors),
        "required_report_fields_present": bool(report) and required_report_fields.issubset(report),
        "finding_fields_valid": not any("finding " in error for error in errors),
        "markdown_json_agree": not missing_markdown_ids and bool(markdown),
        "report_only_boundary_preserved": bool(report) and report.get("report_only") is True,
        "errors": errors,
        "warnings": warnings,
        "recommended_next_task": RECOMMENDED_NEXT_TASK,
    }
