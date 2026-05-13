# Q28 Prompt Summary - Git Workflow Policy v0

Implement the canonical AIDE Git workflow policy layer after Q27 commit
discipline and WorkUnit recovery.

Q28 must define report-only local policy and detection for:

- branch roles;
- workflow detection;
- `main`, `dev`, `task/*`, `release/*`, and `hotfix/*` conventions;
- integration and promotion gates;
- sync rules for multi-machine work;
- safe pruning rules;
- branch-aware task recovery;
- project workflow profiles for AIDE, Eureka, Dominium, website/static-site,
  native client, connector-heavy, data snapshot, and unknown repositories;
- workflow reports future merge/promotion helpers can consume.

Q28 must not create, delete, merge, push, fetch, prune, or otherwise mutate
branches/remotes. Q29 owns helper implementation for land/promote/prune.

The core policy remains:

- `main` is accepted canonical truth.
- `dev` is shareable integration truth, not a second canonical truth.
- `task/*` branches are bounded work.
- `release/*` branches are maintained release lines.
- `hotfix/*` branches are urgent repairs.
- No branch is trusted without validation/evidence.
