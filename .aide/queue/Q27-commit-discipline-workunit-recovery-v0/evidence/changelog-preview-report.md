# Q27 Changelog Preview Report

Status: COMPLETE FOR REVIEW.

## Artifacts

- Changelog preview: `.aide/changelog/CHANGELOG.preview.md`.
- Release-notes preview: `.aide/changelog/RELEASE_NOTES.preview.md`.
- Machine-readable preview: `.aide/changelog/changelog.preview.json`.
- Malformed commit report: `.aide/changelog/malformed-commits.md`.

## Behavior

- `changelog preview` reads structured commit bodies from a Git range.
- Entries are grouped by the recognized changelog categories from `.aide/policies/commit-messages.yaml`.
- Malformed commits are reported and included in `.aide/changelog/malformed-commits.md`.
- The command is deterministic and local. It does not tag, publish releases, call providers, or call network services.

## Validation Result

- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS_WITH_WARNINGS; default `HEAD~20..HEAD` range reported older malformed pre-Q27 commits instead of hiding them.
- `py -3 .aide/scripts/aide_lite.py changelog preview --range HEAD~5..HEAD`: PASS; five structured Q27 commits, four categories, zero malformed commits.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q27_commit_recovery.py`: PASS; covers grouping, malformed commit rendering, and preview JSON shape.
- Golden task `changelog_preview_golden`: PASS; deterministic fixture generated and rendered without release publishing.

## Categories Observed In Q27 Range

- Added
- Changed
- Docs
- Internal

## Malformed Commit Handling

- Old history remains unchanged.
- When old commits are included in a preview range, they are reported in the malformed commit output and the preview returns WARN.
- The Q27 structured commit range returns PASS with no malformed commits.

## Limitations

- Preview output is not a release system.
- The parser depends on structured commit bodies and category prefixes.
- Changelog impact is category-based; no semantic classifier is used.
