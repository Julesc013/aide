# Q05 Remaining Risks

Date: 2026-04-30

## Must Fix Before Q05 Review

None identified.

## Review Notes

- Q05 is intentionally stopped at `needs_review`.
- Q00 through Q03 remain `needs_review`; this is existing queue posture and not introduced by Q05.
- `scripts/aide-queue-next` now reports Q06 because Q05 is at review gate; the helper remains status-only and not dependency-aware.

## Should Fix Later

- `.aide/policies/generated-artifacts.yaml` still contains Q03 planned-boundary wording. Q05 did not edit it because Q05 implementation allowed paths did not include `.aide/policies/**`.
- Full YAML or JSON Schema validation remains deferred.
- Generated artifact manifest parsing remains a restricted line-oriented reader.
- Source-fingerprint drift is warning/review-required in v0; a later Compatibility or policy task may choose stricter severity.

## Deferred By Design

- Final root `CLAUDE.md`.
- Final `.claude/settings.json`.
- Final `.claude/agents/**`.
- New broad `.agents/skills/**` families.
- Q06 Compatibility baseline.
- Q07 Dominium Bridge baseline.
- Runtime, Hosts, Commander, Mobile, IDE extensions, provider/model integrations, browser bridges, app surfaces, release automation, and autonomous service logic.
