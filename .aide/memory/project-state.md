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

## Current Q14 State

Q14 has implemented the first deterministic Token Ledger and Savings Report layer and is awaiting review. It adds metadata-only token records for task packets, context packets, review packets, verification reports, evidence, prompt templates, generated guidance, and named baselines. Q09-Q13 remain review-ready prerequisites, and Q14 stops at its review gate.

## Deferred Surfaces

Gateway, providers, local model setup, model routing, cache boundary, Runtime, Service, Commander, Mobile, IDE host implementation, MCP/A2A, cloud/team mode, vector DB, semantic cache, autonomous maintenance, and real Dominium output remain deferred until reviewed queue items authorize them.

## Next Queue Path

After Q14 review, the recommended next work is Q15 Golden Tasks v0, using `.aide/context/latest-task-packet.md`, `.aide/context/latest-review-packet.md`, `.aide/reports/token-savings-summary.md`, `.aide/reports/token-ledger.jsonl`, and `.aide/verification/latest-verification-report.md` instead of a long chat-history prompt.

## Validation Baseline

Before Q09 edits, `py -3 scripts/aide validate`, `doctor`, and `self-check` passed with warnings only. Harness tests passed 10/10 and Compatibility tests passed 5/5. The warnings were review-gate nuance and generated manifest drift before Q09 refreshed the manifest through the reviewed Harness path.

## Token-Survival Rule

Future implementation prompts should cite repo refs, repo-map/test-map/context-index refs, compact task packets, verifier reports, review packets, token-ledger summaries, evidence packets, and exact line refs. Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, raw prompts/responses, or full files unless exact contents are required for the task.
