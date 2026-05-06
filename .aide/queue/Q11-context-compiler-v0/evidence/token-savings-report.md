# Q11 Token Savings Report

## Latest Context Packet

- path: `.aide/context/latest-context-packet.md`
- chars: 1,855
- lines: 80
- approx_tokens: 464
- method: `ceil(chars / 4)`
- contents_inline: false

## Latest Task Packet

- path: `.aide/context/latest-task-packet.md`
- target task: `Implement Q12 Verifier v0`
- chars: 2,942
- lines: 99
- approx_tokens: 736
- method: `ceil(chars / 4)`
- budget_status: PASS

## Naive Baseline Comparison

Baseline method: approximate the old verbose context habit as concatenating root/project guidance plus the Q11 queue prompt/task records:

- `README.md`
- `ROADMAP.md`
- `AGENTS.md`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`
- `.aide/queue/Q11-context-compiler-v0/prompt.md`
- `.aide/queue/Q11-context-compiler-v0/task.yaml`

Baseline size:

- chars: 178,049
- approx_tokens: 44,513
- method: `ceil(chars / 4)`

Estimated reductions:

- latest context packet only: 99.0%
- latest task packet only: 98.3%
- context packet plus task packet: 97.3%

## Uncertainty And Limits

- Counts are approximate `chars / 4`, not exact provider tokenizer output.
- The baseline is a labelled naive comparison, not a measured provider bill.
- The context compiler reduces prompt-visible context, but Q14 is still needed for formal token-ledger recording and regression tracking.
- Q12 is still needed for mechanical verifier/evidence gates.
