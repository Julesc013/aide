# Impact Planning Evidence

Command:

- `py -3 .aide/scripts/aide_lite.py test impact-plan --from HEAD`

Result:

- PASS.
- Wrote `.aide/tests/latest-impact-plan.json` and `.aide/tests/latest-impact-plan.md`.
- Recommended tier: `T1`.
- Changed-path count in the dirty working tree: 141.
- Proof status: `plan_not_proof`.
- Target test execution: false.

The planner includes committed-ref diff, staged changes, unstaged changes, and untracked files, then maps changed paths to report-only test recommendations.
