# Prompt

Create and process `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`.

This task is a protocol-shaped vertical slice, not a kernel scaffold.

Do not implement the AIDE kernel, service, Commander, provider adapters, branch/worktree automation, full schema suite, OpenTelemetry, SARIF, SPDX, CycloneDX, SLSA, in-toto, OpenAPI, network/model/Gateway calls, release behavior, or target repo mutation.

The WorkUnit created by this task explicitly authorizes implementation:

```yaml
authorizes_implementation: true
implementation_scope: lifecycle-fixture-temp-runner-only
stop_state: needs_review
```

Only introduce the contracts, report fields, helper modules, and internal seams required by this lifecycle fixture runner.

Keep `.aide/scripts/aide_lite.py` as CLI dispatch only. Implement behavior in `core/apply/lifecycle_fixture_runner.py`.

Use minimal practical seams:

- `ScenarioLoader`
- `TransactionCompiler`
- `ScopedExecutor`
- `FixtureVerifier`
- `EvidenceReporter`

Do not build a plugin framework. Do not create unused kernel directories. Do not generalize beyond the `install-managed-section` / `apply-temp` scenario.

Add commands:

```text
py -3 .aide/scripts/aide_lite.py lifecycle-fixture status
py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp
py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify
```

The runner must copy canonical lifecycle fixtures to a temporary workspace, mutate only the temp copy, verify expected postimage and manual preservation, emit evidence and rollback-compatible records, and prove canonical fixtures are unchanged.

All mutation paths must pass a path-jail check:

- resolve under temp workspace root
- reject absolute target paths
- reject parent traversal
- reject symlink escape
- reject any path outside the temp workspace

`lifecycle-fixture verify` must verify the latest completed run report by default. It must fail closed if:

- no latest-run.json exists
- latest-run.json is malformed
- referenced temp workspace is missing
- referenced rollback record is missing
- report hashes do not match actual files
- report claims contradict observed files

Reports must include:

```json
{
  "capability_label": "fixture_temp_apply_only",
  "not_capabilities": [
    "active_repo_apply",
    "target_repo_apply",
    "general_lifecycle_apply",
    "rollback_execution",
    "uninstall_execution",
    "release_ready",
    "production_ready"
  ]
}
```

Stop at `needs_review` with evidence and validation.
