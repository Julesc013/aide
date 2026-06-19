# Case Result Model Review

Each projected case result records:

- the profile-scoped `case_id`;
- the source `case_ref`;
- requirement-level and evaluator snapshots;
- normalized accepted observed outcomes;
- observed outcome;
- evidence, report, and source refs;
- assertion results for evidence-path presence;
- warnings and limitations;
- `execution_performed: false`;
- `runner_ref: null`;
- `admission_performed: false`;
- `subject_admitted: false`;
- `trusted: false`.

The first projection emits 10 case results, matching the accepted profile case
inventory.
