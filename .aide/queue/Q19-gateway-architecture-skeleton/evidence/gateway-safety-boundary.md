# Q19 Gateway Safety Boundary

## Enforced Boundary

- Provider calls: none.
- Model calls: none.
- Outbound network calls: none.
- Real Gateway proxy forwarding: not implemented.
- OpenAI-compatible forwarding: not implemented.
- Anthropic-compatible forwarding: not implemented.
- Raw prompt logging/storage: disabled.
- Raw response logging/storage: disabled.
- Actual `.aide.local/` contents: not committed.
- Local server binding: localhost-only when `gateway serve` is explicitly run.
- Route decisions: advisory only.

## Local State

Q19 respects Q18: committed Gateway state is deterministic metadata/docs under
`.aide/` and machine-local runtime state belongs under gitignored
`.aide.local/`.

## Review Gate

Q20 Provider Adapter v0 must not treat Q19 as permission for live provider calls
or provider forwarding. Provider work must remain queue-gated, must respect
`.aide.local/`, and must preserve verifier, golden-task, route, cache, and
review-gate safeguards.
