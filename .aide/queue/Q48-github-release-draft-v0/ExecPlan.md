# Q48 ExecPlan: GitHub Release Draft v0

## Objective

Create deterministic local GitHub Release draft generation for the Q47 AIDE
Lite release bundle. The output must be reviewable, asset-backed,
checksum-backed, checklist-backed, and explicitly unpublished.

## Scope

- Add Q48 GitHub release draft, publication-boundary, upload-plan, and
  checklist policies.
- Add `.aide/release/github-release-*.schema.json` draft schemas.
- Extend AIDE Lite with `release draft`, `draft-validate`, `draft-status`,
  `upload-plan`, `checklist`, and `publication-boundary`.
- Generate local Markdown/JSON release draft artifacts from Q47 bundle files.
- Add golden tasks, tests, docs, export-pack support, and evidence.

## Boundaries

- No Git tags or tag pushes.
- No GitHub Releases.
- No upload or package publishing.
- No GitHub API or network calls.
- No branch mutation.
- No target repository mutation.
- No install, repair, upgrade, rollback, or uninstall apply mode.
- No provider or model calls.

## Milestones

1. Completed: baseline repo, Q47, and release-bundle artifacts inspected.
2. In progress: queue packet foundation.
3. Pending: release draft policies and schemas.
4. Pending: AIDE Lite command implementation.
5. Pending: unit tests and golden tasks.
6. Pending: documentation and export-pack sync.
7. Pending: draft generation, validation, evidence, and review gate.

## Decisions And Findings

- Q47 is present and `needs_review`, with local bundle validation passing and
  publication actions recorded as false.
- The Q47 bundle is local preview material; Q48 will draft from it without
  treating the draft as a published release.
- Suggested tags are suggestions only and must not be created by Q48.
- If no stable SemVer contract exists, Q48 uses the draft tag shape
  `aide-lite-pack-v0-draft-<short-sha>`.

## Verification Intent

Run the Q48 release draft command family, Q47 release validation, export-pack
and pack-status, AIDE Lite validation/test/selftest/eval surfaces, lifecycle
validations, targeted unit tests, core unittest suites where present, diff
checks, and secret scans. Record inherited warnings honestly.

## Exit Criteria

Q48 status is `needs_review`; release draft policies and schemas exist; local
draft Markdown/JSON, asset list, upload plan, checklist, publication boundary,
and draft validation outputs exist; assets have checksums; no publication,
tagging, upload, network/API call, branch mutation, CI install, target mutation,
or apply action occurs; export pack includes portable release-draft support but
excludes generated draft outputs as target truth; and evidence is complete.
