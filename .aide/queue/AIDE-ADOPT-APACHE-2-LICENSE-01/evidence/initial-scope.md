# Initial Scope

Task: `AIDE-ADOPT-APACHE-2-LICENSE-01`

Objective: adopt a standard Apache-2.0 permissive licensing packet for AIDE and
update the root docs that describe licensing, contribution, generated outputs,
and trademark/project identity.

Allowed writes are limited to the task packet/evidence, queue index, root legal
docs, README, CONTRIBUTING, DOCUMENTATION, PLANS, and IMPLEMENT.

Preflight observations:

- `git status --short --branch` initially reported a clean worktree on `main`,
  ahead of `origin/main` by one existing commit.
- `intent compile` classified the bounded legal-doc task as docs, low risk,
  audit-only sizing, safe to execute, and not blocked.
- Bypass policy requires queue routing for multi-file policy changes, so this
  queue item was materialized before broad edits.

Out of scope:

- runtime implementation
- protocol schema changes
- support-tier or capability-level changes
- release publication, tags, uploads, GitHub mutation, or branch mutation
- provider/model/network calls
- target-repository mutation
- trademark registration
- Contributor License Agreement adoption
- generated-output source-truth promotion
