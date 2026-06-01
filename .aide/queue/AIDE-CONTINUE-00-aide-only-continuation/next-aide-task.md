# Next AIDE Task

Selected task:

`X-OS-00 - AIDE Task OS Schemas and Policies`

## Why Selected

X-TEST-00 has implemented the validation-tier model and remains ready for review. XCHECK-01R already identifies `X-OS-00` as the next AIDE-local Task OS dependency after validation tiering. The Task OS readiness audit says report-only command patterns are ready to build, while apply behavior is not ready.

## Allowed Paths For X-OS-00

- `.aide/queue/X-OS-00-aide-task-os-schemas-and-policies/**`
- `.aide/queue/index.yaml`
- `.aide/policies/task-lifecycle.yaml`
- `.aide/policies/blockers.yaml`
- `.aide/policies/repair-loop.yaml`
- `.aide/policies/waves.yaml`
- `.aide/policies/checkpoints.yaml`
- `.aide/policies/dev-main-promotion.yaml`
- `.aide/policies/capability-reality.yaml`
- `.aide/tasks/**`
- `.aide/ledgers/*.schema.json`
- `.aide/reports/x-os-00-*.md`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- docs/reference files only when needed to explain new policy records

## Forbidden Paths And Operations

- no target repo files
- no `.git/**`, `.github/**`, `.env`, `.aide.local/**`, secrets, raw prompts, or raw responses
- no Task OS apply behavior
- no branch/worktree apply
- no merge, push, promotion, prune, tag, or release publication
- no install/repair/upgrade/rollback/uninstall apply
- no Gateway/provider/model/runtime/host implementation

## Expected Outputs

- task lifecycle policy
- blocker taxonomy policy
- repair-loop policy
- waves and checkpoints policy
- dev/main promotion policy links, still report-only
- capability reality policy
- WorkUnit, attempt, blocker, repair, wave, checkpoint, capability, branch-provenance, and checkpoint-ledger schemas
- evidence and validation records

## Acceptance Criteria

- schemas validate structurally
- policies define report-only Task OS state without apply behavior
- blockers, repairs, waves, checkpoints, and capability states are first-class records
- no target repo mutation or branch mutation occurs
- next task packet points to X-OS-01 only if X-OS-00 finishes and stops at review

## Validation Commands

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 .aide/scripts/aide_lite.py eval run`
- `git diff --check`
- targeted secret scan
