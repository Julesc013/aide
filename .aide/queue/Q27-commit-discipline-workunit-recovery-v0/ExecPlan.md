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

- Initial worktree was clean.
- Current branch was `main`.
- `py -3` was unavailable.
- `python` resolved to Python 3.8.1 and failed on existing Harness code that
  requires `str.removeprefix`.
- `python3` resolved to Python 3.9.13 and was used for validation.
- `python3 scripts/aide validate`, `doctor`, and `self-check` passed with
  existing warnings.
- `python3 .aide/scripts/aide_lite.py validate` failed before Q27 edits.
- `python3 .aide/scripts/aide_lite.py pack-status` failed before Q27 edits.

## Blocker

Q27 cannot proceed under the prompt's prerequisite rule because Q25 pack/local
state acceptance is not coherent at current HEAD:

- `pack-status` reports `checksums_valid: false` and `checksum_problems: 125`.
- AIDE Lite validation reports missing
  `.aide.local.example/secrets/README.md`.
- The missing local-state template path is outside Q27's allowed paths.

## Recovery Plan

1. Repair or review Q25 so the current export pack and local-state template
   baseline validate from repo-local files.
2. Re-run `python3 .aide/scripts/aide_lite.py validate` and `pack-status`.
3. Reopen Q27 from this ExecPlan.
4. Implement the full Q27 policy/tooling/docs/tests/export scope and end at
   `needs_review`.

## Validation Intent

After the Q25 blocker is repaired, Q27 should run the full validation suite
listed in the implementation prompt, including AIDE Lite validate/test/selftest,
golden tasks, commit checks, changelog preview, task inspection/noop/status,
export-pack, pack-status, Harness/Compatibility/Gateway/Provider tests, and a
targeted secret scan.

## Evidence

Blocker evidence is stored under `evidence/`. No Q27 policy or tooling changes
were made.

## Retrospective

Q27 stopped before implementation as required by the prerequisite instruction.
This prevents Q27 from silently repairing or masking Q25-owned pack/local-state
drift.
