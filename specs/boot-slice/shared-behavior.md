# Shared Behavior

## Purpose

This document defines what the future shared core must do for the first boot slice without leaking host-specific logic into shared modules.

## Shared Request Expectations

### `boot.slice.invoke`

The request must provide:

- canonical host family and technology ids
- support mode
- execution mode
- host version id when available
- requested feature id `boot.slice.invoke`

The request may omit document or workspace context.

### `boot.slice.editor-marker`

The request must provide:

- everything required by `boot.slice.invoke`
- `selection_context.active_text`

If `selection_context.active_text` is missing, the shared core must not infer it. The request remains valid, but the response must report the feature unavailable or deferred.

## Shared Response Expectations

Every boot-slice response must preserve the request id and include:

- response status
- diagnostics list
- capability report or equivalent capability artifact
- boot-slice report artifact or equivalent structured output
- explicit unavailable reasons when a requested behavior cannot be completed

For `boot.slice.editor-marker`, the response may also include:

- one deterministic edit
- one deterministic edit preview artifact

## Expected Diagnostics

The boot slice should be able to surface at least these shared diagnostic patterns:

- `capability.unavailable`
- `context.missing-active-text`
- `lane.blocked`
- `lane.deferred`

Exact ids can be refined later, but the meaning must remain stable.

## Capability-Report Expectations

The boot-slice capability report must identify:

- host family
- technology lane
- support mode
- execution mode
- current capability
- target capability
- available boot-slice behaviors
- unavailable boot-slice behaviors with reasons

## Behavior Invariants

The shared core must keep these invariants across all lanes:

- `boot.slice.invoke` always means identify, report, and surface unavailable reasons honestly
- `boot.slice.editor-marker` always means prefix `selection_context.active_text` with `AIDE_BOOT: `
- missing context never becomes guessed context
- blocked and deferred states remain explicit
- transport differences do not change feature meaning

## What Must Remain Host-Agnostic

The shared core may define:

- feature ids
- deterministic transform rules
- report shape
- diagnostics semantics
- capability-negotiation logic

The shared core must not define:

- IDE menu placement
- host package metadata
- host-specific UI text
- host runtime lifecycle quirks
- host-specific fallback rules that cannot be generalized
