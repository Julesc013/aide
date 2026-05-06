# QCHECK Token Survival Foundation Audit

## 1. Executive Verdict

Verdict: **PASS_WITH_WARNINGS**.

The repository now contains a substantial token-survival foundation through
Q20. The practical machinery works locally: compact task/context/review packets,
mechanical verification, token ledger reports, deterministic golden tasks,
outcome recommendations, advisory routing, cache/local-state metadata, local
Gateway status surfaces, and offline provider metadata all ran successfully in
this checkpoint. The highest reliable *accepted* phase remains Q08 or, by
review evidence, Q05/Q06 with notes; the highest claimed implemented phase is
Q20. It is technically safe to continue only if the next queue repairs/reviews
the foundation rather than adding more speculative scaffolding.

Immediate next action: **review and reconcile Q09-Q20 before Q21 feature work**.
The current stack is useful, but it is mostly `needs_review`, `.aide/profile.yaml`
is stale, `aide self-check` still points back to Q09, and `.aide/scripts/tests`
cannot be run by standard `unittest discover`.

## 2. Binding Goal Assessment

Binding goal:

> Using AIDE reduces token usage and charges for equivalent-quality work.

Current evidence for token reduction:

- Latest task packet: 914 approximate tokens vs 60,922-token root-history
  baseline, 98.5% estimated reduction.
- Latest review packet: 1,630 approximate tokens vs 6,995-token review
  baseline, 76.7% estimated reduction.
- Latest context packet: 482 approximate tokens vs 64,915-token broad repo
  context baseline, 99.3% estimated reduction.
- Raw prompt and response storage are disabled in token ledger, cache, Gateway,
  eval, controller, and provider metadata surfaces.

Current evidence for quality preservation:

- `aide_lite.py verify` passed with 0 warnings and 0 errors before audit
  artifacts were added.
- Golden tasks passed: 6 pass / 0 warn / 0 fail.
- Review packet required shape passed and remained under budget.
- Route explain preserved quality gates and remained advisory.
- Provider/Gateway/cache surfaces all report no live calls and no raw logs.
- Harness, Compatibility, Gateway, Provider, and direct AIDE Lite tests passed.

Missing evidence:

- No external coding-task quality eval exists.
- Golden tasks test AIDE's own token-survival substrate, not arbitrary repo work.
- Token estimates use chars/4, not exact tokenizer/provider billing.
- No real premium-model review outcomes are recorded for Q09-Q20.
- Most Q09-Q20 queue items remain `needs_review`; their quality is not accepted.

Assessment: **partially satisfied**. AIDE can already reduce prompt surfaces for
its own queue workflow, and it preserves local mechanical gates. It cannot yet
honestly claim equivalent-quality coding outcomes across real tasks.

## 3. Repository Snapshot

- Branch: `main`
- Commit at audit start: `84b579ce8e50a38aecad23cd6a7408e3646bd8c9`
- Working tree at audit start: clean
- Tracked files: 804
- Max-depth-3 inventory count excluding `.git`: 417 files
- `.aide.local/`: does not exist, is ignored by `.gitignore`, and has no tracked
  paths
- `.env`: absent
- `secrets/`: absent
- Python: `py -3` / Python 3.11.9
- Audit command run refreshed non-canonical generated reports under
  `.aide/context/**`, `.aide/reports/**`, `.aide/cache/**`, `.aide/routing/**`,
  `.aide/gateway/**`, `.aide/evals/runs/**`, and `.aide/controller/**`.

## 4. Queue State

Summary:

- Highest queue item present before this checkpoint: Q20.
- Highest queue item claimed implemented: Q20.
- Highest queue item with raw `passed` status: Q08, plus Q04 and Q07.
- Q05 and Q06 have review evidence indicating PASS_WITH_NOTES, but raw status
  remains `needs_review`.
- Q09-Q20 are implemented and `needs_review`.
- Q18 has `task.yaml` status drift: `running` while `status.yaml` and index say
  `needs_review`.
- Q00-Q03 remain `needs_review` despite later work proceeding.
- QCHECK is now registered as `needs_review`.

Required action:

- Do not continue assuming Q09-Q20 are accepted.
- Add a review/reconciliation queue item before Q21.
- Fix Q18 task/status mismatch.
- Update `.aide/profile.yaml` and self-check guidance after review.

