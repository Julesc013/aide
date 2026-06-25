# Security And Preservation Invariants

- Unknown ownership blocks automatic apply.
- Project-owned data is never silently overwritten or deleted.
- Managed sections require exact managed-section identity.
- Approved plan digest must match apply input.
- Apply cannot discover or add extra operations.
- Every mutable operation requires preimage and postimage evidence.
- Rollback bundle must exist before apply.
- Source-generated AIDE state is never copied into a target as target truth.
- `.aide.local/**`, `.env`, secrets, raw prompts, and raw responses are never
  packaged or mutated.
- Network, provider/model, upload, GitHub Release, and tag creation require
  separate reviewed authority.
- Release artifacts remain no-publish until an explicit publication gate.
- AIDE source repo is never treated as an installed-target fixture.
