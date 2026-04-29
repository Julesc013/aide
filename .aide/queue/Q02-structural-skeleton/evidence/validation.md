# Q02 Validation Evidence

## Date

2026-04-29

## Commands And Results

### Required skeleton directories

Command:

```powershell
$dirs = @('core/contract','core/harness','core/runtime','core/compat','core/control','core/sdk','core/tests','hosts/cli','hosts/service','hosts/commander','hosts/extensions','bridges/dominium'); foreach ($p in $dirs) { if (Test-Path $p -PathType Container) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed.

### Required README files

Command:

```powershell
$files = @('core/README.md','core/contract/README.md','core/harness/README.md','core/runtime/README.md','core/compat/README.md','core/control/README.md','core/sdk/README.md','core/tests/README.md','hosts/README.md','hosts/cli/README.md','hosts/service/README.md','hosts/commander/README.md','hosts/extensions/README.md','hosts/extensions/visualstudio/README.md','hosts/extensions/vscode/README.md','hosts/extensions/xcode/README.md','hosts/extensions/later/README.md','bridges/README.md','bridges/dominium/README.md','bridges/dominium/xstack/README.md','bridges/dominium/profiles/README.md','bridges/dominium/policies/README.md','bridges/dominium/generators/README.md'); foreach ($p in $files) { if (Test-Path $p -PathType Leaf) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed.

### Structural migration map

Command:

```powershell
if (Test-Path docs/reference/structural-migration-map.md -PathType Leaf) { 'OK docs/reference/structural-migration-map.md' } else { 'MISSING docs/reference/structural-migration-map.md'; exit 1 }
```

Result: passed.

### Root documentation updates

Command:

```powershell
$files = @('README.md','DOCUMENTATION.md','ROADMAP.md','PLANS.md','IMPLEMENT.md'); foreach ($p in $files) { if (Select-String -Path $p -Pattern 'Q02|structural skeleton|structural-migration-map|core/' -Quiet) { "OK $p" } else { "MISSING Q02 structural pointer in $p"; exit 1 } }
```

Result: passed.

### Queue status

Command:

```powershell
py -3 scripts/aide-queue-status
```

Result: passed. Summary:

- `Q00-bootstrap-audit`: `needs_review`
- `Q01-documentation-split`: `needs_review`
- `Q02-structural-skeleton`: `needs_review`
- `Q03-profile-contract-v0`: `pending`

### Next queue item

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed. Output:

```text
Q03-profile-contract-v0
status: pending
planning_state: planned
title: Profile and contract v0
```

### Terminology search

Command:

```powershell
$terms = @('AIDE Core','AIDE Hosts','AIDE Bridges','Contract','Harness','Runtime','Compatibility','Control','SDK','Dominium Bridge','XStack','skeleton','future move'); foreach ($term in $terms) { $matches = @(rg -l -F -- $term core hosts/README.md hosts/cli hosts/service hosts/commander hosts/extensions bridges docs/reference README.md DOCUMENTATION.md ROADMAP.md PLANS.md IMPLEMENT.md); if ($LASTEXITCODE -eq 0 -and $matches.Count -gt 0) { "OK $($term): $($matches.Count) files" } else { "MISSING $($term)"; exit 1 } }
```

Result: passed.

- `AIDE Core`: 18 files
- `AIDE Hosts`: 7 files
- `AIDE Bridges`: 9 files
- `Contract`: 13 files
- `Harness`: 15 files
- `Runtime`: 11 files
- `Compatibility`: 12 files
- `Control`: 9 files
- `SDK`: 8 files
- `Dominium Bridge`: 16 files
- `XStack`: 6 files
- `skeleton`: 23 files
- `future move`: 1 file

### Lightweight import-preservation check

Command:

```powershell
py -3 -B -m unittest discover -s shared/tests -t .
```

Result: passed. Output summary: 5 tests ran successfully.

### Diff sanity

Command:

```powershell
git diff --check
```

Result: passed. Git reported line-ending normalization warnings only.

### Allowed-path audit

Command:

```powershell
$allowedExact = @('README.md','DOCUMENTATION.md','ROADMAP.md','PLANS.md','IMPLEMENT.md','.aide/queue/index.yaml','hosts/README.md'); $allowedPrefixes = @('core/','bridges/','hosts/cli/','hosts/service/','hosts/commander/','hosts/extensions/','docs/','.aide/queue/Q02-structural-skeleton/'); $paths = @(git status --porcelain | ForEach-Object { $_.Substring(3).Replace('\\','/') }); $bad = @(); foreach ($p in $paths) { if ($allowedExact -contains $p) { continue }; $ok = $false; foreach ($prefix in $allowedPrefixes) { if ($p.StartsWith($prefix)) { $ok = $true; break } }; if (-not $ok) { $bad += $p } }; if ($bad.Count -gt 0) { 'Forbidden or unexpected paths:'; $bad; exit 1 } else { "OK allowed-path audit: $($paths.Count) changed paths" }
```

Initial result: the audit caught untracked `shared/**/__pycache__` directories created by the lightweight shared test run.

Cleanup command:

```powershell
$root = (Resolve-Path .).Path; $targetRoot = (Resolve-Path shared).Path; $paths = @(Get-ChildItem -Path shared -Recurse -Directory -Filter __pycache__ | ForEach-Object { $_.FullName }); foreach ($p in $paths) { $resolved = (Resolve-Path -LiteralPath $p).Path; if (-not $resolved.StartsWith($targetRoot, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Refusing to remove path outside shared/: $resolved" } }; foreach ($p in $paths) { Remove-Item -LiteralPath $p -Recurse -Force }; "Removed $($paths.Count) generated __pycache__ directories"
```

Cleanup result: removed 6 generated `__pycache__` directories.

Final result: passed. The audit reported 22 changed path entries and no forbidden paths.

## Tests Not Run

No heavy native host, IDE, packaging, release, provider, service, or app tests were run. Q02 is README-only structural skeleton work.
