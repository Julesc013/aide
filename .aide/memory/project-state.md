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

## Current Q20 State

Q20 is implementing the first offline Provider Adapter v0 layer and will stop at `needs_review`. Q19 has implemented the local/report-only Gateway skeleton and awaits review. Q20 adds `.aide/policies/provider-adapters.yaml`, `.aide/providers/**` provider catalog/capability/contract/status artifacts, `core/providers/**` stdlib metadata helpers, and `provider list/status/validate/contract/probe --offline` AIDE Lite behavior. It is metadata-only and does not create live provider calls, model calls, network probes, credentials, Gateway forwarding, Runtime, UI, or raw prompt/response logging.

## Deferred Surfaces

Live provider adapters, credential setup, local model setup, live model routing, real Gateway proxy forwarding, Runtime, Service, Commander, Mobile, IDE host implementation, MCP/A2A, cloud/team mode, vector DB, semantic cache, provider response cache, autonomous maintenance, and real Dominium output remain deferred until reviewed queue items authorize them.

## Next Queue Path

After Q20 review, the recommended next work is Q21 Existing Tool Adapter Compiler v0, using `.aide/providers/latest-provider-status.md`, `.aide/providers/latest-provider-status.json`, `.aide/gateway/latest-gateway-status.md`, `.aide/gateway/latest-gateway-status.json`, `.aide/cache/latest-cache-keys.md`, `.aide/cache/latest-cache-keys.json`, `.aide/routing/latest-route-decision.md`, `.aide/routing/latest-route-decision.json`, `.aide/controller/latest-recommendations.md`, `.aide/context/latest-task-packet.md`, `.aide/context/latest-review-packet.md`, `.aide/evals/runs/latest-golden-tasks.md`, `.aide/reports/token-savings-summary.md`, `.aide/reports/token-ledger.jsonl`, and `.aide/verification/latest-verification-report.md` instead of a long chat-history prompt.

## Validation Baseline

Before Q09 edits, `py -3 scripts/aide validate`, `doctor`, and `self-check` passed with warnings only. Harness tests passed 10/10 and Compatibility tests passed 5/5. The warnings were review-gate nuance and generated manifest drift before Q09 refreshed the manifest through the reviewed Harness path.

## Token-Survival Rule

Future implementation prompts should cite repo refs, repo-map/test-map/context-index refs, compact task packets, verifier reports, review packets, token-ledger summaries, golden-task reports, outcome-controller recommendations, route decisions, cache-key reports, Gateway status reports, provider status reports, evidence packets, and exact line refs. Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, raw prompts/responses, or full files unless exact contents are required for the task. Token reduction is invalid if Q15 golden tasks fail, Q16 recommendations are advisory, Q17 route decisions are advisory, Q18 cache keys remain metadata rather than proof that stale content is safe to reuse, Q19 Gateway status surfaces are local/report-only rather than provider forwarding, and Q20 provider metadata is offline advisory contract data rather than live provider capability proof.
