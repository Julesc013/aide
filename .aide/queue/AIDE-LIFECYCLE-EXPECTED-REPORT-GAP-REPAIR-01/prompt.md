# Prompt

Create `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01` as a no-apply expected-report repair WorkUnit. Add static expected report files for `install-clean`, `install-existing-manual-preserved`, `upgrade-manual-preserved`, `repair-plan-missing-marker`, `repair-plan-malformed-marker`, and `uninstall-manual-preserved`.

Do not mutate generated plans, fixture targets, implementation files, target repositories, branch/worktree state, release state, GitHub state, provider/model/Gateway surfaces, or network state. Do not execute lifecycle apply, fixture apply, rollback, uninstall, active repo apply, or target repo apply.

Stop at `needs_review` and select exactly one next safe WorkUnit.
