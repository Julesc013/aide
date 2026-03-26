"""Static boot-slice policy for the shared-core bootstrap runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

BOOT_SLICE_ID: Final[str] = "boot-slice-01"
BOOT_SLICE_TITLE: Final[str] = "Identify, invoke, report, and mark"
PROTOCOL_VERSION: Final[int] = 1
EDITOR_MARKER_PREFIX: Final[str] = "AIDE_BOOT: "
SUPPORTED_EXECUTION_MODES: Final[tuple[str, ...]] = (
    "embedded",
    "cli-bridge",
    "local-service",
)
SUPPORTED_FEATURES: Final[tuple[str, ...]] = (
    "boot.slice.invoke",
    "boot.slice.editor-marker",
)


@dataclass(frozen=True)
class LanePolicy:
    family: str
    technology: str
    execution_mode_bias: str
    editor_policy: str
    target_capability: str
    notes: str

    @property
    def lane_id(self) -> str:
        return f"{self.family}.{self.technology}"


LANE_POLICIES: Final[dict[tuple[str, str], LanePolicy]] = {
    ("microsoft.visual-studio", "com-addin"): LanePolicy(
        family="microsoft.visual-studio",
        technology="com-addin",
        execution_mode_bias="cli-bridge",
        editor_policy="optional",
        target_capability="L2",
        notes="Legacy-native report-first lane. Editor marker remains optional in the first wave.",
    ),
    ("microsoft.visual-studio", "vsix-v1"): LanePolicy(
        family="microsoft.visual-studio",
        technology="vsix-v1",
        execution_mode_bias="cli-bridge",
        editor_policy="optional",
        target_capability="L2",
        notes="Legacy VSIX report-first lane. Editor marker remains optional in the first wave.",
    ),
    ("microsoft.visual-studio", "vsix-v2-vssdk"): LanePolicy(
        family="microsoft.visual-studio",
        technology="vsix-v2-vssdk",
        execution_mode_bias="embedded",
        editor_policy="required",
        target_capability="L2",
        notes="Reference-native lane whose first accepted proof includes the deterministic editor marker.",
    ),
    ("microsoft.visual-studio", "extensibility"): LanePolicy(
        family="microsoft.visual-studio",
        technology="extensibility",
        execution_mode_bias="local-service",
        editor_policy="optional",
        target_capability="L2",
        notes="Modern out-of-process lane. Editor marker remains optional until the first stable service path exists.",
    ),
    ("microsoft.visual-studio-mac", "monodevelop-addin"): LanePolicy(
        family="microsoft.visual-studio-mac",
        technology="monodevelop-addin",
        execution_mode_bias="cli-bridge",
        editor_policy="optional",
        target_capability="L2",
        notes="Archival-native lane. Editor marker remains optional in the first wave.",
    ),
    ("microsoft.visual-studio-mac", "companion"): LanePolicy(
        family="microsoft.visual-studio-mac",
        technology="companion",
        execution_mode_bias="cli-bridge",
        editor_policy="fallback",
        target_capability="L1",
        notes="Companion fallback lane used when native archival proof is blocked or deferred.",
    ),
    ("apple.xcode", "xcodekit"): LanePolicy(
        family="apple.xcode",
        technology="xcodekit",
        execution_mode_bias="embedded",
        editor_policy="required",
        target_capability="L2",
        notes="Editor-native Xcode lane whose accepted first proof includes the deterministic editor marker.",
    ),
    ("apple.xcode", "companion"): LanePolicy(
        family="apple.xcode",
        technology="companion",
        execution_mode_bias="cli-bridge",
        editor_policy="fallback",
        target_capability="L1",
        notes="Companion fallback lane for older or broader Xcode workflows outside XcodeKit.",
    ),
    ("metrowerks.codewarrior", "ide-sdk"): LanePolicy(
        family="metrowerks.codewarrior",
        technology="ide-sdk",
        execution_mode_bias="cli-bridge",
        editor_policy="optional",
        target_capability="L2",
        notes="Archival-native CodeWarrior lane. Editor marker remains optional until environment bring-up stabilizes.",
    ),
    ("metrowerks.codewarrior", "companion"): LanePolicy(
        family="metrowerks.codewarrior",
        technology="companion",
        execution_mode_bias="cli-bridge",
        editor_policy="fallback",
        target_capability="L1",
        notes="Companion fallback lane for blocked or unresolved native CodeWarrior paths.",
    ),
}


def get_lane_policy(family: str, technology: str) -> LanePolicy | None:
    """Return the static lane policy for the committed boot-slice lanes."""

    return LANE_POLICIES.get((family, technology))
