# Q14 Regression Checks

## Threshold

The default regression warning threshold is 20 percent, defined in `.aide/policies/token-ledger.yaml`.

## Behavior

Q14 compares the current record for a path to previous ledger records for the same path when available.

- If no previous record exists, the result is `baseline_only`.
- If the current approximate tokens increase beyond the threshold, `ledger report` records a regression warning.
- If a compact surface exceeds a hard token budget, the budget warning is reported separately.
- Q14 does not fail ordinary operation solely for a token regression unless a hard budget is exceeded.

## Current Status

The generated token-savings summary is the canonical compact view of current regression warnings. Latest observed status:

- regression warnings: 0
- budget warnings: 1 near-budget review packet warning
- latest review packet: 1,946 approximate tokens against a 2,400 hard limit

The review packet warning is not a regression warning, but it is a useful Q15 signal: evidence review remains compact compared with the naive baseline, yet it is near the configured hard limit.

## Future Usage

Future phases should run:

```bash
py -3 .aide/scripts/aide_lite.py ledger scan
py -3 .aide/scripts/aide_lite.py ledger report
py -3 .aide/scripts/aide_lite.py ledger compare --baseline root_history_baseline --file .aide/context/latest-task-packet.md
```

If a packet grows substantially, the phase evidence should explain whether the growth is load-bearing quality evidence or avoidable prompt drift.
