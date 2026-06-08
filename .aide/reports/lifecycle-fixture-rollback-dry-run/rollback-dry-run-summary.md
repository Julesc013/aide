# Lifecycle Fixture Rollback Dry-Run Summary

Result: `PASS_WITH_WARNINGS`

Mode: report-only / dry-run rollback planning checks.

This report consumed rollback-compatible records as static inputs and did not implement or execute rollback apply. It did not implement or execute uninstall apply. It did not execute lifecycle apply. It did not run scoped transaction apply against fixture targets. It did not mutate fixture targets, the active repo through scoped apply, external target repos, branches, worktrees, release files, provider/model files, Gateway files, or network state.

Checked records:

- `lifecycle-rollback-compatible-record-example`
- `fixture-rollback-install-managed-section`
- `fixture-rollback-upgrade-v2`

Summary:

- rollback-dry-run-checked: yes
- rollback-report-checked: yes
- rollback-record-consumed: yes
- lifecycle fixture rollback: report-only
- generated rollback dry-run: report artifacts only
- current hash: fixture records match referenced SHA-256 preimage/postimage files
- inverse operation: present and requires matching current hash
- precondition: present
- stop condition: present
- manual preservation: present
- protected path: present
- allowed paths: task and report artifacts only
- protected paths: preserved
- forbidden operations: preserved
- review gate: `needs_review`

Warnings:

- The generic rollback example uses placeholder hashes and fixture-content refs, so it is classified as example-only.
- Rollback records are static compatibility evidence only.
- Rollback execution, uninstall execution, lifecycle apply, fixture apply, active repo apply, target repo mutation, production-ready, and release-ready claims remain blocked or deferred.
