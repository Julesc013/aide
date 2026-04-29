# ADR-0004: Profile And Harness Are Distinct

## Status

accepted

## Context

The reboot needs profiles to describe expected behavior and Harness checks to verify behavior. Conflating them would make validation records hard to review.

## Decision

Treat Profile and Harness as distinct concepts. A profile belongs to Contract; the Harness validates profile conformance and records evidence.

## Consequences

- Q03 can define profile contract v0 without building Harness v0.
- Q04 can add Harness v0 checks without redefining the profile.
- Evidence can show whether behavior satisfies the profile rather than becoming the profile itself.

## Supersedes / Superseded By

Supersedes: none. Superseded by: none.
