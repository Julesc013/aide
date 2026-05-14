# Q47 ExecPlan: AIDE Lite Release Bundle v0

## Objective

Create deterministic local release-bundle generation for the portable
`aide-lite-pack-v0` export pack. The bundle must be inspectable, checksummed,
fixture-validated, documented, evidenced, and explicitly not published.

## Scope

- Add Q47 release bundle, artifact, provenance, validation, and versioning
  policies.
- Add `.aide/release` schemas and local generated release outputs.
- Extend AIDE Lite with `release bundle`, `validate`, `status`, `assets`,
  `manifest`, `checksums`, `provenance`, and `clean --dry-run`.
- Add archive generation and extraction/checksum validation using Python
  standard library only.
- Add release golden tasks, unit tests, docs, export-pack support, and evidence.

## Boundaries

- No Git tags.
- No GitHub Releases.
- No uploads or package publishing.
- No branch mutation.
- No target repository mutation.
- No install, repair, upgrade, rollback, or uninstall apply mode.
- No provider, model, or network calls.
- No active CI or GitHub setting mutation.

## Milestones

1. Completed: baseline repo and Q46 dependency inspection.
2. Completed: queue packet foundation.
3. Completed: release policies and schemas.
4. Completed: AIDE Lite command implementation.
5. Completed: unit tests and golden tasks.
6. Completed: documentation and export-pack sync.
7. Completed: bundle generation, validation, evidence, and review gate.

## Decisions And Findings

- Q46 is present and `needs_review`, which is the expected review-gated state
  for this sequence.
- Local `main` is ahead of `origin/main` by two commits before Q47; Q47 does
  not push, fetch, merge, tag, or mutate branch state.
- Q47 artifacts will live under `.aide/release/dist/`; top-level `dist/` is not
  used unless a later policy explicitly requests it.
- Binary archives are generated under `.aide/release/dist/` and are committed
  with their manifest, checksums, provenance, validation, and asset index because
  current repo policy leaves those Q47 local release outputs trackable.
- Initial release archive validation caught an exported example path under
  `.aide.local.example/secrets/`; Q47 now filters release archives against the
  local release forbidden-path policy while leaving the source export pack
  intact.
- `release_no_publish_golden` was tightened so it verifies absence of publishing
  primitives without failing on policy text that documents the prohibited
  boundary.

## Verification Intent

Run the Q47 release command family, export-pack and pack-status, AIDE Lite
validation/test/selftest/eval surfaces, lifecycle validations, targeted unit
tests, core unittest suites where present, checksum/extraction validation, diff
checks, and secret scans. Record inherited warnings and slow or timed-out suites
honestly.

## Exit Criteria

Q47 status is `needs_review`; release policies and schemas exist; local `.zip`
and `.tar.gz` archives, checksums, manifest, install notes, provenance,
validation, and asset index exist; archives extract with required files and no
forbidden paths; checksums validate; export pack includes portable release
support but excludes generated release outputs as target truth; evidence is
complete; and no publication or target mutation occurs.
