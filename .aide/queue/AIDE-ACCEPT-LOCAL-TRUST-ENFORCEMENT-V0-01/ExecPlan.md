# AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01 ExecPlan

## Objective

Accept exactly `local_trust_enforcement_v0` after the build and independent
check both passed with warnings, zero material findings, and complete evidence.

## Scope

Acceptance is limited to this task packet, acceptance reports, queue index, and
root planning/execution logs.

## Acceptance Boundary

Accepted: deterministic local authorization evaluation over accepted trust
records, persisted `AuthorizationEvaluation` and trust events through the
accepted local Service foundation, one-use grant consumption inside a local
SQLite transaction, idempotent replay, and second final-use refusal.

Not accepted: external IAM, credentials, secrets, OIDC, remote policy engines,
process launch, worker execution, transaction approval, provider/model calls,
network calls, preview/apply/rollback, repository mutation, branch/worktree
automation, GitHub mutation, release, or promotion behavior.

## Result

ACCEPTED_WITH_WARNINGS. The next task is
`AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`.
