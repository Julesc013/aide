# Candidate Selection

Selected candidate: `install-managed-section`

Rejected for first apply:

- Broad install scenarios: broader write surface.
- Upgrade scenarios: depend on more lifecycle semantics.
- Repair scenarios: blocked-condition checks, not first mutation proof.
- Rollback scenarios: should follow an apply proof with rollback record evidence.
- Uninstall scenarios: delete semantics are higher risk.

`install-managed-section` is the smallest available fixture mutation proof because it is a single managed-section update with explicit hashes and rollback evidence.
