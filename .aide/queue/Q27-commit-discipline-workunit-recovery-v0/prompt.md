# Q27 Prompt Summary

Implement AIDE's canonical commit discipline and WorkUnit recovery layer:

- structured Conventional Commit subjects with Markdown bodies;
- commit checker, commit template, and optional local hook;
- changelog and release-note preview from structured commit bodies;
- task resumption, WorkUnit idempotency, no-op detection, and recovery policy;
- task inspection, noop-check, dependency, recovery, evidence, and status
  commands in AIDE Lite;
- deterministic golden tasks and tests;
- export-pack integration for future target imports;
- compact documentation and Q27 evidence.

The prompt also required a prerequisite check: if Q25 outputs were missing or
materially incomplete, Q27 must write blocker evidence and stop rather than
silently implementing Q25 repair work inside Q27.

Q27 stopped on that prerequisite rule because baseline AIDE Lite validation and
pack-status fail before Q27 edits.
