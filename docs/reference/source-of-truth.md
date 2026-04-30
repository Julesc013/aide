# Source Of Truth

## Purpose

This reference distinguishes canonical records, generated outputs, caches, and evidence for the AIDE reboot.

## Canonical Records

| Area | Canonical Source |
| --- | --- |
| AIDE repo Profile/Contract | `.aide/profile.yaml` and declaration catalogs under `.aide/` |
| Queue execution state | `.aide/queue/index.yaml` and each task `status.yaml` |
| Queue task instructions | Each task `task.yaml`, `ExecPlan.md`, and `prompt.md` |
| Queue evidence | Each task-local `evidence/` directory |
| Self-hosting policies | `.aide/policies/**` plus `.aide/queue/policy.yaml` |
| Compatibility baseline | `.aide/compat/**` plus `core/compat/**` helpers |
| Dominium Bridge baseline | `bridges/dominium/**` plus `docs/reference/dominium-bridge.md` |
| Human explanation | `docs/**`, root docs, and `core/contract/**` references |
| Bootstrap-era history | Root phase records, `specs/**`, `shared/**`, `hosts/**`, `evals/**`, `governance/**`, `inventory/**`, `matrices/**`, `research/**`, `environments/**`, `labs/**`, and `packaging/**` |

## Generated Outputs

Generated downstream artifacts are outputs. They are not canonical unless a later reviewed policy explicitly marks them as such. Q05 owns generated artifact v0, deterministic generation rules, and drift evidence.

Q05 generated artifact v0 is documented in `docs/reference/generated-artifacts-v0.md`. Current Q05 targets are managed sections in `AGENTS.md` and selected `.agents/skills/**` files, a preview-only Claude guidance file under `.aide/generated/preview/CLAUDE.md`, and a deterministic manifest at `.aide/generated/manifest.yaml`.

Final root `CLAUDE.md`, final `.claude/**`, provider files, IDE extension files, package manifests, and app surfaces remain deferred.

## Caches And Runtime State

Runtime caches, worker state, local IDE state, chat history, and extension UI task queues are not source of truth for AIDE. They may help execute work, but the filesystem records above win when there is a conflict.

## Evidence

Evidence records what was checked, what changed, what remained blocked, and which review gates were reached. Evidence supports a claim; it does not replace the canonical contract or queue status.

## Profile Versus Queue

The Profile is repo contract truth. It says what the repository declares, requires, allows, owns, exposes, and defers.

The queue is execution truth. It says which work item is pending, running, blocked, awaiting review, passed, failed, or superseded.

## Profile Versus Harness

The Profile is declarative. Harness is executable machinery over that truth. Q04 implements Harness v0, and Q05 extends Harness compile and validate behavior for generated artifact markers, previews, manifests, and drift checks.

## Compatibility

Compatibility records how AIDE repo contract surfaces evolve. Q06 defines known v0 version identifiers, a current no-op migration registry, structural replay expectations, upgrade gates, and deprecation record format. Compatibility is source-of-truth for evolution posture, not product semantics.

The Compatibility baseline is documented in `docs/reference/compatibility-baseline.md`. Harness reads these records for structural `validate` and non-mutating `migrate` reports.

## Bridges

Bridges are downstream or project-specific overlays. Q07 defines the first AIDE-side Dominium Bridge baseline under `bridges/dominium/**` and documents it in `docs/reference/dominium-bridge.md`.

The Dominium Bridge records are canonical for AIDE-side bridge metadata only. They do not modify any Dominium repository, do not define Dominium product/runtime semantics, do not implement XStack internals, and do not emit real Dominium generated outputs.

XStack remains Dominium-local and strict. AIDE remains the portable layer below it.

## Bootstrap-Era Records

Old bootstrap documents and implementation records remain historical evidence. The reboot is an in-place refactor, not a greenfield restart, so future work should map and preserve old records unless a reviewed queue item explicitly migrates them.
