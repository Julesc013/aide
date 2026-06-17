# AIDE Latest Task Packet

## PHASE

AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01 - Check AIDE Self-Management Charter

## GOAL

Independently check the AIDE self-management charter and decide whether it is
ready for acceptance, needs hardening, is blocked, or is partial.

## WHY

Track B is now explicitly about AIDE self-management. The charter is a
foundational governance object and must be checked before it becomes accepted
Track B law.

## AUTHORITY

The queue task authorizes check-only report and evidence generation only:

```yaml
track: B
check_only: true
authorizes_implementation: false
stop_state: needs_review
```

Canonical task packet:

- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/task.yaml`
- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/ExecPlan.md`
- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/status.yaml`

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
- `.aide/reports/self-management/check-self-management-charter.md`
- `.aide/reports/self-management/check-self-management-charter.json`
- `.aide/reports/self-management/check-self-management-charter.findings.json`

## ALLOWED_PATHS

- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/self-management/check-self-management-charter.md`
- `.aide/reports/self-management/check-self-management-charter.json`
- `.aide/reports/self-management/check-self-management-charter.findings.json`
- `.aide/reports/task-os-*`
- `PLANS.md`
- `IMPLEMENT.md`

## REVIEWED_READ_ONLY_PATHS

- `AGENTS.md`
- `README.md`
- `.aide/queue/policy.yaml`
- `.aide/policies/self-management.yaml`
- `docs/reference/aide-self-management.md`
- `.aide/queue/AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01/**`
- `.aide/reports/root-authority-contracts.md`
- `.aide/reports/root-authority-contracts.json`
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
- schema implementation
- CLI command implementation
- GovernanceFinding helper, library, or formal schema implementation
- command implementation
- generated-output ledger implementation
- OKF regeneration
- doc truth reconciler implementation
- file moves
- renames
- reference rewrites
- migration apply
- branch/worktree mutation
- GitHub mutation
- release or publishing work
- provider/model calls
- network calls
- Runtime, Service, Commander, Workbench, host runtime, provider runtime, worker runtime, or Track A implementation

## IMPLEMENTATION

- Verify charter consistency, boundaries, evidence, validation, and next-task
  routing.
- Emit GovernanceFinding records as report convention only.
- Stop at `needs_review`.

## VALIDATION

- `git status --short --branch`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
- parse changed JSON/YAML files touched by the build task
- parse `.aide/reports/self-management/check-self-management-charter.findings.json`
- verify Markdown and JSON finding summary agreement
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## EVIDENCE

- `.aide/queue/AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01/evidence/*.md`
- `.aide/reports/self-management/check-self-management-charter.md`
- `.aide/reports/self-management/check-self-management-charter.json`
- `.aide/reports/self-management/check-self-management-charter.findings.json`

## NON_GOALS

No RootAuthorityManifest schema implementation, RepoLayoutInventory protocol
implementation, DocTruthReconciler implementation, OKF drift implementation,
GeneratedOutputLedger implementation, QueueHealthReport implementation,
StructureTransaction implementation, CLI command implementation,
GovernanceFinding helper/library implementation, OKF regeneration, docs repair,
queue acceptance, filesystem migration, runtime/provider behavior, branch
mutation, target-repo mutation, GitHub mutation, release work, provider/model
calls, or network calls.

## ACCEPTANCE

- Queue item exists and is indexed.
- Check reports and GovernanceFinding JSON exist.
- GovernanceFinding JSON parses.
- Markdown and JSON finding summaries agree.
- Build task evidence remains complete.
- Task stops at `needs_review`.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence
refs, unresolved risks/deferrals, commit id, and recommended next gate
`AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1700
- budget_status: PASS
