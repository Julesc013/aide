# Generated Artifact Refresh

## Command

- `py -3 scripts/aide compile --write`

## Result

- Result: PASS_WITH_WARNINGS.
- Final manifest source fingerprint refreshed to
  `sha256:15317a45f454d318aa10cb58605440116a2cb737453e7673142df37e26ce2634`.
- Written file: `.aide/generated/manifest.yaml`.
- Managed sections in `AGENTS.md` and generated AIDE skills were already current.
- Preview `CLAUDE.md` output was already current.
- Deferred Claude targets remained deferred.
- No Dominium Bridge outputs were written.

## Follow-up Validation

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS with 6 warnings.
- The previous `GENERATED-SOURCE-STALE` warning is removed.
- After review reconciliation and the final compile refresh,
  `py -3 scripts/aide validate` reports PASS with 0 warnings.
- `py -3 scripts/aide doctor` and `py -3 scripts/aide self-check` also report
  PASS with 0 warnings and Q35 as the next AIDE-local step.
