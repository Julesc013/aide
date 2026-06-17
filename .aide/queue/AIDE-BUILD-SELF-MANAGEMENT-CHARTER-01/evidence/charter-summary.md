# Charter Summary

## Doctrine

AIDE must be able to manage AIDE as a repo.

Self-management means AIDE observes itself, explains itself, detects drift,
plans structural and knowledge changes, validates those plans, records evidence,
and only later mutates itself through reviewed transactions.

## Current Live Inputs

- Repo layout inventory: 5,136 files, 943 generated files, 2,687 evidence files,
  and 608 orphan candidates.
- Root status: 22 roots, 3 mixed roots, 19 unknown or review-required roots,
  15 high-risk roots.
- `.aide/reports` risk: 102 top-level files, 52 directories, and 365 flat
  check/accept report path references across 156 files.

## Outputs

- `.aide/policies/self-management.yaml`
- `docs/reference/aide-self-management.md`
- `.aide/reports/self-management/charter.*`
- `.aide/reports/self-management/object-backlog.md`
- `.aide/reports/self-management/queue-sequence.md`

## Boundary

This task defines doctrine and queue shape only. It does not implement the
object backlog or command backlog.
