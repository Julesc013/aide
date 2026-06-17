# Validation

## Results

- PASS: `git status --short --branch`
  - Preflight was clean before check task materialization.
  - Current dirty state is limited to check-task allowed paths and generated Task OS status reports.
- PASS_WITH_WARNING: `git diff --check`
  - Reports the existing `.aide/queue/index.yaml` CRLF normalization warning.
- PASS: `git diff --cached --check`
  - No staged whitespace errors were present when run before staging.
- PASS: `py -3 .aide/scripts/aide_lite.py doctor`
  - Passed after the latest task packet `IMPLEMENTATION` section was restored.
- PASS: `py -3 .aide/scripts/aide_lite.py validate`
  - Passed after the latest task packet `IMPLEMENTATION` section was restored.
- PASS: `py -3 .aide/scripts/aide_lite.py task status`
  - Refreshed Task OS status reports and selected `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01` as latest task.
- PASS: `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
  - Reported `classification: complete`, `evidence_files: 6`, and `missing_evidence: 0`.
- PASS: `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-SELF-MANAGEMENT-CHARTER-01`
  - Listed all six expected build-task evidence files.
- PASS: JSON parsing for self-management charter/check reports.
- PASS: YAML parsing through the repo-local `core.protocol.workunit.read_simple_yaml` helper.
  - `PyYAML` is not installed in this environment, so no dependency was added.
- PASS: GovernanceFinding JSON parsed and each finding has required fields.
- PASS: Markdown and JSON reports agree on finding id, severity, surface, taxonomy, and next_task.
- PASS: Charter build commit message policy check when checked directly from commit `bb64e63fdbdbd084a19c8f3f6d47b8229d497e68`.
- PASS_WITH_WARNING: pre-check `py -3 .aide/scripts/aide_lite.py commit check --latest`
  - Failed because the then-latest unrelated commit message was `license update with my name and this year`.
  - This is recorded as a commit-state warning outside the charter check result.

## Post-Commit Check

- PASS: `py -3 .aide/scripts/aide_lite.py commit check --latest`
  - The check task commit passed AIDE commit-message policy after commit creation.
