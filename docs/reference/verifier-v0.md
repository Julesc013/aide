# Verifier v0

## Purpose

Q12 adds the first deterministic AIDE Verifier. It reduces premium-model review cost by checking packet shape, evidence sections, file references, line ranges, changed-file scope, adapter drift, context packet shape, token warnings, and obvious secret risks locally before GPT-5.5 sees a compact review packet.

## Commands

Run from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py verify
py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md
py -3 .aide/scripts/aide_lite.py verify --evidence .aide/queue/Q12-verifier-v0/evidence/verifier-report.md
py -3 .aide/scripts/aide_lite.py verify --changed-files
py -3 .aide/scripts/aide_lite.py verify --write-report .aide/verification/latest-verification-report.md
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Checks

- Required files: verifies Q09-Q12 token, context, and verifier files exist.
- Required sections: verifies compact task packets, evidence packets, review packets, and review templates use expected headings.
- File references: checks conservative refs in backticks or markdown links.
- Line ranges: validates `path#Lstart-Lend` syntax and text-file bounds where feasible.
- Diff scope: classifies `git status --short` paths against the active queue item allowlist and denylist.
- Adapter drift: checks the managed `AGENTS.md` token/context/verifier section.
- Context shape: checks latest context artifacts and avoids raw source markers.
- Token warnings: uses the existing `chars / 4` approximation and token-budget policy.
- Secret safety: scans relevant AIDE/root surfaces for obvious key-like values while allowing policy terms such as `api_key` as text.

## Result Values

- `PASS`: no warnings or errors.
- `WARN`: one or more warnings and no errors.
- `FAIL`: one or more errors.

The command exits nonzero only for `FAIL`.

## Evidence And Review

Q12 writes `.aide/verification/latest-verification-report.md` as compact verifier evidence. Q13 writes `.aide/context/latest-review-packet.md` from task/context/evidence/verifier refs. GPT-5.5 review should receive the review packet instead of the whole repo or long chat history.

## Deferred Work

Q12 is structural only. It does not implement semantic diff analysis, LLM-as-judge, automatic repair, exact tokenizer support, provider billing, token ledger formalization, golden tasks, Gateway, routing, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loops.
