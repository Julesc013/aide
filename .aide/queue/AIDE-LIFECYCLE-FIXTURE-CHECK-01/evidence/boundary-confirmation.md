# Boundary Confirmation

Allowed paths used:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic generated reports from required status/validation commands

Read-only reviewed paths:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`

Protected paths preserved:

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- release roots
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply and install/upgrade/repair/rollback/uninstall implementation files
- `core/**`

Forbidden operations preserved:

- no lifecycle apply implementation or execution;
- no scoped transaction apply against fixture targets;
- no active repo scoped apply mutation;
- no target repo mutation;
- no branch/worktree mutation, merge, push, promotion, release, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.
