# Plan Generator Design

The plan-generation model is deterministic, offline, and no-apply.

Inputs:

- `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/source-pack/manifest.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/*.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/*.rollback.json`
- `.aide/apply/lifecycle-plan.schema.json`

Outputs:

- `.aide/examples/apply/lifecycle-fixtures/generated-plans/*.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/plan-index.json`
- `.aide/reports/lifecycle-fixture-plans/*.plan-report.json`
- `.aide/reports/lifecycle-fixture-plans/plan-generation-report.*`
- `.aide/reports/lifecycle-fixture-plans/plan-validation.*`

No generator CLI command was implemented. The artifacts were generated as deterministic checked-in plan examples from reviewed fixture metadata. The generated plans use `mode` values `dry-run` or `report`, keep `fixture_only=true`, and carry explicit false flags for target mutation, lifecycle apply execution, scoped transaction apply execution, and rollback execution.

Limitations:

- These are static generated plan artifacts, not live planner output from an executable command.
- Multi-file lifecycle apply orchestration remains unimplemented.
- Rollback execution and uninstall/delete execution remain prohibited.
- Target repo and active repo apply authority remains absent.
