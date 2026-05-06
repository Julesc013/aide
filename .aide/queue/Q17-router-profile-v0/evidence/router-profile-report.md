# Q17 Router Profile Report

## Summary

Q17 adds the first deterministic AIDE Router Profile. It is a repo-local
advisory contract and reporting layer that reads compact task/context packets
plus token, verifier, review, golden-task, and outcome signals, then explains
which route class is justified before any model or provider tokens are spent.

## Routing Policy

- Policy path: `.aide/policies/routing.yaml`
- Operating mode: `advisory_only`
- Routing unit: work unit or compact task packet, not raw prompt vibes
- Route classes: `no_model_tool`, `local_small`, `local_strong`,
  `cheap_remote`, `frontier`, `human_review`, `blocked`
- Quality gates: verifier for checkable work, golden tasks for token
  optimization, evidence packets for review, and token budgets for prompt
  surfaces
- Forbidden behaviors: provider calls, model calls, network calls, automatic
  execution, automatic policy mutation, and review-gate bypass

## Model And Provider Metadata

Q17 adds advisory metadata only under `.aide/models/`:

- `.aide/models/providers.yaml`: provider families such as deterministic tools,
  human review, local model families, remote provider families, and aggregators
  with `live_calls_allowed_in_q17: false`
- `.aide/models/capabilities.yaml`: capability dimensions without verified live
  provider claims
- `.aide/models/routes.yaml`: task-class route profiles and escalation
  conditions
- `.aide/models/hard-floors.yaml`: non-demotable minimum routes for
  architecture, security, self-modification, final promotion, governance,
  destructive, and high-stakes review work
- `.aide/models/fallback.yaml`: fallback behavior when signals are missing or
  quality gates fail

No API keys, provider credentials, live endpoints with secrets, current pricing
claims, downloads, or availability probes were added.

## AIDE Lite Commands

Q17 extends `.aide/scripts/aide_lite.py` with:

- `route list`
- `route validate`
- `route explain`
- `route explain --task-packet PATH`

Existing `doctor`, `validate`, `review-pack`, `selftest`, and ledger behavior
now detect or summarize route artifacts where appropriate.

## Route Decision Artifacts

- Schema: `.aide/routing/route-decision.schema.json`
- Latest JSON: `.aide/routing/latest-route-decision.json`
- Latest Markdown: `.aide/routing/latest-route-decision.md`
- Examples: `.aide/routing/examples/**`

The latest route decision is compact metadata only. It does not inline full
task prompts, source files, provider responses, secrets, or local state.

## Hard Floors

Q17 preserves hard floors for:

- architecture decisions
- security review
- self-modification
- final promotion review
- governance policy change
- irreversible or destructive change
- high-stakes review

If a hard floor applies, route heuristics cannot demote the decision to a
cheaper route class merely to save tokens.

## Limitations

- Routing is advisory only.
- Route heuristics are deterministic and conservative, not semantic model
  judgement.
- Provider capabilities are metadata contracts, not live availability claims.
- Exact pricing, exact tokenization, provider billing, Gateway execution,
  local-model setup, and cache/local-state boundaries remain deferred.
