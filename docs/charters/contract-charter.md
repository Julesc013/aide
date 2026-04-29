# Contract Charter

## Purpose

Contract defines reviewable AIDE Core shapes: profiles, schemas, capabilities, requests, responses, diagnostics, generated-artifact rules, and architecture constraints.

## Owned Responsibilities

- Define stable contract records before implementation depends on them.
- Distinguish implemented contract reality from future intent.
- Preserve mappings to bootstrap-era `specs/**` and `shared/schemas/**`.
- Provide inputs for Harness validation and Compatibility claims.

## Non-goals

- Contract does not execute work.
- Contract does not package products or invoke models.
- Q01 does not create the Q03 profile contract v0 implementation.

## Boundaries

- Contract records should be deterministic and reviewable.
- Harness verifies contracts; it does not own their durable semantics.
- Hosts consume contracts through shells and adapters; they do not own durable semantics.

## Relation To AIDE Core / Hosts / Bridges

Contract is an internal AIDE Core domain. AIDE Hosts and AIDE Bridges must conform to Contract records when later queue items implement them.

## Current Status

Current status: partial. Bootstrap-era specs and schemas exist. Q03 is expected to create the first reboot profile contract v0; Q01 only documents the charter.
