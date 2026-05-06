# Q20 Provider Safety Boundary

## No Live Calls

Q20 performs no:

- provider calls
- model calls
- outbound network calls
- provider probe calls
- Gateway forwarding
- OpenAI-compatible forwarding
- Anthropic-compatible forwarding
- local model setup or downloads

`provider probe --offline` is metadata-only. It does not test credentials,
pricing, account status, provider availability, or model availability.

## Credential Boundary

- No credentials are committed.
- Provider catalog records only whether credentials would be required later.
- Future credential references must live under gitignored `.aide.local/`.
- `.aide.local/` remains ignored and untracked.
- `.env`, `secrets/**`, provider keys, API keys, and local traces remain forbidden.

## Prompt And Response Storage

- raw_prompt_storage: false
- raw_response_storage: false
- no raw prompts are stored in provider status
- no raw responses are stored in provider status
- no provider response cache exists

## Gateway Boundary

Gateway status may include provider adapter readiness as local metadata. Gateway
does not forward provider requests, expose model endpoints, or accept raw
provider prompts in Q20.

## Router Boundary

Router decisions may mention provider family candidates as advisory metadata.
They do not execute routes, call adapters, call providers, or bypass verifier,
golden tasks, cache/local-state policy, hard floors, or review gates.

## Future Work Gate

Live provider work requires future reviewed queue items for credentials,
offline/online probes, provider adapters, Gateway forwarding, provider response
cache policy, billing/usage accounting, and exact capability validation.
