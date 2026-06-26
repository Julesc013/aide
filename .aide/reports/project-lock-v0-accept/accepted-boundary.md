# ProjectLock v0 Accepted Boundary

Accepted capability: `project_lock_v0`

This accepts ProjectLock v0 as a target-owned distribution selection and binding
object. It binds the accepted DistributionManifest by digest, records selected
component digests and artifact refs, verifies dependency closure, keeps channel
informational, and preserves optional extensions.

This does not accept install truth, install/update/apply, admission,
authorization, target mutation, runtime, publication, OwnershipLedger, or
InstallRecord behavior.
