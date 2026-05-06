# Q13 Review Packet Savings

## Latest Review Packet

- path: `.aide/context/latest-review-packet.md`
- chars: 9,444
- approximate_tokens: 2,361
- method: `ceil(chars / 4)`
- contents_inline: false
- full_diffs_inline: false

## Latest Q14 Task Packet

- path: `.aide/context/latest-task-packet.md`
- task: `Implement Q14 Token Ledger and Savings Report`
- chars: 3,224
- approximate_tokens: 806
- method: `ceil(chars / 4)`

## Naive Review Baseline

Baseline method: sum chars for a broad manual review bundle that a reviewer might otherwise paste:

- `README.md`: 12,786 chars / 3,197 approximate tokens
- `ROADMAP.md`: 7,685 chars / 1,922 approximate tokens
- `AGENTS.md`: 9,591 chars / 2,398 approximate tokens
- `.aide/context/latest-task-packet.md`: 3,224 chars / 806 approximate tokens
- `.aide/context/latest-context-packet.md`: 1,859 chars / 465 approximate tokens
- `.aide/verification/latest-verification-report.md`: 4,621 chars / 1,156 approximate tokens
- `.aide/queue/Q13-evidence-review-workflow/task.yaml`: 2,825 chars / 707 approximate tokens
- `.aide/queue/Q13-evidence-review-workflow/prompt.md`: 1,111 chars / 278 approximate tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md`: 4,936 chars / 1,234 approximate tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/review-workflow-report.md`: 1,610 chars / 403 approximate tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/remaining-risks.md`: 830 chars / 208 approximate tokens

Baseline total: 51,078 chars / 12,770 approximate tokens.

## Estimated Reduction

- compact review packet vs baseline chars: about 81.5% reduction
- compact review packet vs baseline approximate tokens: about 81.5% reduction

This avoids sending full root docs, full roadmap context, full queue prompt text, and full evidence files to GPT-5.5 by default. The review packet references those files when needed.

## Uncertainty

This is not exact provider billing. It uses the Q09 approximation method, `chars / 4`. Q14 should formalize token ledger records and savings reports.
