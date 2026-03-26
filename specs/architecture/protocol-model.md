# Protocol Model

## Purpose

The protocol model defines the transport-agnostic envelopes used between host adapters and the shared core.

## Request envelope

A request envelope carries:

- stable request id
- protocol version marker
- execution mode
- host identity and host context
- document, workspace, and selection context where available
- requested feature id
- arguments or options

The request shape must allow partial context because not every lane can provide every object at every capability level.

## Response envelope

A response envelope carries:

- the originating request id
- status
- diagnostics
- edits
- actions
- artifacts
- follow-up requirements or notes

## Output categories

- edits: direct content or structured change intents
- actions: host-visible next steps such as open, reveal, prompt, or rerun requests
- artifacts: generated files, reports, or payload blobs that the adapter may persist or present

## Error handling posture

The protocol should prefer explicit structured failure over transport-specific exceptions leaking through the contract.

Responses should therefore be able to represent:

- success
- partial success
- rejected request
- failed execution
- deferred or unavailable result

## Transport-agnostic rule

The same request and response semantics must survive `embedded`, `cli-bridge`, and `local-service`.

No execution mode may introduce a private response shape that bypasses the shared contract.

## Stability rule

Protocol changes are architecture changes. They should be versioned, explicit, and justified in later prompts rather than drifting through implementation shortcuts.
