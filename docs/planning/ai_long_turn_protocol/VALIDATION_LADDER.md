# Validation Ladder

Validation should scale with risk and blast radius. Report actual commands and
actual results only.

## Tier 0: Structural Diff Checks

- `git status --short`
- `git diff --check`
- file existence checks for expected artifacts

## Tier 1: AIDE Structural Checks

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- task-specific `task inspect` and `task evidence`

## Tier 2: Focused Tests

Run tests for changed modules, changed command surfaces, changed schemas, or
changed docs validation hooks.

## Tier 3: Broad Local Checks

Run broader AIDE Lite tests, golden tasks, verifier, review-pack, export-pack,
or pack-status when the changed surface touches those systems.

## Tier 4: External Or Manual Checks

External discovery, target-repo checks, hardware checks, provider/model checks,
publication rehearsals, and human review are not silently simulated. If needed,
record them as deferred or blocked.

## Reporting Rule

Separate:

- tests run
- tests not run
- tests deferred to manual or external execution
- warnings accepted with reason
- blockers that stop the turn
