# ExecPlan: QCHECK Token Survival Foundation Audit

## Purpose

Produce a restartable checkpoint audit of the live repo state after Q09-Q20.
The audit judges the token-survival foundation against AIDE's binding product
constraint and recommends the next queue direction.

## Scope

- Inspect git, queue, docs, generated reports, AIDE Lite surfaces, Gateway
  skeleton, provider metadata, and tests.
- Run structural validation, AIDE Lite commands, unit tests, syntax checks, diff
  checks, local-state checks, and secret scans.
- Write audit reports under this queue item.
- Stop at `needs_review`.

## Non-Goals

- No product fixes.
- No implementation changes.
- No Gateway/provider/runtime/UI work.
- No live provider/model/network calls.
- No deletion or cleanup of stale records.
- No `.aide.local/`, `.env`, secrets, raw prompt logs, or raw response logs.

## Progress

- Inspected governing Profile/Contract, queue policy, source-of-truth reference,
  queue state, git state, file inventory, docs, token reports, provider status,
  and Gateway status.
- Ran requested Harness, AIDE Lite, unit-test, syntax, diff, local-state, and
  secret-scan checks.
- Wrote checkpoint audit artifacts and evidence.

## Validation Summary

See `evidence/commands-run.md` and `test-validation-audit.md`.

## Review Gate

Final checkpoint status is `needs_review`. The audit recommends repair and
review before continuing to more scaffolding.
