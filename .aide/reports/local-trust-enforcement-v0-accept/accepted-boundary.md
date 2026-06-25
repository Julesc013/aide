# Accepted Boundary

Accepted:

- deterministic local authorization evaluation;
- accepted trust record input;
- accepted local Service persistence;
- `AuthorizationEvaluation` object;
- `trust.authorization_evaluated` event;
- `trust.grant_consumed` event;
- one-use grant consumption;
- idempotent replay;
- second final-use refusal.

Not accepted:

- external IAM;
- credentials;
- secrets;
- OIDC;
- remote policy engine;
- process launch;
- worker execution;
- transaction approval;
- provider/model calls;
- network calls;
- preview/apply/rollback;
- repository mutation;
- branch/worktree automation;
- GitHub mutation;
- release or promotion.
