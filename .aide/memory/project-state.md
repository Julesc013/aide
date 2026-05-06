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

## Current Q15 State

Q15 is implementing the first deterministic Golden Tasks v0 quality gate and will stop at `needs_review`. Q14 has implemented metadata-only token ledger and savings reporting and awaits review. Q15 adds repo-local eval policy, golden task catalog, `eval list/run/report`, and deterministic reports so token-saving workflow changes must preserve required packet, verifier, review, ledger, and adapter behavior.

## Deferred Surfaces

Gateway, providers, local model setup, model routing, cache boundary, Runtime, Service, Commander, Mobile, IDE host implementation, MCP/A2A, cloud/team mode, vector DB, semantic cache, autonomous maintenance, and real Dominium output remain deferred until reviewed queue items authorize them.

## Next Queue Path

After Q15 review, the recommended next work is Q16 Outcome Controller v0, using `.aide/context/latest-task-packet.md`, `.aide/context/latest-review-packet.md`, `.aide/evals/runs/latest-golden-tasks.md`, `.aide/reports/token-savings-summary.md`, `.aide/reports/token-ledger.jsonl`, and `.aide/verification/latest-verification-report.md` instead of a long chat-history prompt.

## Validation Baseline

Before Q09 edits, `py -3 scripts/aide validate`, `doctor`, and `self-check` passed with warnings only. Harness tests passed 10/10 and Compatibility tests passed 5/5. The warnings were review-gate nuance and generated manifest drift before Q09 refreshed the manifest through the reviewed Harness path.

## Token-Survival Rule

Future implementation prompts should cite repo refs, repo-map/test-map/context-index refs, compact task packets, verifier reports, review packets, token-ledger summaries, golden-task reports, evidence packets, and exact line refs. Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, raw prompts/responses, or full files unless exact contents are required for the task. Token reduction is invalid if Q15 golden tasks fail.
