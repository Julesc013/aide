# Evidence Review Workflow

## Purpose

Q13 adds deterministic review-packet generation so GPT-5.5 or a human reviewer can review compact evidence instead of full chat history, full repo context, broad roadmap dumps, or full diffs by default.

The primary output is:

```bash
.aide/context/latest-review-packet.md
```

## Commands

Run from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py review-pack
py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md
py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md
```

Optional inputs:

```bash
py -3 .aide/scripts/aide_lite.py review-pack --task-packet .aide/context/latest-task-packet.md --verification .aide/verification/latest-verification-report.md --evidence-dir .aide/queue/Q13-evidence-review-workflow/evidence
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Packet Contents

The review packet includes:

- review objective and decision request
- compact task packet reference
- latest context packet reference
- latest verification report reference and verifier result
- evidence packet references
- changed-file summary from `git status --short`
- validation summary from task-local evidence
- token summary using `chars / 4`
- golden task summary when Q15 applies
- risk summary and non-goals
- reviewer instructions and decision policy reference

It does not inline full source files, full diffs, raw prompt logs, provider keys, local state, caches, or full project history.

## Review Contract

The canonical GPT-5.5 prompt is `.aide/prompts/evidence-review.md`. The reviewer should use only the review packet unless it is insufficient and return:

```text
DECISION:
REASONS:
REQUIRED_FIXES:
OPTIONAL_NOTES:
NEXT_PHASE:
```

Allowed decisions are defined in `.aide/verification/review-decision-policy.yaml`:

- `PASS`
- `PASS_WITH_NOTES`
- `REQUEST_CHANGES`
- `BLOCKED`

## Deferred Work

Q13 does not call GPT-5.5, automate model review, implement LLM-as-judge behavior, perform semantic diff analysis, add exact tokenization, write provider billing records, add golden tasks, implement Gateway/router/cache, or add Runtime/Service/Commander/UI/Mobile/MCP/A2A/host behavior. Q14 adds metadata-only estimated token ledger and savings reporting; Q15 adds deterministic local golden-task quality scaffolding.
