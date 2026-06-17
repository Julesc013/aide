# AIDE Latest Task Packet

## PHASE

AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01 - AIDE Self-Management Charter

## GOAL

Define AIDE self-management doctrine: AIDE must manage AIDE as a repo.

## WHY

Track B is now explicitly about AIDE self-management. AIDE should observe,
classify, compare, explain, plan, dry-run, validate, review, and only later
apply reviewed changes to its own structure, knowledge, docs, evidence, queue,
reports, schemas, policies, generated outputs, and migration safety.

## AUTHORITY

The queue task authorizes policy and documentation only:

```yaml
track: B
implementation_class: policy_and_docs_only
authorizes_implementation: true
stop_state: needs_review
```

Canonical task packet:

- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/task.yaml`
- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/ExecPlan.md`
- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/status.yaml`

## CONTEXT_REFS

- `AGENTS.md`
- `.aide/profile.yaml`
- `.aide/queue/README.md`
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- `.aide/policies/review-gates.yaml`
- `.aide/policies/root-authority.yaml`
- `docs/reference/source-of-truth.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`
- `.aide/policies/self-management.yaml`
- `docs/reference/aide-self-management.md`
- `.aide/reports/self-management/charter.md`
- `.aide/reports/self-management/object-backlog.md`
- `.aide/reports/self-management/queue-sequence.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/self-management.yaml`
- `.aide/reports/self-management/**`
- `.aide/reports/task-os-*`
- `docs/reference/aide-self-management.md`
- `docs/planning/repository-structure/**`
- `governance/root-authority.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/profile.yaml`
- `.aide/policies/root-authority.yaml`
- `docs/reference/source-of-truth.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/repo-layout/inventory.md`
- `.aide/reports/repo-layout/recommendations.md`
- `.aide/reports/repo-layout/migration-risks.md`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- profile contract mutation
- protocol schema creation
- command implementation
- generated-output ledger implementation
- generated-output refresh
- generated-output source-truth promotion
- OKF manual edits
- OKF regeneration
- docs truth repair
- queue acceptance mutation
- file moves
- file deletes
- directory renames
- reference rewrites
- path alias application
- shim creation
- root recycling apply
- refactor map apply
- structure transaction apply
- branch/worktree mutation
- GitHub mutation
- release or publishing work
- provider/model calls
- network calls
- Runtime, Service, Commander, Workbench, host runtime, provider runtime, worker runtime, or Track A implementation

## IMPLEMENTATION

- Define AIDE self-management doctrine.
- Record the proposed `AIDE_SELF_PROFILE` without mutating `.aide/profile.yaml`.
- Record managed surfaces, report-only command backlog, object backlog, and
  queue sequence.
- Stop at `needs_review`.

## VALIDATION

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## EVIDENCE

- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/evidence/*.md`
- `.aide/policies/self-management.yaml`
- `docs/reference/aide-self-management.md`
- `.aide/reports/self-management/charter.json`
- `.aide/reports/self-management/charter.md`
- `.aide/reports/self-management/object-backlog.md`
- `.aide/reports/self-management/queue-sequence.md`
- `docs/planning/repository-structure/self-management-charter.md`

## NON_GOALS

No RootAuthorityManifest schema implementation, RepoLayoutInventory protocol
implementation, DocTruthReconciler implementation, OKF drift implementation,
GeneratedOutputLedger implementation, QueueHealthReport implementation,
StructureTransaction implementation, CLI command implementation, generated
output refresh, OKF regeneration, docs repair, queue acceptance, filesystem
migration, runtime/provider behavior, branch mutation, target-repo mutation,
GitHub mutation, release work, provider/model calls, or network calls.

## ACCEPTANCE

- Queue item exists and is indexed.
- Self-management policy, reference doc, reports, and queue sequence exist.
- AIDE_SELF_PROFILE is recorded as proposed doctrine only.
- Evidence includes changed files, validation commands/results,
  no-forbidden-ops review, and remaining risks.
- Task stops at `needs_review`.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence
refs, unresolved risks/deferrals, commit id, and recommended next gate
`AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1700
- budget_status: PASS
