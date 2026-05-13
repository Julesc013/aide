# Changelog Preview Report

Status: superseded pre-repair blocker record.

Q27 was expected to add deterministic changelog preview commands and generated
preview files:

- `.aide/changelog/CHANGELOG.preview.md`;
- `.aide/changelog/RELEASE_NOTES.preview.md`;
- AIDE Lite `changelog preview` and optional range support.

These were not implemented because baseline Q25 pack/local-state validation
failed before edits.

## Malformed Commit Handling

Not implemented yet. Future Q27 work should report malformed commits rather
than hide them.
