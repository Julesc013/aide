# Q04 Command Smoke

Date: 2026-04-29

## `--help`

Command:

```powershell
py -3 scripts/aide --help
```

Result: passed. The command lists:

- `init`
- `import`
- `compile`
- `validate`
- `doctor`
- `migrate`
- `bakeoff`

## `init`

Command:

```powershell
py -3 scripts/aide init --dry-run
```

Result: passed.

```text
status: already_initialized
detail: .aide/profile.yaml exists; Q04 will not overwrite existing contract records.
```

## `import`

Command:

```powershell
py -3 scripts/aide import
```

Result: passed.

```text
mode: report-only
- AGENTS.md: present
- .agents/skills: present
- .aide: present
- CLAUDE.md: absent
- .claude: absent
mutation: none
canonical_contract_rewrite: false
```

## `compile`

Command:

```powershell
py -3 scripts/aide compile
```

Result: passed.

```text
validation_status: PASS_WITH_WARNINGS
mode: compile plan only
mutation: none
planned_outputs:
- none in Q04
generated_artifacts_created: false
```

## `validate`

Command:

```powershell
py -3 scripts/aide validate
```

Result: passed.

```text
status: PASS_WITH_WARNINGS
summary: 61 info, 9 warning, 0 error
```

The warnings are expected and review-gated; no hard errors were found.

## `doctor`

Command:

```powershell
py -3 scripts/aide doctor
```

Result: passed.

```text
status: PASS_WITH_WARNINGS
next_recommended_step: Q04 review, then Q05 plan only if Q04 passes
```

## `migrate`

Command:

```powershell
py -3 scripts/aide migrate
```

Result: passed.

```text
mode: no-op baseline report
profile_contract_version: aide.profile-contract.v0
migration_engine: not implemented
automatic_migrations: none
q06_compatibility_baseline: deferred
```

## `bakeoff`

Command:

```powershell
py -3 scripts/aide bakeoff
```

Result: passed.

```text
mode: metadata/readiness only
external_calls: none
provider_or_model_calls: none
native_host_calls: none
network_calls: none
executable_bakeoff_scenarios: none in Q04
```

No command created downstream generated artifacts.
