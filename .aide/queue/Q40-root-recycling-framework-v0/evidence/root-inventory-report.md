# Root Inventory Report

## Summary

- inventory path: `.aide/roots/latest-root-inventory.json`
- markdown path: `.aide/roots/latest-root-inventory.md`
- source input ref: `.aide/repo/file-inventory.json`
- root count: 22
- file count: 1,751
- no-apply: true

## Root Status And Risk

The generated root classification currently reports:

- canonical roots: 7
- mixed roots: 3
- review-required roots: 12
- high-risk roots: 15
- medium-risk roots: 1
- low-risk roots: 6
- unknown-owner root candidates: 22

## High-Risk Root Candidates

High-risk root candidates are recorded for review, not mutation:

- `.agents`
- `.aide`
- `.aide.local.example`
- `.codex`
- `core`
- `environments`
- `evals`
- `governance`
- `hosts`
- `labs`
- `packaging`
- `platforms`
- `repo-root`
- `research`
- `shared`

## Caveats

- Q40 uses deterministic path, kind, owner, generated/evidence, and risk
  heuristics only.
- Unknown-owner and high-risk root candidates are review signals, not deletion,
  move, or archive approval.
