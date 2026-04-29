# Harness Charter

## Purpose

Harness owns deterministic validation, fixtures, queue checks, evidence capture, and repeatable proof execution for AIDE Core work.

## Owned Responsibilities

- Keep validation commands explicit and reproducible.
- Detect generated-file drift when later queue items introduce generated outputs.
- Record evidence close to the queue item or proof lane that produced it.
- Provide lightweight checks before heavier native or host tests are considered.

## Non-goals

- Harness is not a product runtime.
- Harness does not bypass review gates.
- Q01 does not create Harness v0; that remains Q04 scope.

## Boundaries

- Harness verifies Contract and Compatibility evidence but does not redefine them.
- Harness may use existing bootstrap-era fixtures and eval records as evidence.
- Harness must not silently run heavy native tests or modify repo state unless a queue item allows it.

## Relation To AIDE Core / Hosts / Bridges

Harness is an internal AIDE Core domain. It validates Core records and bridge or host proof boundaries without turning AIDE Hosts into sources of durable semantics.

## Current Status

Current status: partial. Bootstrap-era tests, fixtures, eval records, and queue helper scripts exist. Reboot Harness v0 is planned for Q04.
