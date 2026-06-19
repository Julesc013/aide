# Result Model Review

The projected result is:

- `kind: ConformanceResult`
- `result_ref:
  aide://conformance-result/minimal_capability_manifest-v1.0.0-evidence-projection-01`
- `profile.ref:
  aide://conformance-profile/minimal_capability_manifest-v1.0.0`
- `subject.ref: aide://capability/minimal_capability_manifest`
- `observation.mode: evidence_projection`

The model records the result as valid and complete while leaving:

- `execution_performed: false`
- `runner_ref: null`
- `admission_performed: false`
- `subject_admitted: false`
- `trusted: false`

This preserves the declaration/profile/result/admission separation.
