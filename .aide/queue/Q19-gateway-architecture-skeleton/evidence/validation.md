# Q19 Validation

Interpreter: `py -3` / Python 3.11.9 unless noted.

## Baseline

- `git status --short`: PASS, clean before baseline commands.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings only.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, existing review-gate/generated-manifest warnings only.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, queue review-gate warnings only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with token-ledger near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote repo snapshot during baseline.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo/context maps during baseline.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote latest context packet during baseline.
- `py -3 .aide/scripts/aide_lite.py verify`: WARN because generated eval run files were dirty from baseline and outside active scope.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, generated compact review packet during baseline.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS with budget warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS with budget warnings.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, six golden tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, six pass / zero warn / zero fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, packet_too_large recommendation class.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, advisory recommendation only.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route decision.
- `py -3 .aide/scripts/aide_lite.py cache init`: PASS.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, generated cache metadata during baseline.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 914 approx tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 1780 approx tokens.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation.

Baseline generated churn was restored before Q19 edits.

## Final

- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 .aide/scripts/aide_lite.py gateway status`: PASS, wrote `.aide/gateway/latest-gateway-status.json` and `.aide/gateway/latest-gateway-status.md`.
- `py -3 .aide/scripts/aide_lite.py gateway endpoints`: PASS, listed `/health`, `/status`, `/route/explain`, `/summaries`, and `/version`; provider/model/network calls none.
- `py -3 .aide/scripts/aide_lite.py gateway smoke`: PASS, `/health`, `/status`, `/route/explain`, `/summaries`, and `/version` returned 200 payloads and `/unknown` returned safe 404 in-process.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest core.gateway.tests.test_gateway_skeleton`: PASS, 9 tests.
- `py -3 .aide/scripts/tests/test_gateway_commands.py`: PASS, 6 tests.
- `py -3 .aide/scripts/aide_lite.py adapt`: PASS, refreshed AGENTS managed guidance to Q19.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, repo snapshot generated without inline contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, repo map/test map/context index generated without inline contents.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 482 approx tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 75 checked files, 25 changed files, 200 info, 0 warnings, 0 errors at the time of the final run.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, compact review packet generated without inline contents.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 73 total ledger records, metadata only, no raw prompt/response storage.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, budget warnings only for existing near-budget surfaces.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, six golden tasks passed; generated `.aide/evals/runs/**` changes were restored because Q19 does not own those paths.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS, latest committed golden task report still PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, existing `packet_too_large` advisory class only.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, advisory recommendation only; applies automatically false.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route class `local_strong`, quality gate PASS, provider/model/network calls none.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS, `.aide.local/` ignored and untracked.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, cache-key metadata report generated without raw contents.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q20 Provider Adapter v0"`: PASS, wrote `.aide/context/latest-task-packet.md`.
- `py -3 .aide/scripts/aide_lite.py route explain --task-packet .aide/context/latest-task-packet.md`: PASS, refreshed route decision for latest task packet.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3626 chars / 907 approx tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with existing token-ledger near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- Direct per-file AIDE Lite tests (`test_aide_lite.py`, `test_verifier.py`, `test_review_pack.py`, `test_token_ledger.py`, `test_golden_tasks.py`, `test_outcome_controller.py`, `test_router_profile.py`, `test_cache_local_state.py`, `test_gateway_commands.py`): PASS, 81 tests.
- `git diff --check`: PASS with line-ending notices only.
- Targeted broad secret scan: PASS after inspection. Matches were policy/example/token terminology, file names such as `latest-task-packet`, and regex policy text; no actual provider key, credential, `.env` content, raw prompt log, raw response log, local cache, or `.aide.local` content was found.
- Targeted high-risk secret-like scans for long `sk-*` values and long `api_key`/`secret`/`token`/`password` assignments: PASS, no matches.

## Known Validation Gaps

- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation. Targeted AIDE Lite gateway tests pass by direct file invocation, and AIDE Lite `selftest` passes.
- `gateway serve` was implemented but not left running as a daemon. Localhost-only behavior is covered by core tests; `gateway smoke` exercises endpoint payloads in-process.
