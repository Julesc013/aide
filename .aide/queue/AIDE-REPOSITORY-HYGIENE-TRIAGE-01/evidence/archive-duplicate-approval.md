# Archive-Duplicate Removal Approval

## Decision

- Decision: approved by repository owner.
- Date: 2026-09-21.
- Canonical manifest SHA-256:
  `381213944009ef69aa4860ccb4269b9a0ecd72091fe3f0cb5fa41de40dcfe47d`.
- Authorized effect: literal removal of the 506 untracked ordinary files in the
  committed manifest after fail-closed loose-file and tracked-ZIP-member checks.

## Context

The owner approved the exact candidate in response to the candidate-bound
request and separately requested safe removal of old changes, worktrees, and
caches. This approval does not authorize tracked-file deletion, archive
retirement, branch deletion, history rewrite, force push, release, or removal
of unique dirty work.

## Required Apply Checks

- Parse the canonical committed manifest bytes and verify its SHA-256.
- Confirm every path remains under the repository and is untracked.
- Confirm every path is an ordinary non-reparse-point file.
- Confirm size and SHA-256 match the manifest.
- Confirm the named tracked ZIP exists and its member bytes have the same hash.
- Abort before deletion if any record fails.
- Remove literal file paths only; do not recursively remove directories.
