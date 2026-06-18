# Validation Results

## Result

`PASS_WITH_WARNINGS`

## Command Results

| Check | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Dirty paths are limited to allowed acceptance outputs. |
| `git diff --check` | PASS_WITH_WARNING | Reports the known `.aide/queue/index.yaml` line-ending warning only. |
| `git diff --cached --check` | PASS | No staged whitespace errors. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Doctor status passed. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Repository validation status passed. |
| `task inspect` for build task | PASS | Status `needs_review`; `missing_evidence: 0`. |
| `task evidence` for build task | PASS | Expected evidence present. |
| `task inspect` for check task | PASS | Status `needs_review`; `missing_evidence: 0`. |
| `task evidence` for check task | PASS | Expected evidence present. |
| JSON parse checks | PASS | Check, findings, and acceptance reports parse. |
| YAML parse checks | PASS | Self-management policy, queue index, and acceptance task files parse. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS | Latest pre-acceptance commit passed policy check. |

## Conclusion

The acceptance gate can stop at `needs_review` with result
`ACCEPTED_WITH_WARNINGS`. The accepted warning is limited to the already
classified queue-index line-ending warning; it does not affect charter
authority, acceptance scope, evidence completeness, or next-task routing.
