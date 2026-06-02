# Validation

Task: AIDE-APPLY-00-transaction-model

## Focused Transaction Checks

- `py -3 -m py_compile .aide/scripts/aide_lite.py` - PASS
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_00_transaction_model.py` - PASS, 5 tests
- `py -3 .aide/scripts/aide_lite.py transaction status` - PASS
- `py -3 .aide/scripts/aide_lite.py transaction fixture-plan` - PASS
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify` - PASS, 225 checks
- `py -3 .aide/scripts/aide_lite.py transaction validate` - PASS, 489 checks

## Focused Golden Tasks

- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_schema_presence_golden` - PASS, 50/50
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_policy_boundary_golden` - PASS, 44/44
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_fixture_plan_golden` - PASS, 7/7
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_fixture_verify_golden` - PASS, 227/227
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_no_real_apply_golden` - PASS, 15/15
- `py -3 .aide/scripts/aide_lite.py eval run --task transaction_export_pack_inclusion_golden` - PASS, 102/102

## Repository Checks

- `git diff --check` - PASS
- `py -3 .aide/scripts/aide_lite.py doctor` - PASS
- `py -3 .aide/scripts/aide_lite.py validate` - PASS
- `py -3 .aide/scripts/aide_lite.py test` - PASS
- `py -3 .aide/scripts/aide_lite.py selftest` - PASS
- `py -3 .aide/scripts/aide_lite.py eval run` - PASS, 164/164 golden tasks
- `py -3 .aide/scripts/aide_lite.py task status` - PASS, latest_task_id AIDE-APPLY-01
- `py -3 .aide/scripts/aide_lite.py capability validate` - PASS
- `py -3 .aide/scripts/aide_lite.py pack-status` - PASS, checksums_valid true, boundary_result PASS
- `py -3 .aide/scripts/aide_lite.py release validate` - PASS
- `py -3 .aide/scripts/aide_lite.py release draft-validate` - PASS
- `py -3 .aide/scripts/aide_lite.py install validate` - PASS
- `py -3 .aide/scripts/aide_lite.py repair validate` - PASS
- `py -3 .aide/scripts/aide_lite.py upgrade validate` - PASS
- `py -3 .aide/scripts/aide_lite.py rollback validate` - PASS
- `py -3 .aide/scripts/aide_lite.py uninstall validate` - PASS
- `py -3 scripts/aide validate` - PASS_WITH_WARNINGS
- `py -3 .aide/scripts/aide_lite.py verify` - PASS, checked_files 89, changed_files 157, warnings 0, errors 0
- `py -3 .aide/scripts/aide_lite.py review-pack` - PASS, wrote `.aide/context/latest-review-packet.md`, approx_tokens 2172, budget_status PASS, verifier_result PASS
- `py -3 .aide/scripts/aide_lite.py route explain` - PASS advisory route, route_class frontier, verifier_status PASS, golden_task_status PASS, provider/model calls none, network calls none
- Targeted `rg` secret scan over the new transaction, policy, docs, test, and queue evidence surfaces - PASS, no matches

## Validation Caveats

- `py -3 scripts/aide validate` reported the existing Harness v0 warning `GENERATED-SOURCE-STALE` for `.aide/generated/manifest.yaml`.
- `route explain` reported `token_budget_status: over_budget` and `quality_gate_status: WARN` for the compact prompt/advisory route posture. It remained advisory-only and no-call.
- An initial `verify` run warned that validation-generated task OS, capability, git-helper, routing, review, and eval-run reports were not covered by AIDE-APPLY-00 `allowed_paths`. The queue task scope was corrected for those generated validation artifacts, and the final `verify` run passed with zero warnings.
- The transaction model validates schema shape, required files, command registration, fixture records, export-pack inclusion, and no-real-apply boundaries. It does not authorize or execute real file writes.
- One unsupported exploratory command form was attempted during task discovery: `task inspect AIDE-FIX-OS-03...`; the supported syntax requires `--task-id`. No repository state changed from that failed command.
