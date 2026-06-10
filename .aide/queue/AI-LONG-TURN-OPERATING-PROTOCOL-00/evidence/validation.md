# Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py intent compile --prompt "...broader request..."` | PASS_WITH_BLOCKER | Classified the broader prompt as blocked and requiring split. |
| `py -3 .aide/scripts/aide_lite.py intent compile --prompt "...docs-only split..."` | PASS | Produced the current safe docs WorkUnit draft. |
| `git diff --check` | PASS | No whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py intent validate` | PASS | Intent policy, schemas, latest packet, and WorkUnit draft validated. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00` | PASS | Status `needs_review`; classification `complete`; missing evidence `0`. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00` | PASS | Listed changed-files, intent, remaining-risks, and validation evidence. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Required AIDE artifacts and local-state protections present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | AIDE structural validation passed. |
| `Test-Path scripts/check_architecture_boundaries.py` | NOT_RUN | Returned `False`; requested helper is not present in this AIDE repo. |
| `Test-Path scripts/check_generated_artifact_cleanliness.py` | NOT_RUN | Returned `False`; requested helper is not present in this AIDE repo. |
| `Test-Path scripts/eureka_test_select.py` | NOT_RUN | Returned `False`; Eureka-specific helper is not present in this AIDE repo. |

## Generated Drift Handling

Preflight status commands refreshed Task OS and Git helper reports. Those files
were outside the WorkUnit deliverable and were restored before implementation.
Final validation left no generated report drift outside the allowed paths.
