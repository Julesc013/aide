# Schema Summary

Created schema files:

- `.aide/apply/lifecycle-manifest.schema.json`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/apply/lifecycle-report.schema.json`
- `.aide/apply/lifecycle-rollback-record.schema.json`

Created non-mutating examples:

- `.aide/examples/apply/lifecycle/lifecycle-manifest.example.json`
- `.aide/examples/apply/lifecycle/lifecycle-plan.report-only.example.json`
- `.aide/examples/apply/lifecycle/lifecycle-report.report-only.example.json`
- `.aide/examples/apply/lifecycle/lifecycle-rollback-record.example.json`
- `.aide/examples/apply/lifecycle/fixture-repository-spec.example.json`

The schemas require explicit paths, allowed roots, protected roots, preimage hash requirements, postimage hash requirements, rollback-compatible record references, evidence, review gates, and capability labels. They distinguish report, dry-run, fixture-apply, active-repo-apply, and target-apply modes as schema labels only. Active repo apply and target apply remain blocked until future reviewed authority exists.
