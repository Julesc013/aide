# AIDE Full Reboot Audit Report

Date: 2026-04-29

## Executive Verdict

The reboot foundation is coherent through Q03 and ready for Q04 Harness v0 implementation. The repository has preserved bootstrap-era history, added durable documentation families, introduced additive Core / Hosts / Bridges skeletons, and created a declarative `.aide/` Profile/Contract v0 without claiming a full product, Runtime, generated artifacts, or host implementations.

Q04 is not implemented. The Q04 packet is plan-complete and the next pending queue item, but `scripts/aide` does not exist and the Harness command surface is absent. This is expected current state and does not block starting Q04 implementation. It does block Q05.

Q05-generated-artifacts-v0 remains blocked until Q04 provides at least a local `aide validate`, `aide doctor`, and non-mutating `aide compile` command surface that can validate before and after generation.

## Current Commit, Branch, And Worktree

Observed before audit files were written:

- Branch: `main`
- Current commit: `0485cd5d2563397ef6a5855ad4572af7b6238a58`
- Latest commit summary: `0485cd5 Review foundation before Q05`
- `git status --short --branch`: `## main...origin/main`
- Worktree at audit start: clean
- Staged files at audit start: none
- Untracked files at audit start: none
- Suspicious generated target files checked: `CLAUDE.md` absent, `.claude/` absent

Observed after committing this audit:

- Branch: `main`
- Current commit: the commit containing this audit report
- Latest commit summary: `Audit reboot state before Q04`
- `git status --short --branch`: `## main...origin/main [ahead 1]`
- Worktree after audit commit: clean

This audit intentionally wrote only `.aide/queue/full-audit/**`.

## Current Repo Architecture Summary

AIDE is a pre-product, bootstrap-era repository being rebooted in place. The current repo has two visible layers:

