# Prompt: AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01

Create and process `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`.

Implement the first deterministic Track B doc/knowledge truth reconciler. It
must observe, classify, compare, and report. It must not repair, rewrite,
regenerate, move, rename, normalize, delete, or apply source artifacts.

The reconciler emits GovernanceFinding records as a report convention only:

- id
- severity
- surface
- taxonomy
- claim
- expected
- observed
- evidence_refs
- affected_paths
- recommendation
- next_task

Recommended next task on success:

`AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`

Stop at `needs_review` with evidence.
