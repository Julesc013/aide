# Harness v0

## Purpose

Harness v0 is the first executable AIDE Harness surface for the reboot. It reads the Q03 `.aide/` Profile/Contract and performs local structural checks, diagnostics, and non-mutating reports.

The Profile is declarative repo truth. Harness is executable machinery over that truth.

## Entry Point

Run from the repo root:

```powershell
py -3 scripts/aide --help
```

Implemented commands:

- `py -3 scripts/aide init`
- `py -3 scripts/aide import`
- `py -3 scripts/aide compile`
- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide migrate`
- `py -3 scripts/aide bakeoff`

## Validation Model

Harness v0 uses Python standard library only. It does not parse full YAML and does not enforce JSON Schema. Validation is limited to:

- required file checks
- required directory checks
- simple text anchor checks
- queue index and task packet checks
- evidence file checks
- generated-artifact absence checks
- source-of-truth document checks

Diagnostic severities:

- `info`: observed fact, never blocks.
- `warning`: review or follow-up needed, but does not fail `aide validate`.
- `error`: hard structural failure; `aide validate` returns nonzero.

## Command Boundaries

`aide init` is non-destructive. It reports that the current repo is already initialized when `.aide/profile.yaml` exists.

`aide import` is report-only. It inspects guidance surfaces such as `AGENTS.md`, `.agents/skills/`, `.aide/`, `CLAUDE.md`, and `.claude/` without rewriting contract files.

`aide compile` prints a compile plan only. It creates no downstream artifacts. Q05 owns generated artifacts, generated-file markers, and stale-output drift checks.

`aide validate` is the primary hard check. It validates enough of the current `.aide/` contract and queue to catch missing required records and premature generated artifacts.

`aide doctor` prints diagnostics and the next recommended repair or review step.

`aide migrate` is a no-op baseline report. Q06 owns compatibility baseline and migration hardening.

`aide bakeoff` reads eval metadata only. It does not call models, providers, native tools, browser tools, network services, package managers, or external APIs.

## Implemented Now

Q04 implements:

- `scripts/aide`
- minimal Harness modules under `core/harness/**`
- structural validation and diagnostics
- compile, migration, import, init, and bakeoff reports
- lightweight standard-library Harness tests
- Q04 evidence and review-gated status

## Deferred

Still deferred:

- generated downstream artifacts: Q05
- compatibility baseline and migration engine: Q06
- Dominium Bridge baseline: Q07
- Runtime, service, providers, app surfaces, IDE extensions, Commander, Mobile, packaging, release automation, and autonomous worker execution

## Known v0 Limitations

Q04 does not mutate final `.aide/` contract catalogs. Some Q03 records still mark Harness commands as planned or not implemented. Harness v0 reports that as a warning and leaves canonical contract refresh to a later review-gated task.
