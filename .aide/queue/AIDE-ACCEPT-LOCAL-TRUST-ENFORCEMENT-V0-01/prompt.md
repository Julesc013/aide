# Prompt

Create and process `AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01`.

Accept exactly:

```text
local_trust_enforcement_v0
```

Accepted meaning:

```text
AIDE can deterministically evaluate accepted local trust records, persist an
AuthorizationEvaluation and trust events through the accepted local Service
foundation, consume a one-use grant in a local SQLite transaction, and refuse a
second final-use attempt.
```

Do not accept:

```text
external IAM
credentials
secrets
OIDC
remote policy engine
process launch
worker execution
transaction approval
provider/model calls
network calls
preview/apply/rollback
repository mutation
branch/worktree automation
GitHub mutation
release or promotion
```

Stop at `needs_review` with:

```text
result: ACCEPTED_WITH_WARNINGS
recommended_next_task: AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01
```
