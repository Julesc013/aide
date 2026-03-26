# Shared Versus Host Boundary

## Boundary principles

- Put reusable product behavior in `shared/`.
- Keep host adapters thin and explicit.
- Do not let host-specific UI, packaging, or runtime quirks leak into shared modules unless they can be expressed as stable contract data.
- Prefer stable shared contracts over duplicated lane-specific business logic.

## What belongs in shared logic

The following belong in `shared/` because they can be defended as cross-host:

- request and response envelopes
- capability reporting and feature eligibility logic
- feature manifests and requirement checks
- settings normalization and precedence evaluation
- diagnostics generation and normalization
- transforms that act on abstract document, selection, workspace, or artifact inputs
- transport-agnostic orchestration for `embedded`, `cli-bridge`, and `local-service`

## What stays host-specific

The following remain outside the shared core:

- IDE menus, tool windows, command registration, and host UI wiring
- packaging, installation, signing, notarization, marketplace, or archive shape
- host-specific runtime bootstrapping and lifecycle glue
- host-only policy exceptions that cannot be generalized without weakening the contract
- direct bindings to IDE SDK objects that do not have a stable cross-host representation

## Practical examples

- Shared: a feature that takes a document context, selection range, settings snapshot, and feature arguments, then returns text edits and diagnostics.
- Host-specific: a Visual Studio command handler, an Xcode containing-app extension entry point, or a CodeWarrior automation bootstrapper.
- Shared: capability negotiation that decides whether a lane can attempt `project-awareness`.
- Host-specific: translating a particular IDE project model into the shared workspace-context shape.

## Leakage rules

- If logic depends on one host's UI object model, it does not belong in `shared/`.
- If logic can be expressed in terms of stable request, response, feature, settings, or diagnostics contracts, it should move toward `shared/`.
- Shared modules may accept host identity and lane metadata as inputs, but they must not import host-lane policy directly.
- Host adapters may perform local preflight and data extraction, but they should avoid embedding feature semantics that the shared core can own.

## Deciding where new logic belongs

Place new logic in `shared/` when all of these are true:

- it applies to more than one host family or execution mode
- it can be described without host-specific UI or packaging details
- it fits the stable request and response model

Keep logic in a host lane when any of these are true:

- it binds directly to host-specific SDK objects or lifecycle hooks
- it exists only to satisfy one host's packaging, bootstrapping, or UI rules
- it cannot yet be generalized without inventing abstractions the research corpus does not justify
