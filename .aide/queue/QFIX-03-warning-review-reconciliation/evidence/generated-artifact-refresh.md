# Generated Artifact Refresh

## Command

- `py -3 scripts/aide compile --write`

## Result

- Result: PASS_WITH_WARNINGS.
- Manifest source fingerprint refreshed to
  `sha256:31528290f242dbebb27650e866b4b30ee182413a334860377624fa0bd0709189`.
- Written file: `.aide/generated/manifest.yaml`.
- Managed sections in `AGENTS.md` and generated AIDE skills were already current.
- Preview `CLAUDE.md` output was already current.
- Deferred Claude targets remained deferred.
- No Dominium Bridge outputs were written.

## Follow-up Validation

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS with 6 warnings.
- The previous `GENERATED-SOURCE-STALE` warning is removed.
- Remaining Harness warnings are review-gate warnings for Q00, Q01, Q02, Q03,
  Q05, and Q06.
