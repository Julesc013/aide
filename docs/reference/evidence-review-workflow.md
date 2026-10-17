# Evidence Review Workflow

## Purpose

Q13 adds deterministic review-packet generation so an authorized model or human
reviewer can begin with compact evidence and inspect relevant code and contracts.
Packet generation does not call a reviewer or prove semantic correctness.

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

The shared procedure is `.aide/prompts/evidence-review.md`, linked by generated
packets and the repository's aide-review skill. Missing guidance is reported by
the packet verifier. Reviewers follow relevant source, callers and compatibility
obligations when needed, without acquiring execution or mutation authority.
They return:

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

## Proportionate engineering judgment

The prompt selects reuse, behavior-preserving refactoring, downstream impact and
structural reasoning from pinned PStack and Ponytail sources. Its portable source
links and MIT notices travel with it; no upstream companion skills, model-routing
rules or plugins are required. Supported compatibility shims remain legitimate.
Line count and visual similarity are investigation signals, not proof of defects.

Findings state a triggering condition, impact, evidence and bounded remedy.
Unrelated cleanup does not block acceptance; no actionable findings is valid.
Unknown total usage remains unknown. Structural packet tests establish wiring,
not reviewer quality, whole-task savings or universal reliability. Project-owned
acceptance and tailoring continue to govern imported copies.

## Original Q13 boundary

Q13 does not call models, automate review, implement an LLM judge or semantic diff
analyzer, add exact tokenization or write provider billing records. This boundary
does not prohibit an authorized reviewer from reasoning over relevant source.
Q13 did not add Runtime/Service/Commander/UI/Mobile/MCP/A2A/host behavior; later
reviewed work retains its own scope. Q14 introduced estimated token ledgers and
Q15 deterministic local golden-task scaffolding; neither substitutes for measured
complete outcomes.
