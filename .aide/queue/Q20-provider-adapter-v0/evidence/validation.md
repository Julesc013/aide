# Q20 Validation

Interpreter: `py -3` / Python 3.11.9 unless noted.

## Baseline

- `git status --short`: PASS, clean before baseline commands.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, existing queue review-gate/generated-manifest warnings only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with existing token-ledger near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, generated baseline snapshot.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, generated baseline repo/context maps.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 482 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 75 checked files, 5 changed files from baseline-generated artifacts, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, baseline review packet 6,900 chars / 1,725 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 73 total records, three near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, three near-budget warnings.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, six golden tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, six pass / zero warn / zero fail.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, existing packet_too_large advisory class only.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, advisory recommendation only.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route class `local_strong`.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS, `.aide.local/` ignored and untracked.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, generated cache metadata only.
- `py -3 .aide/scripts/aide_lite.py gateway status`: PASS.
- `py -3 .aide/scripts/aide_lite.py gateway endpoints`: PASS.
- `py -3 .aide/scripts/aide_lite.py gateway smoke`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,626 chars / 907 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 6,900 chars / 1,725 approximate tokens after baseline refresh.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation.

Baseline generated churn was restored before Q20 edits.

## Final

- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS. Warnings are existing queue review-gate/generated-manifest drift warnings; no Q20 hard errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS. Same existing review-gate/generated-manifest warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS. Self-check remains report-only with no provider/model/network calls.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS. Provider adapter artifacts are present and Q20 is `needs_review`.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS. Four token-ledger near-budget warnings remain: cache report, Q17 validation evidence, Q18 validation evidence, and latest review packet.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, `.aide/context/repo-snapshot.json` written, 791 files, contents not inlined.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, repo map/test map/context index written, contents not inlined.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, latest context packet 1,926 chars / 482 approximate tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, 89 checked files, 38 changed files, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest review packet 8,387 chars / 2,097 approximate tokens, contents not inlined.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 73 total records, 4 near-budget warnings, 0 regression warnings, raw prompt/response storage false.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, 73 records. Largest surfaces include `AGENTS.md` 3,181 tokens, cache report 2,243 tokens, Q18 validation evidence 2,203 tokens, Q17 validation evidence 2,141 tokens, and review packet 2,097 tokens.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 golden tasks.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 6 pass / 0 warn / 0 fail, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS, token-quality statement present.
- `py -3 .aide/scripts/aide_lite.py outcome report`: WARN, existing `packet_too_large` advisory class only, 0 failures, advisory-only.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, one advisory recommendation `REC-PACKET-BUDGET`, applies automatically false.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS, route classes and hard floors listed; provider/model/network calls none.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS, route decision shape valid.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, advisory route class `local_strong`, task class `bounded_code_patch`, risk `medium`, quality gates PASS, token budget near_budget, provider/model/network calls none.
- `py -3 .aide/scripts/aide_lite.py cache status`: PASS, `.aide.local/` ignored and no tracked/staged local-state paths.
- `py -3 .aide/scripts/aide_lite.py cache report`: PASS, 8 metadata keys written, contents not inlined, raw prompt/response storage false.
- `py -3 .aide/scripts/aide_lite.py gateway status`: PASS, local skeleton status refreshed, missing readiness refs 0, no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py gateway endpoints`: PASS, Q19 local/report-only endpoints listed; forbidden forwarding endpoints remain absent.
- `py -3 .aide/scripts/aide_lite.py gateway smoke`: PASS, `/health`, `/status`, `/route/explain`, `/summaries`, `/version`, and safe 404 checked.
- `py -3 .aide/scripts/aide_lite.py provider list`: PASS, 13 provider families listed, all `live_calls_allowed_in_q20=false`.
- `py -3 .aide/scripts/aide_lite.py provider status`: PASS, latest provider status JSON/Markdown written, 13 provider families, 6 credential-required planned families, `credentials_configured=false`, `live_provider_calls=false`, `live_model_calls=false`.
- `py -3 .aide/scripts/aide_lite.py provider validate`: PASS, required provider policy/metadata/core files present, no obvious secrets, provider metadata validates.
- `py -3 .aide/scripts/aide_lite.py provider contract`: PASS, adapter contract required fields printed and Q20 no-call boundary confirmed.
- `py -3 .aide/scripts/aide_lite.py provider probe --offline`: PASS, metadata-only readiness; no provider/network/model calls; future credentials location `.aide.local/`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q21 Existing Tool Adapter Compiler v0"`: PASS, latest Q21 task packet unchanged at 3,654 chars / 914 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 3,654 chars / 914 approximate tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS, 8,387 chars / 2,097 approximate tokens / near budget.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS, internal provider checks included.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL, existing hidden `.aide` start-directory importability limitation (`ImportError: Start directory is not importable`). This was present at baseline and is not introduced by Q20.
- Direct execution of `.aide/scripts/tests/test_*.py`: PASS, 90 tests across AIDE Lite, verifier, review-pack, token-ledger, golden-task, outcome-controller, router, cache, gateway-command, and provider-adapter tests.
- `git diff --check`: PASS, no whitespace errors. Git emitted Windows line-ending normalization warnings only.
- Targeted `rg` secret scan: PASS after inspection. Matches are policy/test/template terms, path names, regex definitions, placeholder wording, and generated references such as `TOKEN_ESTIMATE`, `api_key`, `SECRET`, and `sk-ant` pattern text; no actual provider key, credential, `.env` content, `.aide.local` state, raw prompt log, or raw response log was found.

## Known Gaps

- Q20 remains metadata-only and offline. No provider probes, credential setup, model calls, network calls, Gateway forwarding, live routing, provider billing, or provider response cache were implemented.
- Root Harness warnings about older queue review gates and generated-manifest source fingerprint drift remain pre-existing repository posture, not Q20 regressions.
- `.aide/scripts/tests` direct test execution passes, but Python `unittest discover` with hidden `.aide` as the start directory still fails before loading tests.
