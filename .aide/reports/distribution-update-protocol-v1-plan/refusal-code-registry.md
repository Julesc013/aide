# Refusal-Code Registry

Candidate v1 refusal codes:

| Code | Meaning |
| --- | --- |
| `distribution.manifest_missing` | Candidate distribution manifest is absent. |
| `distribution.manifest_digest_mismatch` | Manifest digest does not match recorded source. |
| `distribution.unsupported_protocol_range` | Target cannot read required protocol range. |
| `project_lock.missing` | Target has no ProjectLock where one is required. |
| `project_lock.digest_mismatch` | ProjectLock does not bind to candidate distribution. |
| `ownership.unknown` | Path or section ownership is unknown. |
| `ownership.project_owned` | Operation targets project-owned content. |
| `ownership.never_touch` | Operation targets an explicit never-touch path or section. |
| `managed_section.identity_mismatch` | Managed section marker or identity does not match. |
| `plan.scope_expansion` | Apply attempted to add operations not in approved plan. |
| `plan.digest_mismatch` | Approved plan digest does not match apply input. |
| `preimage.mismatch` | Target preimage hash differs from approved plan. |
| `rollback_bundle.missing` | Required rollback bundle was not created before apply. |
| `source_state.contamination` | Source-generated state would become target truth. |
| `release.no_publish_boundary` | Operation attempts publication in a no-publish phase. |
| `network.forbidden` | Operation attempts network access without authority. |
| `target_mutation.forbidden` | Operation attempts target mutation outside approved apply. |

The first implementation task should define only the refusal codes needed by
`DistributionManifest v1`; the remaining codes become future build inputs.
