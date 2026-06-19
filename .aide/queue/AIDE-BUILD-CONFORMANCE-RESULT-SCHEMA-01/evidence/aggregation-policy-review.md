# Aggregation Policy Review

Aggregation preserves this order:

1. Required case `ERROR` produces aggregate `ERROR`.
2. Required case `FAIL` produces aggregate `FAIL`.
3. Missing, unavailable, skipped, or not-run required cases produce
   `INCOMPLETE`.
4. If all required cases satisfy accepted outcomes and warnings exist, the
   aggregate is `PASS_WITH_WARNINGS`.
5. If all required cases satisfy accepted outcomes and no warnings exist, the
   aggregate is `PASS`.

Optional and advisory findings do not block required-case satisfaction in this
slice; they remain warning/informational debt.

The first projected result has all 8 required cases satisfied and records
`PASS_WITH_WARNINGS`.
