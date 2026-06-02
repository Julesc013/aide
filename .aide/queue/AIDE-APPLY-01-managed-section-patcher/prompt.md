# AIDE-APPLY-01 Prompt

Implement `AIDE-APPLY-01 - Managed Section Patcher` in the AIDE repository.

The governing prompt requires marker-based managed-section parsing, fixture-only patch planning and verification, manual content preservation outside markers, missing/duplicate/malformed/nested marker conflict detection, section hashes, transaction-compatible records, rollback-compatible preimage/postimage evidence, report-only commands, examples, tests, golden tasks, docs, evidence, and a next task packet for `AIDE-CHECK-APPLY-01`.

The prompt explicitly forbids active repository apply, target repository mutation, branch/worktree mutation, merge/push/promotion, release publication, GitHub API mutation, provider/model/network calls, Gateway forwarding, and install/repair/upgrade/rollback/uninstall apply behavior.

Primary allowed implementation paths are recorded in `task.yaml`.
