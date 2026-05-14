# Remaining Risks

- This is a bounded performance hotfix, not a complete repo-wide optimization pass.
- `eval run` still executes the full golden-task catalog and remains intentionally heavier than selftest.
- Additional performance work should be split into follow-up WorkUnits for inventory scanning, golden-task data caching, and harness subprocess cost.
