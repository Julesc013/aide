# AIDE Compact Project State

Maximum target length: 1200 approximate tokens under `.aide/policies/token-budget.yaml`.

## Current Repo Phase

AIDE is in a self-hosting reboot and remains pre-product. The accepted first shipped foundation is Contract/Profile v0, Harness v0, Compatibility baseline records, the AIDE-side Dominium Bridge baseline, and report-first self-hosting automation.

## Accepted Queue State Through Q08

- Q04 Harness v0 passed with notes.
- Q05 generated artifacts v0 is implemented; raw status remains `needs_review`, while review evidence records `PASS_WITH_NOTES` and allowed later dependency use.
- Q06 Compatibility baseline is implemented; raw status remains `needs_review`, while review evidence records `PASS_WITH_NOTES`.
- Q07 Dominium Bridge baseline passed with notes.
- Q08 self-hosting automation passed with notes.
- Q00-Q03 raw statuses remain `needs_review`; this nuance is visible and must not be silently flattened.

## Current Q16 State

Q16 is implementing the first advisory Outcome Controller v0 and will stop at `needs_review`. Q15 has implemented deterministic local golden tasks and awaits review. Q16 adds controller policy, failure taxonomy, outcome ledger records, `outcome add/report`, `optimize suggest`, local signal readers, and advisory recommendations. It does not apply recommendations automatically.

## Deferred Surfaces

Gateway, providers, local model setup, model routing, cache boundary, Runtime, Service, Commander, Mobile, IDE host implementation, MCP/A2A, cloud/team mode, vector DB, semantic cache, autonomous maintenance, and real Dominium output remain deferred until reviewed queue items authorize them.

## Next Queue Path

After Q16 review, the recommended next work is Q17 Router Profile v0, using `.aide/controller/latest-recommendations.md`, `.aide/controller/latest-outcome-report.md`, `.aide/context/latest-task-packet.md`, `.aide/context/latest-review-packet.md`, `.aide/evals/runs/latest-golden-tasks.md`, `.aide/reports/token-savings-summary.md`, `.aide/reports/token-ledger.jsonl`, and `.aide/verification/latest-verification-report.md` instead of a long chat-history prompt.

## Validation Baseline

Before Q09 edits, `py -3 scripts/aide validate`, `doctor`, and `self-check` passed with warnings only. Harness tests passed 10/10 and Compatibility tests passed 5/5. The warnings were review-gate nuance and generated manifest drift before Q09 refreshed the manifest through the reviewed Harness path.

## Token-Survival Rule

Future implementation prompts should cite repo refs, repo-map/test-map/context-index refs, compact task packets, verifier reports, review packets, token-ledger summaries, golden-task reports, outcome-controller recommendations, evidence packets, and exact line refs. Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, raw prompts/responses, or full files unless exact contents are required for the task. Token reduction is invalid if Q15 golden tasks fail, and Q16 recommendations are advisory until a future queue item or explicit human approval implements them.
