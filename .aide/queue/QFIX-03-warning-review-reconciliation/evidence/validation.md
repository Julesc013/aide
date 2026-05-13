# Validation

Validation was run from `C:\Inbox\Git Repos\aide` on 2026-05-14.

## Harness

| Command | Result | Notes |
| --- | --- | --- |
| `git diff --check` | PASS | No whitespace errors. Git printed local LF/CRLF normalization notices only. |
| `py -3 scripts/aide compile --write` | PASS | Refreshed `.aide/generated/manifest.yaml`; final source fingerprint is current. |
| `py -3 scripts/aide validate` | PASS | `149 info, 0 warning, 0 error`. |
| `py -3 scripts/aide doctor` | PASS | `149 info, 0 warning, 0 error`; next step now points to Q35. |
| `py -3 scripts/aide self-check` | PASS | Validation section reports `warning: 0`; queue health has no AIDE-local `needs_review` blockers. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests passed. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests passed. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests passed. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests passed. |

## AIDE Lite

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | No WARN/FAIL checks after token ledger budget cleanup. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Internal estimate, ignore, snapshot, index, context, pack, adapt, drift, line-ref, verifier, review-pack, ledger, eval, commit, changelog, task, git workflow, outcome, optimize, route, cache, gateway, provider, adapter, and validate checks passed. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Same internal surface checks passed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 30/30 golden tasks passed; `warn_count: 0`, `fail_count: 0`. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | PASS | `budget_warnings: 0`; near-budget surfaces are retained as a watchlist, not validation warnings. |
| `py -3 .aide/scripts/tests/test_token_ledger.py` | PASS | 10 tests passed, including eval-report budget and near-budget watchlist behavior. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | NOT APPLICABLE | Raw package discovery fails because `.aide` is not an importable package; QFIX-02 canonical command is `py -3 .aide/scripts/aide_lite.py test`. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p "test_*.py"` | NOT USED | Raw discovery without `-t` timed out; canonical AIDE Lite test and targeted touched test passed. |

## Changelog And Pack

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | PASS | Preview generated; 9 malformed historical commits are reported for review, not hidden or treated as command failure. |
| `py -3 .aide/scripts/aide_lite.py changelog validate` | PASS | Markdown and JSON preview artifacts have required structure. |
| `py -3 .aide/scripts/aide_lite.py changelog status` | PASS | Preview-only status reports 50 commits, 90 entries, 9 malformed historical commits. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 206 files, 209 checksums, boundary PASS, no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary PASS, provenance result `DIRTY_SOURCE_RECORDED`. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q35 GitHub Protection and CI Advisory v0"` | PASS | Latest task packet unchanged at 3,692 chars / 923 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 923 approximate tokens, within 3,200-token hard limit. |

## Secret Scan

| Command | Result | Notes |
| --- | --- | --- |
| Broad `rg` policy scan | PASS_AFTER_INSPECTION | Matches are policy terms, path names, test fixtures, and regex text such as `TOKEN`, `api_key`, and `sk-ant`; no actual provider key, private key, `.env` content, `.aide.local` state, raw prompt, or raw response was found. |
| Strict key-shaped `rg` scan | PASS_AFTER_INSPECTION | Matches are test assertions that forbid `OPENAI_API_KEY=` and `BEGIN PRIVATE KEY`; no actual secret value was found. |
