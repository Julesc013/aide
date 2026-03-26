# Settings Model

## Purpose

The settings model defines how shared defaults, host-specific overrides, and feature-specific adjustments are represented without tying configuration to one execution mode or host runtime.

## Settings layers

- shared settings: cross-host defaults owned by the shared core
- host overrides: lane-specific adjustments keyed by family, technology, or execution mode
- feature overrides: feature-specific toggles or parameter overrides
- request-level options: per-invocation adjustments supplied by the host adapter

## Stable keys

- settings keys should be stable, lowercase, and namespaced
- keys should describe behavior, not one host's UI wording

Examples:

- `editor.max-selection-bytes`
- `diagnostics.include-evidence`
- `service.request-timeout-ms`

## Precedence posture

At a high level, precedence should run from broadest to most specific:

1. shared defaults
2. host or lane overrides
3. feature overrides
4. request-level options

The model should remain explicit about where an override came from so diagnostics and later debugging stay reconstructable.

## Shared versus host settings

Settings belong in the shared model when they alter reusable feature behavior or protocol behavior.

Settings remain host-specific when they exist only to wire a host UI, packaging rule, installation location, or runtime bootstrap detail that the shared core should not own.

## Cross-mode requirement

Settings must be representable across `embedded`, `cli-bridge`, and `local-service`.

That means:

- no mode may depend on opaque in-memory-only configuration
- settings resolution must be serializable into request payloads where needed
- host overrides must be expressible as stable data, not hidden adapter code
