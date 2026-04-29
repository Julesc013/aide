# Full Audit Validation

Date: 2026-04-29

All commands were run from the repository root unless noted.

## Git State

Command:

```powershell
git branch --show-current
git rev-parse HEAD
git log -1 --oneline
git status --short --branch
```

Result: passed.

Observed:

```text
main
0485cd5d2563397ef6a5855ad4572af7b6238a58
0485cd5 Review foundation before Q05
## main...origin/main
```

Command:

```powershell
git status --short
git status --ignored --short | Select-Object -First 80
```

Result: passed. No staged, untracked, or ignored generated files were reported before audit files were written.

## Queue Checks

Command:

```powershell
py -3 scripts/aide-queue-status
```

Result: passed.

Observed:

```text
Q00-bootstrap-audit          needs_review active
Q01-documentation-split      needs_review implemented
Q02-structural-skeleton      needs_review implemented
Q03-profile-contract-v0      needs_review implemented
Q04-harness-v0               pending      planning_complete
Q05-generated-artifacts-v0   pending      planned
Q06-compatibility-baseline   pending      planned
Q07-dominium-bridge-baseline pending      planned
Q08-self-hosting-automation  pending      planned
```

Command:

```powershell
py -3 scripts/aide-queue-next
```

Result: passed.

Observed:

```text
Q04-harness-v0
status: pending
planning_state: planning_complete
title: Harness v0
task: .aide/queue/Q04-harness-v0/task.yaml
prompt: .aide/queue/Q04-harness-v0/prompt.md
```

## Harness Checks

Command:

```powershell
if (Test-Path scripts/aide) { & scripts/aide --help } else { Write-Output 'MISSING scripts/aide'; exit 127 }
```

Result: failed as expected for current repo state. Exit code `127`.

Output:

```text
MISSING scripts/aide
```

Command:

```powershell
$commands = @('--help','validate','doctor','compile','migrate','bakeoff')
foreach ($cmd in $commands) {
  if (Test-Path scripts/aide) {
    & scripts/aide $cmd
    "EXIT $cmd $LASTEXITCODE"
  } else {
    "MISSING scripts/aide for scripts/aide $cmd"
  }
}
```

Result: passed as an audit check. Every Harness command was reported missing because `scripts/aide` is absent.

Observed:

```text
MISSING scripts/aide for scripts/aide --help
MISSING scripts/aide for scripts/aide validate
MISSING scripts/aide for scripts/aide doctor
MISSING scripts/aide for scripts/aide compile
MISSING scripts/aide for scripts/aide migrate
MISSING scripts/aide for scripts/aide bakeoff
```

## Documentation Directory Checks

Command:

