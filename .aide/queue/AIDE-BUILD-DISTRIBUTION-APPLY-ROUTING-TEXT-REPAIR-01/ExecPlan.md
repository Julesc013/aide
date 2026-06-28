# AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01

## Objective

Repair stale operator-facing `distribution-apply status`, `distribution-apply plan`, and `distribution-apply verify` routing text after `aide_self_consumer_fixture_v0` acceptance.

## Scope

Allowed writes:

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_distribution_apply_routing_text_repair.py`
- `.aide/reports/distribution-apply-routing-text-repair/**`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

No core distribution engine behavior, canonical fixture, target repository, canary, release, provider/model/network, branch/worktree, or push behavior is in scope.

## Plan

1. Confirm live queue truth and predecessor acceptance evidence.
2. Capture before routing output from `distribution-apply status`, `plan`, and `verify`.
3. Patch CLI routing text so accepted self-consumer fixture state is printed and the next task routes to product-status projection.
4. Add a focused test for status, bare plan, scenario plan, and verify routing output.
5. Run focused, no-apply/no-publish, broad, task evidence, and hygiene validation.
6. Stop at `needs_review`.

## Progress

- [x] Live queue truth reviewed.
- [x] Before routing text captured.
- [x] CLI routing text repaired in `.aide/scripts/aide_lite.py`.
- [x] Focused routing text test added.
- [x] Validation passed with warnings.
- [x] Evidence and reports written.
- [x] Stopped at `needs_review`.

## Result

`PASS_WITH_WARNINGS`.

## Next

`AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`.
