# Local prototype validation

- Pilot suite: 51 tests pass; command/output in unit-tests.txt.
- Python parse: eight runtime modules parse.
- Git whitespace check: passed.
- Independent assurance: separate reviewer; material findings repaired and regression tested. Reviewed source identity is recorded separately.
- Global AIDE validate: FAIL; two portable export/pack checksum problems in preflight-validation.json. The same failure class was present in initial preflight before runtime code.
- AIDE Git policy: PASS. Detect: main canonical, dev absent. Plan: blocked pending dirty-change classification. No branch mutation or remote integration performed.
- FacMan workspace hygiene: PASS; three existing task roots, no in-tree output roots. No FacMan product code/policies changed.

Real OS/process tests cover creation boundaries, supervisor death, child/grandchild cleanup, output caps, cancellation, actual Python validation and active source/storage thresholds.

Synthetic tests cover model/session and integration request/observation boundaries. Their UUIDs and receipt references are not Codex/GitHub evidence.

Missing: real model/auth/sandbox qualification; protected broker and permitted actors; two real consecutively integrated tasks; actual Codex sandbox-descendant recovery; durable broker fault tests; selected-source preparation; OS restart supervision.

Result: local prototype validated; full continuous-worker acceptance incomplete.

