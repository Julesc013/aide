# Capability Boundary

Accepted predecessor capability:

```text
fixture_backed_dominium_validation_adapter
```

Proposed by this build only:

```text
live_dominium_validation_command_readonly_v0
```

This build proves:

- registered capability lookup for `dominium.validation.run`;
- exactly one Dominium CLI process entered through `apps/workbench/module/validation/cli.py`;
- Dominium stdout JSON was parsed;
- the command result came from Dominium output, not a constructed success result;
- `run_validation_command()` and `ValidationServiceAdapter` boundary evidence was present;
- Dominium checkout state stayed unchanged.

This build does not accept or implement:

- general Dominium command dispatch;
- Workbench apply behavior;
- Service/runtime;
- worker execution;
- provider/model/network calls;
- preview/apply/rollback;
- source or target mutation;
- branch/worktree automation;
- GitHub mutation;
- release or promotion.