## 5. Layer State Matrix

| Layer | Present | Implemented | Tested | Documented | Evidence | Status | Token Value | Quality Value | Current Risk | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bootstrap P00-P15 continuity | yes | historical | partial | yes | historical | mixed | indirect | continuity | stale historical claims possible | keep as historical |
| Q00-Q08 reboot foundation | yes | mostly | Harness checks | yes | yes | Q04/Q07/Q08 passed; Q00-Q03/Q05/Q06 nuanced | indirect | governance | review-gate nuance | reconcile review posture |
| Q09 Token Survival | yes | yes | yes | yes | yes | needs_review | high | medium | unaccepted | review |
| Q10 AIDE Lite | yes | yes | direct tests | yes | yes | needs_review | high | medium | large monolith | review and split later |
| Q11 Context Compiler | yes | yes | direct tests | yes | yes | needs_review | high | medium | metadata only | review |
| Q12 Verifier | yes | yes | direct tests | yes | yes | needs_review | high | high mechanical | structural only | review and deepen |
| Q13 Evidence Review | yes | yes | direct tests | yes | yes | needs_review | high | high review discipline | packet depends on evidence quality | review |
| Q14 Token Ledger | yes | yes | direct tests | yes | yes | needs_review | high | medium | estimates only | review |
| Q15 Golden Tasks | yes | yes | direct tests | yes | yes | needs_review | medium | high local | self-referential | review and add real tasks |
| Q16 Outcome Controller | yes | yes | direct tests | yes | yes | needs_review | medium | medium | advisory heuristics | review |
| Q17 Router Profile | yes | yes | direct tests | yes | yes | needs_review | medium | high hard floors | advisory only | review |
| Q18 Cache/Local State | yes | yes | direct tests | yes | yes | needs_review | medium future | high safety | task.yaml status drift | repair/review |
| Q19 Gateway Skeleton | yes | skeleton | unit tests | yes | yes | needs_review | low immediate | medium visibility | easy to overread as product Gateway | freeze until review |
| Q20 Provider Adapter | yes | metadata only | unit/direct tests | yes | yes | needs_review | low immediate | high safety boundary | capability unproven | freeze until review |
| Q21+ Tool Integration | task packet only | no | no | planned | no | future | potentially high | unknown | premature before review | defer until repair/review |

## 6. Code Audit

Strengths:

- Python remains standard-library only for AIDE Lite, Gateway, and Provider code.
- Most command outputs are deterministic and stable enough for committed metadata.
- Commands report no provider/model/network calls.
- The safety boundary is consistently encoded in tests and status artifacts.
- `core/gateway` and `core/providers` are importable and tested.

Findings:

1. `.aide/scripts/aide_lite.py` is now a very large multi-domain script. It is
   useful for bootstrapping but becoming hard to reason about.
2. Standard `unittest discover -s .aide/scripts/tests -t .` fails because the
   hidden `.aide` start directory is not importable.
3. AIDE Lite currently uses simple text/YAML-like parsing in several places.
   That is acceptable for stdlib-only phases, but brittle for future contracts.
4. `current_queue_ref()` is stale and only knows Q09-Q17.
5. Some tests validate anchors and report shapes more than semantic behavior.
6. Generated commands mutate latest artifacts as a side effect of validation.
   This is expected but should be clearer in audit/review workflows.
7. Cache keys mark dirty state during an audit because report commands create
   uncommitted generated artifacts.

Top missing tests:

- End-to-end review of one real code-change queue item using compact packets.
- Failure-mode tests for malformed queue status/index contradictions.
- Importable test discovery from `.aide/scripts/tests`.
- Regression tests for `.aide/profile.yaml` freshness versus queue index.

## 7. Docs Audit

Accurate:

- README, ROADMAP, PLANS, IMPLEMENT, DOCUMENTATION, AGENTS, and reference docs
  now broadly describe Q09-Q20.
- Provider/Gateway docs correctly state no live calls or forwarding.
- Token ledger docs correctly state estimates are not billing truth.

Stale or inconsistent:

- `.aide/profile.yaml` still says current focus is Q09 and lists Gateway/providers
  as deferred without reflecting Q19/Q20 metadata-only implementation.
