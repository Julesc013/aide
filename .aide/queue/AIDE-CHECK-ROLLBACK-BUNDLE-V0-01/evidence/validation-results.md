# Validation Results

Result: `PASS_WITH_WARNINGS`

Material findings: `0`

Missing evidence: `0`

Validation was run before and after task materialization. Final command outcomes are recorded after the final validation pass:

- Core RollbackBundle validation passed with warnings and zero validation errors.
- Predecessor regression validation passed with warnings and zero validation errors.
- Q43-Q48 no-apply/no-publish validators and broad AIDE validation passed.
- Source and check task inspect/evidence passed with `missing_evidence: 0`.
- Path, credential-like, and source-output misuse scans found no material leak.
- Git whitespace and commit-policy checks passed after staging/commit.

Warnings:

- RollbackBundle v0 remains proposed until acceptance.
- Same-session check independence is limited, but this check did not modify implementation.
- Source-output scan hits are expected negative fixture labels or explicit no-target-truth boundary text.
- The live projection only contains reverse operation classes reachable from the current accepted UpdatePlan; fixture coverage validates the remaining reverse operation classes.
