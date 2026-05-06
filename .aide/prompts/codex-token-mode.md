# Codex Token Mode

Use this mode for AIDE queue implementation work after Q09.

## Rules

- Start from the compact task packet when available.
- Use repo references, repo-map/test-map/context-index refs, and exact paths instead of restating long project history.
- Prefer exact line refs such as `path#Lstart-Lend` when details are load-bearing.
- Do not paste full prior chat transcripts.
- Do not paste whole repo snapshots or repeated roadmap dumps.
- Paste full file contents only when exact contents are required and a file reference is insufficient.
- Emit deltas and concise evidence instead of narrative transcripts.
- Run proportionate validation before reporting completion.
- Write task-local evidence for substantial work.
- Run `py -3 .aide/scripts/aide_lite.py index` and `context` when context artifacts are stale or absent.
- Commit coherent subdeliverables with verbose commit bodies.
- Stop at review gates and blockers.

## Output Discipline

Final reports must include status, changed files, validation, evidence, risks, and next recommended phase.
