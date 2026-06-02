# Validation

Result: PARTIAL_NEEDS_REPAIR.

Validation commands passed except explicitly unsupported command forms. The readiness blocker is report consistency, not a runtime validation failure.

Passed highlights:

- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 158/158.
- Post-artifact rerun of `doctor`, `validate`, `test`, `selftest`, and `eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 89 checked files, 52 changed files, 0 warnings, 0 errors.
- `git diff --check`: PASS after final evidence edits.
- Targeted secret scan: PASS; no matches after excluding the evidence file that records the scan pattern.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 325 tests in 603.233 seconds.
- All Task OS commands: PASS as report-only.
- All capability commands: PASS as report-only.
- `pack-status`: PASS.
- `release validate`: PASS.
- `release draft-validate`: PASS.
- `install/repair/upgrade/rollback/uninstall validate`: PASS.
- `commit check --latest`: PASS.
- `changelog preview` and `changelog validate`: PASS.

Unsupported or expected advisory results:

- `test plan`: unsupported exact subcommand; `tier-plan` and `impact-plan` passed.
- `test summary-validate` without `--file`: unsupported input; explicit example validation passed.
- `git plan`: BLOCKED advisory due dirty checkpoint tree; dry_run true and no mutation.
- `pack --task "AIDE-FIX-OS-03 ..."`: PASS; latest task packet points to the repair task; budget PASS.

Blocking readiness issue:

- Task OS checkpoint/next-plan reports are stale relative to X-OS-02 truth and must be repaired before AIDE-APPLY-00.
- Latest task parsing also reduces `AIDE-FIX-OS-03` to `X-OS-03`; the repair should make generated reports use canonical queue ids.
