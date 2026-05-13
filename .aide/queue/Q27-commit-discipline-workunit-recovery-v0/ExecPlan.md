# Q27 ExecPlan - Commit Discipline And WorkUnit Recovery v0

## Purpose

Q27 is intended to make AIDE commits changelog-ready and make queued work
replay-safe, resumable, and recoverable from repo-local evidence.

## Scope

The planned scope includes commit-message policy, commit hook template,
commit/changelog/task command surfaces in AIDE Lite, WorkUnit and recovery
policies, golden tasks, tests, export-pack integration, documentation, and
evidence.

## Non-Goals

- No provider, model, or network calls.
- No Gateway forwarding or product runtime changes.
- No branch workflow helpers, CI, releases, installer, rollback, or deployment.
- No mutation of Eureka, Dominium, or other external repositories.

## Allowed Paths

The authoritative allowlist is in `task.yaml`. Q27 may edit AIDE queue,
policy, AIDE Lite, tests, golden tasks, export pack, compact docs, and
documentation paths listed there. It may not edit `.aide.local/**`, secrets,
runtime/product implementation, or external repos.

## Current Facts

- Initial worktree was clean at `05330b0842a3e39487bb67d8d8b44b4c40902ad7`.
- Current branch is `main`.
- Q25 `pack-status` now passes with `DIRTY_SOURCE_RECORDED` provenance.
- AIDE Lite validate/test/selftest/eval run pass before Q27 edits.
- Harness validate/doctor/self-check pass with existing review-gate warnings.
- Q27, Q28, and Q29 were superseded blocker attempts and are being redone in
  order by explicit operator instruction.

## Implementation Plan

1. Reopen the Q27 packet and record baseline validation.
2. Add AIDE commit-message, task-resumption, WorkUnit, and recovery policies.
3. Add commit template, hook template, and standards reports.
4. Extend AIDE Lite with commit, changelog, and task recovery command surfaces.
5. Add deterministic golden tasks and unittest coverage.
6. Update docs, export the pack, regenerate Q28 task context, and write
   evidence.
7. End Q27 at `needs_review`.

## Validation Intent

Q27 should run the full validation suite listed in the implementation prompt,
including AIDE Lite validate/test/selftest,
golden tasks, commit checks, changelog preview, task inspection/noop/status,
export-pack, pack-status, Harness/Compatibility/Gateway/Provider tests, and a
targeted secret scan.

## Evidence

Implementation evidence is stored under `evidence/`. Previous blocker evidence
is replaced by this redo pass.

## Retrospective

Q27 is a governance/tooling phase only. It does not add branch workflow helpers,
provider calls, model calls, release publishing, CI, or product runtime work.
