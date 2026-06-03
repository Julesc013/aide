# AIDE-APPLY-02-REPAIR-01 ExecPlan

## Purpose

Repair exactly the four `AIDE-CHECK-APPLY-02` findings against `AIDE-APPLY-02 - Scoped Transaction Executor v0`.

## Scope

- Make the checked-in dry-run example runnable with current fixture hashes.
- Add resolved-path containment checks for target and output paths.
- Bound v0 apply behavior by blocking multi-mutating apply before mutation.
- Ensure direct core persisted reports include repo-relative `report_path`.
- Add focused tests and evidence.

## Non-Goals

- No lifecycle repair apply.
- No install apply.
- No upgrade apply.
- No rollback/uninstall apply.
- No target repo mutation.
- No branch/worktree mutation.
- No merge, push, promotion, release publication, GitHub mutation, provider/model call, Gateway call, or network call.
- No broad active-repo apply.
- No production-ready, release-ready, target-repo-capable, install-capable, upgrade-capable, repair-apply-capable, rollback/uninstall-capable, or broad-apply-capable label.

## Milestones

1. Confirm repair authority from AIDE-CHECK-APPLY-02 and AIDE-APPLY-02 packets.
2. Add repair task scaffold and allowed-path evidence.
3. Implement the four repairs and targeted tests.
4. Refresh scoped executor reports and validation evidence.
5. End at `needs_review` and hand off to recheck.

## Progress

- 2026-06-04: Repair task scaffold created from AIDE-CHECK-APPLY-02 repair proposal.
- 2026-06-04: Four checkpoint findings repaired, targeted tests and scoped/managed/transaction validations run, evidence written, and task left at `needs_review` for `AIDE-CHECK-APPLY-02-RECHECK-01`.

## Validation Intent

Run targeted unit tests, AIDE Lite scoped-transaction command tests, scoped-transaction status/fixture-plan/fixture-verify/validate/run example, managed-section validation, transaction validation, task inspect/evidence checks, full AIDE validation, JSON/YAML checks, boundary searches, secret scan, `git diff --check`, and commit check after commit.
