# Accepted Limitation Model

RollbackBundle v0 accepts limitations as explicit, evidenced metadata.

Accepted limitation semantics:

- `manual_review_required` requires later human review before any future apply task may rely on the bundle.
- `rollback_unavailable` records an unavailable recovery path and must not be treated as apply permission.
- `refuse` records a closed decision that downstream tasks must preserve unless a later reviewed repair or policy task changes the evidence.
- conflict-only and limitation-only bundles may pass with warnings when they do not claim apply authority.

The limitation model is advisory and preparatory. It does not roll back, authorize rollback, or reduce later apply-gate requirements.
