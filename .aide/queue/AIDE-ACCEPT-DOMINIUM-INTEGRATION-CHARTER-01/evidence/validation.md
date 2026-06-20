# Validation

Validation results before final staging:

- `git status --short --branch`: PASS at task start; later dirty paths are limited to the acceptance allowlist.
- `git diff --check`: PASS. Git reported CRLF normalization warnings for `.aide/queue/index.yaml`, `IMPLEMENT.md`, and `PLANS.md`; no whitespace errors were reported.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- Acceptance JSON parsing: PASS.
- Bounded remote Dominium HEAD confirmation: PASS, remote `main` remains `623ab08ae8c867719d5abc2e60c16a6fbb37b313`.
- Source-chain report consistency: PASS.
- Ownership uniqueness check: PASS, 41 ownership concepts with no duplicate semantic owner assignments.
- Namespace uniqueness check: PASS.
- Object-mapping required-field check: PASS, 13 rows include the required mapping fields.
- DAG acyclicity check: PASS, 55 nodes and 25 edges.
- Dependency resolution check: PASS, all task graph edge endpoints resolve.
- Mutation-prerequisite check: PASS, runtime and mutation facts remain false.
- Downstream queue-directory absence check: PASS.
- Dominium worktree immutability check: PASS.
- Secret-like scan: PASS, no matches with the bounded strict pattern.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, complete, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`: PASS, `missing:` empty.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Post-staging/post-commit validation:

- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