- `scripts/aide self-check` still recommends Q09 as next step.
- Q18 `task.yaml` says `running`; status/index say `needs_review`.
- Q05/Q06 raw statuses remain `needs_review` while self-check accepts them by
  review evidence.
- Q00-Q03 remain `needs_review` but later work depends on their outputs.
- AIDE Lite generated context packet's current queue reference can lag because
  its hardcoded lookup ends at Q17.

## 8. Validation Results

See `test-validation-audit.md` and `evidence/commands-run.md`.

High-level result:

- Harness validate/doctor/self-check: PASS_WITH_WARNINGS.
- AIDE Lite stack: PASS, with token near-budget warnings and outcome advisory
  WARN for packet size.
- Unit tests: core Harness/Compat/Gateway/Provider pass.
- AIDE Lite tests: direct test files pass; hidden-dir unittest discovery fails.
- Syntax compile: PASS, 55 files.
- Secret scan: no real secrets found after inspection.

## 9. Token-Survival Audit

What works now:

- `pack` creates compact task packets.
- `context` creates compact repo metadata packets.
- `review-pack` creates compact evidence review packets.
- `ledger scan/report` records estimated token metadata.
- `estimate` reports surface budget status.
- `eval run` protects local packet/evidence/ledger behavior.
- `route explain` routes advisory work units without spending model tokens.

What remains limited:

- `chars/4` is an estimate only.
- Baselines are naive but useful.
- No quality-adjusted cost benchmark exists.
- No real provider billing, cached-token, or reasoning-token accounting exists.
- No cross-repo workload has been measured.

Verdict: the token-saving substrate is real and immediately usable for AIDE's
own queue work, but the product claim must remain scoped.

## 10. Quality Gate Audit

Present gates:

- Verifier: structural, file refs, diff scope, token warnings, obvious secrets.
- Golden tasks: deterministic local checks over AIDE token-survival artifacts.
- Review packet: compact evidence-only review request with decision policy.
- Token ledger: budget and regression warnings.
- Route hard floors: security, architecture, self-modification, governance.
- Cache/local-state boundary: prevents committed runtime state.
- Provider/Gateway no-call tests: preserve safety.

Missing gates:

- Real coding task golden suite.
- Cross-repo acceptance fixtures.
- Semantic diff analysis.
- Reviewer outcome tracking for Q09-Q20.
- CI integration.

Claim status: AIDE can claim "smaller prompt with mechanical local gates" today.
It cannot yet claim "same or better arbitrary coding quality."

## 11. Security / Privacy / Secret Audit

- `.aide.local/`: ignored, untracked, absent.
- `.env`: absent.
- `secrets/`: absent.
- Targeted scan matched policy/test/template strings only.
- Provider metadata contains no credentials and all Q20 live calls are disabled.
- Cache reports contain metadata and hashes, not content.
- Token ledger stores metadata only.
- Gateway responses are local/report-only and do not include raw prompt/response
  bodies.

Risk: future provider/Gateway phases must not relax these constraints without a
reviewed credential/local-state policy.

## 12. Consistency Audit

| Contradiction | Severity | Recommended Fix | Urgent |
| --- | --- | --- | --- |
| `.aide/profile.yaml` says current focus is Q09 while queue/docs are at Q20 | high | QFIX profile/current-focus reconciliation | yes |
| `scripts/aide self-check` next step says Q09 | high | Update self-check logic/report after review | yes |
| Q18 `task.yaml` status `running` vs index/status `needs_review` | medium | QFIX queue status reconciliation | yes |
| Q09-Q20 implemented but all `needs_review` | high | Batch review or review packets per phase | yes |
| Q05/Q06 accepted by review evidence but raw status `needs_review` | medium | Decide whether raw status stays nuanced or moves to passed_with_notes model | soon |
| AIDE Lite context current queue hardcoded through Q17 | medium | Fix current queue discovery | soon |
| `.aide/scripts/tests` direct tests pass but discover fails | medium | Add importable test package path or supported runner | soon |
| Generated manifest source fingerprint stale | medium | Reviewed generated-artifact refresh or accepted drift note | soon |

## 13. Completeness Audit

Complete enough for review:

- Q09-Q20 queue packets, evidence, docs, commands, and tests exist.
- Token-survival workflow is usable locally.
- Provider/Gateway boundaries are safe and no-call.

