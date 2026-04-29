# Q04 Validation

Date: 2026-04-29

All commands were run from the repository root.

## Harness Commands

Command:

```powershell
py -3 scripts/aide --help
```

Result: passed. Output listed the implemented Harness v0 commands: `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.

Command:

```powershell
py -3 scripts/aide validate
```

Result: passed. Exit code `0`.

Summary:

```text
AIDE Harness v0 validate
status: PASS_WITH_WARNINGS
summary: 61 info, 9 warning, 0 error
validation_model: structural file, directory, anchor, and queue checks only
full_yaml_schema_validation: not implemented in Q04
```

Warnings were expected:

- Q00 through Q04 are at review gates.
- `.aide/profile.yaml`, `.aide/toolchain.lock`, and `.aide/commands/catalog.yaml` still contain Q03-era Harness planned/not-implemented wording because Q04 was not allowed to mutate final contract catalogs.
- Q05 remains `pending` in the simple queue index while Q04 is `needs_review`; future workers must run Q04 review before Q05.

Command:

```powershell
py -3 scripts/aide doctor
```

Result: passed. Exit code `0`.

Summary:

```text
status: PASS_WITH_WARNINGS
summary: 61 info, 9 warning, 0 error
next_recommended_step: Q04 review, then Q05 plan only if Q04 passes
```

Command:

```powershell
py -3 scripts/aide compile
```

Result: passed. Exit code `0`.

Summary:

```text
AIDE Harness v0 compile
validation_status: PASS_WITH_WARNINGS
mode: compile plan only
mutation: none
planned_outputs:
- none in Q04
generated_artifacts_created: false
```

Command:

```powershell
py -3 scripts/aide migrate
```

Result: passed. Exit code `0`.

Summary:

```text
AIDE Harness v0 migrate
mode: no-op baseline report
profile_contract_version: aide.profile-contract.v0
compat_schema_status: baseline
migration_baseline_status: placeholder
migration_engine: not implemented
automatic_migrations: none
q06_compatibility_baseline: deferred
migration_needed: no executable migration is defined for Q04
```

Command:

```powershell
py -3 scripts/aide bakeoff
```

Result: passed. Exit code `0`.

Summary:

```text
AIDE Harness v0 bakeoff
mode: metadata/readiness only
external_calls: none
provider_or_model_calls: none
native_host_calls: none
network_calls: none
executable_bakeoff_scenarios: none in Q04
```

Command:

```powershell
py -3 scripts/aide init --dry-run
```

Result: passed. Exit code `0`. Output reported `status: already_initialized` and did not overwrite `.aide/`.

Command:

```powershell
py -3 scripts/aide import
```

Result: passed. Exit code `0`. Output reported importable guidance surfaces and did not mutate contract records.

## Tests

Command:

```powershell
py -3 -m unittest discover -s core/harness/tests -t .
```

Initial result: failed because the new test directory was not importable. This was fixed by adding `core/harness/tests/__init__.py`.

Final result: passed.

```text
Ran 4 tests in 0.107s
OK
```

Command:

```powershell
py -3 -m py_compile scripts/aide core/harness/aide_harness.py core/harness/commands.py core/harness/contract_loader.py core/harness/diagnostics.py core/harness/tests/test_aide_harness.py
```

Result: passed.

During one parallel validation sweep, a cleanup command emitted a non-terminating `Remove-Item` error while Python cache directories were still being written. The cleanup was rerun with `-ErrorAction Stop` after the tests finished, and generated `__pycache__` directories were removed.

## Queue Helpers

Command:

```powershell
py -3 scripts/aide-queue-status
```

Result: passed. Q04 reports `needs_review` with `planning_state: implemented`; Q05 through Q08 remain pending/planned.

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed. Output reported `Q05-generated-artifacts-v0` as the next pending item because the existing helper is status-only and not dependency-aware. This is recorded as a Q04 risk; Q05 must not proceed until Q04 review passes.

## Generated Artifact Absence

Command:

```powershell
$paths = @('CLAUDE.md','.claude')
foreach ($p in $paths) {
  if (Test-Path $p) { "FOUND $p"; exit 1 } else { "OK absent $p" }
}
```

Result: passed.

```text
OK absent CLAUDE.md
OK absent .claude
```

## Terminology Search

Command:

```powershell
$terms = @('Profile','Harness','validate','doctor','compile plan','source of truth','generated','Compatibility','Dominium Bridge')
foreach ($term in $terms) {
  $matches = @(rg -l -F -- $term README.md ROADMAP.md DOCUMENTATION.md PLANS.md IMPLEMENT.md docs/reference/harness-v0.md core/harness .aide/queue/Q04-harness-v0 2>$null)
  if ($LASTEXITCODE -eq 0 -and $matches.Count -gt 0) {
    "OK $term :: $($matches.Count) files"
  } else {
    "MISSING $term"
    exit 1
  }
}
```

Result: passed. All required terms were found.

## Diff And Path Checks

Command:

```powershell
git diff --check
```

Result: passed. Git emitted line-ending normalization warnings only; no whitespace errors were reported.

Command:

```powershell
$changed = git status --porcelain -uall | ForEach-Object { $_.Substring(3).Replace('\','/') }
$bad = @()
foreach ($p in $changed) {
  if ($p -eq 'README.md' -or
      $p -eq 'ROADMAP.md' -or
      $p -eq 'DOCUMENTATION.md' -or
      $p -eq 'PLANS.md' -or
      $p -eq 'IMPLEMENT.md' -or
      $p -eq '.aide/queue/index.yaml' -or
      $p.StartsWith('core/harness/') -or
      $p -eq 'scripts/aide' -or
      $p -eq 'docs/reference/harness-v0.md' -or
      $p.StartsWith('.aide/queue/Q04-harness-v0/')) {
    "ALLOW $p"
  } else {
    $bad += $p
    "DENY $p"
  }
}
if ($bad.Count) { exit 1 } else { 'PASS allowed-path audit' }
```

Result: passed. All changed files stayed inside the Q04 allowed paths.

Command:

```powershell
Get-ChildItem -Recurse core/harness,scripts -Directory -Filter __pycache__ | Select-Object FullName
```

Result: passed. No Python cache directories remained after cleanup.
