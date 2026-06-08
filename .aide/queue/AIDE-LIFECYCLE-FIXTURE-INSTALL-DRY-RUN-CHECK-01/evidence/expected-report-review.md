# Expected Report Review

Result: `PASS_WITH_WARNINGS`

- Generated plan reports checked: 5.
- Static expected reports checked: 3.
- Missing static expected report refs: `install-clean`, `install-existing-manual-preserved`.
- Missing refs classification: non-blocking for checkpoint acceptance; repair-worthy as a future evidence-completeness improvement.
- Status and blocker matches: PASS.
- Mutation-state result: PASS; reports preserve no-apply booleans.
- Overclaim result: PASS; no reviewed report claims production-ready, release-ready, install apply implemented, or lifecycle apply implemented.

The static expected reports do not use a `scenario_id` field; the review matches them through `lifecycle_plan_id`, status, blocked reason, and report paths.