Partial:

- Review acceptance is missing for Q09-Q20.
- `.aide/profile.yaml` and self-check are stale.
- Tests are split between direct execution and importable suites.

Scaffold-only:

- Gateway skeleton is local/report-only.
- Provider adapters are metadata-only.
- Router is advisory-only.
- Cache is key metadata only.
- Outcome controller is recommendation-only.

Missing:

- Real external-repo task evaluation.
- Exact tokenizer/provider billing.
- Live provider execution policy and implementation.
- Tool adapter compiler.
- CI or one-command full validation runner.

## 14. Red-Herring Audit

See `red-herring-audit.md`. Short version: Gateway and provider scaffolding are
safe because they are no-call contracts, but more work in that direction would be
low ROI until review acceptance, profile sync, and real tool/task evals exist.

## 15. Grand Plan Reassessment

Q09-Q20 direction was mostly correct: context reduction, evidence review,
verification, token accounting, golden tasks, routing, cache/local-state, and
provider/Gateway boundaries are the right order for safe token survival.

What was overbuilt:

- AIDE Lite accumulated too many domains in one script.
- Gateway/provider skeletons arrived before Q09-Q18 were reviewed.
- Some reports are more numerous than the current product usage justifies.

What was underbuilt:

- Queue review/reconciliation.
- One-command validation ergonomics.
- Real coding golden tasks.
- Cross-repo usefulness proof.

Shortest path to token savings this week:

1. Review/reconcile Q09-Q20.
2. Fix profile/self-check/test-discovery drift.
3. Use `pack`, `context`, `review-pack`, `ledger report`, and `eval run` on the
   next real queue item instead of long prompts.

Shortest path to other repos:

1. Extract or document a minimal AIDE Lite package boundary.
2. Add a small external fixture repo or synthetic repo workload.
3. Measure compact packets and quality gates against that workload.

Shortest path to safe Gateway/provider execution:

1. Keep provider calls disabled.
2. Add existing-tool adapter compiler first.
3. Add credential/local-state setup tests before any live probe.
4. Require golden tasks and verifier to pass before provider execution.

## 16. Immediate Fix List

P0 before continuing:

- Review or reconcile Q09-Q20 status/evidence.
- Update `.aide/profile.yaml` current focus and implemented reality.
- Fix self-check next recommendation.
- Fix Q18 `task.yaml` status drift.

P1 soon:

- Fix `.aide/scripts/tests` unittest discovery.
- Fix `current_queue_ref()` hardcoding.
- Add one-command audit/validation runner.
- Add real coding-task golden fixtures.

P2 cleanup:

- Split AIDE Lite into importable modules after the foundation is reviewed.
- Reduce noisy generated report churn.
- Decide whether Q05/Q06 raw status should remain nuanced.

Deferred:

- Live Gateway forwarding.
- Provider probes/calls.
- Exact tokenizer/provider billing.
- UI/Commander/Runtime/MCP/A2A.

## 17. Recommended Next Queue

Next three:

1. `QFIX-foundation-review-reconciliation`: review Q09-Q20, reconcile statuses,
   update Profile/current focus, self-check recommendation, and Q18 status drift.
2. `QFIX-aide-lite-test-discovery-and-runner`: make `.aide/scripts/tests`
   importable/discoverable and add a single supported validation runner.
3. `Q21-existing-tool-adapter-compiler-v0`: compile deterministic existing-tool
   adapter metadata only after the two fixes above.

Next ten:

1. QFIX foundation review reconciliation.
2. QFIX AIDE Lite test discovery and validation runner.
3. Q21 Existing Tool Adapter Compiler v0.
4. Q22 Real Coding Golden Tasks v0.
5. Q23 External Repo Pilot v0.
6. Q24 AIDE Lite module split.
7. Q25 Token Quality Scorecard.
8. Q26 Provider Probe Policy v0.
9. Q27 Credential Setup Boundary.
10. Q28 Gateway Provider Adapter Dry-Run Harness.

## 18. Final Recommendation

**Repair first.** Do not continue directly to more Gateway/provider/runtime/UI
work. The token-survival substrate works and should be preserved, but the next
queue should review/reconcile the Q09-Q20 foundation and fix drift before adding
another layer.
