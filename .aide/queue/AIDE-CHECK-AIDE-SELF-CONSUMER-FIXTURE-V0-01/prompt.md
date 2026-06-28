# Prompt: AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01

Create and process `AIDE-CHECK-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.

Use live `.aide/queue/index.yaml` as canonical truth.

Review `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01` independently.

Scope:

- check-only
- no implementation except task-local evidence/report generation if required
- no real target apply
- no AIDE source repo self-apply
- no ScreenSave/Eureka/Dominium canary
- no release artifact generation
- no public release
- no network/provider/model calls
- no branch/worktree automation
- no push
- no target repo mutation

Verify fixture structure, lifecycle scenario coverage, DistributionApplyEngine binding and receipt boundaries, canonical fixture preservation, target-owned state preservation, Q43-Q48 no-apply/no-publish validators, broad validation, task evidence completeness, and absence of overclaiming.

Expected result: `PASS`, `PASS_WITH_WARNINGS`, `FAILED_VALIDATION`, `BLOCKED`, or `PARTIAL`.

If `PASS` or `PASS_WITH_WARNINGS`, recommend exactly `AIDE-ACCEPT-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.

If `FAILED_VALIDATION`, recommend exactly `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-REPAIR-01`.

Stop at `needs_review` with evidence.
