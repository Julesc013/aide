# AIDE-APPLY-02 Prompt

Implement `AIDE-APPLY-02 - Scoped Transaction Executor v0` only after re-reading this queue packet, `ExecPlan.md`, `status.yaml`, `allowed-paths.md`, `protected-paths.md`, `forbidden-operations.md`, `validation-checklist.md`, and `review-gate.md`.

The implementation must stay inside the exact allowed paths recorded in this task and must not widen scope without a review-gated authorization update.

## Required Shape

- scoped transaction executor v0 only;
- explicit operator-provided target paths only;
- explicit operation allowlists;
- explicit path boundaries;
- managed-section operations by default;
- preimage hash checks before mutation;
- postimage verification after mutation;
- staged-change records;
- rollback-compatible records;
- dry-run/report mode;
- plan/apply/report split;
- validation evidence;
- review-gated status;
- fixture coverage;
- managed-section patcher integration;
- capability reality labels.

## Forbidden

- no install apply;
- no upgrade apply;
- no repair apply;
- no rollback/uninstall apply;
- no target repo mutation;
- no branch/worktree mutation;
- no merge;
- no push;
- no promotion;
- no release publication;
- no GitHub mutation;
- no provider/model calls;
- no Gateway calls;
- no network calls;
- no broad active-repo apply;
- no broad deletes;
- no broad moves;
- no mutation outside explicit allowed paths;
- no mutation without preimage hash checks;
- no mutation without postimage verification;
- no mutation without rollback-compatible records;
- no mutation without evidence;
- no self-promotion from review-gated to accepted or production-ready.

## Validation

Run the validation commands in `validation-checklist.md`, record evidence in `evidence/`, and end with status `needs_review`. The next task after implementation is `AIDE-CHECK-APPLY-02`.
