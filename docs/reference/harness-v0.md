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
- generated-artifact marker, manifest, and drift checks after Q05
- compatibility baseline version, migration, replay, upgrade-gate, and deprecation checks after Q06
- source-of-truth document checks

Diagnostic severities:

- `info`: observed fact, never blocks.
- `warning`: review or follow-up needed, but does not fail `aide validate`.
- `error`: hard structural failure; `aide validate` returns nonzero.

## Command Boundaries

`aide init` is non-destructive. It reports that the current repo is already initialized when `.aide/profile.yaml` exists.

`aide import` is report-only. It inspects guidance surfaces such as `AGENTS.md`, `.agents/skills/`, `.aide/`, `CLAUDE.md`, and `.claude/` without rewriting contract files.

`aide compile` is still non-mutating by default. Q05 adds:

- `py -3 scripts/aide compile --dry-run` for an explicit generation plan;
- `py -3 scripts/aide compile --preview` for preview-only output under `.aide/generated/preview/**`;
- `py -3 scripts/aide compile --write` for the approved managed sections, preview output, and `.aide/generated/manifest.yaml`.

Generated artifacts remain non-canonical compiled or managed outputs.

`aide validate` is the primary hard check. It validates enough of the current `.aide/` contract and queue to catch missing required records, generated artifact marker problems, stale manifest or source fingerprints, and deferred final Claude targets.

`aide doctor` prints diagnostics and the next recommended repair or review step.

`aide migrate` reports the Q06 Compatibility baseline. It lists known v0 versions, the `baseline-current-noop` migration registry entry, unknown-future-version posture, and the fact that no files are mutated.

`aide bakeoff` reads eval metadata only. It does not call models, providers, native tools, browser tools, network services, package managers, or external APIs.

## Implemented Now

Q04 implements:

- `scripts/aide`
- minimal Harness modules under `core/harness/**`
- structural validation and diagnostics
- compile, migration, import, init, and bakeoff reports
- lightweight standard-library Harness tests
- Q04 evidence and review-gated status

Q05 extends Harness v0 with:

- deterministic generated artifact planning;
- managed-section and preview generation;
- `.aide/generated/manifest.yaml`;
- generated marker and drift validation.

Q06 extends Harness v0 with:

- compatibility version registry checks;
- no-op migration baseline reporting;
- replay-corpus, upgrade-gate, and deprecation record checks.

## Deferred

Still deferred:

- full migration engine and mutating apply mode: later reviewed work
- Dominium Bridge baseline: Q07
- Runtime, service, providers, app surfaces, IDE extensions, Commander, Mobile, packaging, release automation, and autonomous worker execution

## Known v0 Limitations

Harness v0 still uses structural file, directory, text-anchor, marker, and fingerprint checks. It does not parse full YAML and does not enforce JSON Schema.

Compatibility baseline checks are also structural. They recognize the current v0 AIDE string identifiers and treat unknown or future identifiers as errors rather than attempting automatic migration.

Generated artifact v0 does not emit final root `CLAUDE.md`, final `.claude/**`, provider files, IDE extension files, package manifests, app surfaces, or release artifacts.