- Bootstrap-era implementation and evidence remain in their original homes: `shared/**`, `hosts/**`, `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `specs/**`, `environments/**`, `labs/**`, `evals/**`, `packaging/**`, and root phase records.
- Reboot-era self-hosting structure is being added around `docs/**`, `.aide/**`, `core/**`, `bridges/**`, and README-only host category skeletons.

The canonical reboot model is present:

- Public model: AIDE Core, AIDE Hosts, AIDE Bridges.
- Internal Core split: Contract, Harness, Runtime, Compatibility, Control, SDK.
- First shipped stack: Contract + Harness + Compatibility + Dominium Bridge.
- XStack remains Dominium-local and strict.

## Completed Reboot Work

- Q00 produced a baseline freeze and reboot audit with evidence.
- Q01 created durable documentation families, charters, decisions, terminology records, and migration maps.
- Q02 created additive README-only structural skeletons for Core, Hosts, Bridges, and Dominium Bridge, without moving bootstrap-era code.
- Q03 created `.aide/` Profile/Contract v0 records, documented contract shapes, and source-of-truth references.
- Q04 planning exists and is self-contained, but implementation has not started.
- The foundation review records Q00-Q03 as acceptable with notes and blocks Q05 because Q04 is missing.

## Incomplete Reboot Work

- Q04 Harness v0 is not implemented.
- Q05 generated artifacts v0 is not ready.
- Q06 compatibility baseline is deferred.
- Q07 Dominium Bridge baseline is deferred.
- Q08 self-hosting automation is deferred.
- Runtime, Service, Commander, Mobile, IDE Hosts, provider adapters, app surfaces, release automation, and autonomous worker execution remain later work.

## Queue State

`.aide/queue/index.yaml` is coherent:

- Q00-Q03: `needs_review`, implemented evidence present.
- Q04: `pending`, `planning_state: planning_complete`.
- Q05-Q08: `pending`, `planning_state: planned`.

`scripts/aide-queue-next` reports Q04 as the next pending item. Q04 is therefore the correct next implementation task.

## Documentation State

The documentation split exists and is navigable:

- `docs/constitution/`
- `docs/charters/`
- `docs/roadmap/`
- `docs/reference/`
- `docs/decisions/`
- `docs/design-mining/`

Root docs point to the reboot architecture and preserve pre-product honesty. Minor freshness risk remains: some root overview text still frames Q04 as the next plan or implementation step even though Q04 planning now exists. This is not a Q04 blocker; Q04 implementation can update those statements.

## `.aide/` Profile/Contract State

`.aide/profile.yaml` and `.aide/toolchain.lock` exist and identify this repo as the AIDE self-hosting repo in `reboot/pre-product` lifecycle status.

Required declaration areas exist:

- `.aide/components/`
- `.aide/commands/`
- `.aide/policies/`
- `.aide/tasks/`
- `.aide/evals/`
- `.aide/adapters/`
- `.aide/compat/`
- `.aide/queue/`

The contract is declarative. It correctly says Harness is planned for Q04, generated artifacts are planned for Q05, compatibility baseline is Q06, and Dominium Bridge baseline is Q07.

## Harness State

Harness v0 is absent:

- `scripts/aide` is missing.
- `core/harness/` contains only the skeleton README.
- `aide init`, `aide import`, `aide compile`, `aide validate`, `aide doctor`, `aide migrate`, and `aide bakeoff` do not exist.
- `.aide/commands/catalog.yaml` marks those commands as planned future Harness commands.

This is the expected current state before Q04 implementation.

## Compatibility State

Compatibility is first-class but not overclaimed:

- Compatibility appears in docs, the profile, component catalog, policy records, and `.aide/compat/**`.
- `.aide/compat/schema-version.yaml` records current Contract/Profile versions.
- `.aide/compat/migration-baseline.yaml` is a placeholder owned by Q06.
- No migration engine or compatibility baseline has been implemented.

This is sufficient for Q04. It is not sufficient for Q06 claims.

## Dominium Bridge State

Dominium Bridge has a skeleton only:

- `bridges/dominium/README.md` exists.
- `bridges/dominium/xstack/`, `profiles/`, `policies/`, and `generators/` are placeholder homes.
- XStack is documented as Dominium-local and strict.
- Q07 owns any baseline bridge implementation.

## Generated Artifact Readiness

Generated artifact source-of-truth policy is clear enough to plan later work:

- Generated outputs are non-canonical compiled targets.
- Q05 owns generated artifact v0.
- `CLAUDE.md` and `.claude/` are absent.
- No generated target artifacts were detected.

Q05 cannot proceed yet because Q04 Harness validation does not exist.

## Risk Register

The main immediate risk is sequencing, not architecture: starting Q05 before Q04 would create generated output without local validation and drift checks.

Other risks:

- Q00-Q03 remain `needs_review`, so future prompts must explicitly acknowledge or resolve those review gates.
- Root docs have small freshness lag around Q04 planning status.
- Contract shape validation is currently documented and manual; executable enforcement waits for Q04.
- Compatibility and migration posture remain policy-bound but deferred to Q06.

## Blocker Register

No blocker prevents Q04 implementation.

Blockers before Q05:

- Q04 Harness v0 implementation missing.
- Q04 command smoke evidence missing.
- No executable generated-artifact drift check exists yet.
- Q00-Q03 review posture should be accepted or explicitly cited before generated outputs are emitted.

## Recommended Next Task

Run Q04 Harness v0 implementation using `.aide/queue/Q04-harness-v0/prompt.md`, with explicit acknowledgement that Q00-Q03 remain review-gated but have foundation-review support.

Q04 should create the smallest deterministic Harness v0:

- `scripts/aide`
- `core/harness/**` implementation files
- `aide init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`
- `docs/reference/harness-v0.md`
- Q04 evidence and status updates

## Can Q04 Proceed?

Yes. Q04 can proceed with the existing plan and explicit authorization. The current facts match the Q04 ExecPlan dependency model.

## Does Q05 Remain Blocked?

Yes. Q05 remains blocked until Q04 is implemented and reviewed.

## Decision

PROCEED_TO_Q04_IMPLEMENTATION
