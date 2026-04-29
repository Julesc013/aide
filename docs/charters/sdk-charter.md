# SDK Charter

## Purpose

SDK is the future AIDE Core domain for authored integration surfaces, extension-facing helpers, and stable developer contracts.

## Owned Responsibilities

- Provide future developer-facing APIs only after Contract and Harness evidence exist.
- Keep authored integrations aligned with Compatibility and Control policy.
- Avoid making host-specific shells the durable source of semantics.
- Preserve clear boundaries between SDK, Runtime, and Bridges.

## Non-goals

- SDK is not implemented by Q01.
- SDK is not an IDE extension family, provider adapter, or app surface.
- SDK does not bypass Contract or Harness review.

## Boundaries

- SDK depends on stable Contract records.
- SDK must remain distinct from Runtime execution.
- SDK must not absorb Dominium Bridge or XStack governance concerns.

## Relation To AIDE Core / Hosts / Bridges

SDK is an internal AIDE Core domain. AIDE Hosts and AIDE Bridges may eventually use SDK surfaces, but Q01 only documents the intended boundary.

## Current Status

Current status: deferred. SDK work is future queue scope after earlier Contract, Harness, Compatibility, and Bridge evidence exists.
