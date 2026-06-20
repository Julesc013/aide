# Critical-Path Task Graph

The full machine-readable graph is in `critical-path.json`.

Order:

1. Charter closure: `AIDE-CHECK-DOMINIUM-INTEGRATION-CHARTER-01`, then `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01`.
2. Read-only seam: build/check/accept `AIDE-DOMINIUM-READONLY-SEAM-V0`.
3. Validation slice: build/check/accept `AIDE-DOMINIUM-WORKUNIT-VALIDATION-SLICE`.
4. Read-only Workbench: build/check/accept `AIDE-BUILD-WORKBENCH-READONLY-01`.
5. Durable local substrate: local store then local service foundations.
6. Trust and invocation: PrincipalIdentity, AdmissionRecord, PolicyDecision, CapabilityGrant, CapabilityInvocation, ExecutionReceipt, RevocationRecord.
7. Preview: DevelopmentTransaction and PreviewSession.
8. First mutation: Dominium document preview/apply/rollback.
9. Scene hero workflow: scene preview/apply/undo evidence.

Downstream queue directories were not created.
