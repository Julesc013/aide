# Combined isolated-host API-query source checkpoint

Base dev `fce11e7fce3e8106a71f5a2391fd6f0517d7e0c8` was clean. The
published source candidate `ad1076a3b165d15bfb68045908dfef1f5acd13c2`
has tree `db819d476dc4a483f5e0a033fba9787097c0f949` and is an
evidence-only descendant of independently reviewed repair
`1011d008fc39b135a5ef27062b5b8ee9c95cdc7f` (tree
`68cbc4d2b15049b7c589204d29003cf4affd93fc`). That review passed source
with 140 permitted tests; it did not qualify a native effect.

The actual no-commit merge found four documentation conflicts:
`DOCUMENTATION.md`, `IMPLEMENT.md`, `PLANS.md`, and
`docs/reference/integration-broker-core.md`. Both sides' substantive content
was retained. Runtime source, direct tests, queue index, and task evidence
merged without textual conflicts. The source candidate added no generated
portable or release artifacts to this merge. No native API object or real host
query was created by the integration run.

| Check | Observed result |
| --- | --- |
| Permitted combined-source tests | 140/140 PASS in 1.518 seconds |
| Excluded effect tests | Three `NativeApiSetQueryApi` synthetic-object tests and one live loopback test, explicitly not run |
| Exact C default commit range | PASS_WITH_DISPOSITIONS; `1011d008-api-query-why-bullet` accepted |
| Exact C raw range | FAIL on the original missing `## Why` bullet |
| Canonical validate | Exit 0 |
| Canonical doctor | Exit 0 |
| Staged diff whitespace | PASS |

The test runner and logs are external at
`D:\Projects\AIDE\_review_scratch\host-dev-permitted-tests.py` and
`host-dev-permitted-tests.log`; range, validate, and doctor logs are in the
same directory with `host-dev-` prefixes. These tests do not establish physical
host bytes, restricted principal, native query, private image/grants,
AppContainer Python, hosted target, credential/model, or activation guarantees.

This source merge awaits an exact integrated candidate commit and independent
technical integration review before a remote dev fast-forward.
