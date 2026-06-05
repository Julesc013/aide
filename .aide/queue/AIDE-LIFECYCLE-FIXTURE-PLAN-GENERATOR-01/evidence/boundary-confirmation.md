# Boundary Confirmation

Allowed paths used:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PLAN-GENERATOR-01/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/**`
- `.aide/reports/lifecycle-fixture-plans/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- deterministic generated reports from required status/validation commands

Read-only inputs:

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/source-pack/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/**`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/**`
- `.aide/apply/lifecycle-*.schema.json`

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
- lifecycle apply, install/upgrade/repair/rollback/uninstall, scoped transaction executor, managed-section, and `core/**` implementation surfaces

Forbidden operations preserved:

- no lifecycle apply implementation or execution;
- no scoped transaction apply against fixture targets;
- no active repo scoped apply mutation;
- no rollback apply implementation or execution;
- no target repo mutation;
- no branch/worktree mutation, merge, push, promotion, release, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.
