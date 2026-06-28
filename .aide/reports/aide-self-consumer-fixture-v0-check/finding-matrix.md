# Finding Matrix

| Check area | Result | Notes |
| --- | --- | --- |
| Fixture root bounded under `.aide/fixtures/aide-self-consumer-fixture-v0` | PASS | Corpus is contained in the expected fixture root. |
| Lifecycle scenarios | PASS | Nine expected scenarios are present. |
| Focused test coverage | PASS | Focused test covers fixture boundary, lifecycle proofs, preservation, source/target separation, and report consistency. |
| Target-owned state preservation | PASS | Ownership map and scenarios preserve target-owned examples. |
| Source repo not installed target | PASS | Source repo confusion scenario refuses closed. |
| DistributionApplyEngine bindings | PASS | Accepted context, UpdatePlan, RollbackBundle, predecessor, and receipt boundaries remain verified by DistributionApplyEngine validation. |
| Canonical fixture preservation | PASS | Fixture hashes match before and after plan/run/verify validation. |
| Q43-Q48 no-apply/no-publish boundaries | PASS | Validators remain no-apply/no-publish. |
| Overclaiming scan | PASS | No real target apply, canary readiness, public release, provider/model/network, push, or branch automation claim is added. |

Material finding count: `0`.
