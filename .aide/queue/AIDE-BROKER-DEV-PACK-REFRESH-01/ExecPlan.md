# ExecPlan: Post-Integration Portable Artifact Refresh

## Objective

Return `dev` to a self-consistent portable-artifact state after the broker
runtime integration changed tracked export inputs.

## Scope

This task owns local regeneration of `.aide/export/aide-lite-pack-v0/**`, local
release outputs under `.aide/release/**`, its task evidence, and the narrow
parent closeout records. Runtime source, configuration, publication, tags,
GitHub mutation, and target repositories are outside scope.

## Progress

- [x] Observe the post-landing validation failure and exact manifest source.
- [x] Compile the broad intent and split out this non-publishing local slice.
- [x] Create an isolated task branch and worktree from published dev.
- [x] Admit the bounded local artifact refresh.
- [x] Commit and publish the admission checkpoint.
- [x] Regenerate the portable export pack from a clean source commit.
- [x] Regenerate the local release bundle from the refreshed export pack.
- [x] Regenerate the preview-only release draft and checksum-bound planning records.
- [x] Run pack, release, consumer, doctor, and canonical validation.
- [ ] Commit and publish exact refreshed artifacts and evidence.
- [ ] Land through dev, observe refs, and close the parent integration task.

## Verification

- Compare generated path scope against the task allowlist.
- Run `pack-status`, `release validate`, and applicable manifest/checksum views.
- Run `test_export_import.py` and `test_q47_release_bundle.py`.
- Run `doctor`, `validate`, and commit checks.
- Record all skips, failures, and retained publication gates honestly.

## Recovery

Before artifact commit, discard only generator-owned output from this isolated
task worktree and regenerate. After publication, fix forward. Never use these
local artifacts as proof of a public GitHub Release.

## Results

- `export-pack` reported 826 included files, 829 checksums, and boundary PASS.
- `pack-status`, `release validate`, `release checksums`, and release draft
  validation passed.
- The ZIP and tar.gz were rebuilt from clean source `b3e5c7aa`; release bundle
  id is `aide-lite-pack-v0-b3e5c7aa2a1732fa`.
- The generated delta contains 26 paths, all under the authorized export and
  release roots.
- Portable lifecycle discovery passed 25 cases; release-bundle discovery passed
  10 cases; canonical validate and doctor passed.
- The release draft remains preview-only and no-publish. No tag, upload,
  GitHub release, API call, active CI, target mutation, or branch mutation was
  performed by the artifact generators.
