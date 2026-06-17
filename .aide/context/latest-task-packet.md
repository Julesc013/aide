# AIDE Latest Task Packet

## PHASE

AIDE-STRUCTURE-00-current-truth-and-root-authority-audit - Current Truth And Root Authority Audit

## GOAL

Perform a check-only current-truth and root-authority audit before any file
shuffle, root creation, reference rewrite, source-truth promotion, or
documentation repair.

## WHY

The 2026-06-17 structure note and live repository doctrine agree that the next
safe step is not to move files. AIDE needs current repo/root/refactor evidence,
root authority candidates, and explicit stale-status findings before any future
root authority contract or move map.

## AUTHORITY

The queue task explicitly forbids implementation:

```yaml
check_only: true
report_only: true
authorizes_implementation: false
stop_state: needs_review
```

Canonical task packet:

- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/task.yaml`
- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/ExecPlan.md`
- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/status.yaml`

## CONTEXT_REFS

- `AGENTS.md`
- `.aide/profile.yaml`
- `.aide/queue/README.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- `.aide/policies/review-gates.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/task-resumption.yaml`
- `.aide/policies/recovery.yaml`
- `docs/reference/source-of-truth.md`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/roots/latest-root-inventory.md`
- `.aide/roots/latest-root-classification.md`
- `.aide/roots/latest-root-recycling-plan.md`
- `.aide/refactors/current-move-map.md`
- `.aide/refactors/map-validation-report.md`
- `.aide/reports/reconciler/findings.md`
- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.md`
- `docs/planning/repository-structure/current-truth-and-root-authority-audit.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/structure-current-state.json`
- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.json`
- `.aide/roots/latest-root-authority-candidates.md`
- `.aide/reports/task-os-*`
- `.aide/reports/reconciler/**`
- `.aide/repo/**`
- `.aide/roots/**`
- `.aide/refactors/**`
- `.aide/git/**`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## REVIEWED_READ_ONLY_PATHS

- `README.md`
- `.aide/knowledge/okf/**`
- `docs/reference/repo-intelligence-index.md`
- `docs/reference/root-recycling-framework.md`
- `docs/reference/refactor-control-plane.md`
- `docs/reference/move-salvage-path-aliases.md`
- existing queue task packets and evidence referenced by the reports

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- file moves
- file deletes
- reference rewrites
- path alias application
- shim creation
- new top-level root creation
- generated-output source-truth promotion
- source truth mutation
- queue acceptance mutation
- branch/worktree mutation
- GitHub mutation
- release or publishing work
- provider/model calls
- network calls
- Runtime, Service, Commander, host runtime, provider runtime, or broad kernel work

## IMPLEMENTATION

- Use existing AIDE report-only repo/root/refactor/Reconciler/Task OS helpers.
- Record current root list, current counts, drift findings, and root authority
  candidates.
- Keep root-authority contracts, docs repair, OKF refresh, and file movement as
  separate future queue tasks.
- Stop at `needs_review`.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py pack --task "AIDE-STRUCTURE-00-current-truth-and-root-authority-audit"`
- `py -3 .aide/scripts/aide_lite.py git plan`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py repo inventory`
- `py -3 .aide/scripts/aide_lite.py repo status`
- `py -3 .aide/scripts/aide_lite.py repo validate`
- `py -3 .aide/scripts/aide_lite.py roots inventory`
- `py -3 .aide/scripts/aide_lite.py roots classify`
- `py -3 .aide/scripts/aide_lite.py roots plan`
- `py -3 .aide/scripts/aide_lite.py roots status`
- `py -3 .aide/scripts/aide_lite.py roots validate`
- `py -3 .aide/scripts/aide_lite.py refactor status`
- `py -3 .aide/scripts/aide_lite.py refactor map-status`
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`
- `py -3 .aide/scripts/aide_lite.py reconciler report`
- `py -3 .aide/scripts/aide_lite.py reconciler validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## EVIDENCE

- `.aide/queue/AIDE-STRUCTURE-00-current-truth-and-root-authority-audit/evidence/*.md`
- `.aide/reports/structure-current-state.json`
- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.json`
- `.aide/roots/latest-root-authority-candidates.md`
- `docs/planning/repository-structure/current-truth-and-root-authority-audit.md`

## NON_GOALS

No root authority contract implementation, docs normalization repair, OKF
refresh, file moves, file deletes, reference rewrites, path aliases, shims, new
top-level roots, generated-output source-truth promotion, queue acceptance,
branch mutation, target-repo mutation, GitHub mutation, release work,
provider/model calls, network calls, runtime work, host runtime, provider
runtime, production readiness, or release readiness.

## ACCEPTANCE

- Queue item exists and is indexed.
- Reports record current repo/root/refactor/task/Reconciler truth.
- Reports identify current root authority candidates.
- Drift findings are recorded without repair.
- Evidence includes changed files, validation commands/results, no-forbidden-ops
  review, and remaining risks.
- Task stops at `needs_review`.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence
refs, unresolved risks/deferrals, commit id, and next task
`AIDE-STRUCTURE-01-root-authority-contracts`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1600
- budget_status: PASS
