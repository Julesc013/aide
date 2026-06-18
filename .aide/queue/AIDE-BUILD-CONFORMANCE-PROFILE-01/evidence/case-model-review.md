# Case Model Review

The profile defines ten `ConformanceCase` records:

- 8 required cases
- 1 optional case
- 1 advisory case

Each case records:

- `case_id`
- profile-scoped `case_ref`
- title and description
- requirement level
- evaluator identifier
- accepted outcomes
- evidence requirements
- dependencies
- source refs
- null `result_ref`
- false result/execution/admission flags

The helper enforces unique case IDs, dependency existence, dependency-cycle
absence, valid requirement levels, and accepted outcomes for required cases.
