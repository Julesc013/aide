# ExecPlan: QCHECK-cross-repo-adapter-readiness-audit

## Goal

Audit the post-QFIX/Q21-Q24 AIDE state and determine whether AIDE is ready for
serious Eureka handover work without implementing fixes, changing adapters, or
mutating target repositories.

## Scope

Allowed writes are limited to this checkpoint packet:

- `.aide/queue/QCHECK-cross-repo-adapter-readiness-audit/**`

Read-only inspection may include the sibling Eureka and Dominium repos when
present. No target command that writes files is allowed.

## Plan

1. Inspect git, queue, profile, command catalog, and existing checkpoint state.
2. Run Harness, AIDE Lite, adapter, export-pack status, and unit-test validation.
3. Inspect Eureka and Dominium target-pilot evidence read-only.
4. Audit token reduction, quality gates, pack boundary, adapter safety, and
   handover readiness.
5. Refresh report artifacts and evidence.
6. Run final structural validation and commit the audit artifacts if safe.

## Findings Summary

- AIDE validation and tests pass, with known Harness warnings for old review
  gates and generated manifest drift.
- Q09-Q20 are reconciled as `passed` with notes.
- QFIX-01, QFIX-02, Q21, Q24, and this checkpoint remain `needs_review`, which
  matches their stop-at-review prompts.
- Eureka and Dominium target pilots are present in sibling repos and show large
  estimated compact-packet reductions.
- The current profile and Harness self-check next-step guidance are stale after
  Q24 and still point toward QFIX-02/Q21.
- The Q21 importer is usable for fixture import but too broad for the narrower
  target-pilot scopes; both real pilots used manual manifest-guided imports
  after a successful dry-run.
- The current export pack boundary passes, but committed checksum validation now
  fails on `manifest.yaml`; the manifest also records an older source commit
  and `source_dirty_state: true`, so clean-pack provenance must be repaired
  before broad external handoff.

## Review Gate

This audit stops at `needs_review`. It recommends a repair/handover-prep queue
item before any broader Eureka handover.
