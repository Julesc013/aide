# Validation

Task: AIDE-CHECK-APPLY-00-transaction-model-review

## Preflight Results

- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "...AIDE-CHECK-APPLY-00..."` - PASS; task_class docs, risk_class high, sizing_class audit_only, safe_to_execute true.
- `py -3 .aide/scripts/aide_lite.py git plan` - report-only, blocked by dirty_tree_requires_classification after generated preflight reports; no branch, worktree, push, or remote mutation.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; report-only.
- Initial command-surface search - FAIL due malformed `rg` regex quoting; no state change.
- Corrected command-surface search - PASS; no transaction apply implementation found.

## Final Validation

- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS; report_only, `real_repo_apply_allowed: false`, no target/branch mutation, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py transaction validate` - PASS; 489 checks, report_only, no target/branch mutation, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_no_real_apply_golden` - PASS; 15/15 checks.
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_export_pack_inclusion_golden` - PASS; 102/102 checks.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 .aide/scripts/aide_lite.py eval run` - PASS; 164/164 golden tasks.
- `py -3 .aide/scripts/aide_lite.py test` - PASS.
- `py -3 .aide/scripts/aide_lite.py selftest` - PASS.
- `py -3 .aide/scripts/aide_lite.py verify` - WARN on first run because full golden validation refreshed capability reports outside the initial checkpoint allowlist.
- Allowlist adjustment - PASS; added `.aide/reports/capability-*.md` after inspecting the diffs and confirming they only refreshed deterministic report metadata from commit `cd7c7bfcc4a27927e865a86df88b3a0e92ffa892` to `ce8e207116684b562887dccd8c0c3ebc8bb5726e`.
- `py -3 .aide/scripts/aide_lite.py verify` - PASS after allowlist adjustment; final checked_files 89, changed_files 44, warnings 0, errors 0.
- `py -3 .aide/scripts/aide_lite.py review-pack` - PASS; wrote `.aide/context/latest-review-packet.md`, final approx_tokens 2111, verifier_result PASS.
- `py -3 .aide/scripts/aide_lite.py route explain` - PASS as advisory-only; verifier_status PASS, golden_task_status PASS, provider/model/network calls none; quality_gate_status WARN because token_budget_status is over_budget.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; task_count 65, checkpoint status `needs_review`, latest_task_id `AIDE-APPLY-01`.
- `py -3 .aide/scripts/aide_lite.py doctor` - PASS.
- `py -3 scripts/aide validate` - PASS_WITH_WARNINGS; known `GENERATED-SOURCE-STALE` warning for `.aide/generated/manifest.yaml`.

## Pending Commit Hygiene

- `git diff --check` - PASS.
- targeted secret scan over changed files - PASS; no secret-like patterns found.
- `py -3 .aide/scripts/aide_lite.py commit check --message`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
