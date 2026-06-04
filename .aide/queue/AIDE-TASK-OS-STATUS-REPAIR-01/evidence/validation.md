# Validation

## Preflight

- `git status --short --branch` - PASS. Initial state was `## main...origin/main`.
- `git remote -v` - PASS. `origin` fetch/push: `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD` - PASS. Initial HEAD: `6eb0e6a9d0405a85ba11b743954493f924648c18`.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS, reproduced stale state before repair: raw `AIDE-APPLY-02`, missing latest status.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only.

## Tests

- `py -3 -m unittest .aide.scripts.tests.test_x_os_01_task_os_commands` - NOT_RUN as final validation because `.aide` is not an importable module name; initial attempt failed with `ValueError: Empty module name`.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_x_os_01_task_os_commands.py` - PASS. Ran 8 tests in 8.670s, OK.

## Task OS Reports

- `py -3 .aide/scripts/aide_lite.py task status` - PASS. Latest task ID: `AIDE-TASK-OS-STATUS-REPAIR-01`.
- `py -3 .aide/scripts/aide_lite.py task classify` - PASS. Latest task ID: `AIDE-TASK-OS-STATUS-REPAIR-01`; lifecycle state: `done_local`.
- `py -3 .aide/scripts/aide_lite.py task repair-plan` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py task requeue-plan` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py task resume-plan` - PASS. Latest task ID: `AIDE-TASK-OS-STATUS-REPAIR-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan` - PASS. Selected next WorkUnit: `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`; `lifecycle_apply_authorized: false`.
- `py -3 .aide/scripts/aide_lite.py blocker status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py blocker classify` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py wave status` - PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py wave plan` - PASS. Reports selected next WorkUnit and labels the X-OS sequence historical.
- `py -3 .aide/scripts/aide_lite.py checkpoint status` - PASS. Next recommended action: `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`.
- `py -3 .aide/scripts/aide_lite.py checkpoint plan` - PASS, report-only.

## Repo Validation

- `git diff --check` - PASS.
- `py -3 .aide/scripts/aide_lite.py validate` - initial run FAILED because the replacement latest task packet was missing required `OUTPUT_SCHEMA` and `TOKEN_ESTIMATE` sections.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS after adding the missing packet sections.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status` - PASS, report-only; target mutation false, branch mutation false, provider/model/Gateway/network calls none.
- `py -3 .aide/scripts/aide_lite.py managed-section status` - PASS, report-only; active repo apply false, target mutation false, branch mutation false, provider/model/network calls none.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS, report-only; real repo apply false, target mutation false, branch mutation false, provider/model/network calls none.

## Machine-Readable Checks

- `py -3 -c "import json ..."` over `.aide/reports/task-os-task-classification.json` and `.aide/reports/task-os-blocker-classification.json` - PASS.
- `py -3 -c "import pathlib, yaml ..."` over changed YAML files - NOT_RUN/PyYAML unavailable; failed with `ModuleNotFoundError: No module named 'yaml'`.
- `py -3 -c` structural YAML sanity check over `.aide/queue/index.yaml`, task `task.yaml`, and task `status.yaml` - PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - pre-evidence run PASS but classified partial because final evidence files were not yet written.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - pre-evidence run PASS but reported missing `changed-files.md`, `validation.md`, and `remaining-risks.md`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - final run PASS. Status `needs_review`, classification `complete`, evidence files 8, missing evidence 0, recovery suggestion `noop_already_complete`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-TASK-OS-STATUS-REPAIR-01` - final run PASS. Evidence available: `boundary-confirmation.md`, `changed-files.md`, `diagnosis.md`, `next-task-prompt.md`, `remaining-risks.md`, `repair-summary.md`, `review.md`, and `validation.md`; missing none.

## Boundary Searches

- Positive boundary search over changed Task OS files and reports - PASS. Required terms were present, including `current_toml_state`, `latest_indexed_task_id`, `latest_task_packet_id`, `selected_next_workunit`, `AIDE-TASK-OS-STATUS-REPAIR-01`, `AIDE-APPLY-LIFECYCLE-PLAN-01`, `lifecycle_apply_authorized: false`, `planning-only`, `superseded`, `historical`, and all forbidden-operation terms.
- Negative stale-signature search - PASS:
  - `latest_task_id: \`AIDE-APPLY-02\`` count 0 in `task-os-task-status.md`.
  - `latest_task_status: \`missing\`` count 0 in `task-os-task-status.md`.
  - `Next AIDE-local work: Q49` count 0 in `README.md`.
  - `lifecycle_apply_authorized: true` count 0 in Task OS command and next-plan reports.
  - `target_mutation: true` and `branch_mutation: true` count 0 in `task-os-task-status.md`.

## Secret Scan

- Broad changed-file scan command searched for `SECRET`, `TOKEN`, `API_KEY`, `PRIVATE_KEY`, `PASSWORD`, `GITHUB_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `AWS_ACCESS_KEY`, and `AWS_SECRET_ACCESS_KEY` patterns - WARN. It found existing policy/test marker strings in `.aide/scripts/aide_lite.py`, not new credentials.
- Diff-added-line secret scan with the same credential-marker family - PASS. `diff_added_secret_hits: 0`.

## Generated Report Churn

Required broader status commands refreshed only `current_commit` stamps in non-Task-OS reports. Those out-of-scope generated changes were restored with targeted patches. The retained generated report changes are under `.aide/reports/task-os-*`.
