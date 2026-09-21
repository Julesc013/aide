# Unified Specification Convergence Status

## Current Boundary

AIDE's live specification tree is `specs/`. Private source archives and review
packages are custody inputs, not an alternate specification root.

Source S21, `AIDE-Unified-Specification-2026-09-20(1).zip`, is preserved under
private verified custody with SHA-256
`61236cb58baa1233c2d110b3d13a4c8a10f83362b58cc3f6bb6595c8f1aa179c`.
It must not be extracted over the repository or published as an AIDE release.

## Adopted Increments

The first convergence increment adopts and adapts three desired-state families:

- product scope and profiles;
- authority and decision provenance;
- status and outcome dimensions.

It also adds a navigable `specs/control-plane/` area while preserving every
existing architecture and boot-slice path.

The second increment adopts three connected contract families:

- WorkUnits, immutable attempts, decomposition, and continuation;
- capability bindings, invocations, receipts, and declared effects;
- logical identities, locators, revisions, lineage, and qualified digests.

Candidate `UR-*` identifiers remain attributable source aliases. Live clauses
use the `AIDE-WORK-*`, `AIDE-CAP-*`, and `AIDE-ID-*` namespaces and explicitly
preserve current queue, schema, policy, and review ownership.

## Imported Draft Coverage

The remaining 34 generated control-plane chapters are now physically present
under `specs/control-plane/` as explicit proposed drafts. The
[draft chapter index](../../specs/control-plane/draft-import.md) records their
topics and source identities, and the adjacent import manifest binds exact
source and destination bytes.

The import preserves 244 proposed `UR-*` requirement aliases and 244 matching
unrun `UC-*` acceptance designs. Those aliases are review input, not adopted
`AIDE-*` requirements or passing tests. The six adopted foundation contracts
remain byte-identical and retain precedence where scopes overlap.

## Deferred Material

- Draft clauses in recovery, compatibility, trust, lifecycle, knowledge,
  optimization, interop, experience, engineering, and runtime families still
  require separate semantic dispositions before adoption.
- Large generated requirements, decision, source-mapping, and acceptance-case
  registers remain external review inputs.
- Root-authority policy changes remain separately reviewable.
- Draft presence and candidate documentation patches are not implicit adoption.

## Maturity

Adoption means the selected text now expresses reviewed desired behavior. It
does not claim that every requirement is implemented, behaviorally qualified,
activated, supported, or released. Those facts remain owned by exact source,
tests, evidence, environment records, support matrices, and release records.
