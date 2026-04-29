# Q04 Planning Validation

Created: 2026-04-29

## Plan-Only Scope

This evidence file records validation for creating the Q04 planning packet only. No Harness command implementation, `scripts/aide` entrypoint, generated downstream artifact, Runtime, Host, Bridge, provider integration, app surface, or Q05+ work was created.

## Validation Commands

### Required Q04 queue files

Command:

```powershell
$paths = @(
  '.aide/queue/Q04-harness-v0/task.yaml',
  '.aide/queue/Q04-harness-v0/ExecPlan.md',
  '.aide/queue/Q04-harness-v0/prompt.md',
  '.aide/queue/Q04-harness-v0/status.yaml',
  '.aide/queue/Q04-harness-v0/evidence/planning-validation.md'
)
foreach ($p in $paths) {
  if (Test-Path $p) { "PASS $p" } else { "MISSING $p"; exit 1 }
}
```

Result: passed. All required Q04 planning files exist.

### Queue status

Command:

```powershell
py -3 scripts/aide-queue-status
```

Result: passed. Q04 is listed as `pending` with `planning_complete`; Q00 through Q03 remain `needs_review`; Q05 through Q08 remain pending.

### Next queue item

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed. Output identified `Q04-harness-v0` as the next pending item, with task and prompt paths populated.

### Queue index references

Command:

```powershell
Select-String -Path .aide/queue/index.yaml -Pattern 'Q04-harness-v0|Q04-harness-v0/task.yaml|Q04-harness-v0/ExecPlan.md|Q04-harness-v0/prompt.md|Q04-harness-v0/evidence'
```

Result: passed. `.aide/queue/index.yaml` references the Q04 task, ExecPlan, prompt, and evidence path.

### ExecPlan required sections

Command:

```powershell
$required = @(
  'Purpose',
  'Background And Current Repo Context',
  'Scope',
  'Non-goals',
  'Allowed Paths For Q04 Implementation',
  'Forbidden Paths For Q04 Implementation',
  'Harness Command Model',
  'Contract Loading Strategy',
  'Validation Severity Model',
  'Compile/Report Boundary',
  'Migration Boundary',
  'Bakeoff Boundary',
  'Planned Deliverables',
  'Milestones',
  'Progress',
  'Surprises And Discoveries',
  'Decision Log',
  'Validation And Acceptance',
  'Idempotence And Recovery',
  'Evidence To Produce',
  'Outcomes And Retrospective'
)
$text = Get-Content -Raw .aide/queue/Q04-harness-v0/ExecPlan.md
$missing = @()
foreach ($s in $required) {
  if ($text -notmatch "(?m)^## $([regex]::Escape($s))\s*$") { $missing += $s }
}
if ($missing.Count) { 'MISSING SECTIONS:'; $missing; exit 1 } else { 'PASS all required ExecPlan sections present' }
```

Result: passed. All required Q04 ExecPlan sections are present.

### Diff hygiene

Command:

```powershell
git diff --check
```

Result: passed. Git reported line-ending normalization warnings for `.aide/queue/index.yaml` and `PLANS.md`, but no whitespace errors.

### Allowed-path audit

Command:

```powershell
$changed = git status --porcelain -uall | ForEach-Object { $_.Substring(3) }
$bad = @()
foreach ($p in $changed) {
  $n = $p -replace '\\','/'
  if ($n -eq '.aide/queue/index.yaml' -or $n -eq 'PLANS.md' -or $n.StartsWith('.aide/queue/Q04-harness-v0/')) {
    "ALLOW $n"
  } else {
    $bad += $n
    "DENY $n"
  }
}
if ($bad.Count) { exit 1 } else { 'PASS allowed-path audit -uall' }
```

Result: passed. Changed paths are limited to `.aide/queue/Q04-harness-v0/**`, `.aide/queue/index.yaml`, and `PLANS.md`.

### Plan-only implementation guard

Command:

```powershell
Test-Path scripts/aide
```

Result: passed for plan-only scope. The command returned `False`, confirming the future Q04 Harness entrypoint was not created by this planning task.

## Summary

Q04 planning is complete and ready for a future implementation worker. No implementation work was performed.
