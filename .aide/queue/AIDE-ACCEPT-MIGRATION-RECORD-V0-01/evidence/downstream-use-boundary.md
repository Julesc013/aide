# Downstream Use Boundary

Downstream objects may cite MigrationRecord v0 only as migration decision metadata.

They must not infer:

- migration apply
- target mutation
- source latest output as target truth
- UpdatePlan existence
- rollback or receipt readiness
- release or canary readiness
