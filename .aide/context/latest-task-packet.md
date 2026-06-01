# AIDE Latest Task Packet

## PHASE

AIDE-ONLY - X-OS-00 AIDE Task OS Schemas and Policies

## GOAL

X-OS-00 - AIDE Task OS Schemas and Policies

## WHY

AIDE-CONTINUE-00 reconciled the queue after X-TEST-00 and deferred target-repo work. The next AIDE-local dependency is a report-only Task OS policy and schema layer for WorkUnits, blockers, repairs, waves, checkpoints, branch provenance records, and capability reality. This packet is a seed for X-OS-00 only; it does not authorize implementation inside AIDE-CONTINUE-00.

## CONTEXT_REFS

- `.aide/queue/AIDE-CONTINUE-00-aide-only-continuation/audit-report.md`
- `.aide/queue/AIDE-CONTINUE-00-aide-only-continuation/next-aide-task.md`
- `.aide/reports/aide-only-continuation.md`
- `.aide/reports/current-aide-roadmap.md`
- `.aide/queue/XCHECK-01R-cross-repo-aide-adoption-validation-efficiency-taskos-readiness-audit/x-series-next-plan.md`
- `.aide/queue/XCHECK-01R-cross-repo-aide-adoption-validation-efficiency-taskos-readiness-audit/taskos-readiness-audit.md`
- `.aide/queue/X-TEST-00-aide-cross-repo-validation-tier-model-v0/status.yaml`
- `.aide/queue/X-TEST-00-aide-cross-repo-validation-tier-model-v0/evidence/policy-schemas.md`
- `docs/reference/promotion-validation-gates.md`
- `docs/reference/validation-tier-model.md`
- `docs/reference/test-telemetry-contracts.md`
- `.aide/context/latest-context-packet.md`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-summary.md`

## DECISIONS_IN_FORCE

- `X-TEST-01` is deferred target work, not deleted, failed, completed, or superseded.
- `X-TEST-00` is implemented and ready for review; do not duplicate it.
- Task OS work starts report-only and dry-run-only.
- Apply, branch/worktree apply, merge, push, promotion, release publication, target sync, GitHub API mutation, Gateway/provider/model runtime, and target mutation remain gated.

## ALLOWED_PATHS

- `.aide/queue/X-OS-00-aide-task-os-schemas-and-policies/**`
- `.aide/queue/index.yaml`
- `.aide/policies/task-lifecycle.yaml`
- `.aide/policies/blockers.yaml`
- `.aide/policies/repair-loop.yaml`
- `.aide/policies/waves.yaml`
- `.aide/policies/checkpoints.yaml`
- `.aide/policies/dev-main-promotion.yaml`
- `.aide/policies/capability-reality.yaml`
- `.aide/tasks/**`
- `.aide/ledgers/*.schema.json`
- `.aide/reports/x-os-00-*.md`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- docs/reference files only when needed to explain the new policy records

## FORBIDDEN_PATHS

- no Eureka, Dominium, or other target repo files
- no `.git/**`, `.github/**`, `.env`, `.aide.local/**`, secrets, provider/model credentials, raw prompts, or raw responses

## FORBIDDEN_OPERATIONS

- no target sync, target install, target repair, target upgrade, target rollback, target uninstall, or target test execution
- no Task OS apply behavior
- no transactional apply implementation
- no branch creation, worktree creation, merge, push, promotion, prune, tag, or release publication
- no install/repair/upgrade/rollback/uninstall apply mode
- no Gateway/provider/model/runtime/host implementation
- no root moves, file deletes, file renames, reference rewrites, aliases, or shims

## IMPLEMENTATION

- Create a reviewed X-OS-00 queue item before editing Task OS policy/schema files.
- Read AIDE-CONTINUE-00, XCHECK-01R, X-TEST-00 evidence, and promotion/apply gate docs first.
- Keep the diff inside the X-OS-00 allowlist.
- Define schemas and policies only; do not add apply behavior.
- Preserve generated/manual boundaries.
- Use exact repo refs when a claim depends on a file.

## EXPECTED_OUTPUTS

- X-OS-00 queue packet with ExecPlan, status, prompt, reports, and evidence
- task lifecycle policy
- blocker taxonomy policy
- repair-loop policy
- wave and checkpoint policies
- dev/main promotion policy links in report-only form
- capability reality policy
- schemas for WorkUnits, task attempts, blockers, repair tasks, waves, checkpoints, task ledger, blocker ledger, capability ledger, branch provenance, and checkpoint ledger

## ACCEPTANCE

- X-OS-00 records source AIDE Task OS schemas and policies without applying behavior.
- Blockers, repairs, waves, checkpoints, and capability reality are first-class records.
- No branch, target, provider/model, release publication, GitHub API, or apply behavior occurs.
- Validation and evidence are recorded.
- Status stops at `needs_review`.

## EVIDENCE

- changed files
- policy and schema inventory
- validation commands and results
- warning disposition
- gated future-work confirmation
- unresolved risks and deliberate deferrals

## NON_GOALS

- no X-TEST-01 or X-TEST-03 target execution
- no target sync or target pilot
- no transactional apply implementation
- no branch/worktree apply
- no merge, push, promotion, prune, tag, or release publication
- no GitHub API mutation
- no Gateway/provider/model runtime
- no install/repair/upgrade/rollback/uninstall apply

## VALIDATION

- `git status --short --branch`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 .aide/scripts/aide_lite.py eval run`
- targeted secret scan

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `COMMITS`, `CHANGED_FILES`, `VALIDATION`, `RISKS`, and `NEXT`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: 5572
- approx_tokens: 1393
- budget_status: PASS
- warnings:
  - none
- formal ledger: `.aide/reports/token-ledger.jsonl`
