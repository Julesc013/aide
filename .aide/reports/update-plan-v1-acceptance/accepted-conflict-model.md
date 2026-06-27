# Accepted Conflict And Manual-Review Model

Accepted fail-closed behavior includes:

- unknown ownership cannot be auto-updated;
- never-touch targets are refused;
- project-owned, project-overlay, local-only, runtime-generated, evidence-only, and preserved legacy content cannot be overwritten by managed update operations;
- case collisions fail closed;
- symlink/reparse uncertainty fails closed;
- path traversal and absolute paths fail closed;
- predecessor mismatches fail closed;
- missing required digests and rollback requirements fail closed;
- unknown required features and required extensions fail closed;
- source output cannot become target truth;
- apply authority and target mutation claims fail closed.

The accepted live projection includes two warning-class conflicts:

- `.git/**` as `never_touch_refusal`
- `unclassified/**` as `manual_review_required`

Both are accepted because they use `fail_closed_no_apply` and do not claim update apply authority.
