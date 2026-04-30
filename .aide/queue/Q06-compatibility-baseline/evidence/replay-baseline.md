# Q06 Replay Baseline Evidence

Date: 2026-04-30

## Replay Definition

Q06 replay means deterministic Harness summary expectations. It is not Runtime replay and does not call providers, models, native tools, browsers, network services, package managers, or release automation.

The replay record is `.aide/compat/replay-corpus.yaml`.

## Expected Commands

- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide compile --dry-run`
- `py -3 scripts/aide migrate`

Expected hard errors for the current repo: `0`.

Expected warnings: review-gate warnings for Q00 through Q03, Q05, and Q06 while those items remain review-gated. These warnings are accepted for Q06 v0 and do not mean compatibility records are invalid.

## Implemented Helper

`core/compat/replay_manifest.py` exposes the same summary expectations for lightweight tests and future Harness hardening.

`core/compat/tests/test_compat_baseline.py` confirms replay metadata includes `validate` and `migrate`.

## Boundary

Replay expectations are stable summary anchors, not full stdout snapshots. Full Runtime replay remains out of scope.
