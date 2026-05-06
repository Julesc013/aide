# Q10 Token Savings Report

## Latest Packet

- path: `.aide/context/latest-task-packet.md`
- target task: `Implement Q11 Context Compiler v0`
- chars: 2,566
- lines: 91
- approx_tokens: 642
- method: `ceil(chars / 4)`
- budget_status: PASS

## Naive Baseline Comparison

Baseline method: approximate the old verbose prompt habit as concatenating broad repo guidance plus the current task prompt:

- `README.md`
- `ROADMAP.md`
- `AGENTS.md`
- `PLANS.md`
- `.aide/queue/Q10-aide-lite-hardening/prompt.md`

Baseline size:

- chars: 74,297
- approx_tokens: 18,575
- method: `ceil(chars / 4)`

Estimated reduction:

- compact packet approx tokens: 642
- naive baseline approx tokens: 18,575
- estimated reduction: 96.5%

## How Q10 Improves Repeatability Over Q09

- `pack` now renders generic Q11+ packets from task text instead of being Q10-specific.
- `adapt` is drift-aware and can run twice with no diff.
- `validate` checks latest packet sections, budget posture, adapter status, and obvious secrets.
- `snapshot` reports summary counts and remains content-free.
- `estimate` handles missing and binary-like files safely.
- Tests exist both in the Harness test suite and under `.aide/scripts/tests`.

## Uncertainty And Limitations

- Counts are approximate `chars / 4`, not provider tokenizer output.
- The baseline is a labelled naive comparison, not a measured provider bill.
- Q14 is still needed for formal token-ledger recording and regression tracking.
- Q11 is still needed for deeper context compilation beyond shallow snapshot refs.
