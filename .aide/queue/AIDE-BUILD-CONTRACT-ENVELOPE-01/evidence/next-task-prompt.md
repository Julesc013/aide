# Next Task Prompt

Recommended next task:

```text
AIDE-CHECK-CONTRACT-ENVELOPE-01
```

Prompt seed:

```text
Perform an independent check of AIDE-BUILD-CONTRACT-ENVELOPE-01.

Review the minimal contract envelope helper, schema, CLI dispatch, focused
tests, queue evidence, and generated reports.

Confirm:
- apiVersion/kind/metadata/spec/status envelope shape is present.
- Unknown optional fields are tolerated.
- Unknown required capabilities fail closed.
- Compatibility fields are SemVer-like where validated.
- Existing lifecycle fixture runner reports remain readable and are not
  destructively migrated.
- Projections preserve fixture_temp_apply_only and explicit non-capabilities.
- Reports are truthful and use repo-relative source paths.
- CLI behavior is dispatch-only.
- Tests and validation pass.
- No WorkUnit CLI, Test Broker, Service, Commander, provider adapters,
  branch/worktree automation, target repo apply, rollback execution, release,
  promotion, network, Gateway, GitHub mutation, or model/provider calls were
  introduced.

Do not repair inline. If defects are found, produce a bounded repair prompt.
End with PASS, PASS_WITH_WARNINGS, or REJECTED_NEEDS_REPAIR.
```
