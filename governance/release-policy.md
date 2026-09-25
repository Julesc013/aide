# AIDE Release Policy

## Current Phase

The repository has implemented and integrated AIDE Lite source, but has not
qualified or published a stable AIDE release. `dev` is integration progress;
`main` and an immutable release tag require separate exact review and evidence.
The first stable Lite profile is a bounded Windows local CLI and portable-pack
contract target, not a whole-product readiness claim.

## Phase Gate

- Continue implementation through bounded queue WorkUnits and the applicable
  independent technical gates. A contract or local preview does not qualify
  release behavior.
- Stable publication requires a reviewed public compatibility and version
  rule, exact supported profile, final source and asset identity, mandatory
  behavioral/consumer evidence, and a separate release-effect review.
- Host, native, hosted, model-enabled, and non-Windows lifecycle apply claims
  require their own evidence; they are not inherited from Lite qualification.

## Release Naming Rule

- Release artifacts may contain exact version names, release channels, or target identifiers when that makes the deliverable precise.
- This does not change the source naming law: source directories remain based on compatibility technology or host contract rather than exact versions.

## Historical Phase Order

The bootstrap plan ordered work as follows; this list is historical context,
not a current release gate or a claim that every phase is complete:

1. inventory
2. matrix
3. scaffold
4. harness
5. shared core
6. adapters
7. environments
8. evals
9. packaging

## Governance Rule

- Governance and release policy are binding during this phase.
- No release artifact should imply broad compatibility before inventory, matrices, evals, and packaging evidence exist.
- Q47/Q48 local bundles and drafts remain preview-only, no-publish evidence.
  A later frozen release-effect WorkUnit must verify the published bytes and
  downloaded consumers before a stable claim is complete.
