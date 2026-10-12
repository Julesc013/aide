# AIDE Latest Task Packet

## PHASE

phase: AIDE-DAILY-USE-PLAN-AMENDMENT-01

## GOAL

Prepare and validate the owner's capability-specific daily-use planning amendment
under AIDE-CONVERGENCE-AND-DELIVERY-01. Acceptance awaits exact independent review.

## WHY

Useful workflows need specific prerequisites and observable outcomes. Preserve
the shared architecture and P0-P11/C1-C12; begin cost observation, usability and
selective reuse with the first useful task.

## CONTEXT_REFS

- `.aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/task.yaml`
- `.aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/ExecPlan.md`
- `.aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/status.yaml`
- `.aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/next-briefs.md`
- `docs/roadmap/staged-expansion-roadmap.md`
- `docs/roadmap/development-workflows.json`
- `.aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/REPORT.md`
- `.aide/queue/AIDE-SESSION-CONTAINMENT-01/status.yaml`
- `.aide/policies/review-gates.yaml`

## ALLOWED_PATHS

The exact allowlist is `task.yaml` scope.allowed_paths. It covers this child,
named parent routing records, index/intake, current Profile/task packet,
compiler-owned generated sections, capability-derived views, README/root indexes
and the two named roadmap files. References to later briefs grant no other paths.

## FORBIDDEN_PATHS

- Runtime or provider implementation, unadmitted `.aide.local/**` changes
- User credentials, account/ACL changes, unrelated target writes or deletion
- Released assets/tags, publication, remote or dev/main integration effects
- Manual AGENTS/skill policy sections and adoption of proposed specifications

## IMPLEMENTATION

Separate implementation prerequisites, activation gates, qualification evidence
and preferred sequencing at capability granularity. Specify all eight daily-use
phases and prepare only ready briefs. Correct current published-release prose;
retain historical evidence and original released bytes. Observe exact new-host
metadata once without inheriting old qualification or consumed model allowances.

## VALIDATION

- `py -3 -B .aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/check_plan.py`
- `py -3 -B .aide/scripts/aide_lite.py doctor`
- `py -3 -B .aide/scripts/aide_lite.py validate`
- `py -3 -B scripts/aide compile --dry-run`
- `git diff --check`, explicit changed-file allowlist and relative-link checks
- Structured commit check after the concrete prepared-result commit

## EVIDENCE

Task-local baseline/final results, host observation, next briefs, changed-files,
validation, remaining risks and exact candidate/review state. Unknown controller
usage remains unknown. Local full logs are ignored; compact findings and hashes
are portable evidence, not substitutes for an absent raw receipt.

## NON_GOALS

No model/native qualification, task-store replacement, target mutation, blanket
specification adoption, archive rebuild, release or automatic integration.

## ACCEPTANCE

Typed relationships permit independent early reuse, read-only native/relay,
lesson-correction and contributor fixtures. Daily-use phases specify positive,
refusal and recovery outcomes. Costs and harvest start immediately. Independent
review remains pending; planning and structural PASS do not imply operational use.

## OUTPUT_SCHEMA

Report changed files, checks, commit, exact review state, unresolved boundaries
and the next dependency-ready action. Preserve the active goal until its actual
outcomes are achieved or the goal service's blocked threshold is met.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- scope: compact task brief; measure with the existing estimate command
