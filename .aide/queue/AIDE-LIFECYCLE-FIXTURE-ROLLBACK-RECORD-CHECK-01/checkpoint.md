# Checkpoint

Disposition: `ACCEPTED_WITH_NOTES`

Rollback-compatible lifecycle fixture records are accepted with notes as static, report-backed evidence before rollback dry-run. The review verified:

- Rollback record schema `.aide/apply/lifecycle-rollback-record.schema.json` parses and requires `rollback_execution_implemented=false`.
- Generic lifecycle rollback record example parses and matches required fields.
- Fixture rollback records exist for `install-managed-section` and `upgrade-v2`.
- Generated plans reference rollback record destinations for the two fixture records.
- Expected reports reference rollback-compatible record refs for `install-managed-section`, `upgrade-v2`, and `rollback-record-generated`.
- Referenced preimage and postimage content hashes match recorded SHA-256 values.
- Inverse operations require matching current hash before restoration.
- Rollback preconditions and stop conditions cover current hash match, review gate, protected paths, unknown ownership, missing preimage, manual content mismatch, and broad delete as an unsupported case.
- Manual preservation notes distinguish generated-file and managed-section ownership from manual content outside AIDE ownership.
- Protected path checks include `.git`, `.github`, `.aide.local`, `.env`, and `secrets`.
- Plans and reports preserve no-mutation and no-execution flags.

This checkpoint does not authorize rollback apply, rollback execution, uninstall apply, lifecycle apply, fixture apply, active repo apply, target repo apply, branch/worktree mutation, release work, provider/model/Gateway/network calls, GitHub mutation, or broad active-repo apply.
