# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD~1..HEAD
source_head: 9a0843c3a7633002f91a0ec3e707fe613650eb5f
preview_only: true

## Highlights

- Fixed: Exact predecessor rollback now accepts an unchanged authored CRLF AGENTS.md managed section. (9a0843c3a763)

## Validation Summary

- 9a0843c3a763: PASS: Red regression reproduced the AGENTS.md baseline error on source 723322cf; green regression passed after repair.

## Known Risks

- 9a0843c3a763: The local archives generated from source 723322cf remain rejected and are not advanced to dev.

## Follow-up

- 9a0843c3a763: Obtain independent source delta review, regenerate new local pack/release bytes, rerun importer and consumer gates, then review the exact dev effect.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
