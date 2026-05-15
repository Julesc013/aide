# Validation Evidence

## Summary

Validation result: PASS_WITH_WARNINGS.

The warnings are classified and do not block Q49 preflight. They do block any claim that AIDE is officially published or that Q36-Q48 have passed review.

## Passing Gates

- AIDE Lite core validation: PASS.
- AIDE Lite canonical tests: PASS.
- AIDE Lite selftest: PASS.
- Golden tasks: PASS, 132/132.
- Install model validation: PASS.
- Repair model validation: PASS.
- Upgrade model validation: PASS.
- Rollback model validation: PASS.
- Uninstall model validation: PASS.
- Pack status: PASS.
- Release validation: PASS.
- Release draft validation: PASS.
- Harness/core/compat/gateway/provider tests: PASS.
- Secret/local-state scan: PASS_AFTER_INSPECTION.

## Warnings

- `scripts/aide validate`, `doctor`, and `self-check` report inherited generated manifest freshness warnings.
- `repo validate` reports unknown classifications.
- `quality ledger` reports advisory quality warnings.
- `commit check --range HEAD~20..HEAD` fails on two older malformed commits; `commit check --latest` passes.
- Changelog preview records malformed historical commits; changelog validation passes and remains preview-only.
- Broad unittest discovery under `.aide/scripts/tests` timed out; canonical `.aide/scripts/aide_lite.py test` passes.
- Git helpers report dirty tree during the audit, expected while writing QCHECK artifacts.
- `origin/main` is behind local `main`; QCHECK did not push.

## Final Validation Rerun

Final validation after writing QCHECK artifacts:

| Command | Result |
|---|---|
| `git diff --check` | PASS |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py test` | PASS |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS |
| `py -3 .aide/scripts/aide_lite.py release validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py install validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py repair validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q49 Dominium Fresh Install Preflight"` | PASS |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS |
| targeted secret scan | PASS_AFTER_INSPECTION; 3749 policy/example/test/doc matches, no actual secrets |
| post-commit `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS |

Generated validation/status churn was restored before staging so the audit commit remains scoped.
