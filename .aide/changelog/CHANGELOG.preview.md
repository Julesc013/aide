# AIDE Changelog Preview

This file is generated from local Git history and is a preview only.

source_range: 716ec1fd0ad6fb2d3875417c4db7b867a7b393fe..b5827566fbe270a604907b8c20437a1228373d81
source_head: b5827566fbe270a604907b8c20437a1228373d81
commit_count: 3
malformed_count: 0
preview_only: true
release_publishing: false

## Summary

- Changed: 1
- Fixed: 2

## Changed

- selected-task continuation now has source qualification evidence. (1cd847805188 test(task): qualify selected-task continuation and preserved effects)

## Fixed

- task resume-plan no longer declares execution safe or recommends blanket reruns. (3625acf79209 fix(task): derive continuation advice from the selected WorkUnit)
- portable task resume-plan preserves selected task state without claiming execution readiness. (b5827566fbe2 fix(pack): deliver qualified selected-task continuation advice)

## Malformed Commits

- None.

## Release Caveat

- Preview only. No tags, GitHub Releases, branch mutation, or publishing were performed.
