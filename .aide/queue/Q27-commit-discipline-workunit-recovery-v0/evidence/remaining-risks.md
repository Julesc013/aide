# Remaining Risks

- Q27 is not implemented.
- Current `pack-status` fails before Q27 edits, so export-pack integrity is not
  a reliable baseline for Q27 regression detection.
- Current AIDE Lite validation fails because
  `.aide.local.example/secrets/README.md` is missing.
- The missing local-state template path is outside Q27's allowed paths.
- Existing Q25 evidence says pack-status passed at Q25 time, but current HEAD
  does not reproduce that result.
- Q27 commit checker, hook, changelog preview, WorkUnit policy, recovery policy,
  golden tasks, tests, docs, and export integration remain future work after
  the blocker is cleared.

## Recommended Next Action

Repair or re-review Q25 so current repo-local validation passes:

- `python3 .aide/scripts/aide_lite.py validate`;
- `python3 .aide/scripts/aide_lite.py pack-status`.

Then reopen Q27 and implement the full requested scope.
