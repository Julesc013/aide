# Manual Preservation Review

Result: `PASS`

Ownership distinction result:

- Install rollback record uses ownership `managed-section`.
- Upgrade rollback record uses ownership `generated-file`.
- Unknown ownership is an unsupported rollback reason.

Manual content preservation result:

- Managed-section rollback record states outside-marker content is not owned by AIDE.
- Generated-file rollback record states manual files remain out of scope.

Unknown file/delete result:

- Unknown ownership and target truth replacement are unsupported rollback reasons.

Broad-delete blocked result:

- `broad delete` is recorded as an unsupported rollback reason.

Defects: none.
