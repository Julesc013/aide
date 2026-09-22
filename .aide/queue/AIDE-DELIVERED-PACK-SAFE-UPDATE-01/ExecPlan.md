# ExecPlan: Delivered Pack Safe Update

## Objective

Make a validated delivered pack capable of a supported, fail-closed update in
a disposable consumer repository while preserving target-owned content and
recording enough state to diagnose interruption safely.

## Scope

- Add a target-local portable import receipt containing exact installed
  managed-file and managed-section baselines.
- Compare previous baseline, current target, and incoming pack before deciding
  update, unchanged, add, or conflict.
- Permit predecessor-pack proof only after validating that pack's checksums.
- Bind optional preview/apply workflows to one deterministic plan digest.
- Preflight every operation before the first payload write.
- Persist an atomic intent journal and per-step observations during apply.
- Exercise the path only in disposable extracted-artifact consumers.

## Non-Goals

- Source-checkout self-update or mutation of a real project.
- Automatic merge of locally edited managed bytes.
- Repair, rollback, uninstall, fleet rollout, main promotion, tag, upload, or
  publication.
- Bulk adoption of the imported lifecycle specification chapters.

## Dependencies

- `dev@a2ba43624bf99d3354a2a7429a3241e3967310fc`.
- Independently importable archive behavior from
  `AIDE-DELIVERED-PACK-IMPORT-CLOSURE-01`.
- Existing pack checksum validation and safe-mode boundary.
- Accepted fixture-only ownership/apply contracts; their real-target
  non-capabilities remain intact.

## Allowed Paths

The exact allowlist is in `task.yaml`. The implementation owner is
`.aide/scripts/aide_lite.py`; focused regression owners are
`test_export_import.py` and `test_q47_release_bundle.py`.

## Progress

- [x] Refresh published refs and characterize current importer/apply owners.
- [x] Create an isolated task worktree from exact published `dev`.
- [x] Admit the bounded child and record retained gates.
- [x] Add red tests for baseline update, conflict-first refusal, stale plan,
      predecessor proof, and interruption evidence.
- [x] Add the extracted-artifact update regression after the core path is green.
- [x] Implement the smallest coherent lifecycle extension in `import-pack`.
- [x] Run focused validation immediately.
- [x] Run adjacent distribution, release, and repository validation.
- [x] Regenerate and qualify exact delivered bytes.
- [x] Record implementation and qualification evidence with explicit paths.
- [ ] Publish the exact qualified task candidate.
- [ ] Prepare and validate exact task-to-`dev` integration.

## Test Oracle

A positive update must begin from a validated pack and a disposable installed
consumer whose current managed bytes match its recorded baseline (or a
validated predecessor pack). A pass requires exact incoming bytes, a new
receipt, preserved target-authored content, and an idempotent rerun. Unknown
ownership, local edits, stale plan identity, tampered predecessor input, and
partial/uncertain interruption state must refuse before unproven writes.

## Recovery

The task branch is disposable until publication. Consumer fixtures live only
under test-managed temporary directories. An interrupted fixture apply must
retain its target-local intent journal; rerun classifies observed preimages and
postimages instead of blindly replaying. Shared history is never rewritten.

## Decisions

- Keep the portable lifecycle implementation in the delivered `aide_lite.py`
  interface so extracted safe-mode installations do not depend on source-only
  `core/` modules.
- Treat a path collision without a matching baseline as unknown ownership.
- Use exact byte digests as the first supported three-way oracle; semantic
  merges remain deferred and explicit.
- Preserve the original applied-plan identity on an idempotent rerun when the
  incoming pack and managed baseline are already identical.

## Qualification Result

The implementation source is
`31bd91bd10ed57e98e658380cd9372e074867f63`. The stabilized artifact metadata at
`12918667778a6ff001d4abd8967bf46a922a5131` passes the focused, adjacent, broad,
pack-provenance, release-bundle, and release-draft checks recorded in
`evidence/validation.md`. The exact ZIP and tar.gz artifacts pass extracted-CLI
consumer updates and no-op reruns. Publication to the task ref and integration
to `dev` remain the next controlled steps; no main, tag, upload, or public
release action is authorized by this task.
