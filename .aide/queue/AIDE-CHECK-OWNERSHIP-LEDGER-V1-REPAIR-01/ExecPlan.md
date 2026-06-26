# AIDE-CHECK-OWNERSHIP-LEDGER-V1-REPAIR-01 ExecPlan

## Objective

Independently verify whether `AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01` closes the five material findings from `AIDE-CHECK-OWNERSHIP-LEDGER-V1-01` without accepting `ownership_ledger_v1` or starting downstream distribution objects.

## Scope

Allowed writes are limited to this check task packet, this check report directory, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

Forbidden writes include the OwnershipLedger schema, helper, tests, fixtures, source reports, repair reports, Q43-Q48 implementation, release archives, target repositories, ScreenSave, Eureka, and Dominium.

## Independent Checks

- Verify source task baseline, status, evidence, and routing.
- Verify exactly five source findings and exactly five repair dispositions.
- Inspect schema/helper/projection alignment for repaired file-entry and managed-section fields.
- Exercise production behavior as the system under test for direct repaired edge cases.
- Recompute check-local digests for committed OwnershipLedger reports.
- Verify Q43 migration mapping, manual-review handling, unmapped refusal, and no-apply boundary.
- Verify conflict fixtures and direct behavior for path/case/file-section/section/link/source/evidence failures.
- Verify fixture corpus coverage and deterministic validation results.
- Run focused tests, CLI validation, regression validation, broad validation, diff checks, task inspect/evidence, and commit policy.

## Stop Conditions

Stop at `needs_review`.

If all five findings close with zero material findings, recommend exactly `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`.

If any material finding remains, recommend exactly `AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-02`.
