# AIDE State

## Git State

- Repository: `julesc013/aide`.
- Branch: `main`.
- HEAD: `6246811cf02ece09bd25b53ce0625919db658f51`.
- Remote: `origin https://github.com/Julesc013/aide.git`.
- Local branches: `main`.
- Remote branches visible locally: `origin/main`.
- Tags: none.
- Initial worktree: clean.
- `.aide.local/`: ignored by `.gitignore`.
- Git helper ahead/behind: local `main` is 39 commits ahead of `origin/main`.
- No fetch, push, merge, branch creation, branch deletion, tag creation, or
  remote mutation was performed.

## Queue State

- Prior AIDE-local queue items through Q31, Q34, and QFIX-03 are marked
  `passed`.
- Q32 and Q33 are target-repo prompts, not AIDE-local queue items.
- Q35 is not present as a queue packet.
- QCHECK-03 is registered and ends at `needs_review`.

## Current Validation Summary

- Harness validate: PASS, 149 info, 0 warning, 0 error.
- Harness doctor: PASS, 149 info, 0 warning, 0 error.
- Harness self-check: PASS, validation warning count 0.
- AIDE Lite doctor/validate/test/selftest: PASS.
- AIDE Lite eval run: PASS, 30/30, warn_count 0.
- AIDE Lite verify: PASS, 0 warnings, 0 errors.
- Commit check latest and range: PASS.
- Changelog preview/validate/status: PASS, preview-only, 8 malformed legacy
  commits reported for review.
- Git policy: PASS.
- Git helper commands: non-mutating dry-run/report-only; blocked where expected
  by audit dirty tree, missing `dev`, and canonical branch role.
- GitHub command family: unavailable; Q35 missing.
- Pack-status: PASS.
- Core unit tests: Harness, Compat, Gateway, Providers all PASS.

## Generated Reports Refreshed

- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/changelog/**`
- `.aide/git/**`
- `.aide/reports/token-ledger.jsonl`
- `.aide/reports/token-savings-summary.md`
- `.aide/export/aide-lite-pack-v0/**`

## Current Limitation

The local repo is governance-ready through Q34/QFIX-03. It is not GitHub/CI
advisory-ready because Q35 has not been implemented.
