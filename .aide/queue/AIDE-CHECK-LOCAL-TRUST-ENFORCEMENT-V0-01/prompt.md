# Prompt

Create and process `AIDE-CHECK-LOCAL-TRUST-ENFORCEMENT-V0-01`.

Repo truth outranks this prompt. Independently verify
`AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-01` without repairing implementation or
accepting the proposed capability.

Verify:

```text
accepted trust contract alignment
accepted local Service use
exact digest admission and policy/grant boundaries
one-use grant consumption
idempotent replay
second final-use refusal
SQLite object/event/idempotency persistence
complete refusal matrix
false boundary fields
deterministic projection
no process launch
no external IAM, credentials, secrets, OIDC, network, worker execution,
transaction approval, preview/apply/rollback, repository mutation,
GitHub mutation, release, or promotion
```

If material findings remain, recommend exactly:

```text
AIDE-BUILD-LOCAL-TRUST-ENFORCEMENT-V0-REPAIR-01
```

If the check passes, recommend exactly:

```text
AIDE-ACCEPT-LOCAL-TRUST-ENFORCEMENT-V0-01
```

Stop at `needs_review`.
