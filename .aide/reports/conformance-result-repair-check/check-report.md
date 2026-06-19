# ConformanceResult Repair Check Report

- task_id: AIDE-CHECK-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
- status: PASS_WITH_WARNINGS
- checked_task_id: AIDE-BUILD-CONFORMANCE-RESULT-SCHEMA-REPAIR-01
- checked_commit: 00407e4d63d6ad72ce5184bee5b22e07fc56856e
- result_ref: aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01
- profile_ref: aide://conformance-profile/minimal_capability_manifest-v1.0.0
- subject_ref: aide://capability/minimal_capability_manifest
- digest_algorithm: sha256-canonical-json-v1
- recorded_digest_repaired: sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70
- independent_pristine_profile_digest: sha256:a3fffc002bcf4bcc4ea9ffb938ae904cb28a9b6b05936f4e25064ef451e9bb70
- profile_digest_matches_pristine_profile: true
- bad_digest_fails_validation: true
- profile_source_mutated: false
- projection_deterministic: true
- aggregate_outcome: PASS_WITH_WARNINGS
- execution_performed: false
- admission_performed: false
- subject_admitted: false
- trusted: false
- recommended_next_task: AIDE-ACCEPT-CONFORMANCE-RESULT-SCHEMA-01

## Material Findings

- none

## Warning Debt

- The result remains evidence-projected and was not produced by a runner.
- A conformance runner is not implemented.
- Automatic observation collection is not implemented.
- The referenced profile remains candidate and is not active.
- Admission is not implemented.
- The subject is not admitted by the result.
- PatchTransaction is not implemented.
- AdapterManifest is not implemented.
- ContextPack v2 is not implemented.
