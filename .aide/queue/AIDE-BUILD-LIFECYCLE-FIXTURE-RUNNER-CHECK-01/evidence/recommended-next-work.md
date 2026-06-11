# Recommended Next Work

Primary next task:

`AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01`

Reason:

- CHECK-01 result is `PASS_WITH_WARNINGS`.
- Core behavior, reports, hashes, boundaries, negative capability labels, and dynamic validation passed.
- Remaining work is hardening coverage, not repair.

Prompt seed:

```text
Create and process AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-HARDEN-01. Harden the
reviewed lifecycle fixture temp runner without widening authority. Focus only
on failure cases, malformed marker handling, report schema validation,
path-jail edge cases, unsupported scenario/mode/operation conformance, and
clearer evidence. Do not implement service, Commander, provider adapters,
branch/worktree automation, target repo apply, active repo apply, rollback
execution, uninstall execution, release, promotion, network, Gateway, GitHub
mutation, or model/provider calls. End at needs_review with evidence.
```
