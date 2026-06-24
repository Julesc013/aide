# Validation Results

Executed so far:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PASS, classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-EXECUTION-HOST-CONTRACT-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`: PASS, classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-EXECUTION-HOST-CONTRACT-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`: PASS, classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-EXECUTION-HOST-CONTRACT-V0-01`: PASS, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py execution-host validate`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Acceptance reports and evidence local absolute path scan: PASS, no matches.
- Acceptance reports and evidence secret-like scan: PASS, no matches.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS after acceptance commit.
