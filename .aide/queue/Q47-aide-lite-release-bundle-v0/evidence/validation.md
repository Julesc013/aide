# Validation

## Baseline And Core Validation

- `git status --short`: PASS, dirty tree recorded before Q47 final artifact commit.
- `git branch --show-current`: PASS, `main`.
- `git tag --list`: PASS, no tags listed.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; inherited generated manifest fingerprint warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same inherited warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS before final status update; same inherited warning.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 125 tasks passed.

## Lifecycle Validators

- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN; inherited unknown file classification warnings.
- `py -3 .aide/scripts/aide_lite.py quality validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py roots validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py tools validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py refactor validate-map`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.

## Changelog, Git, And GitHub Advisory

- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS; preview-only, malformed_commits 15, release_publishing false.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS; advisory-only, no GitHub API mutation and no workflow write.

## Export And Release Commands

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; included_files 603, checksum_count 606, boundary_result PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary_result PASS, provenance_result `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py release bundle`: PASS; zip/tar.gz, checksums, manifest, install notes, previews, provenance, asset index, and validation reports generated.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS; fixture extraction, checksums, and forbidden-path checks passed.
- `py -3 .aide/scripts/aide_lite.py release status`: PASS; artifact_count 11, no_publish true.
- `py -3 .aide/scripts/aide_lite.py release assets`: PASS.
- `py -3 .aide/scripts/aide_lite.py release manifest`: PASS.
- `py -3 .aide/scripts/aide_lite.py release checksums`: PASS.
- `py -3 .aide/scripts/aide_lite.py release provenance`: PASS.
- `py -3 .aide/scripts/aide_lite.py release clean --dry-run`: PASS; deleted 0.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q48 GitHub Release Draft v0"`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 4096 chars / 1024 approximate tokens.

## Unit Tests

- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS; 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS; 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS; 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS; 8 tests.

## Secret Scan

- Requested broad `rg` scan: PASS_AFTER_INSPECTION. Matches were policy, documentation, generated-reference, regex, test, path, and historical evidence terms such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, `sk-ant`, and `latest-task-packet`; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt log, or raw response log was found. The requested root `tools` path is absent, so `rg` emitted a missing-path diagnostic.
- Strict key-shaped `rg` scan: PASS_AFTER_INSPECTION. Matches were test or evidence strings that forbid `OPENAI_API_KEY=` and `BEGIN PRIVATE KEY`; no committed credential value was found.

## Publication Boundary

No Git tag, GitHub Release, upload, package publish, branch create/delete/merge,
push, prune, active CI install, target repo mutation, provider/model call, or
network call was performed.
