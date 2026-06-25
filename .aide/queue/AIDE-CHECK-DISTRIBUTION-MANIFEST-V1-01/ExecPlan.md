# AIDE-CHECK-DISTRIBUTION-MANIFEST-V1-01 ExecPlan

## Objective

Independently check `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01` without repairing
implementation, accepting `distribution_manifest_v1`, or beginning
`ProjectLock v0`.

## Scope

- Verify live queue and source-task baseline.
- Inspect schema, helper, fixture corpus, reports, Q47 release evidence, and
  Q48 publication boundary evidence.
- Run a task-local adversarial checker for:
  - schema/envelope and extension compatibility;
  - immutable identity and digest behavior;
  - component graph closure;
  - artifact integrity and pre-access path safety;
  - checksum value verification;
  - protocol range semantics;
  - Q47 mapping and non-capability claims.
- Materialize independent evidence and reports under this check task.
- Stop at `needs_review` with either acceptance routing or repair routing.

## Dependencies

- Source build task: `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`.
- Source commit: `ad975887910f6a7238ef076ce2fef0fd43687e37`.
- Existing Q47 local release bundle and Q48 release-draft evidence.

## Verification Intent

- Run the evidence-local independent checker.
- Run focused DistributionManifest tests and broad AIDE validation.
- Run task inspect/evidence for the source and check tasks.
- Run Git whitespace checks, leak scans, and commit policy.

## Review Gate

Stop at `needs_review`. If material findings remain, recommend exactly
`AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-REPAIR-01`. If none remain, recommend
exactly `AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`.
