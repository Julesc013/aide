# AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01 ExecPlan

## Objective

Repair the two material PatchTransaction path-scope fail-closed defects found by
`AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`.

## Scope

- Reject drive-prefixed relative paths such as `C:repo/file.txt`.
- Reject duplicate-normalized path declarations such as `src//file.py` plus
  `src/file.py`.
- Preserve existing fail-closed behavior for absolute paths, Windows absolute
  paths, UNC paths, traversal, empty or dot-only paths, declared paths outside
  allowed scope, forbidden matches, direct allowed/forbidden overlap, separator
  normalization, and prefix-boundary checks.
- Add focused regression tests.
- Regenerate PatchTransaction projection/validation reports if needed.
- Write repair-specific reports, evidence, and next-task prompt.

## Dependencies

- Failed check: `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01`.
- Repaired build: `AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`.
- Blocked acceptance: `AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01`.

## Allowed Paths

- `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `core/protocol/patch_transaction.py`
- `.aide/scripts/tests/test_aide_patch_transaction.py`
- `.aide/reports/patch-transaction/**`
- `.aide/reports/patch-transaction-repair/**`
- `PLANS.md`
- `IMPLEMENT.md`

## Milestones

- Live queue and failed check reviewed.
- Failure reproduced with direct scope probes.
- Validator repaired.
- Focused tests added.
- Repair reports and evidence written.
- Validation matrix run.
- Task stopped at `needs_review`.

## Verification Intent

Run compile checks, focused PatchTransaction unit tests, direct path-scope
probes, PatchTransaction status/project/validate, predecessor validators, task
inspect/evidence checks, broad AIDE validation, JSON report parsing,
deterministic projection review, source mutation review, Git diff checks, a
secret-like scan, and commit policy validation.

## Exit Criteria

The task stops at `needs_review` with `PASS_WITH_WARNINGS`; the two material
path-scope findings are repaired; no apply, approval, policy, rollback,
admission, trust, runtime, provider/network/Gateway/GitHub, branch/worktree,
release, promotion, or target-repository mutation behavior is added; and the
next task is `AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01`.

## Progress

- Live queue confirmed the failed check recommends this repair.
- Validator now rejects Windows drive-prefix strings before treating paths as
  repository-relative locators.
- Scope validation now fails on duplicate normalized paths.
- Focused regression tests cover both material findings.

## Non-Capabilities

This repair does not accept PatchTransaction, approve a transaction, apply a
patch, mutate a target repository, execute rollback, evaluate policy, activate
a profile, admit or trust a subject, build AdapterManifest, build ContextPack
v2, run workers, implement runtime/Test Broker/Service/Commander/Workbench,
call providers/models/network/Gateway/GitHub, create branches or worktrees,
publish releases, or promote anything.
