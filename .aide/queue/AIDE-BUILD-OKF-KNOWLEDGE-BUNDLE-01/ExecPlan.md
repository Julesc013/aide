# ExecPlan: AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01

## Purpose

Build the first deterministic OKF-compatible AIDE knowledge bundle projection. The bundle explains current AIDE queue, protocol, evidence, ReferenceID, and EventRecord truth without becoming execution authority.

## Scope

- Add `core/knowledge/okf_bundle.py` and `core/knowledge/__init__.py`.
- Add thin `okf status/project/validate/lint` dispatch in `.aide/scripts/aide_lite.py`.
- Generate `.aide/knowledge/okf/**`.
- Generate `.aide/reports/okf/**`.
- Add focused tests and task-local evidence.
- Update `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Non-Goals

No runtime, service, Commander, provider/model calls, Gateway calls, network calls, event store, event replay, Reconciler, CapabilityManifest, ConformanceProfile, PatchTransaction, AdapterManifest, ContextPack v2, scheduler, leases, worker execution, branch/worktree automation, target apply, active apply, release, GitHub mutation, production readiness, or release readiness.

## Allowed Paths

The allowed paths are the paths listed in `task.yaml`. Any required edit outside those paths is a blocker.

## Current Facts To Verify

- Live queue truth recommends `AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01` after `AIDE-ACCEPT-EVENT-RECORD-SCHEMA-01`.
- `.aide/context/latest-task-packet.md` remains stale and points at lifecycle fixture runner work.
- EventRecord acceptance result is `ACCEPTED_WITH_WARNINGS`.
- The accepted capability target for this task is `minimal_okf_knowledge_bundle`.

## Milestones

- [x] Inspect repo state and queue truth.
- [x] Confirm predecessor EventRecord acceptance evidence.
- [x] Add OKF helper and parser/validator.
- [x] Add thin CLI dispatch.
- [x] Generate bundle and reports.
- [x] Add focused tests.
- [x] Write task evidence.
- [x] Run final validation set.
- [x] Commit local change.

## Decisions

- Use a stdlib-only deterministic frontmatter subset rather than adding a YAML dependency.
- Treat `index.md` and `log.md` as reserved files without required frontmatter.
- Treat broken links, orphan pages, missing optional refs, structural frontmatter subset use, and stale latest-task-packet as warning-class unless they reveal authority overclaiming.
- Preserve the authority boundary: protocol executes, evidence proves, references identify, events remember, OKF knowledge explains.

## Validation

Validation is recorded in `evidence/validation.md` and includes Python compile checks, focused unit tests, OKF CLI commands, report JSON parsing, predecessor protocol validators, task inspect/evidence, broad repository validation, and diff whitespace checks.

## Evidence

Evidence lives under `.aide/queue/AIDE-BUILD-OKF-KNOWLEDGE-BUNDLE-01/evidence/`.

## Recovery

The projection is deterministic. A future worker can rerun `py -3 .aide/scripts/aide_lite.py okf project --source current-repo` to regenerate `.aide/knowledge/okf/**` and `.aide/reports/okf/**`. If validation helpers rewrite unrelated generated reports, restore only that generated churn and record it.

## Retrospective

Implementation completed as projection-only knowledge-plane work and stopped at `needs_review`.
