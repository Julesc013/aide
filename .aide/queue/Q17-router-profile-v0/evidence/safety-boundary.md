# Q17 Safety Boundary

## Advisory Only

Q17 route decisions are advice, not execution. They may be used by future queue
items to justify a work-unit route class, but they do not run tools beyond local
deterministic AIDE Lite commands and do not apply themselves automatically.

## Explicitly Not Implemented

- provider calls
- model calls
- network calls
- Gateway or proxy behavior
- Runtime, Service, Commander, UI, Mobile, MCP/A2A, host, or app-surface work
- local model setup, downloads, probes, or live availability checks
- provider billing integration or pricing claims
- exact tokenizer dependency
- automatic route execution
- automatic prompt, policy, or route mutation
- self-modifying optimizer behavior
- autonomous loops

## Hard-Floor Safety

Hard-floor task classes cannot be demoted by routing heuristics:

- architecture decisions
- security review
- self-modification
- final promotion review
- governance policy change
- irreversible or destructive change
- high-stakes review

When a hard floor applies, Q17 routes conservatively to `frontier`,
`human_review`, or a blocked-style repair path depending on available signals.

## Data Safety

- Route artifacts store metadata only.
- Raw prompts and raw responses are not stored.
- Provider keys and credentials are forbidden.
- Ignored/local paths such as `.git/**`, `.env`, `secrets/**`, and
  `.aide.local/**` remain excluded.
- Provider families in `.aide/models/providers.yaml` are advisory metadata with
  `live_calls_allowed_in_q17: false`.

## Review Gate

Q17 stops at `needs_review`. It does not authorize Q18 implementation, Gateway
work, live routing, or provider execution. Future phases must use queue packets,
validation, evidence, and review gates before acting on route recommendations.
