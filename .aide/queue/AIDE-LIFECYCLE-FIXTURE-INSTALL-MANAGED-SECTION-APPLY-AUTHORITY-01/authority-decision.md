# Authority Decision

Disposition: `AUTHORIZE_EXACT_FIXTURE_APPLY`

Authorized future task: `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`

Preferred retry task: `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01-RETRY`

This authorizes exactly one future fixture-scoped mutation:

- scenario: `install-managed-section`
- operation: `update_managed_section`
- fixture root: `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section`
- target path: `manual/with-managed-section.md`
- preimage hash: `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60`
- postimage hash: `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b`

This does not authorize any other fixture apply, broad install apply, upgrade apply, repair apply, rollback execution, uninstall execution, active repo apply, target repo mutation, branch/worktree mutation, push, merge, release, GitHub mutation, provider/model calls, Gateway calls, network calls, production-ready claims, or release-ready claims.

This authority task itself executed no apply.
