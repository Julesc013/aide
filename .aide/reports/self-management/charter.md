# AIDE Self-Management Charter Report

- task_id: AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01
- generated_at: 2026-06-18
- source_commit: 13bb0c2
- track: B
- status: review_required

## Core Requirement

AIDE must be able to manage AIDE as a repo.

It must observe, explain, detect drift, plan structural change, validate, record
evidence, emit events, update OKF when authorized, and mutate only through
reviewed transactions.

## Current Live Inputs

- 5,136 files.
- 943 generated files.
- 2,687 evidence files.
- 608 orphan candidates.
- 22 roots.
- 3 mixed roots.
- 19 unknown or review-required roots.
- 15 high-risk roots.
- `.aide/reports`: 102 top-level files, 52 directories, 365 flat report path
  references across 156 files.

## Deliverables

- `.aide/policies/self-management.yaml`
- `docs/reference/aide-self-management.md`
- `.aide/reports/self-management/object-backlog.md`
- `.aide/reports/self-management/queue-sequence.md`

## Boundary

This charter does not implement schemas, commands, generated-output ledgers,
OKF regeneration, docs repair, queue acceptance, file movement, reference
rewrites, transaction apply, runtime behavior, branch mutation, target mutation,
provider/model calls, network calls, or release work.
