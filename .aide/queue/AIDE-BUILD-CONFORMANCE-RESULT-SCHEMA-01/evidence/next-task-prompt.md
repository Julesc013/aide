# Next Task Prompt

The next gate is:

```text
AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-01
```

Expected outcome:

- independently check `AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-01`;
- verify schema/helper/report/CLI/test/evidence completeness;
- verify exact binding to
  `aide://conformance-profile/minimal_capability_manifest-v1.0.0`;
- verify profile digest handling;
- verify case-result outcome semantics;
- verify aggregation fail-closed behavior for required cases;
- verify optional/advisory warning behavior;
- verify `record_valid`, `profile_requirements_satisfied`, and admission flags
  remain independent;
- verify no runner, execution, collection, activation, admission, trust, adapter,
  PatchTransaction, runtime, provider/network/Gateway/GitHub, branch/worktree,
  target apply, release, or production behavior was implemented.

Stop at `needs_review` and recommend exactly:

```text
AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01
```
