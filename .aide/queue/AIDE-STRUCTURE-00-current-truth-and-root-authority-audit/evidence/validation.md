# Validation

## Commands Run

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short --branch` | PASS | Initial tree was clean on `main`; later dirty state is task-owned. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | No hard doctor failures. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Broad validation passed; output is large. |
| `py -3 .aide/scripts/aide_lite.py pack --task "AIDE-STRUCTURE-00-current-truth-and-root-authority-audit"` | PASS | Wrote latest task packet; packet was then corrected to this task's exact queue scope. |
| `py -3 .aide/scripts/aide_lite.py git plan` | BLOCKED_EXPECTED | Dry-run helper blocked on dirty tree classification after task artifacts were created. No branch mutation occurred. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` | PASS_WITH_MISSING_EVIDENCE_INITIAL | Expected before required evidence files were complete. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` | PASS_WITH_MISSING_EVIDENCE_INITIAL | Expected before required evidence files were complete. |
| `py -3 .aide/scripts/aide_lite.py repo inventory` | PASS | file_count=5136, unknown_count=0, orphan_candidate_count=608. |
| `py -3 .aide/scripts/aide_lite.py repo status` | PASS | generated_count=943, evidence_count=2687. |
| `py -3 .aide/scripts/aide_lite.py repo validate` | PASS | Repo intelligence validation passed. |
| `py -3 .aide/scripts/aide_lite.py roots inventory` | PASS | root_count=22, file_count=5136, no_apply=true. |
| `py -3 .aide/scripts/aide_lite.py roots classify` | PASS | review_required_file_count=5047. |
| `py -3 .aide/scripts/aide_lite.py roots plan` | PASS | no_apply=true; no moves, deletes, or rewrites. |
| `py -3 .aide/scripts/aide_lite.py roots status` | PASS | mixed_root_count=3, unknown_root_count=19, high_risk_root_count=15. |
| `py -3 .aide/scripts/aide_lite.py roots validate` | PASS | Root recycling validation passed. |
| `py -3 .aide/scripts/aide_lite.py refactor status` | PASS | no_apply=true, apply_available_in_q39=false. |
| `py -3 .aide/scripts/aide_lite.py refactor map-status` | PASS | move_entries=0, salvage_entries=20, aliases=0, rewrite_entries=40. |
| `py -3 .aide/scripts/aide_lite.py refactor validate-map` | PASS | No-apply map validation passed. |
| `py -3 .aide/scripts/aide_lite.py reconciler status` | PASS_WITH_WARNINGS | Existing Reconciler surface is report-only. |
| `py -3 .aide/scripts/aide_lite.py reconciler report` | PASS_WITH_WARNINGS | findings_count=4; no repair or mutation. |
| `py -3 .aide/scripts/aide_lite.py reconciler validate` | PASS_WITH_WARNINGS | Report-only boundary preserved. |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS | task_count=141; latest_task_id is this audit. |
| `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` | PASS | status=needs_review, classification=complete, missing_evidence=0. |
| `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-STRUCTURE-00-current-truth-and-root-authority-audit` | PASS | Required evidence files present. |
| `git diff --check` | PASS_WITH_WARNING | No whitespace errors; Git warned that `.aide/queue/index.yaml` line endings will be normalized from CRLF to LF when touched. |
| `py -3 .aide/scripts/aide_lite.py validate` | FAIL_THEN_PASS | First final run failed because the latest task packet used `FORBIDDEN_PATHS_AND_ACTIONS` and lacked `TOKEN_ESTIMATE`; packet was fixed and the rerun passed. |

## Final Validation Result

PASS_WITH_WARNINGS.

Warnings are limited to recorded report-only drift, expected Git helper dirty
tree blocking before commit, and the line-ending warning on `.aide/queue/index.yaml`.
