# Combined source validation

Date: 2026-09-24 AEST. Worktree: isolated integration branch based on remote
dev `f77ecba2`; source merge staged but not yet committed at test time. Logs
are retained outside the repository as
`D:\Projects\AIDE\_review_scratch\combined-test_*.py.log`.

| Suite | Executed | Passed | Skipped | Result |
| --- | ---: | ---: | ---: | --- |
| GitHub observation and policy | 50 | 50 | 0 | PASS |
| PR observation | 21 | 21 | 0 | PASS |
| GitHub HTTP | 19 | 19 | 0 | PASS |
| Provider bridge | 12 | 12 | 0 | PASS |
| Integration broker | 37 | 36 | 1 | PASS_WITH_SKIP |
| Q31 export governance | 6 | 6 | 0 | PASS |
| Export/import | 25 | 25 | 0 | PASS |
| Q47 release bundle | 18 | 18 | 0 | PASS |
| Q48 GitHub release draft | 11 | 11 | 0 | PASS |
| **Total** | **199** | **198** | **1** | **PASS_WITH_SKIP** |

Every listed suite exited zero. The one skip is the existing Windows symlink
creation privilege case, not an executed pass. An initial typo selected
`test_integration_broker.py`, ran zero tests, and exited 5; the actual file
`test_continuous_worker_integration_broker.py` was then run and passed with
the stated skip. No test assertion failed.

`git diff --check` and staged diff checks passed. The exact merge commit,
canonical validation, pack provenance, and derived-artifact replay were pending
at this source candidate checkpoint. Merge `6a581dbc` then failed canonical
validate only for inherited pack source `1397b703` versus combined HEAD.
Bounded child `AIDE-CW-GITHUB-TARGET-PACK-REFRESH-01` subsequently cleared
that failure, passed canonical checks, and qualified direct ZIP and tar.gz
consumers. Its evidence records the exact final bytes.
