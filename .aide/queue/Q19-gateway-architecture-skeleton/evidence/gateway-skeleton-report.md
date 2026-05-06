# Q19 Gateway Skeleton Report

## Summary

Q19 adds a local/report-only Gateway skeleton. It exposes existing repo-local
AIDE evidence and advisory route metadata through compact health, status, route,
summaries, and version surfaces without provider calls, model calls, outbound
network calls, or proxy forwarding.

## Policy and Architecture

- Gateway policy: `.aide/policies/gateway.yaml`
- Architecture: `.aide/gateway/architecture.md`
- Endpoint policy: `.aide/gateway/endpoints.yaml`
- Lifecycle: `.aide/gateway/lifecycle.yaml`
- Security boundary: `.aide/gateway/security-boundary.md`

The policy declares `local_skeleton`, `report_only`, and
`no_provider_forwarding` operating modes. Future OpenAI-compatible,
Anthropic-compatible, provider-adapter, local-model-adapter, MCP, and Gateway
cache targets are documented as future targets only.

## Core Skeleton

- `core/gateway/gateway_status.py` reads committed repo-local artifacts and
  returns compact status dictionaries.
- `core/gateway/server.py` provides a stdlib `http.server` skeleton that binds
  only to localhost by default.
- Endpoint payloads are testable in-process without starting a daemon.

## AIDE Lite Commands

- `py -3 .aide/scripts/aide_lite.py gateway status`
- `py -3 .aide/scripts/aide_lite.py gateway endpoints`
- `py -3 .aide/scripts/aide_lite.py gateway smoke`
- `py -3 .aide/scripts/aide_lite.py gateway serve --host 127.0.0.1 --port 8765`

`gateway serve` is optional foreground behavior; Q19 does not auto-start or
daemonize the server.

## Status Artifacts

- JSON: `.aide/gateway/latest-gateway-status.json`
- Markdown: `.aide/gateway/latest-gateway-status.md`

The latest status reports show provider calls disabled, model calls disabled,
outbound network disabled, raw prompt storage disabled, and raw response storage
disabled.

## Limitations

Q19 is not a production Gateway. It has no authentication, authorization,
provider adapters, provider billing, OpenAI/Anthropic-compatible forwarding,
Runtime worker, service manager, live route execution, exact tokenizer, or live
cache.
