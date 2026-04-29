# Self-Bootstrap Validation Evidence

## Scope

This evidence record belongs to the self-bootstrap task that created the initial AIDE filesystem queue scaffold. It does not complete Q00. Q00 remains ready for a future worker.

## Created Or Updated By Bootstrap

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/queue/README.md`
- `.aide/queue/index.yaml`
- `.aide/queue/policy.yaml`
- `.aide/queue/Q00-bootstrap-audit/task.yaml`
- `.aide/queue/Q00-bootstrap-audit/ExecPlan.md`
- `.aide/queue/Q00-bootstrap-audit/prompt.md`
- `.aide/queue/Q00-bootstrap-audit/status.yaml`
- `.aide/queue/Q00-bootstrap-audit/evidence/bootstrap-validation.md`
- `.aide/policies/autonomy.yaml`
- `.aide/policies/bypass.yaml`
- `.aide/policies/review-gates.yaml`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `scripts/aide-queue-next`
- `scripts/aide-queue-status`
- `scripts/aide-queue-run`
- `docs/reference/self-bootstrap.md`

## Validation Commands

All validation below was run from the repository root on 2026-04-29.

### Required File Existence

Command:

```powershell
$required = @(
'.aide/profile.yaml',
'.aide/toolchain.lock',
'.aide/queue/README.md',
'.aide/queue/index.yaml',
'.aide/queue/policy.yaml',
'.aide/queue/Q00-bootstrap-audit/task.yaml',
'.aide/queue/Q00-bootstrap-audit/ExecPlan.md',
'.aide/queue/Q00-bootstrap-audit/prompt.md',
'.aide/queue/Q00-bootstrap-audit/status.yaml',
'.aide/queue/Q00-bootstrap-audit/evidence/bootstrap-validation.md',
'.aide/policies/autonomy.yaml',
'.aide/policies/bypass.yaml',
'.aide/policies/review-gates.yaml',
'.agents/skills/aide-queue/SKILL.md',
'.agents/skills/aide-execplan/SKILL.md',
'.agents/skills/aide-review/SKILL.md',
'AGENTS.md',
'scripts/aide-queue-next',
'scripts/aide-queue-status',
'scripts/aide-queue-run',
'docs/reference/self-bootstrap.md'
)
$missing = $required | Where-Object { -not (Test-Path $_) }
if ($missing) { $missing | ForEach-Object { "MISSING $_" }; exit 1 }
"PASS required files exist: $($required.Count)"
```

Result: passed. Output reported `PASS required files exist: 21`.

### Script Syntax

Command:

```powershell
py -3 -m py_compile scripts/aide-queue-next scripts/aide-queue-status scripts/aide-queue-run
```

Result: passed with no syntax errors. The generated `scripts/__pycache__` directory was removed after the check.

Cleanup command:

```powershell
Remove-Item -LiteralPath scripts/__pycache__ -Recurse -Force
```

Result: passed after confirming the resolved path stayed under `scripts/`.

### Queue Status

Command:

```powershell
py -3 scripts/aide-queue-status
```

Result: passed. Summary output:

```text
Q00-bootstrap-audit          pending      active   Baseline freeze and reboot audit
Q01-documentation-split      pending      planned  Documentation split for reboot model
Q02-structural-skeleton      pending      planned  Minimal self-hosting structural skeleton
Q03-profile-contract-v0      pending      planned  Profile and contract v0
Q04-harness-v0               pending      planned  Harness v0
```

### Queue Next

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed. Output identified `Q00-bootstrap-audit` as the next pending item and pointed to its `task.yaml` and `prompt.md`.

### Queue Runner Skeleton

Command:

```powershell
py -3 scripts/aide-queue-run
```

Result: passed. Output printed the Q00 task metadata and prompt. It did not invoke Codex or modify repository state.

### Anchor Scan

Command:

```powershell
rg -n "canonical|Q00-bootstrap-audit|review gate|ExecPlan|bypass|filesystem queue" AGENTS.md README.md DOCUMENTATION.md docs/reference/self-bootstrap.md .aide .agents/skills/aide-queue .agents/skills/aide-execplan .agents/skills/aide-review scripts/README.md
```

Result: passed. Required queue, policy, Q00, review-gate, bypass, and ExecPlan anchors were present.

### Allowed Path Audit

Command:

```powershell
git status --porcelain
```

plus a PowerShell allowlist check against:

```text
AGENTS.md
README.md
PLANS.md
IMPLEMENT.md
DOCUMENTATION.md
docs/**
.aide/**
.agents/**
scripts/**
```

Result: passed. The audit reported 16 changed path entries, all inside the allowed set.

### Whitespace And Generated Drift

Command:

```powershell
git diff --check
```

Result: passed. Git reported line-ending normalization warnings for existing tracked Markdown files, but no whitespace errors.

Command:

```powershell
if (Test-Path scripts/__pycache__) { 'PYCACHE_PRESENT'; exit 1 } else { 'PASS no scripts/__pycache__' }
```

Result: passed. No generated Python bytecode remained in the worktree.

## Deliberate Deferrals

- Q00 was not executed by this bootstrap task.
- Q01 through Q04 were listed in the queue only; no task folders or implementation were created for them.
- `scripts/aide-queue-run` remains non-destructive and does not invoke Codex or any worker.
- No full YAML validator, schema validator, package manager, runtime, host implementation, IDE extension, provider integration, release automation, or app surface was created.

## Blockers

None for the self-bootstrap scaffold.
