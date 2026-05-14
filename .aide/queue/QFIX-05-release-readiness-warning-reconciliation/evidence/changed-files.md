# Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml`
- `.aide/queue/QFIX-05-release-readiness-warning-reconciliation/**`

## Generated Artifact State

- `.aide/generated/manifest.yaml`

## Inspected But Unchanged Generated Targets

- `AGENTS.md`
- `.agents/skills/aide-queue/SKILL.md`
- `.agents/skills/aide-execplan/SKILL.md`
- `.agents/skills/aide-review/SKILL.md`
- `.aide/generated/preview/CLAUDE.md`

## Readiness Records

- `IMPLEMENT.md`
- `PLANS.md`

## Excluded Generated Command Reports

- `.aide/git/**` helper reports were inspected and then restored so the commit
  does not carry stale branch-state output.
- `.aide/evals/runs/latest-golden-tasks.*` was refreshed by `eval run` and then
  restored because QFIX-05 records the command result without changing eval-run
  artifacts outside scope.
