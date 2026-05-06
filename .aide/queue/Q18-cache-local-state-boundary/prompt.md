# Q18 Prompt Packet

## Phase

Q18 - Cache + Local State Boundary

## Goal

Define `.aide.local/` as the ignored local runtime-state root, add a safe
`.aide.local.example/` layout, define cache/local-state policy, implement
deterministic cache-key metadata commands, generate current cache-key reports,
and prepare the Q19 compact packet.

## Why

Future Gateway/provider/runtime work must not commit secrets, raw prompts, raw
responses, local traces, cache blobs, or machine-specific state. Q18 creates the
boundary before any live cache exists.

## Context Refs

- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-context-packet.md`
- `.aide/routing/latest-route-decision.md`
- `.aide/reports/token-savings-summary.md`
- `.aide/controller/latest-recommendations.md`
- `.aide/memory/project-state.md`
- `.aide/policies/routing.yaml`

## Allowed Paths

See `task.yaml` for the exact allowlist. Keep implementation inside Q18 cache,
local-state, AIDE Lite, test, documentation, generated packet/report, and
evidence paths.

## Forbidden Paths

Do not commit `.aide.local/**`, `.env`, `secrets/**`, provider credentials,
raw prompts, raw responses, real cache blobs, Gateway/provider/runtime/UI work,
network calls, model calls, or external provider calls.

## Acceptance

Q18 is review-ready when `.gitignore`, `.aide.local.example/**`, cache and
local-state policies, `.aide/cache/**`, AIDE Lite cache commands, cache tests,
latest cache-key reports, latest Q19 task packet, docs, and evidence exist and
validation is recorded.
