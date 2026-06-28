# Validation Commands

Focused build validation:

- `py -3 -m py_compile core/distribution/apply_engine.py core/distribution/temp_workspace.py core/distribution/operation_executor.py core/distribution/rollback_verifier.py core/distribution/apply_reports.py .aide/scripts/tests/test_aide_distribution_apply_engine_v0.py .aide/scripts/aide_lite.py`
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_distribution_apply_engine_v0.py"`
- `py -3 .aide/scripts/aide_lite.py distribution-apply status`
- `py -3 .aide/scripts/aide_lite.py distribution-apply plan --scenario managed-file-update`
- `py -3 .aide/scripts/aide_lite.py distribution-apply run --scenario managed-file-update --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py distribution-apply verify`

Predecessor regression validation:

- `distribution-manifest status/project/validate`
- `project-lock status/project/validate`
- `ownership-ledger status/project/validate/migrate-q43`
- `install-record status/project/validate`
- `migration-record status/project/validate`
- `update-plan status/project/validate`
- `rollback-bundle status/project/validate`
- `update-receipt status/project/validate`

Boundary and broad validation:

- `install validate`
- `repair validate`
- `upgrade validate`
- `rollback validate`
- `uninstall validate`
- `release validate`
- `release draft-validate`
- `release publication-boundary`
- `py -3 .aide/scripts/aide_lite.py validate`

Final hygiene validation:

- task inspect/evidence
- path scan over changed reports/evidence
- credential-pattern scan over changed reports/evidence
- source-output misuse scan
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py commit check --latest`
