# Changed Files

Expected X-TEST-00 paths:

- `.aide/queue/index.yaml`
- `.aide/queue/X-TEST-00-aide-cross-repo-validation-tier-model-v0/**`
- `.aide/policies/test-tiers.yaml`
- `.aide/policies/impacted-tests.yaml`
- `.aide/policies/test-telemetry.yaml`
- `.aide/policies/full-discovery-handoff.yaml`
- `.aide/policies/test-summary-reduction.yaml`
- `.aide/policies/validation-promotion-gates.yaml`
- `.aide/policies/file-classification.yaml`
- `.aide/tests/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_x_test_00_validation_tiers.py`
- `.aide/evals/golden-tasks/**`
- `.aide/commands/catalog.yaml`
- `.aide/reports/x-test-00-*.md`
- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/verification/latest-verification-report.md`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`
- `.aide/changelog/*preview*` and `.aide/changelog/latest-changelog-report.md`
- `.aide/github/github-advisory.*`
- `.aide/generated/manifest.yaml`
- `.aide/repo/file-inventory.json` and related repo intelligence reports refreshed to remove unknown classifications.
- `docs/reference/validation-tier-model.md`
- `docs/reference/test-telemetry-contracts.md`
- `docs/reference/impacted-test-planning.md`
- `docs/reference/full-discovery-handoff.md`
- `docs/reference/promotion-validation-gates.md`

Safe generated validation artifacts may also refresh during required validation.
