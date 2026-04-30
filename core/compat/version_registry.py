"""Version registry for the Q06 AIDE Compatibility baseline.

The registry is intentionally small and line-oriented. It is not a YAML
parser and it does not implement a migration engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


BASELINE_VERSION = "aide.compat-baseline.v0"


@dataclass(frozen=True)
class VersionSurface:
    id: str
    current_version: str
    source_path: str
    version_key: str
    owner_queue_item: str
    status: str
    posture: str


@dataclass(frozen=True)
class VersionFinding:
    code: str
    severity: str
    message: str
    path: str
    hint: str = ""


VERSION_SURFACES = [
    VersionSurface(
        "profile_contract",
        "aide.profile-contract.v0",
        ".aide/profile.yaml",
        "profile_contract_version",
        "Q03-profile-contract-v0",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "profile",
        "aide.profile.v0",
        ".aide/profile.yaml",
        "schema_version",
        "Q03-profile-contract-v0",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "toolchain_lock",
        "aide.toolchain-lock.v0",
        ".aide/toolchain.lock",
        "schema_version",
        "Q03-profile-contract-v0",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "queue_index",
        "aide.queue-index.v0",
        ".aide/queue/index.yaml",
        "schema_version",
        "Q00-bootstrap-audit",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "queue_policy",
        "aide.queue-policy.v0",
        ".aide/queue/policy.yaml",
        "schema_version",
        "Q00-bootstrap-audit",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "queue_status",
        "aide.queue-status.v0",
        ".aide/queue/Q06-compatibility-baseline/status.yaml",
        "schema_version",
        "Q00-bootstrap-audit",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "commands_catalog",
        "aide.commands-catalog.v0",
        ".aide/commands/catalog.yaml",
        "schema_version",
        "Q03-profile-contract-v0",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "compat_schema_versions",
        "aide.compat-schema-versions.v0",
        ".aide/compat/schema-versions.yaml",
        "schema_version",
        "Q06-compatibility-baseline",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "compatibility_baseline",
        BASELINE_VERSION,
        ".aide/compat/schema-versions.yaml",
        "compatibility_baseline_version",
        "Q06-compatibility-baseline",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "migration_baseline",
        "aide.migration-baseline.v0",
        ".aide/compat/migration-baseline.yaml",
        "schema_version",
        "Q06-compatibility-baseline",
        "current-noop",
        "no_automatic_mutation",
    ),
    VersionSurface(
        "replay_corpus",
        "aide.replay-corpus.v0",
        ".aide/compat/replay-corpus.yaml",
        "schema_version",
        "Q06-compatibility-baseline",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "upgrade_gates",
        "aide.upgrade-gates.v0",
        ".aide/compat/upgrade-gates.yaml",
        "schema_version",
        "Q06-compatibility-baseline",
        "current",
        "allow_current",
    ),
    VersionSurface(
        "deprecations",
        "aide.deprecations.v0",
        ".aide/compat/deprecations.yaml",
        "schema_version",
        "Q06-compatibility-baseline",
        "current",
        "warn_deprecated",
    ),
    VersionSurface(
        "generated_manifest",
        "aide.generated-manifest.v0",
        ".aide/generated/manifest.yaml",
        "schema_version",
        "Q05-generated-artifacts-v0",
        "current",
        "review_required_for_generated_artifact_contract_change",
    ),
    VersionSurface(
        "generated_artifact_generator",
        "q05.generated-artifacts.v0",
        ".aide/generated/manifest.yaml",
        "generator_version",
        "Q05-generated-artifacts-v0",
        "current",
        "review_required_for_generated_artifact_contract_change",
    ),
    VersionSurface(
        "harness_command_surface",
        "aide.harness-command-surface.v0",
        ".aide/compat/schema-versions.yaml",
        "harness_command_surface",
        "Q04-harness-v0",
        "current",
        "allow_current",
    ),
]

DEPRECATED_VERSIONS: dict[str, dict[str, str]] = {}


def known_surfaces() -> list[VersionSurface]:
    return list(VERSION_SURFACES)


def known_version_map() -> dict[str, str]:
    return {surface.id: surface.current_version for surface in VERSION_SURFACES}


def classify_version(surface_id: str, version: str) -> tuple[str, str]:
    """Return a conservative compatibility class and severity."""

    current = known_version_map().get(surface_id)
    if current is None:
        return "unknown_surface", "error"
    if version == current:
        return "current", "info"
    deprecated = DEPRECATED_VERSIONS.get(surface_id, {})
    if version in deprecated:
        return "deprecated", "warning"
    return "unknown_or_future", "error"


def _read_text(root: Path, relative: str) -> str | None:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except OSError:
        return None


def _matching_values(text: str, key: str) -> list[str]:
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$")
    values: list[str] = []
    for raw_line in text.splitlines():
        match = pattern.match(raw_line)
        if match:
            value = match.group(1).strip()
            if " #" in value:
                value = value.split(" #", 1)[0].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            values.append(value)
    return values


def _check_surface(root: Path, surface: VersionSurface) -> VersionFinding:
    text = _read_text(root, surface.source_path)
    if text is None:
        return VersionFinding(
            "COMPAT-VERSION-FILE",
            "error",
            f"compatibility surface {surface.id} source file is missing or unreadable",
            surface.source_path,
            "restore the source file or rerun the queue item that owns it",
        )

    values = _matching_values(text, surface.version_key)
    if surface.current_version in values:
        return VersionFinding(
            "COMPAT-VERSION-CURRENT",
            "info",
            f"{surface.id} is at current version {surface.current_version}",
            surface.source_path,
        )

    if values:
        observed = ", ".join(values)
        return VersionFinding(
            "COMPAT-VERSION-UNKNOWN",
            "error",
            f"{surface.id} has unrecognized version value(s): {observed}",
            surface.source_path,
            f"expected {surface.version_key}: {surface.current_version}",
        )

    return VersionFinding(
        "COMPAT-VERSION-MISSING",
        "error",
        f"{surface.id} is missing version key {surface.version_key}",
        surface.source_path,
        f"add {surface.version_key}: {surface.current_version}",
    )


def collect_version_findings(repo_root: Path) -> list[VersionFinding]:
    findings = [_check_surface(repo_root, surface) for surface in VERSION_SURFACES]

    expected_gate_ids = {
        "allow_current",
        "warn_deprecated",
        "block_unknown_future",
        "review_required_for_schema_change",
        "review_required_for_generated_artifact_contract_change",
        "no_automatic_mutation",
    }
    gate_text = _read_text(repo_root, ".aide/compat/upgrade-gates.yaml")
    if gate_text is None:
        findings.append(
            VersionFinding(
                "COMPAT-UPGRADE-GATES",
                "error",
                "upgrade gate record is missing",
                ".aide/compat/upgrade-gates.yaml",
            )
        )
    else:
        gate_ids = set(re.findall(r"^\s+- id:\s*(.+?)\s*$", gate_text, re.MULTILINE))
        missing = sorted(expected_gate_ids - gate_ids)
        if missing:
            findings.append(
                VersionFinding(
                    "COMPAT-UPGRADE-GATES",
                    "error",
                    f"upgrade gate record is missing gate id(s): {', '.join(missing)}",
                    ".aide/compat/upgrade-gates.yaml",
                )
            )
        else:
            findings.append(
                VersionFinding("COMPAT-UPGRADE-GATES", "info", "upgrade gate ids are present", ".aide/compat/upgrade-gates.yaml")
            )

    deprecation_text = _read_text(repo_root, ".aide/compat/deprecations.yaml")
    if deprecation_text is None:
        findings.append(
            VersionFinding("COMPAT-DEPRECATIONS", "error", "deprecation record is missing", ".aide/compat/deprecations.yaml")
        )
    elif "active_deprecations: []" in deprecation_text and "record_format:" in deprecation_text:
        findings.append(VersionFinding("COMPAT-DEPRECATIONS", "info", "deprecation record format is present", ".aide/compat/deprecations.yaml"))
    else:
        findings.append(
            VersionFinding(
                "COMPAT-DEPRECATIONS",
                "error",
                "deprecation record must include an empty active_deprecations list and record_format",
                ".aide/compat/deprecations.yaml",
            )
        )

    replay_text = _read_text(repo_root, ".aide/compat/replay-corpus.yaml")
    if replay_text is None:
        findings.append(VersionFinding("COMPAT-REPLAY", "error", "replay corpus record is missing", ".aide/compat/replay-corpus.yaml"))
    elif "runtime_replay: false" in replay_text and "expected_commands:" in replay_text:
        findings.append(VersionFinding("COMPAT-REPLAY", "info", "replay corpus is structural and non-runtime", ".aide/compat/replay-corpus.yaml"))
    else:
        findings.append(
            VersionFinding(
                "COMPAT-REPLAY",
                "error",
                "replay corpus must declare runtime_replay: false and expected_commands",
                ".aide/compat/replay-corpus.yaml",
            )
        )

    return findings

