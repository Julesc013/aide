# Q17 Implementation Prompt

Implement Q17 Router Profile v0 as deterministic repo-local advisory routing.

## Objective

Define route classes, hard floors, model/provider metadata, route-decision
artifacts, and AIDE Lite route list/explain/validate commands so future work can
choose a no-model, local, cheap, frontier, human, or blocked route from compact
evidence before spending tokens.

## Scope

Use only Q17 allowed paths. Do not implement Gateway, provider calls, live model
calls, local model setup, Runtime, UI, MCP/A2A, autonomous loops, automatic
prompt/policy mutation, exact tokenizer, billing integration, or Q18 cache/local
state.

## Required Outputs

- Q17 queue packet and evidence.
- `.aide/policies/routing.yaml`.
- `.aide/models/**` advisory registry.
- `.aide/routing/**` docs, schema, examples, latest decision JSON/Markdown.
- AIDE Lite `route list`, `route explain`, and `route validate`.
- Tests for deterministic routing and gate-aware decisions.
- Documentation and Q18 compact task packet.

## Validation

Run the Q17 validation command set and record all pass/fail/warning results in
evidence. Q17 must stop at `needs_review`.
