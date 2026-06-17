# Initial Scope

## Decision

Created `AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` as a
check-only queue item.

## Allowed Work

- Read live repo, queue, root, refactor, generated report, and documentation
  surfaces.
- Refresh deterministic report-only status artifacts where the existing AIDE
  helper commands do so.
- Write audit reports and task-local evidence.

## Forbidden Work

No file moves, deletes, reference rewrites, path alias application, shim
creation, new top-level root creation, generated-output source-of-truth
promotion, source truth mutation, queue acceptance mutation, branch mutation,
target-repo mutation, GitHub mutation, release work, provider/model calls,
network calls, runtime work, host runtime work, or product readiness claims.

## Starting State

- Branch: `main`.
- Initial `git status --short --branch`: clean before `task status`; generated
  Task OS reports changed after the status helper ran and are in the task
  allowlist.
- No existing `AIDE-STRUCTURE` queue item was found before creating this one.
