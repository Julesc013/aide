# Rollback Record Proof

## Recorded Fields

- `managed-section-operation.schema.json` includes pre/post image hashes, section hashes, manual prefix/suffix hashes, and `rollback_ref`.
- `managed-section-patch.schema.json` includes replacement, expected existing, existing section, and resulting file hashes.
- `managed-section-report.schema.json` includes a `rollback_evidence` object.

## Fixture Proof

- `core.apply.managed_sections.patch_file_in_fixture()` records preimage and postimage hashes plus a rollback record.
- The rollback record sets `apply_allowed: false` and `rollback_execution: false`.
- `core/apply/tests/test_managed_sections.py` verifies fixture preimage, postimage, and rollback evidence.

## Boundary

Rollback evidence is proof material only in AIDE-APPLY-01. No rollback apply, delete, overwrite, or managed-section removal behavior was enabled.
