# Q41 Tool Inventory Report

Latest inventory: `.aide/tools/latest-tool-inventory.json`

## Summary

- Source commit recorded by latest tool inventory: `9b5b0ba5da291c9366d25dc708b11b4a73c0bcb1`.
- Tool candidates detected: 200.
- High or release-risk candidates: 12 release-risk candidates.
- Unknown capability/fate candidates: 16.
- Unknown tool execution: false.
- No-apply mode: true.

## Capability Counts

- audit: 37
- context: 84
- docs: 11
- generate: 13
- install: 7
- package: 1
- release: 12
- repo_policy: 56
- test: 82
- unknown: 16
- validate: 35

## Risk Counts

- low: 31
- medium: 143
- release: 12
- unknown: 14

## Detection Inputs

Q41 uses tracked files, Q37 repo intelligence where present, Q38 quality
references where present, root inventory references where present, path/name
patterns, extensions, shebang detection, command catalogs, and doc references.
It does not execute candidate tools while detecting them.
