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

This redo prompt follows Q25 pack/import repair and the Q26 Eureka handover
checkpoint. Earlier Q27 blocker evidence is retained in Git history, but this
packet is reopened as the canonical implementation packet and must end at
`needs_review`.
