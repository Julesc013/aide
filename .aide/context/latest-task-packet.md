# AIDE Latest Task Packet

## PHASE

AIDE-STRUCTURE-01-root-authority-contracts - Root Authority Contracts

## GOAL

Create bounded root authority contracts for Track B after the check-only
current-truth and root-authority audit.

## WHY

The completed Track B audit recommends root authority contracts before any
structural cleanup. AIDE needs a machine-readable root authority policy, human
governance note, repository layout reference, overlap report, migration rules,
validation plan, and follow-up prompt shells before any future move map or
structural apply work.

## AUTHORITY

The queue task authorizes contract and policy documentation only:

```yaml
implementation_class: contract_and_policy_docs_only
authorizes_implementation: true
stop_state: needs_review
```

Canonical task packet:

- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/task.yaml`
- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/ExecPlan.md`
- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/status.yaml`

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
- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.md`
- `docs/planning/repository-structure/current-truth-and-root-authority-audit.md`
- `.aide/policies/root-authority.yaml`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/root-authority-contracts.md`
- `docs/planning/repository-structure/root-authority-contracts.md`
- `docs/planning/repository-structure/track-b-follow-up-prompts.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/policies/root-authority.yaml`
- `.aide/reports/root-authority-contracts.json`
- `.aide/reports/root-authority-contracts.md`
- `.aide/reports/task-os-*`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `docs/planning/repository-structure/**`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/reports/structure-current-state.md`
- `.aide/roots/latest-root-authority-candidates.md`
- `docs/planning/repository-structure/current-truth-and-root-authority-audit.md`
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
- generated-output drift acceptance changes
- source truth mutation outside root-authority contract scope
- queue acceptance mutation
- root recycling apply
- refactor map apply
- broad docs repair
- OKF refresh
- branch/worktree mutation
- GitHub mutation
- release or publishing work
- provider/model calls
- network calls
- Runtime, Service, Commander, host runtime, provider runtime, worker runtime, Workbench, or broad kernel work

## IMPLEMENTATION

- Write root authority contracts from existing audit evidence.
- Record root authority map, overlap report, candidate target structure,
  migration rules, validation plan, and follow-up prompt shells.
- Keep docs repair, OKF refresh, fate maps, interop policy, file movement, and
  structural apply work as separate future queue tasks.
- Stop at `needs_review`.

## VALIDATION

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-01-root-authority-contracts`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-01-root-authority-contracts`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## EVIDENCE

- `.aide/queue/AIDE-STRUCTURE-01-root-authority-contracts/evidence/*.md`
- `.aide/policies/root-authority.yaml`
- `governance/root-authority.md`
- `docs/reference/repository-layout.md`
- `.aide/reports/root-authority-contracts.json`
- `.aide/reports/root-authority-contracts.md`
- `docs/planning/repository-structure/root-authority-contracts.md`
- `docs/planning/repository-structure/track-b-follow-up-prompts.md`

## NON_GOALS

No docs normalization repair, OKF refresh, file moves, file deletes, reference
rewrites, path aliases, shims, new top-level roots, generated-output
source-truth promotion, queue acceptance, CapabilityManifest acceptance,
ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, branch
mutation, target-repo mutation, GitHub mutation, release work, provider/model
calls, network calls, runtime work, host runtime, provider runtime, production
readiness, or release readiness.

## ACCEPTANCE

- Queue item exists and is indexed.
- Root authority policy, governance note, repository layout reference, reports,
  and follow-up prompts exist.
- Root authority map, overlap report, candidate target structure, migration
  rules, and validation plan are recorded.
- Evidence includes changed files, validation commands/results, no-forbidden-ops
  review, and remaining risks.
- Task stops at `needs_review`.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence
refs, unresolved risks/deferrals, commit id, and next Track B task
`AIDE-STRUCTURE-02-status-doc-sync`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1700
- budget_status: PASS
