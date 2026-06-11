# Future Apply Contract

The future apply task may attempt exactly one fixture mutation only after verifying `authority-packet.json`.

Required mutation:

- operation: `update_managed_section`
- target: `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md`
- expected preimage hash: `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60`
- expected postimage hash: `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b`

The future task must:

- verify worktree state;
- verify allowed paths;
- verify current preimage hash;
- run dry-run/report mode first if supported;
- execute exactly one scoped fixture managed-section mutation;
- preserve manual content outside markers;
- verify postimage hash;
- maintain rollback-compatible record evidence;
- generate report and no-extra-mutation proof;
- stop at `needs_review`.

The future task must not execute rollback, uninstall, upgrade apply, lifecycle repair apply, active repo apply, target repo mutation, branch/worktree mutation, push, merge, release, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply.
