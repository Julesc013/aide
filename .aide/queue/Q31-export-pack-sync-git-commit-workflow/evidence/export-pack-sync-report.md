# Q31 Export Pack Sync Report

## Pack Regeneration

- Command: `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
- Result: PASS
- Pack path: `.aide/export/aide-lite-pack-v0`
- Included files: 194
- Checksum entries: 197
- Boundary result: PASS
- Provider/model calls: none
- Network calls: none

## Pack Status

- Command: `py -3 .aide/scripts/aide_lite.py pack-status`
- Result: PASS
- Checksums valid: true
- Provenance result: `DIRTY_SOURCE_RECORDED`
- Boundary result: PASS
- Checksum problems: 0
- Provenance problems: 0
- Boundary violations: 0

The dirty provenance is expected because Q31 evidence and generated artifacts
are still being finalized in the working tree at export time. The manifest does
not pretend the source tree was clean.

## Included Governance Files

- `.aide/policies/commit-messages.yaml`
- `.aide/hooks/commit-msg`
- `.aide/git/commit-template.md`
- `.aide/reports/aide-commit-message-standard.md`
- `.aide/policies/task-resumption.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/recovery.yaml`
- `.aide/reports/aide-task-resumption-standard.md`
- `.aide/reports/aide-workunit-recovery-standard.md`
- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/README.md`
- `.aide/git/project-profiles.yaml`
- `.aide/git/helper-policy.yaml`
- `.aide/git/helper-commands.md`
- `.aide/scripts/aide_lite.py`
- Q27-Q31 governance golden tasks
- portable `docs/reference/**` governance docs

## Export Policy Result

`.aide/policies/export-import.yaml` now names portable include classes for
commit discipline, hook/template support, changelog preview, task resumption,
WorkUnit recovery, generic Git workflow policy, branch roles, promotion/sync/
prune policy, dry-run helper policy, project workflow profiles, golden tasks,
and reference docs.

It also names source-specific exclusions for generated Git detection reports,
latest helper plans, AIDE dev/main policy outputs, changelog previews, queue
history, generated context/reports/status artifacts, `.aide.local/`, secrets,
raw prompts, and raw responses.
