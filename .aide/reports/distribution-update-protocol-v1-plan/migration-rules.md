# Migration Rules

Migration is explicit and evidence-backed.

## Allowed v1 Migration Types

- schema field rename with old/new field mapping
- ownership class refinement
- managed-section identity upgrade
- compatibility finding normalization
- release bundle metadata promotion into `DistributionManifest v1`
- install/upgrade operation normalization into `UpdatePlan v1`

## Required Evidence

- source schema/version
- target schema/version
- source digest
- migrated digest
- migration reason
- compatibility impact
- rollback or non-destructive fallback
- evidence references

## Refusal Conditions

- unsupported source schema
- missing ownership evidence
- source-generated target truth contamination
- unsafe overwrite
- delete without explicit owned preimage
- managed-section identity mismatch
- missing rollback path
- target-specific state would be overwritten

No migration is automatic merely because a file has an old format.
