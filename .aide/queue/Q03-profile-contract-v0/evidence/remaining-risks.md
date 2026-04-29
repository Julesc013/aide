# Q03 Remaining Risks

## Review Dependencies

- Q00 remains `needs_review`.
- Q01 remains `needs_review`.
- Q02 remains `needs_review`.
- Q03 proceeded because the current human prompt explicitly authorized implementation, but the prior queue outputs still need review before they are accepted baseline.

## Deferred Work

- Q04 must implement any executable Harness import, compile, validate, doctor, migrate, bakeoff, or drift-check behavior.
- Q05 must define deterministic generated downstream artifact production and drift evidence.
- Q06 must reconcile compatibility baseline, migrations, shims, and upgrade gates.
- Q07 must define Dominium Bridge and XStack baseline behavior.
- Q08 must handle self-hosting automation after prior evidence is reviewed.

## Validation Limits

- Q03 used structural and text validation only.
- No full YAML parser or JSON Schema validator was introduced.
- No heavy native host tests were run.
- The documented shapes are sufficient for Q03 review but need Q04 Harness work before they become executable validation.

## Policy Risks

- Q03 added Profile-level policy files but did not modify existing autonomy, bypass, or review-gate policy files.
- Generated downstream artifacts remain non-canonical until future review.
- Compatibility policy remains a pointer and does not replace bootstrap-era governance, inventory, matrices, research, or eval records.
