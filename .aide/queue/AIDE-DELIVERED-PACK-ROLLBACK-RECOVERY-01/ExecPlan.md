# Interrupted rollback continuation

Objective: let `rollback-pack` finish its own partial rollback from the exact
saved intent and previously supplied pack pair, without treating another
pending import as a rollback. Keep the accepted 1.0.0 Lite source and assets
frozen on `dev` until an exact release delta is reviewed.

Scope: the existing portable rollback/import CLI, focused importer tests, one
reference section, and this queue record. Reuse `recover_partial_import` and
the lifecycle lock. No new recovery engine, physical worktree or target repo.

Order: characterize the pending intent and exact digest; add a failing test
for an interrupted rollback using two payload writes; add refusal probes for
wrong direction, pack pair, digest and altered target. Implement the smallest
guarded continuation. Run affected tests in one bounded D job, obtain
independent source review, then decide dev/release integration separately.

Acceptance: explicit CLI recovery returns a success state only after receipt
and intent reconciliation; ordinary retry remains `RECOVERY_REQUIRED`;
malformed or competing states leave target and intent untouched. The exact
source/commit/test receipt and limits are recorded in task evidence.

Source implementation now exposes a saved `recovery_plan_digest` only for a
safe-mode intent in the rollback direction. An explicit `--recover-partial`
call reuses the existing guarded importer under the lifecycle lock and reports
`ROLLED_BACK_RECOVERED` after receipt/intent reconciliation. The first focused
test failed on the missing field, then passed after implementation. Eight
rollback cases and an additional CLI junction case pass through the D runner.
Exact job identities and observed limits are in `evidence/source-validation.md`.
Freeze source for independent review; do not project into the accepted Lite
release or move dev before an exact release delta decision.

The first independent review of `0bc7da3f` returned REQUEST_CHANGES: a
rollback-direction import intent bypassed the completed-receipt and equal
safe-payload-path checks. A differing-path reverse import reproduced the
finding. The repair validates the same receipt baseline before offering the
saved recovery digest; ordinary rollback uses that shared validation too.
The focused regression is green. Obtain review of the superseding exact
source after affected tests, while keeping the frozen Lite release separate.
