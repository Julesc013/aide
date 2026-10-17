# Repaired source: evidence binding refresh required

/root/review_disked_continuation confirmed both code findings resolved for
source1512c17c/templatebb19f63b, then returned REQUEST_CHANGES because the capability
binding still referenced the pre-repair CLI. Full validation independently failed
with STALE(source_inputs_changed); validate-after-review.log retains that result.

Disposition: refresh through the existing capability ledger command, then full
validation and exact source/template rebinding. No code changes or job allocation
followed the rejected evidence binding. This is not a waived validation failure.
