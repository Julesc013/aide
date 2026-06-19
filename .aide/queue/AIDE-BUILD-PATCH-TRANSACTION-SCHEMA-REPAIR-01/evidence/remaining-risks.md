# Remaining Risks

Remaining warning-class items:

- PatchTransaction remains schema/projection/validation only.
- Full JSON Schema Draft validation remains absent.
- General diff parsing remains absent.
- Artifact resolution and VCS reachability checks remain absent.
- Policy evaluation, approval, apply, rollback, event store, admission, trust,
  and runtime behavior remain absent.
- The repair still requires independent recheck before PatchTransaction
  acceptance can resume.

Recommended next task:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```
