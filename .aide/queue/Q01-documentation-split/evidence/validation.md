# Q01 Validation Evidence

## Date

2026-04-29

## Commands And Results

### Required documentation directories

Command:

```powershell
$paths = @('docs/constitution','docs/charters','docs/roadmap','docs/design-mining','docs/decisions','docs/reference'); foreach ($p in $paths) { if (Test-Path $p -PathType Container) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed.

- `docs/constitution`
- `docs/charters`
- `docs/roadmap`
- `docs/design-mining`
- `docs/decisions`
- `docs/reference`

### Required charter files

Command:

```powershell
$paths = @('docs/charters/core-charter.md','docs/charters/contract-charter.md','docs/charters/harness-charter.md','docs/charters/compatibility-charter.md','docs/charters/hosts-charter.md','docs/charters/bridges-charter.md','docs/charters/control-charter.md','docs/charters/sdk-charter.md'); foreach ($p in $paths) { if (Test-Path $p -PathType Leaf) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed.

### Required decision records

Command:

```powershell
$paths = @('docs/decisions/ADR-0001-reboot-in-place.md','docs/decisions/ADR-0002-core-hosts-bridges.md','docs/decisions/ADR-0003-core-split.md','docs/decisions/ADR-0004-profile-vs-harness.md','docs/decisions/ADR-0005-compatibility-first-class.md','docs/decisions/ADR-0006-xstack-dominium-local.md','docs/decisions/ADR-0007-hosts-are-shells.md'); foreach ($p in $paths) { if (Test-Path $p -PathType Leaf) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed.

### Root documentation update check

Command:

```powershell
$paths = @('README.md','DOCUMENTATION.md','ROADMAP.md','PLANS.md','IMPLEMENT.md'); foreach ($p in $paths) { if (Select-String -Path $p -Pattern 'Q01|documentation|docs/' -Quiet) { "OK $p" } else { "MISSING Q01/docs pointer in $p"; exit 1 } }
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
- `Q02-structural-skeleton`: `pending`
- `Q03` through `Q08`: `pending`

### Next queue item

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed. Output:

```text
Q02-structural-skeleton
status: pending
planning_state: planned
title: Minimal self-hosting structural skeleton
```

### Terminology search

Command:

```powershell
$terms = @('AIDE Core','AIDE Hosts','AIDE Bridges','Contract','Harness','Runtime','Compatibility','Control','SDK','Dominium Bridge','XStack','bootstrap-era','pre-product'); foreach ($term in $terms) { $matches = @(rg -l -F -- $term docs README.md DOCUMENTATION.md ROADMAP.md PLANS.md IMPLEMENT.md); if ($LASTEXITCODE -eq 0 -and $matches.Count -gt 0) { "OK $($term): $($matches.Count) files" } else { "MISSING $($term)"; exit 1 } }
```

Result: passed.

- `AIDE Core`: 24 files
- `AIDE Hosts`: 20 files
- `AIDE Bridges`: 19 files
- `Contract`: 23 files
- `Harness`: 26 files
- `Runtime`: 17 files
- `Compatibility`: 27 files
- `Control`: 16 files
- `SDK`: 14 files
- `Dominium Bridge`: 19 files
- `XStack`: 12 files
- `bootstrap-era`: 21 files
- `pre-product`: 10 files

### Documentation sanity check

Command:

```powershell
git diff --check
```

Result: passed. Git reported line-ending normalization warnings only.

### Allowed-path audit

Command:

```powershell
$allowedExact = @('README.md','DOCUMENTATION.md','ROADMAP.md','PLANS.md','IMPLEMENT.md','.aide/queue/index.yaml'); $allowedPrefixes = @('docs/','.aide/queue/Q01-documentation-split/'); $paths = @(git status --porcelain | ForEach-Object { $_.Substring(3).Replace('\\','/') }); $bad = @(); foreach ($p in $paths) { if ($allowedExact -contains $p) { continue }; $ok = $false; foreach ($prefix in $allowedPrefixes) { if ($p.StartsWith($prefix)) { $ok = $true; break } }; if (-not $ok) { $bad += $p } }; if ($bad.Count -gt 0) { 'Forbidden or unexpected paths:'; $bad; exit 1 } else { "OK allowed-path audit: $($paths.Count) changed paths" }
```

Result: passed. The audit reported 34 changed paths and no forbidden paths.

### Post-evidence sanity rerun

After recording evidence and updating the ExecPlan, `IMPLEMENT.md`, queue status, and queue index, these checks were rerun:

- `git diff --check`: passed with line-ending normalization warnings only.
- `py -3 scripts/aide-queue-status`: passed; Q01 remained `needs_review`.
- `py -3 scripts/aide-queue-next`: passed; next pending item remained `Q02-structural-skeleton`.
- allowed-path audit: passed with 34 changed paths and no forbidden paths.

## Tests Not Run

No heavy host, native, shared runtime, packaging, or release tests were run. Q01 is documentation-only, and the strongest relevant checks were structural docs checks, queue helper checks, terminology scans, and diff sanity checks.
