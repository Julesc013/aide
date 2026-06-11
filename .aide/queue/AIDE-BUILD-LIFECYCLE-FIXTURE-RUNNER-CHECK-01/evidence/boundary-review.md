# Boundary Review

Result: `PASS`

Hash evidence:

| Path | Before | After |
| --- | --- | --- |
| `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/manual/with-managed-section.md` | `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60` | `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60` |
| `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/manual/with-managed-section.md` | `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b` | `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b` |
| `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json` | `sha256:04b31be8dcdad7c0e8c27993f4cfabda5414f0b0ecf8bab81e28968a877eb2b6` | `sha256:04b31be8dcdad7c0e8c27993f4cfabda5414f0b0ecf8bab81e28968a877eb2b6` |
| `.aide/reports/lifecycle-fixture-runner/workspaces/latest/manual/with-managed-section.md` | not canonical | `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b` |

Boundary results:

- canonical fixture mutation: not observed
- canonical expected fixture mutation: not observed
- generated plan mutation: not observed
- temp fixture mutation: observed under report workspace
- temp postimage matches expected postimage: verified
- manual content preservation: verified by runner report
- active repo apply: not observed
- target repo mutation: not observed
- rollback execution: not implemented and not executed
- branch/worktree mutation: not observed
