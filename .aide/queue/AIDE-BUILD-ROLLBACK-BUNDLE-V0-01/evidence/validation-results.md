# Validation Results

Result: `PASS_WITH_WARNINGS`

Material findings: `0`

Missing evidence after evidence completion: `0`

Core RollbackBundle validation:

- PASS: `py_compile` for `core/protocol/rollback_bundle.py`, `.aide/scripts/tests/test_aide_rollback_bundle_v0.py`, and `.aide/scripts/aide_lite.py`.
- PASS: focused RollbackBundle unittest discovery, `7` tests.
- PASS_WITH_WARNINGS: `rollback-bundle status`; schema/helper/reports present, next task `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`, no apply/mutation capabilities reported.
- PASS_WITH_WARNINGS: `rollback-bundle project`; projection digest `sha256:9c53cf199c7e66f6679c150df8647d60a72073e6dcd558925e67bee455d935d6`, `15` reverse operations, `6` preimage artifacts, risk `medium`.
- PASS_WITH_WARNINGS: `rollback-bundle validate`; `error_count: 0`, fixture matrix passed, predecessor bindings present, no apply/mutation capabilities reported.

Predecessor regression validation:

- PASS_WITH_WARNINGS with `error_count: 0`: `distribution-manifest validate`.
- PASS_WITH_WARNINGS with `error_count: 0`: `project-lock validate`.
- PASS_WITH_WARNINGS with `error_count: 0`: `ownership-ledger validate`.
- PASS_WITH_WARNINGS with `error_count: 0`: `ownership-ledger migrate-q43`.
- PASS_WITH_WARNINGS with `error_count: 0`: `install-record validate`.
- PASS_WITH_WARNINGS with `error_count: 0`: `migration-record validate`.
- PASS_WITH_WARNINGS with `error_count: 0`: `update-plan validate`.

Boundary and global validation:

- PASS: Q43-Q48 no-apply/no-publish validators returned exit code `0`.
- PASS: broad `py -3 .aide\scripts\aide_lite.py validate` returned status `PASS` and exit code `0`.

Task and Git validation:

- Initial task inspection reported `missing_evidence: 2` for `validation.md` and `remaining-risks.md`.
- Added the missing task-local evidence files.
- PASS: `git diff --check`.
- Staged diff and commit-policy checks are recorded after staging and commit.

Warnings and non-material validation notes:

- RollbackBundle v0 is proposed, not accepted. Independent check remains required.
- PASS_WITH_WARNINGS is expected because this is a build task that stops at `needs_review`.
- A dotted-module unittest invocation failed before the supported discovery invocation passed. This was command-form noise, not product behavior.
- One parallel RollbackBundle project command hit a Windows file-lock race while another command was generating the same fixture/report tree. A sequential rerun passed.
- One hygiene scan command used an unsupported PowerShell option; the corrected scan completed and found no material leak.
