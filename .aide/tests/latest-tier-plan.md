# AIDE Validation Tier Plan

- mode: report_only
- repo: aide
- commit: eb100b4e315dd0fa1da5eaeed7ab2116d0c991a1
- branch: main
- normal_post_task: T0 + T1
- larger_task: T0 + T1 + relevant T2
- promotion_checkpoint_release: T0 + T1 + relevant T2 + T3
- full_suite_default: T3 promotion only
- report_only: true
- no_target_execution: true

## Tiers

- T0: smoke_syntax_policy_architecture - Fast checks that prove basic repo shape, syntax, policy anchors, and report-only boundaries.
- T1: impacted_tests - Changed-path-driven tests selected by the impacted-test plan without claiming complete proof.
- T2: component_integration - Component or integration suites relevant to larger or cross-cutting changes.
- T3: full_promotion_suite - Full discovery, checkpoint, promotion, or release validation with compact telemetry.
