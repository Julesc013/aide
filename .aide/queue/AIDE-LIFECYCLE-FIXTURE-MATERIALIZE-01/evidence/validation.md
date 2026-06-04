# Validation

## Preflight

- `git status --short --branch`: PASS; initial output `## main...origin/main`.
- `git remote -v`: PASS; origin fetch/push configured.
- `git rev-parse HEAD`: PASS; initial HEAD `07838e3e281cd65639ddd7c6d692b029f87edbfd`.
- `git show --stat --oneline --name-status HEAD`: PASS; latest commit was `07838e3 feat(aide): add lifecycle schema validator`.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; preflight latest task was `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS with stale selection warning; selected `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`: NOT_RUN in positional form; CLI requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`: PASS; classification `complete`.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`: NOT_RUN in positional form; CLI requires `--task-id`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`: PASS; missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS; 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS; 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.

## Post-Change Validation

- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; task count `79`, latest task `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS with stale selection warning; selected `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local next batch selects `AIDE-LIFECYCLE-FIXTURE-CHECK-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`: PASS; status `needs_review`, classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`: PASS; evidence files `9`, missing `0`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS; report-only, lifecycle apply not implemented or executed.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS; 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS; 298 checks, shape-only.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS after trimming `.aide/context/latest-task-packet.md`; latest task packet tokens `1755`.
- changed JSON parse: PASS; parsed 21 fixture/report JSON files.
- PyYAML import: NOT_RUN/PASS_WITH_WARNING; `ModuleNotFoundError: No module named 'yaml'`.
- YAML structural fallback: PASS; checked 3 changed YAML files for required shape and tabs.
- fixture invariants: PASS; 13 scenarios, 7 expected reports, 2 rollback records, `target_files_mutated=false`, `lifecycle_apply_executed=false`.
- boundary text searches: PASS; required boundary terms found.
- overclaim enabling marker search: PASS_WITH_WARNING; hits occurred only in lifecycle-schema validation report lines that assert enabling markers are omitted.
- changed-file secret scan: PASS_WITH_WARNING; hits were protected-path words such as `secret`/`secrets` and existing `token` task names, not credentials or key material.

## Tests

No code changed, so targeted Python tests and `py_compile` were not rerun in the post-change phase. The existing lifecycle-schema command validation still passed.
