# Validation

Validation results:

- `git status --short --branch`: PASS. Dirty paths are limited to the allowed check task/report paths, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.
- `git diff --check`: PASS with Git line-ending normalization warnings for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors reported.
- Charter/check structural validation: PASS.
  - Parsed check JSON and charter JSON reports.
  - Verified current remote Dominium `main` with `git ls-remote`.
  - Verified local Dominium `origin/main` equals remote `main` before immutable object inspection.
  - Verified current remote Dominium canonical inputs are byte-identical except `README.md`.
  - Verified current remote Dominium queue markers match the charter.
  - Verified ownership, namespace, object mapping, refusal mapping, dependency resolution, DAG acyclicity, mutation prerequisites, and downstream task absence.
  - Verified no Dominium local changes and no changed AIDE path outside the check allowlist.
  - Verified secret-like scan found no matches.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `status: needs_review`, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `status: needs_review`, `classification: complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Post-staging/post-commit validation:

- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
