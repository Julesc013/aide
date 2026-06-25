# AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01

## Objective

Close exactly the nine material findings from `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01` without starting ProjectLock v0 or accepting DistributionManifest v1.

## Scope

Allowed implementation scope is limited to the DistributionManifest v1 schema, helper, fixtures, focused tests, generated DistributionManifest v1 reports, this repair task packet, queue index routing, and focused planning/execution logs.

## Frozen Finding Matrix

The machine-readable oracle is `evidence/finding-matrix.json`. No production edit begins until each finding has an implementation target, positive test, negative test, and evidence artifact.

## Execution Steps

1. Confirm baseline and source check findings.
2. Materialize task-local turn context, allowed paths, stop conditions, validation plan, finding matrix, and campaign state.
3. Add failing-focused tests for the nine findings.
4. Repair schema/helper/fixtures in the smallest coherent diff.
5. Regenerate DistributionManifest v1 reports and fixture corpus.
6. Run focused and broad validation.
7. Write evidence and stop at `needs_review`, recommending exactly `AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-REPAIR-01`.

## Non-Capabilities

This repair does not implement install/update/repair/rollback/uninstall apply, release publication, target mutation, network calls, provider/model calls, Workbench/MCP runtime, source-change preview/apply/rollback, ProjectLock v0, or acceptance.
