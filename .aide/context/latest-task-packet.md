# AIDE Latest Task Packet

task_id: AIDE-ENGINEERING-REVIEW-01
projection_only: true

## PHASE

AIDE-ENGINEERING-REVIEW-01 - Strengthen bounded engineering review through existing owners

## GOAL

AIDE-ENGINEERING-REVIEW-01: repair demonstrated portable self-test fixture gaps under amendment7b8ae471; preserve original failure and assertions; qualify source and delivered review checks with separate processes

## WHY

Continue AIDE token survival by using repo-local context refs, compact objectives, deterministic validation, and evidence packets instead of long chat history.

## CONTEXT_REFS

- `.aide/queue/AIDE-ENGINEERING-REVIEW-01/task.yaml` (selected scope and acceptance)
- `.aide/queue/AIDE-ENGINEERING-REVIEW-01/ExecPlan.md` (continuation; when present)
- `.aide/queue/AIDE-ENGINEERING-REVIEW-01/status.yaml` (actual state; when present)
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `.aide/context/repo-snapshot.json` (present)
- `.aide/context/repo-map.json` (present)
- `.aide/context/repo-map.md` (present)
- `.aide/context/test-map.json` (present)
- `.aide/context/context-index.json` (present)
- `.aide/context/latest-context-packet.md` (present)
- `.aide/repo/latest-repo-intelligence.md` (present)
- `.aide/repo/file-inventory.json` (present)
- `.aide/reports/file-quality-summary.md` (present)
- `.aide/reports/file-quality-ledger.json` (present)
- `.aide/refactors/latest-refactor-readiness.md` (present)
- `.aide/refactors/latest-refactor-plan.example.json` (present)
- `.aide/routing/latest-route-decision.json` (present)
- `.aide/routing/latest-route-decision.md` (present)
- `.aide/cache/latest-cache-keys.json` (present)
- `.aide/cache/latest-cache-keys.md` (present)
- `.aide/prompts/compact-task.md`
- `.aide/policies/token-budget.yaml`
- `.aide/policies/cache.yaml`
- `.aide/policies/local-state.yaml`

## ALLOWED_PATHS

- `.aide/queue/AIDE-ENGINEERING-REVIEW-01/**`
- `.agents/skills/aide-review/SKILL.md`
- `.aide/prompts/evidence-review.md`
- `.aide/verification/review-decision-policy.yaml`
- `.aide/verification/review-packet.template.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_review_pack.py`
- `docs/reference/evidence-review-workflow.md`
- `.aide/queue/index.yaml`
- `.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/ExecPlan.md`
- `.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/status.yaml`
- `.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/evidence/engineering-review-admission.md`
- `.aide/intake/latest-*`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/capability-*`
- `.aide/export/aide-lite-pack-v0/**`
- `.aide/changelog/CHANGELOG.preview.md`
- `.aide/changelog/RELEASE_NOTES.preview.md`
- `.aide/changelog/changelog.preview.json`
- `.aide/changelog/latest-changelog-report.md`
- `.aide/changelog/malformed-commits.md`
- `.aide/changelog/release-notes.preview.json`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## FORBIDDEN_PATHS


- baseline protected paths and effects remain governed by repository policy
- raw provider credentials, API keys, local caches, raw prompt logs
- Gateway, provider, Runtime, Service, Commander, Mobile, MCP/A2A, host, or app-surface implementation paths unless the queue packet explicitly authorizes them

## IMPLEMENTATION

- This projection is context; it does not admit work or activate effects. Read the selected queue authority and review gates.
- Read the queue packet and relevant repo refs first.
- Keep changes inside the allowed paths.
- Make the smallest coherent diff that satisfies acceptance.
- Preserve generated/manual boundaries.
- Do not inline whole source files unless exact contents are required.
- Use exact refs such as `path#Lstart-Lend` when file details are load-bearing.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py index`
- `py -3 .aide/scripts/aide_lite.py context`
- `py -3 .aide/scripts/aide_lite.py repo inventory`
- `py -3 .aide/scripts/aide_lite.py repo validate`
- `py -3 .aide/scripts/aide_lite.py verify`
- `py -3 .aide/scripts/aide_lite.py review-pack`
- `py -3 .aide/scripts/aide_lite.py route explain`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 scripts/aide validate`
- `git diff --check`

## COMMITS

- Commit coherent subdeliverables with verbose bodies.
- Stop at review gates.

## EVIDENCE

- changed files
- validation commands and results
- verifier result
- review packet path and result when review-pack is available
- advisory route decision path and result when Q17 routing is available
- compact packet size and budget status
- unresolved risks and deferrals

## NON_GOALS

- No Gateway, provider calls, live model routing, local model setup, exact tokenizer, provider billing ledger, Runtime, Service, Commander, Mobile, MCP/A2A, UI, host/app implementation, or autonomous loop unless this packet is superseded by a reviewed queue item that explicitly authorizes it.

## ACCEPTANCE

- Task-specific acceptance criteria are met.
- Validation is run and recorded.
- Evidence is written.
- No secrets, raw prompt logs, local caches, or `.aide.local` contents are committed.

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `COMMITS`, `CHANGED_FILES`, `VALIDATION`, route/verifier/token results, `RISKS`, and `NEXT`.
Include the verifier result when Q12 verifier behavior is available.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: 5652
- approx_tokens: 1413
- budget_status: PASS
- warnings:
  - none
- formal ledger: `.aide/reports/token-ledger.jsonl`
