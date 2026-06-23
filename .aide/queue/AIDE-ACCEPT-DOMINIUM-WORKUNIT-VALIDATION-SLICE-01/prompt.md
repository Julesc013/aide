# AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Accept only this capability:

```text
fixture_backed_dominium_validation_adapter
```

Do not claim:

```text
live_dominium_validation
general_dominium_command_execution
Workbench integration
Service/runtime integration
worker execution
provider/model/network calls
preview, apply, or rollback
source or target repository mutation
branch/worktree or GitHub mutation
release or promotion behavior
```

Preserve these warnings:

- the target is a temporary fixture workspace;
- the executor is `local_fixture_callable`;
- live Dominium command execution remains unproven;
- non-Windows and minimum-Python portability were not separately proven;
- older historical seam modules timed out and remain unproven.

Stop at `needs_review` with:

```text
result: ACCEPTED_WITH_WARNINGS
accepted_capability: fixture_backed_dominium_validation_adapter
```

Recommend exactly:

```text
AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```
