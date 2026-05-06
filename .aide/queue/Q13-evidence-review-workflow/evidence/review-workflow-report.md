# Q13 Review Workflow Report

## Review-Pack Command

Q13 adds `py -3 .aide/scripts/aide_lite.py review-pack`.

The command writes `.aide/context/latest-review-packet.md` from:

- `.aide/context/latest-task-packet.md`
- `.aide/context/latest-context-packet.md`
- `.aide/verification/latest-verification-report.md`
- current queue evidence refs
- `git status --short` changed-file summaries
- validation and risk evidence
- `.aide/prompts/evidence-review.md`
- `.aide/verification/review-decision-policy.yaml`

## Generated Review Packet Summary

- path: `.aide/context/latest-review-packet.md`
- contents_inline: false
- full_diffs_inline: false
- raw_prompt_logs_inline: false
- provider_or_model_calls: none

Final packet stats are recorded in `.aide/queue/Q13-evidence-review-workflow/evidence/review-packet-savings.md`.

## Decision Policy Summary

`.aide/verification/review-decision-policy.yaml` defines:

- `PASS`
- `PASS_WITH_NOTES`
- `REQUEST_CHANGES`
- `BLOCKED`

It forbids approving missing validation as a pass and keeps full-history requests reserved for insufficient packets.

## Verifier Integration

Q13 adds `verify --review-packet PATH` and includes latest review-packet checks in default verification when the packet exists.

The verifier checks:

- required review-packet sections
- decision request shape
- file refs
- forbidden prompt patterns
- approximate review-packet budget
- raw source marker absence

## Limitations

Review-pack is deterministic and structural. It does not call GPT-5.5, judge code quality semantically, perform full diff analysis, or repair implementation work.