```powershell
$paths = @(
  'docs/constitution','docs/charters','docs/roadmap','docs/reference','docs/decisions','docs/design-mining',
  '.aide/components','.aide/commands','.aide/policies','.aide/tasks','.aide/evals','.aide/adapters','.aide/compat','.aide/queue',
  'core','core/contract','core/harness','core/runtime','core/compat','core/control','core/sdk','core/tests',
  'bridges','bridges/dominium','hosts/cli','hosts/service','hosts/commander','hosts/extensions'
)
foreach ($p in $paths) { if (Test-Path $p -PathType Container) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed. All listed directories exist.

## Contract File Checks

Command:

```powershell
$required = @(
  '.aide/profile.yaml',
  '.aide/toolchain.lock',
  '.aide/components/catalog.yaml',
  '.aide/commands/catalog.yaml',
  '.aide/policies/autonomy.yaml',
  '.aide/policies/bypass.yaml',
  '.aide/policies/review-gates.yaml',
  '.aide/policies/generated-artifacts.yaml',
  '.aide/policies/compatibility.yaml',
  '.aide/tasks/catalog.yaml',
  '.aide/evals/catalog.yaml',
  '.aide/adapters/catalog.yaml',
  '.aide/compat/schema-version.yaml',
  '.aide/compat/migration-baseline.yaml',
  'docs/reference/source-of-truth.md',
  'docs/reference/profile-contract-v0.md'
)
foreach ($p in $required) { if (Test-Path $p) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed. All required contract files exist.

## Structural Skeleton Checks

Command:

```powershell
$required = @(
  'core/README.md',
  'core/contract/README.md',
  'core/harness/README.md',
  'core/runtime/README.md',
  'core/compat/README.md',
  'core/control/README.md',
  'core/sdk/README.md',
  'core/tests/README.md',
  'hosts/README.md',
  'hosts/cli/README.md',
  'hosts/service/README.md',
  'hosts/commander/README.md',
  'hosts/extensions/README.md',
  'hosts/extensions/visualstudio/README.md',
  'hosts/extensions/vscode/README.md',
  'hosts/extensions/xcode/README.md',
  'hosts/extensions/later/README.md',
  'bridges/README.md',
  'bridges/dominium/README.md',
  'bridges/dominium/xstack/README.md',
  'bridges/dominium/profiles/README.md',
  'bridges/dominium/policies/README.md',
  'bridges/dominium/generators/README.md',
  'docs/reference/structural-migration-map.md'
)
foreach ($p in $required) { if (Test-Path $p) { "OK $p" } else { "MISSING $p"; exit 1 } }
```

Result: passed. All required skeleton READMEs and the structural migration map exist.

## Terminology Scan

Command:

```powershell
$terms = @(
  'AIDE Core',
  'AIDE Hosts',
  'AIDE Bridges',
  'Contract',
  'Harness',
  'Runtime',
  'Compatibility',
  'Control',
  'SDK',
  'Dominium Bridge',
  'XStack',
  'source of truth',
  'generated artifacts',
  'pre-product',
  'bootstrap-era',
  'Q04',
  'Q05'
)
foreach ($term in $terms) {
  $matches = @(rg -l -F -- $term README.md ROADMAP.md PLANS.md IMPLEMENT.md DOCUMENTATION.md AGENTS.md .aide docs core hosts bridges 2>$null)
  if ($LASTEXITCODE -eq 0 -and $matches.Count -gt 0) {
    "OK $term :: $($matches.Count) files"
  } else {
    "MISSING $term"
    exit 1
  }
}
```

Result: passed. All required terms were found.

Observed counts:

```text
OK AIDE Core :: 53 files
OK AIDE Hosts :: 35 files
OK AIDE Bridges :: 37 files
OK Contract :: 73 files
OK Harness :: 78 files
OK Runtime :: 61 files
OK Compatibility :: 58 files
OK Control :: 35 files
OK SDK :: 48 files
OK Dominium Bridge :: 57 files
OK XStack :: 34 files
OK source of truth :: 15 files
OK generated artifacts :: 32 files
OK pre-product :: 22 files
OK bootstrap-era :: 64 files
OK Q04 :: 45 files
OK Q05 :: 35 files
```

## Generated Artifact Checks

Command:

```powershell
$paths = @('CLAUDE.md','.claude')
foreach ($p in $paths) {
  if (Test-Path $p) { "FOUND $p"; exit 1 } else { "OK absent $p" }
}
```

Result: passed.

Observed:

```text
OK absent CLAUDE.md
OK absent .claude
```

## Repository Map Input

Command:

```powershell
$dirs = @('core','shared','hosts','bridges','governance','inventory','matrices','research','specs','environments','labs','evals','packaging','scripts','.agents','.aide','docs','fixtures','platforms')
foreach ($d in $dirs) {
  if (Test-Path $d) {
    $files = @(rg --files $d 2>$null)
    "${d}: $($files.Count) files"
  } else {
    "${d}: missing"
  }
}
```

Result: passed. File counts were recorded as audit input.

## Exploratory Command That Failed And Was Rerun

Command:

```powershell
rg -n "status:|implemented|planned|not_implemented|deferred|skeleton|future" core/README.md core/*/README.md hosts/README.md hosts/*/README.md hosts/extensions/*/README.md bridges/README.md bridges/dominium/**/*.md | Select-Object -First 160
```

Result: failed with exit code `1` because PowerShell passed wildcard path patterns literally to `rg` on Windows. This was a command-form issue, not a repository issue.

Corrected command:

```powershell
$files = rg --files core hosts bridges | Where-Object { $_ -match 'README\.md$' }
Select-String -Path $files -Pattern 'status:|implemented|planned|not implemented|deferred|skeleton|future|Q02|Q04|Q07' | Select-Object -First 160
```

Result: passed. Skeleton READMEs consistently mark future/deferred work and avoid claiming implementation.

## Tests Not Run

No heavy host/native tests, external provider or model calls, browser tests, network calls, packaging or release automation, or secret-dependent checks were run.

## Final Audit Packet Checks

Command:

```powershell
$files = @(
  '.aide/queue/full-audit/audit-report.md',
  '.aide/queue/full-audit/repo-map.md',
  '.aide/queue/full-audit/queue-audit.md',
  '.aide/queue/full-audit/contract-audit.md',
  '.aide/queue/full-audit/harness-readiness.md',
  '.aide/queue/full-audit/q05-blocker-review.md',
  '.aide/queue/full-audit/planning-recommendations.md',
  '.aide/queue/full-audit/validation.md',
  '.aide/queue/full-audit/risks.md',
  '.aide/queue/full-audit/summary-for-planning-chat.md'
)
foreach ($f in $files) { if (Test-Path $f) { "OK $f" } else { "MISSING $f"; exit 1 } }
```

Result: passed. All required audit deliverables exist.

Command:

```powershell
py -3 scripts/aide-queue-status
py -3 scripts/aide-queue-next
```

Result: passed. Queue state remained unchanged; Q04 is still the next pending item.

Command:

```powershell
$matches = @(Select-String -Path .aide/queue/full-audit/audit-report.md -Pattern '^(PROCEED_TO_Q04_IMPLEMENTATION|BLOCK_Q04|PROCEED_TO_Q05|BLOCK_AND_REPAIR_FOUNDATION)$')
$matches | ForEach-Object { $_.Line }
if ($matches.Count -ne 1) { "BAD decision marker count $($matches.Count)"; exit 1 }
```

Result: passed. The single final decision marker is:

```text
PROCEED_TO_Q04_IMPLEMENTATION
```

Command:

```powershell
git diff --check
```

Result: passed. No whitespace errors were reported.

Command:

```powershell
$changed = git status --porcelain -uall | ForEach-Object { $_.Substring(3).Replace('\','/') }
$bad = @()
foreach ($p in $changed) {
  if ($p.StartsWith('.aide/queue/full-audit/')) {
    "ALLOW $p"
  } else {
    $bad += $p
    "DENY $p"
  }
}
if ($bad.Count) { exit 1 } else { 'PASS allowed-path audit' }
```

Result: passed. Only `.aide/queue/full-audit/**` paths were changed.

Command:

```powershell
git status --short
```

Result: passed. Output showed only the untracked `.aide/queue/full-audit/` directory before commit:

```text
?? .aide/queue/full-audit/
```

## Commit And Final Worktree State

Command:

```powershell
git add .aide/queue/full-audit
git commit -m "Audit reboot state before Q04" ...
```

Result: passed. Created commit:

```text
Audit reboot state before Q04
```

The first audit commit was amended to include the final audit state. The exact current commit hash is the commit containing this validation file and can be read with `git log -1 --oneline`. Git emitted line-ending normalization warnings for the new audit Markdown files. No content or scope error was reported.

Command:

```powershell
git status --short --branch
git log -1 --oneline
py -3 scripts/aide-queue-next
```

Result: passed.

Observed after commit:

```text
## main...origin/main [ahead 1]
Audit reboot state before Q04
Q04-harness-v0
status: pending
planning_state: planning_complete
title: Harness v0
task: .aide/queue/Q04-harness-v0/task.yaml
prompt: .aide/queue/Q04-harness-v0/prompt.md
```

Command:

```powershell
if (Test-Path scripts/aide) { & scripts/aide --help } else { Write-Output 'MISSING scripts/aide'; exit 127 }
```

Result: failed as expected for current pre-Q04 state. Exit code `127`; output:

```text
MISSING scripts/aide
```

Command:

```powershell
$paths = @('CLAUDE.md','.claude')
foreach ($p in $paths) {
  if (Test-Path $p) { "FOUND $p"; exit 1 } else { "OK absent $p" }
}
```

Result: passed. Generated target artifacts remain absent.
