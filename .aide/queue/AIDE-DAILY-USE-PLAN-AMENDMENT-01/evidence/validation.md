# Validation of the prepared planning candidate

Date: 2026-10-12. Host: GUNMETAL-WIN. Python: 3.14.8.
This is structural/functional planning verification, not operational containment
or downstream product qualification. Independent review remains outstanding.

## Baseline and repair

The initial doctor exited1 and validate exited1. The baseline validate reported
14 failures: 13 required sections missing from the old latest task packet, and
stale capability evidence bindings. Full local ignored logs and their hashes,
sizes, duration and individual exits are in `baseline-checks.json`.

The packet was replaced with a complete bounded brief. `pack --task` first
produced a generic UNSPECIFIED template for this non-Q id; that result was not
adopted as task authority. The task-local brief supplies the exact phase and
references task.yaml scope. Explicit `capability ledger` refreshed only derived
bindings/current explanations; the JSON capability classifications were unchanged.

## Results

| Command | Actual result | Scope |
|---|---|---|
| `py -3 -B .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/check_plan.py` | PASS | 12 milestones,22 capabilities,8 phases;6 invalid plans refused |
| `py -3 -B .aide/scripts/aide_lite.py validate` | Exit0, no FAIL/WARN lines | Existing repository structural validation after bounded repairs |
| `py -3 -B .aide/scripts/aide_lite.py doctor` | Exit0, no FAIL/WARN lines | Existing diagnostics after corrected current views |
| `py -3 -B .aide/scripts/aide_lite.py capability validate` | Exit0 | Explicitly refreshed advisory capability views; no behavioural proof |
| `py -3 -B scripts/aide compile --write` | Exit0, PASS_WITH_WARNINGS | Compiler-owned manifest refreshed; AGENTS/skill managed sections unchanged; deferred outputs preserved |
| `py -3 -B .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | 911 approximate tokens, within3200 budget | Character-based estimate, not exact model accounting |
| `py -3 -B .aide/scripts/aide_lite.py task inspect --task-id AIDE-DAILY-USE-PLAN-AMENDMENT-01` | Task resolved | Missing evidence3 at that early observation; required files subsequently added |
| `py -3 -B .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/check_candidate.py` | PASS | Exact task allowlist, added links and unchanged published tag/release paths |
| `git diff --check` | Exit0 | Whitespace/diff integrity |
| `py -3 -B .aide/scripts/aide_lite.py verify --changed-files --write-report .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/verification.json` | WARN, errors0,warnings18 | Existing last-active-task scope selection; all warnings retained and exact child scope checked separately |
| `py -3 -B .aide/scripts/aide_lite.py review-pack --task-packet .aide/context/latest-task-packet.md --verification .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/verification.json --evidence-dir .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence --output .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/review-packet.md` | PASS budget, verifier WARN preserved | Review preparation, not an independent verdict |

`final-checks.json` contains exact full-output hashes, sizes, duration and exits.
No required runtime test was skipped and relabelled PASS. Broad runtime/model/
release suites and eval runs were not executed for this planning-only diff.
Their prior results retain their exact subjects. Two initial CLI argument
mistakes returned usage errors before execution; corrected estimate and task
inspect commands are recorded above. No substantive failure was suppressed.
An initial commit-message preflight refused missing bullet/category/trailer
formatting before staging or branch advancement; the draft was corrected using
the existing standard. This is a mechanical preparation repair, not a waived gate.

## Metadata-only closeout

Task/index review-state and evidence completion are checked with the existing
Harness, plan checker, exact candidate checker and diff checks. Full unchanged
source validation is reused rather than rerun for appended receipt text.
The frozen candidate manifest excludes itself; an actual reviewed commit/tree
will provide the definitive source subject. Structured commit status is recorded
in the closeout receipt after commit creation, not predicted here.
