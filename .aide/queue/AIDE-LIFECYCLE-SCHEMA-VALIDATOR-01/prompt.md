# Prompt Seed

Task ID: `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`

Create and wire local validation for lifecycle schemas and non-mutating examples. Use AIDE Lite report-only commands with stdlib JSON validation. Validate lifecycle manifest, plan, report, rollback-compatible record schemas, example non-mutation boundaries, fixture-shape examples, protected paths, path traversal, rollback execution prohibition, and capability label honesty. Do not implement or execute lifecycle apply, install apply, upgrade apply, repair apply, rollback/uninstall apply, active repo apply, target repo mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply. End at `needs_review` with evidence and one safe next WorkUnit.
