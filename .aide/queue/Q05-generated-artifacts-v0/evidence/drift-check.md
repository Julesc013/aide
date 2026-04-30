# Q05 Drift Check Evidence

Date: 2026-04-30

## Implemented Checks

Harness validation now checks:

- `.aide/generated/manifest.yaml` schema marker;
- manifest source fingerprint against current Q05 source inputs;
- required generated target existence;
- managed/preview marker presence;
- marker body fingerprint against actual generated section body;
- manifest content fingerprint against generated body fingerprint;
- final root `CLAUDE.md` absence;
- final `.claude/**` absence;
- intentionally deferred Claude targets.

## Observed Current State

`py -3 scripts/aide validate` reports:

- `GENERATED-SOURCE-CURRENT` for `.aide/generated/manifest.yaml`;
- `GENERATED-CURRENT` for `AGENTS.md`;
- `GENERATED-CURRENT` for `.agents/skills/aide-queue/SKILL.md`;
- `GENERATED-CURRENT` for `.agents/skills/aide-execplan/SKILL.md`;
- `GENERATED-CURRENT` for `.agents/skills/aide-review/SKILL.md`;
- `GENERATED-CURRENT` for `.aide/generated/preview/CLAUDE.md`;
- `GENERATED-DEFERRED` for `.claude/settings.json`;
- `GENERATED-DEFERRED` for `.claude/agents/*`.

## Drift Severity

- Marker/body mismatch is an `error`.
- Missing required generated target is an `error`.
- Markerless final Claude target is an `error`.
- Source fingerprint drift is a `warning` in Q05 v0 and requires review/regeneration.
- Deferred targets are `info` while absent.

## Test Coverage

`core/harness/tests/test_aide_harness.py` includes a generated marker drift test that modifies generated body text in memory and confirms the marker fingerprint no longer matches.
