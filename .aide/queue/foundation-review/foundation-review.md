# AIDE Foundation Review: Q00-Q04

Date: 2026-04-29

## Executive Verdict

The Q00-Q03 foundation is coherent, evidence-backed, and careful about the reboot doctrine. It preserves bootstrap-era history, keeps the Core / Hosts / Bridges model visible, defines the internal Core split, and makes `.aide/` the declarative Profile/Contract source of truth without overclaiming Runtime, Hosts, Bridges, or generated artifacts.

Q04 is not complete. The repository contains a Q04 plan-only packet, but no Harness v0 implementation, no `scripts/aide` entrypoint, and no working `aide validate`, `aide doctor`, `aide compile`, `aide migrate`, or `aide bakeoff` command surface. Because Q05 requires at least pre/post Harness validation and generated-file drift checks, Q05 must be blocked until Q04 is implemented and reviewed.

Recommended decision: block Q05 and run a focused Q04 implementation/fix task.

## Per-Item Review Status

| Queue item | Queue status observed | Review outcome | Notes |
| --- | --- | --- | --- |
| Q00-bootstrap-audit | `needs_review` | PASS_WITH_NOTES | Baseline docs and evidence exist; it correctly stops at review and does not implement Q01+. |
| Q01-documentation-split | `needs_review` | PASS_WITH_NOTES | Documentation families, charters, decisions, maps, and terminology records exist; work is docs-only. |
| Q02-structural-skeleton | `needs_review` | PASS_WITH_NOTES | README-only `core/`, host-category, and `bridges/` skeletons exist; bootstrap-era code was mapped, not moved. |
| Q03-profile-contract-v0 | `needs_review` | PASS_WITH_NOTES | Declarative `.aide/` Profile/Contract v0 exists and keeps Profile distinct from Harness. |
| Q04-harness-v0 | `pending`, `planning_complete` | REQUEST_CHANGES | Q04 is plan-only. Required Harness implementation and entrypoint are absent. |

## Architectural Consistency Review

The reboot architecture is internally consistent through Q03:

- Public model is consistently documented as AIDE Core, AIDE Hosts, and AIDE Bridges.
- Internal Core split is consistently documented as Contract, Harness, Runtime, Compatibility, Control, and SDK.
- First shipped stack is stated as Contract + Harness + Compatibility + Dominium Bridge without claiming the stack is implemented.
- Runtime, Service, Commander, Mobile, IDE extension families, provider adapters, app surfaces, and full SDK remain deferred.
- XStack remains Dominium-local, not generic AIDE doctrine.

The main inconsistency is sequencing, not doctrine: Q04 is listed in this review request as completed, but the repository state says Q04 is only planned.

## Source-Of-Truth Review

The source-of-truth model is clear:

- `.aide/profile.yaml` and `.aide/**` catalogs are canonical for the self-hosting Profile/Contract.
- `.aide/queue/**` is canonical for queue execution state, prompts, ExecPlans, status, and evidence.
- `docs/reference/source-of-truth.md` distinguishes canonical records, generated outputs, caches, evidence, Profile, queue, and Harness.
- Generated downstream artifacts are explicitly non-canonical outputs until a later reviewed policy says otherwise.

This is strong enough for Q04 implementation, but not enough for Q05 because no Harness exists to validate or detect generated drift.

## Queue Integrity Review

The queue index is coherent for the actual repository state:

- Q00-Q03 are `needs_review`.
- Q04 is `pending` with `planning_state: planning_complete`.
- Q05-Q08 remain pending/planned.
- Q00-Q04 task packets and evidence directories exist where expected for their current state.

The queue is not coherent with proceeding directly to Q05 because the next pending item is Q04, not Q05, and Q04 is not implemented.

## Profile/Contract Review

Q03 created the expected minimal Contract/Profile v0:

- `.aide/profile.yaml` identifies the repo as the AIDE self-hosting repo with lifecycle `reboot/pre-product`.
- `.aide/toolchain.lock` records Contract/Profile posture without pretending package, worker, model, Runtime, or Harness automation exists.
- `.aide/components/`, `.aide/commands/`, `.aide/policies/`, `.aide/tasks/`, `.aide/evals/`, `.aide/adapters/`, and `.aide/compat/` exist.
- `core/contract/**` contains documented v0 shapes, not an executable validator.
- Profile and Harness are repeatedly distinguished in docs and contract records.

The contract is reviewable and honest. It is not a substitute for Harness execution.

## Harness Review

Q04 Harness v0 is absent:

- `scripts/aide` does not exist.
- `core/harness/` contains only the Q02 skeleton README.
- `.aide/commands/catalog.yaml` still marks `aide init`, `aide import`, `aide compile`, `aide validate`, `aide doctor`, `aide migrate`, and `aide bakeoff` as planned future Harness commands.
- Requested Harness command checks all fail because the entrypoint is missing.

This is the blocking foundation issue.

## Compatibility Readiness Review

Compatibility is visible and first-class:

- Compatibility appears in charters, roadmap, Profile, toolchain lock, components, policies, and `.aide/compat/**`.
- Full migration behavior and compatibility baseline are correctly deferred to Q06.
- Existing bootstrap-era inventory, matrices, research, environments, evals, packaging records, and host proofs remain compatibility inputs.

Compatibility posture does not block Q04, but Q05 must avoid changing compatibility or migration semantics.

## Generated-Artifact Readiness Review

Generated artifact source-of-truth rules are directionally clear:

- Generated outputs are non-canonical.
- Q05 owns generated artifact v0 and drift evidence.
- `CLAUDE.md` and `.claude/**` are absent.

However, Q05 readiness is blocked because the Harness is not available to validate before/after generation or detect stale generated output. Generated-file markers and drift checks should be part of Q05, but they need Q04's command surface first.

## Risks Before Q05

- Q04 Harness v0 is not implemented.
- Q00-Q03 remain in `needs_review` status, even though this review finds them acceptable with notes.
- Root overview docs are slightly behind the latest queue posture because they describe Q04 as next planning/implementation work, while Q04 planning now exists.
- Q05 could create generated artifacts without an executable local validator unless Q04 is completed first.

## Required Fixes Before Q05

1. Implement Q04 Harness v0 using `.aide/queue/Q04-harness-v0/prompt.md`.
2. Add the `scripts/aide` entrypoint and required commands: `init`, `import`, `compile`, `validate`, `doctor`, `migrate`, and `bakeoff`.
3. Ensure `aide validate` and `aide doctor` produce actionable output and that `aide validate` returns nonzero on hard failures.
4. Ensure `aide compile` reports only a compile plan and does not emit Q05 generated artifacts.
5. Record Q04 evidence: changed files, validation, command smoke, and remaining risks.
6. Move Q04 to `needs_review`, then review/pass it before Q05 planning or implementation.

## Recommended Decision

Do not proceed to Q05 yet. The smallest next task is a QFIX/Q04 implementation task that completes Harness v0 exactly as already planned.

## Final Decision

BLOCK_Q05
