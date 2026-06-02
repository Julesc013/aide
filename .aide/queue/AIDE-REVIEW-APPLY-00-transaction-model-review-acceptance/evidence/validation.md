# Validation

Task: AIDE-REVIEW-APPLY-00-transaction-model-review-acceptance

## Required Commands

- `git status --short --branch`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 .aide/scripts/aide_lite.py eval run`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py transaction fixture-plan`
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`
- `py -3 .aide/scripts/aide_lite.py verify`
- `py -3 .aide/scripts/aide_lite.py review-pack`
- `py -3 .aide/scripts/aide_lite.py pack-status`
- `py -3 .aide/scripts/aide_lite.py release validate`
- `py -3 .aide/scripts/aide_lite.py release draft-validate`
- `py -3 .aide/scripts/aide_lite.py install validate`
- `py -3 .aide/scripts/aide_lite.py repair validate`
- `py -3 .aide/scripts/aide_lite.py upgrade validate`
- `py -3 .aide/scripts/aide_lite.py rollback validate`
- `py -3 .aide/scripts/aide_lite.py uninstall validate`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
- targeted secret scan

## Results

- `git status --short --branch` - PASS; branch `main`, review/report artifacts dirty before commit.
- `git diff --check` - PASS.
- `py -3 .aide/scripts/aide_lite.py doctor` - PASS.
- `py -3 .aide/scripts/aide_lite.py validate` - PASS.
- `py -3 .aide/scripts/aide_lite.py test` - PASS.
- `py -3 .aide/scripts/aide_lite.py selftest` - PASS.
- `py -3 .aide/scripts/aide_lite.py eval run` - PASS; 164/164 golden tasks.
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS; report_only, `real_repo_apply_allowed: false`, no target/branch mutation, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py transaction validate` - PASS; 489 checks.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-plan` - PASS; fixture_only, real_repo_apply_allowed false.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify` - PASS; 225 checks.
- `py -3 .aide/scripts/aide_lite.py verify` - PASS; final checked_files 89, changed_files 47, warnings 0, errors 0.
- `py -3 .aide/scripts/aide_lite.py review-pack` - PASS; wrote `.aide/context/latest-review-packet.md`, final approx_tokens 2111, verifier_result PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status` - PASS; checksums_valid true, boundary_result PASS, provenance_result DIRTY_SOURCE_RECORDED.
- `py -3 .aide/scripts/aide_lite.py release validate` - PASS; no_publish true, tag_created false, github_release_created false, upload_performed false.
- `py -3 .aide/scripts/aide_lite.py release draft-validate` - PASS; no_publish true, tag_created false, github_release_created false, upload_performed false, network_api_call false.
- `py -3 .aide/scripts/aide_lite.py install validate` - PASS; no_apply true, target_mutation false, overwrite_allowed_default false, migration_automatic false.
- `py -3 .aide/scripts/aide_lite.py repair validate` - PASS; no_apply true, target_mutation false, overwrite_allowed_default false, delete_allowed_default false, migration_automatic false.
- `py -3 .aide/scripts/aide_lite.py upgrade validate` - PASS; no_apply true, target_mutation false, overwrite_allowed_default false, delete_allowed_default false, migration_automatic false.
- `py -3 .aide/scripts/aide_lite.py rollback validate` - PASS; no_apply true, target_mutation false, overwrite_allowed_default false, delete_allowed_default false, managed_section_removal_allowed_default false.
- `py -3 .aide/scripts/aide_lite.py uninstall validate` - PASS; no_apply true, target_mutation false, delete_allowed_default false, managed_section_removal_allowed_default false, blanket_aide_deletion false.
- `py -3 .aide/scripts/aide_lite.py task status` - PASS; task_count 66, AIDE-REVIEW-APPLY-00 status `needs_review`, latest_task_id `AIDE-APPLY-01`.
- `py -3 scripts/aide validate` - PASS_WITH_WARNINGS; known `GENERATED-SOURCE-STALE` warning for `.aide/generated/manifest.yaml`.
- `py -3 .aide/scripts/aide_lite.py commit check --latest` - PASS for current pre-commit HEAD.
- `py -3 .aide/scripts/aide_lite.py commit check --message` - PASS for planned structured commit message.
- targeted secret scan over changed files - PASS after removing a self-match from `evidence/secret-scan.md`; no secret-like values found.

## Notes

- The broad contradiction search found expected no-apply boundary/proof prose.
- A corrected targeted forbidden marker search found proof statements and validator forbidden-string checks only; the initial targeted search form failed due PowerShell regex quoting and did not change repository state.
- `.aide/reports/aide-apply-00-readiness.md` remains a stale historical generated report from the earlier Task OS checkpoint and is superseded by queue state and current transaction reports.
- Post-commit `commit check --latest` remains pending until the structured commit exists.
