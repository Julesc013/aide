# X-TEST-00 Validation Tier Model

Status: implemented for review.

- T0: smoke, syntax, policy, architecture, no-call checks.
- T1: impacted tests selected from changed paths.
- T2: relevant component and integration tests.
- T3: full promotion/checkpoint/release suite.

Normal post-task validation is T0 + T1. Larger tasks add relevant T2. T3 is reserved for promotion/checkpoint/release evidence and external full-discovery handoff.

No tests were deleted, skipped, or reclassified to fake green results.

