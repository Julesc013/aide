# Q00 Repo Census Evidence

## Source Checks

Q00 inspected the repository root and the allowed control-plane trees before writing `docs/reference/repo-census.md`.

Commands used during census preparation:

```powershell
git status --short --branch
Get-ChildItem -Force | Select-Object Mode,Length,Name | Sort-Object Name
rg --files .aide .agents docs scripts | Sort-Object
```

## Observed Root Directories

- `.agents`
- `.aide`
- `.codex`
- `.git`
- `docs`
- `environments`
- `evals`
- `fixtures`
- `governance`
- `hosts`
- `inventory`
- `labs`
- `matrices`
- `packaging`
- `platforms`
- `research`
- `scripts`
- `shared`
- `specs`

## Observed Root Files

- `AGENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `DOCUMENTATION.md`
- `IMPLEMENT.md`
- `MAINTENANCE.md`
- `PLANS.md`
- `README.md`
- `ROADMAP.md`

## Census Result

The root tree was mapped into Q00 classifications in `docs/reference/repo-census.md`. No files or source directories were moved.

## Verification Boundary

This census is structural. It verifies repository shape and documented baseline posture; it does not rerun all host, shared-core, packaging, or environment checks from earlier phases.
