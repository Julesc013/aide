# Independent Artifact Refresh Review

## Verdict

`REQUEST_CHANGES`

This verdict is bound to exact commit
`38fe712810b856f84ee59dffa8a1100d447cbfd4` and tree
`d279fb9191e9f43b29663d125b89977eb134f4a8`, reviewed against base
`cc85be9c472a16f39aae98ba00fd5de145098862`.

## Findings

### F1 - HIGH - The local asset indexes contain three stale artifact identities

`.aide/release/dist/release-assets.json` and its byte-identical
`latest-release-artifacts.json` projection do not describe the files currently
present in the candidate. The stale records are:

| Artifact | Recorded SHA-256 | Actual SHA-256 | Recorded/actual size |
| --- | --- | --- | --- |
| `aide-lite-pack-v0.checksums.json` | `79c07dc12fadb726ad2841626e5a2ab29c90c1a68f9d47c5c2766dfd2695e6ab` | `965db2435e40d479e89ce57e1cef96b20d0fbaf77f4e0d951e031b3338047f5a` | 1200 / 1200 |
| `release-validation.json` | `c42acc5280fa5f2d1d00a18b2a362bf515ff3d63e411843d2d12ce45b319e37a` | `11e1700d29651d67f662840ff510d89c2cd53d0fd97754c0a621f36a81cc37b3` | 3416 / 3166 |
| `SHA256SUMS.txt` | `fee18729126d3829de10d5e55cd117123ef662136c9d6efd83b8287f6b6efc6d` | `fa821c3f1c68bca499846ebc88571ceeb30ce5f051cc13128011978fb2d044c4` | 690 / 690 |

The affected records begin at
`.aide/release/dist/release-assets.json:5`, `:89`, and `:125`. The current
`release checksums` validator passes because it validates the separate core
checksum map, not the hashes recorded inside the local asset index. The GitHub
draft asset index is current, but that does not repair the contradictory local
index.

Impact: the claimed two-stage provenance closure is incomplete. A consumer of
the local asset index receives false digests, and the current validation path
does not detect the inconsistency.

Required change: fix generation order or dependency modeling so every retained
asset index is generated after its dependencies reach final bytes, validate all
recorded hashes and sizes, regenerate the records, and review the new exact
commit/tree.

### F2 - MEDIUM - Release metadata embeds a machine-local checkout path

The provenance and draft records embed
`D:/Projects/AIDE/aide-distribution-portability-pack-refresh` at
`.aide/release/dist/release-provenance.json:23` and
`.aide/release/github-release-draft.json:175`. The provenance report is also
listed as a future publish candidate at
`.aide/release/github-release-assets.json:135`.

This exposes machine topology in a tracked release candidate and makes generated
metadata depend on the checkout location. A replay from exact artifact commit
`da1051793d4c91ccff8d6c23b66ce1fa598729aa` in a disposable checkout passed all
four generators but differed from the candidate in 14 release metadata files;
the checkout-specific `source_repo` value is one direct cause of that
non-portability.

Required change: use a stable repository identity such as the canonical
`julesc013/aide` identity already recorded by the export manifest, or keep any
local path in evidence that is excluded from release and publish candidates.
Add a cross-checkout deterministic regression.

### F3 - MEDIUM - Required release-note assets describe an unrelated old head

The required changelog and release-note assets still identify
`d5e3e818841931702cd4e2cde49452744afab985` at
`.aide/release/dist/CHANGELOG.preview.md:6` and
`.aide/release/dist/RELEASE_NOTES.preview.md:6`. They describe the old
capability-ledger increment, not source commit `c730eac442021cdd6f71e6d8038d096af0c6378b`,
artifact commit `da1051793d4c91ccff8d6c23b66ce1fa598729aa`, or the reviewed
candidate. Both are marked required future publish candidates in
`.aide/release/github-release-assets.json:83` and `:96`.

The explicit preview/no-publish labels prevent this from being a false claim
that a release occurred, but the content is not candidate-accurate release
material.

Required change: regenerate the previews for an exact reviewed range, or mark
them stale and blocked/excluded from any publish candidate until a release range
is frozen.

## What Passed

- All 30 changed paths are within the task's allowed queue, export, and release
  scopes. No `.codex`, `.github`, runtime source, target repository, tag, remote,
  or machine configuration was changed.
- The three-commit range is a descendant of the exact base and passes commit
  message policy and `git diff --check`.
- Pack status is `PASS_SOURCE_ANCESTOR`; checksums and archive boundaries pass,
  and there are no replacement refs.
- ZIP SHA-256 is
  `3f24c8e27e21c1884c866ad4faf15538a1fd53cb2905e9d9abe41f6fbe170905`.
  tar.gz SHA-256 is
  `fb855c0e88d26138014038ff3ed5c2c5f2fc26a57f08fafd0f842492a327e758`.
- ZIP and tar contain the same 831 files with identical content. They have no
  unsafe paths, links, exact duplicates, case-folded Unicode duplicates,
  private-state filenames, or high-confidence secret-token hits. ZIP timestamps
  are fixed at 1980-01-01; tar mtimes and uid/gid values are zero.
- The release projection intentionally excludes
  `.aide.local.example/secrets/README.md` and regenerates its internal manifest,
  checksums, and report. The projected archives validate internally.
- The archive blobs are identical at artifact commit `da1051793...` and closure
  commit `38fe7128...`; the second stage did not alter ZIP or tar bytes.
- Both exact tracked archives independently completed safe import dry-run,
  digest-bound apply, idempotent rerun, receipt creation, and `doctor` in
  disposable consumer repositories.
- Re-runs passed: 25 export/import tests, 10 release-bundle tests, 8 GitHub draft
  tests, canonical `validate`, and `doctor`.
- No publication effect occurred. The draft, checklist, upload plan, and
  validation records retain no-publish markers and block tag, upload, GitHub
  Release, network, branch, CI, and provider/model effects.

## Provenance Assessment

The two-stage account is truthful about the archive bytes: clean source commit
`c730eac442021cdd6f71e6d8038d096af0c6378b` generated the payload, artifact
commit `da1051793d4c91ccff8d6c23b66ce1fa598729aa` contains those bytes, and closure
commit `38fe712810b856f84ee59dffa8a1100d447cbfd4` preserves them while recording
ancestor provenance.

It is not yet truthful to call the complete release-metadata dependency graph
closed because F1 leaves two committed asset indexes internally stale. F2 also
means metadata generation is not checkout-location independent. Integration of
this exact candidate should wait for a repaired, regenerated, independently
reviewed commit.

## Review Effects

No ref, branch, remote, tag, GitHub object, target repository, source file,
generated artifact, or machine setting was changed. Only this review record and
its JSON companion were created, and both remain uncommitted.
