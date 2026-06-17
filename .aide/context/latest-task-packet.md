# AIDE Latest Task Packet

## PHASE

AIDE-BUILD-REPO-LAYOUT-INVENTORY-01 - Report-Only Repository Layout Inventory

## GOAL

Create a report-only Track B inventory of the current `.aide` and `core`
layouts.

## WHY

The root authority contract is in place, but AIDE still needs concrete layout
facts before any rationalization or migration prompt. This task records current
directory pressure, naming overlaps, `.aide/reports` shape, flat path
assumptions, migration risks, and recommendations without applying changes.

## AUTHORITY

The queue task authorizes report generation only:

```yaml
track: B
report_only: true
authorizes_implementation: false
stop_state: needs_review
```

Canonical task packet:

- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/task.yaml`
- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/ExecPlan.md`
- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/status.yaml`

## CONTEXT_REFS

- `AGENTS.md`
- `.aide/profile.yaml`
- `.aide/queue/README.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- `.aide/policies/review-gates.yaml`
- `.aide/policies/root-authority.yaml`
- `docs/reference/source-of-truth.md`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/root-authority-contracts.md`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`
- `docs/planning/repository-structure/repo-layout-inventory.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/repo-layout/**`
- `.aide/reports/task-os-*`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/policies/root-authority.yaml`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/root-authority-contracts.md`
- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.md`
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
- directory renames
- queue task folder renames
- schema filename churn
- reference rewrites
- path alias application
- shim creation
- new top-level root creation
- `.aide/reports` restructure
- generated OKF manual edits
- generated-output source-truth promotion
- source truth mutation
- queue acceptance mutation
- rationalization apply work
- root recycling apply
- refactor map apply
- branch/worktree mutation
- GitHub mutation
- release or publishing work
- provider/model calls
- network calls
- Runtime, Service, Commander, Workbench, host runtime, provider runtime, worker runtime, or Track A protocol implementation

## IMPLEMENTATION

- Inventory `.aide` and `core` using tracked file listings and report-only
  helper status commands.
- Record root/directory authority classes, naming overlaps, generated-output
  boundaries, `.aide/reports` layout pressure, and migration risks.
- Do not generate a rationalization/apply prompt before design review.
- Stop at `needs_review`.

## VALIDATION

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py repo status`
- `py -3 .aide/scripts/aide_lite.py roots status`
- `py -3 .aide/scripts/aide_lite.py refactor map-status`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-REPO-LAYOUT-INVENTORY-01`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## EVIDENCE

- `.aide/queue/AIDE-BUILD-REPO-LAYOUT-INVENTORY-01/evidence/*.md`
- `.aide/reports/repo-layout/inventory.json`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.json`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`
- `docs/planning/repository-structure/repo-layout-inventory.md`

## NON_GOALS

No broad filesystem migration, file moves, file deletes, directory renames,
queue task folder renames, schema filename churn, reference rewrites, path
aliases, shims, new top-level roots, `.aide/reports` rewrite storm, generated
OKF edits, generated-output source-truth promotion, queue acceptance,
CapabilityManifest acceptance, ConformanceProfile, PatchTransaction,
AdapterManifest, MCP, A2A, ContextPack v2, worker adapters, runtime, scheduler,
Workbench, Commander, legacy IDE bridges, branch mutation, target-repo
mutation, GitHub mutation, release work, provider/model calls, or network calls.

## ACCEPTANCE

- Queue item exists and is indexed.
- Repo layout inventory reports exist under `.aide/reports/repo-layout/`.
- Reports classify `.aide` and `core`, name overlaps, report layout risks,
  migration rules, and recommendations.
- Evidence includes changed files, validation commands/results, no-forbidden-ops
  review, and remaining risks.
- No rationalization/apply prompt is generated.
- Task stops at `needs_review`.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence
refs, unresolved risks/deferrals, commit id, and recommended next gate
`AIDE-CHECK-REPO-LAYOUT-INVENTORY-01`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1800
- budget_status: PASS
