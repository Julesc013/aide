# Validation Evidence

- final_status: PASS_WITH_WARNINGS
- initial_doctor_validate_failure: stale generated managed-section validation report wording contained literal forbidden-marker strings while describing their absence
- repair_action: existing `managed-section fixture-verify` command refreshed `.aide/reports/managed-section-fixture-validation.md`
- rerun_status: `doctor` PASS, `validate` PASS

## Passed Commands

| Command | Result |
| --- | --- |
| `git status --short --branch` | PASS |
| `git log --oneline -50` | PASS |
| `git remote -v` | PASS |
| `git rev-parse HEAD` | PASS |
| `git rev-parse --show-toplevel` | PASS |
| `git tag --list` | PASS |
| `git diff --check` | PASS |
| `git check-ignore -v tmp/` | PASS |
| `git check-ignore -v tmp/*` | PASS |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS after rerun |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS after rerun |
| `py -3 .aide/scripts/aide_lite.py test` | PASS |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS, 171/171 |
| `py -3 .aide/scripts/aide_lite.py managed-section status` | PASS |
| `py -3 .aide/scripts/aide_lite.py managed-section validate` | PASS, 333 checks |
| `py -3 .aide/scripts/aide_lite.py managed-section fixture-plan` | PASS |
| `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify` | PASS, 138 checks |
| `py -3 .aide/scripts/aide_lite.py transaction status` | PASS |
| `py -3 .aide/scripts/aide_lite.py transaction validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py transaction fixture-plan` | PASS |
| `py -3 .aide/scripts/aide_lite.py transaction fixture-verify` | PASS |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS with expected dirty-source provenance |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py capability validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py task status` | PASS |
| `py -3 -m unittest discover -s core/apply/tests -t .` | PASS, 10 tests |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_01_managed_sections.py` | PASS, 6 tests |
| targeted high-confidence secret scan | PASS |

## Warning Classification

- expected_generated_state: stale managed-section validation report wording was refreshed; generated reports also update source commit and latest-task references.
- expected_review_gate: AIDE-APPLY-01 and AIDE-CHECK-APPLY-01 remain `needs_review`.
- expected_dirty_pack_provenance: pack-status records dirty source before the checkpoint commit.
- fixture_only_patch: managed-section patch behavior remains fixture-only.
- managed_section_note: accepted with notes, not unconditional production apply readiness.
- assigned_next: latest task packet advances to AIDE-APPLY-02.
