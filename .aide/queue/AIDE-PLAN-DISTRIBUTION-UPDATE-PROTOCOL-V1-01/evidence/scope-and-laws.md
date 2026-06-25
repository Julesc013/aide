# Scope And Laws

## Frozen Laws

- Unknown ownership blocks automatic apply.
- Install does not imply admission.
- Conformance does not imply authorization.
- An approved plan cannot expand its scope during apply.
- Project-owned data is never silently overwritten or deleted.
- Managed sections are modified only through exact managed-section identity.
- Source-generated AIDE state is not copied into a target as target truth.
- Every update has a preimage, postimage, evidence, and rollback path.
- The AIDE source repository is never treated as the installed-target fixture.

## Plan Scope

This task normalizes a future v1 object model and queue dependency graph over
the existing Q43-Q48 foundation. It does not replace Q43-Q48 and does not
authorize implementation.

## Out Of Scope

- install/update/repair/rollback/uninstall apply
- release publication
- Git tags or GitHub Releases
- network or provider/model calls
- target repository mutation
- Workbench or MCP runtime
- source-change preview/apply/rollback
- public stable release readiness
