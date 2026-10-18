# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 66c0b90b6aa0b68cd24659b6279f66b987cb585c..a1a45098f87eacd12571767ebc0fad1e7932f6d5
source_head: a1a45098f87eacd12571767ebc0fad1e7932f6d5
preview_only: true

## Highlights

- Added: Inspect offline results against their request and selected inputs (8a6b32ef484f)

## Validation Summary

- a986ce94b103: PASS - existing handoff source and campaign prerequisites inspected
  NOT RUN - new source and installed consumer qualification
- 8a6b32ef484f: PASS - syntax and preserved original test assertions
  FAIL - doctor/validate: changed-source capability binding; reviewed refresh pending
  NOT RUN - 97 source methods and installed qualification
- 3e2bbd3277ab: PASS - source97; original79 retained; job retirement; CURRENT binding
  FAIL - development pack provenance awaits the reviewed export refresh
  NOT RUN - delivered97, installed consumer and final preview
- a1a45098f87e: PASS - delivered97; ownership6; installed exchange and real records
  PASS - exporter, doctor, validate, pack-status; eight release assets unchanged
  NOT RUN - final fixed preview

## Known Risks

- 8a6b32ef484f: Selected files are incomplete dependency coverage; no automatic apply or acceptance

## Follow-up

- No follow-up summaries were extracted.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
