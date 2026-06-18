# Case Model Review

Result: `PASS`

Each ConformanceCase is profile-scoped, has a stable case id/ref, declares a
requirement level, evaluator, evidence expectation, dependency data where
needed, and preserves `result_ref: null` until ConformanceResult exists.

Required cases fail closed. Optional and advisory cases may warn without
admitting capabilities.
