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
- Run `py -3 .aide/scripts/aide_lite.py verify` before claiming substantial queue work is complete when Q12 verifier behavior is available.
- Run `py -3 .aide/scripts/aide_lite.py review-pack` before premium-model review when Q13 review workflow behavior is available.
- Run `py -3 .aide/scripts/aide_lite.py ledger scan`, `ledger report`, and relevant `ledger compare` commands when Q14 token-ledger behavior is available.
- Run `py -3 .aide/scripts/aide_lite.py eval run` when Q15 golden-task behavior is available and the work touches token-saving, context, verifier, review, ledger, adapter, or eval surfaces.
- Run `py -3 .aide/scripts/aide_lite.py outcome report` and `optimize suggest` when Q16 outcome-controller behavior is available.
- Treat controller recommendations as advisory only; do not mutate prompts, policies, routing, or context artifacts automatically.
- Implement controller recommendations only through a future queue item or explicit human approval, and rerun golden tasks before promotion.
- Do not store raw prompts or raw responses in committed ledger records.
- Treat token reduction as invalid if golden tasks fail.
- Treat token savings as invalid if quality evidence, validation, provenance, or review gates are weakened.
- Write task-local evidence for substantial work.
- Run `py -3 .aide/scripts/aide_lite.py index` and `context` when context artifacts are stale or absent.
- Commit coherent subdeliverables with verbose commit bodies.
- Stop at review gates and blockers.

## Output Discipline

Final reports must include status, changed files, validation, verifier result when available, review packet path when available, token ledger result when available, golden task result when available, outcome-controller recommendation status when available, evidence, risks, and next recommended phase.
