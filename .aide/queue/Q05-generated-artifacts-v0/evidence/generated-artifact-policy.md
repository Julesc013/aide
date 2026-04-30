# Q05 Generated Artifact Policy Evidence

Date: 2026-04-30

## Source Of Truth

- `.aide/` remains canonical for the AIDE Profile/Contract.
- `.aide/queue/` remains canonical for long-running queue execution state.
- Generated downstream artifacts are managed or preview outputs and are not canonical truth.
- Runtime cache, chat state, IDE task queues, and generated previews are not source of truth.

## Target Modes Used

| Target | Mode | Result |
| --- | --- | --- |
| `AGENTS.md` | managed section | Written between AIDE generated markers. |
| `.agents/skills/aide-queue/SKILL.md` | managed section | Written between AIDE generated markers. |
| `.agents/skills/aide-execplan/SKILL.md` | managed section | Written between AIDE generated markers. |
| `.agents/skills/aide-review/SKILL.md` | managed section | Written between AIDE generated markers. |
| `.aide/generated/preview/CLAUDE.md` | generated preview only | Written as a non-canonical preview. |
| `.claude/settings.json` | deferred | Not created. |
| `.claude/agents/*` | deferred | Not created. |

## Marker And Manifest Model

- Marker prefix: `AIDE-GENERATED`.
- Generator: `aide-harness-generated-artifacts-v0`.
- Generator version: `q05.generated-artifacts.v0`.
- Manifest path: `.aide/generated/manifest.yaml`.
- Fingerprints use stable SHA-256 values.
- Wall-clock timestamps are intentionally absent from generated files.

## Safety Rules Enforced

- `aide compile` is non-mutating by default.
- `aide compile --preview` writes only preview output under `.aide/generated/preview/**`.
- `aide compile --write` writes only approved managed sections, preview output, and the manifest.
- Markerless preview targets are blocked rather than overwritten.
- Final root `CLAUDE.md` and final `.claude/**` are hard validation errors under Q05 policy.
