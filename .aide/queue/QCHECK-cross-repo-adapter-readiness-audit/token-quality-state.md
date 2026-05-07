# Token And Quality State

## Method

All token counts are chars / 4 approximate tokens, rounded up where evidence
does so. They are not exact tokenizer counts, hidden reasoning-token counts,
cached-token discounts, or provider billing records.

## Token Evidence

| Repo / Surface | Chars | Approx Tokens | Baseline Approx Tokens | Estimated Reduction |
| --- | ---: | ---: | ---: | ---: |
| AIDE task packet | 3,716 | 929 | 65,250 | 98.6% |
| AIDE context packet | 1,943 | 486 | 69,706 | 99.3% |
| AIDE review packet | 6,639 | 1,660 | 7,015 | 76.3% |
| Eureka task packet | 3,792 | 948 | 68,647 | 98.6% |
| Eureka review packet | 4,208 | 1,052 | not measured | n/a |
| Dominium task packet | 4,347 | 1,087 | 110,115 | 99.0% |
| Dominium review packet | 5,125 | 1,282 | not measured | n/a |

Adapter previews are not compared to a baseline because they are guidance
outputs, not task packets. They range from 241 to 332 approximate tokens each.

## Quality Gates Present

- Mechanical verifier.
- Review packet generation.
- Token ledger and budget warnings.
- Six AIDE substrate golden tasks.
- Evidence packets in queue items.
- Route hard floors and no-call route explanation.
- Cache/local-state metadata boundary.
- Gateway smoke test for no-call endpoints.
- Provider metadata validation.
- Adapter validation and drift checks.
- Target-pilot validation evidence in Eureka and Dominium.

## Claims AIDE Can Make Now

Supported:

- AIDE reduces compact task-packet size versus documented naive baselines.
- AIDE preserves required packet structure for task handoff.
- AIDE avoids copying source repo queue/history/generated state into target
  repos when imported carefully.
- AIDE Lite validation is reliable in the source repo.
- Adapter guidance is concise and non-destructive.

Partially supported:

- AIDE preserves quality gates for substrate behavior.
- AIDE helps doctrine-heavy repos avoid context bloat while preserving refs.

Not yet supported:

- Exact provider billing reduction.
- Exact tokenizer reduction.
- Arbitrary coding-quality preservation.
- Live GPT/provider review quality.
- Existing-tool obedience to generated adapter guidance.

## Quality Risks

- Eureka and Dominium target-specific golden tasks are absent.
- Target pilot review gates remain open.
- Q21 importer direct apply is broader than real target prompt scopes.
- Stale profile/self-check guidance can cause future agents to re-litigate old
  phases.
- Dirty export-pack provenance weakens handover trust.
