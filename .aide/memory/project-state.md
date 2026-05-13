# AIDE Compact Project State

Maximum target length: 1200 approximate tokens under `.aide/policies/token-budget.yaml`.

## Current Repo Phase

AIDE is in a self-hosting reboot and remains pre-product. QFIX-03 reconciled the AIDE-local queue review blockers through Q31 and Q34 from repo-local evidence, refreshed generated artifact state, and left Q32/Q33 as target-repository prompts. The current AIDE-local next packet is Q35 GitHub Protection and CI Advisory v0.

## Accepted Queue State

- Q00 through Q08 are accepted foundation records; early phases carry notes but no active AIDE-local `needs_review` blocker.
- Q09 through Q20 are accepted token-survival, Gateway skeleton, and offline provider-metadata foundation records; live providers, model calls, Gateway forwarding, Runtime, and UI remain deferred.
- Q21, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q34, and QFIX-03 are accepted with notes as governance, export/import, branch workflow, and changelog-preparation work.
- Q32 and Q33 must run from Eureka and Dominium respectively; they are not AIDE-local execution items.

## Deferred Surfaces

Live provider adapters, credential setup, local model setup, live model routing, real Gateway proxy forwarding, Runtime, Service, Commander, Mobile, IDE host implementation, MCP/A2A, cloud/team mode, vector DB, semantic cache, provider response cache, autonomous maintenance, and real Dominium output remain deferred until reviewed queue items authorize them.

## Next Queue Path

Use `.aide/context/latest-task-packet.md` for Q35 GitHub Protection and CI Advisory v0. Q35 remains advisory and must not mutate GitHub settings, branch protection, CI, branches, tags, or releases unless a future reviewed queue item explicitly authorizes it.

## Validation Baseline

After QFIX-03, `py -3 scripts/aide validate`, `doctor`, and `self-check` report zero warnings. Generated artifact drift should be fixed with `py -3 scripts/aide compile --write` only through reviewed work.

## Token-Survival Rule

Future implementation prompts should cite repo refs, repo-map/test-map/context-index refs, compact task packets, verifier reports, review packets, token-ledger summaries, golden-task reports, outcome-controller recommendations, route decisions, cache-key reports, Gateway status reports, provider status reports, evidence packets, and exact line refs. Do not paste full prior transcripts, whole repo dumps, repeated roadmap dumps, raw prompts/responses, or full files unless exact contents are required for the task. Token reduction is invalid if Q15 golden tasks fail, Q16 recommendations are advisory, Q17 route decisions are advisory, Q18 cache keys remain metadata rather than proof that stale content is safe to reuse, Q19 Gateway status surfaces are local/report-only rather than provider forwarding, and Q20 provider metadata is offline advisory contract data rather than live provider capability proof.
