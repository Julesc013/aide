# AIDE Latest Task Packet

## PHASE

AI-LONG-TURN-OPERATING-PROTOCOL-00 - Long-Turn Operating Protocol

## GOAL

Create docs-only operating protocol material for long-running AIDE and Codex
queued turns, including turn budgets, validation ladders, stop conditions,
manual evidence gates, queue handoff rules, final report format, and failure
recovery.

## WHY

The attached prompt requested a long-turn controller protocol but also included
stale product and branch state plus broader branch-sensitive and
publication-sensitive language. AIDE intake split that request to a safe
docs-only WorkUnit before implementation.

## CONTEXT_REFS

- `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/`
- `.aide/intake/latest-intent-packet.md`
- `.aide/intake/latest-workunit-draft.md`
- `docs/planning/ai_long_turn_protocol/`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## ALLOWED_PATHS

- `.aide/intake/latest-intent-packet.json`
- `.aide/intake/latest-intent-packet.md`
- `.aide/intake/latest-workunit-draft.json`
- `.aide/intake/latest-workunit-draft.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/index.yaml`
- `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/**`
- `docs/planning/ai_long_turn_protocol/**`
- `DOCUMENTATION.md`
- `PLANS.md`
- `IMPLEMENT.md`

## REVIEWED_READ_ONLY_PATHS

- `AGENTS.md`
- `.aide/queue/README.md`
- `.aide/queue/policy.yaml`
- `.aide/profile.yaml`
- `.aide/policies/bypass.yaml`
- `.aide/policies/review-gates.yaml`
- `.aide/policies/work-units.yaml`
- `.aide/policies/task-resumption.yaml`
- `docs/reference/source-of-truth.md`
- `docs/reference/intent-compiler.md`
- `docs/reference/workunit-idempotency.md`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.env`
- `.env.*`
- `secrets/**`
- `credentials/**`
- `.aide.local/**`
- runtime behavior
- branch creation, merge, promotion, deletion, push, prune, or force update
- release publication, tags, uploads, or public launch
- target repository mutation
- provider/model calls
- Gateway calls
- network calls
- external discovery execution
- fabricated evidence

## REVIEW

- Confirm the docs-only split is recorded from the broader attached prompt.
- Review the new protocol templates for scope control and stop conditions.
- Verify the documentation index, planning index, and implementation log match
  the added protocol.
- Verify validation evidence is complete.
- Stop at `needs_review`.

## IMPLEMENTATION

- Compile the attached request through AIDE intake.
- Record the blocked broader prompt and safe docs-only split.
- Add the `AI-LONG-TURN-OPERATING-PROTOCOL-00` queue packet.
- Add protocol templates under `docs/planning/ai_long_turn_protocol/`.
- Update root documentation, planning, and implementation records.
- Do not change runtime behavior or perform branch, publication, target-repo,
  provider/model, Gateway, network, or external discovery work.

## EVIDENCE

- `.aide/queue/AI-LONG-TURN-OPERATING-PROTOCOL-00/evidence/*.md`
- `docs/planning/ai_long_turn_protocol/VALIDATION_REPORT.md`

## NON_GOALS

No runtime implementation, product gate change, launch, promotion, branch
mutation, push, tag, publication, target-repo mutation, provider/model calls,
Gateway calls, network calls, external discovery execution, or evidence
fabrication.

## VALIDATION

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AI-LONG-TURN-OPERATING-PROTOCOL-00`
- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py commit check --latest` after commit

## ACCEPTANCE

- Queue packet exists and is indexed.
- Protocol docs and templates exist.
- Evidence records intake split, changed files, validation, and remaining risks.
- Root docs mention the protocol.
- Status ends at `needs_review`.
- No forbidden behavior is introduced.

## OUTPUT_SCHEMA

Return the standard AIDE final report: summary, file list, validation commands
and results, unresolved issues, and deliberate deferrals.

## TOKEN_ESTIMATE

- approx_tokens: 1200
- budget_status: PASS
