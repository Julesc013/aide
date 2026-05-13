# Q27 WorkUnit Recovery Report

Status: COMPLETE FOR REVIEW.

## Policy

- Task resumption policy: `.aide/policies/task-resumption.yaml`.
- WorkUnit policy: `.aide/policies/work-units.yaml`.
- Recovery policy: `.aide/policies/recovery.yaml`.
- Task resumption report: `.aide/reports/aide-task-resumption-standard.md`.
- WorkUnit recovery report: `.aide/reports/aide-workunit-recovery-standard.md`.

## Semantics

- Stable task ids are required for non-trivial work.
- Recovery starts from repo-local state before asking the user.
- Repeated prompts inspect queue index, task/status/evidence files, latest task packet, changed files, and validation evidence.
- Already complete tasks return `noop_already_complete` when status/evidence support completion.
- Partial tasks recommend continuing from status/evidence.
- Missing or destructive states remain blocked.
- WorkUnit states include `planned`, `ready`, `running`, `partial`, `needs_review`, `passed`, `passed_with_notes`, `blocked`, `superseded`, `noop_already_complete`, and `reopened`.

## Command Behavior

- `task inspect`: reads queue index/latest packet, resolves short ids such as `Q28` to canonical queue ids, reports status/evidence/classification, and suggests recovery.
- `task status`: prints compact queue status.
- `task noop-check`: reports no-op/continue/blocked state without mutation.
- `task dependencies`: reports declared dependency ids and current statuses.
- `task recover`: report-only by default; can write a local recovery report when explicitly requested.
- `task evidence`: lists available and missing evidence files.
- `task current`: prints the current task id inferred from the latest packet or queue state.

## Validation Result

- `py -3 .aide/scripts/aide_lite.py task inspect`: PASS; resolved the Q28 compact task packet to `Q28-git-workflow-policy-v0` and reported superseded/partial state.
- `py -3 .aide/scripts/aide_lite.py task noop-check`: PASS; reported `inspect_blocker_then_reopen_or_continue_if_operator_overrides` for the superseded Q28 packet.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; listed 32 queue entries.
- `py -3 .aide/scripts/aide_lite.py task dependencies`: PASS; reported Q28 depends on Q27.
- `py -3 .aide/scripts/aide_lite.py task evidence`: PASS; listed Q28 evidence files and no missing required evidence files.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q27_commit_recovery.py`: PASS; includes complete/no-op, partial/resume, and short-id resolution fixtures.
- Golden tasks `task_resumption_standard_golden` and `workunit_idempotency_golden`: PASS.

## Limitations

- Recovery commands are report-first. They do not autonomously edit arbitrary task files or resolve destructive ambiguity.
- Completion classification is evidence-surface based, not a semantic proof that every task objective is satisfied.
- Branch-aware recovery belongs to Q28/Q29 and is intentionally not implemented here.
