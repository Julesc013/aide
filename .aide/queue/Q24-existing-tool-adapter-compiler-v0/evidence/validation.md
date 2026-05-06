# Validation

Interpreter used: `py -3` on Windows.

## Baseline Before Q24 Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | WARN | Worktree had pre-existing generated export-pack drift in `manifest.yaml` and `checksums.json`. |
| `git branch --show-current` | PASS | `main`. |
| `git rev-parse HEAD` | PASS | `4817b08319d10bef409debe802f9fff9b198526c`. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings; generated manifest drift and older review gates remain reported. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same warning posture. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only; no mutation, external calls, provider/model calls, or network calls. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 present; adapter status current before Q24 implementation. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Canonical AIDE Lite internal checks. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Compatibility alias. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 102 tests. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 111 included files, 115 checksums, boundary PASS. |

## Implementation And Regression Checks

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py adapter list` | PASS | Listed Codex, Claude Code, Aider, Cline, Continue, Cursor, Windsurf, and disabled VS Code optional target. |
| `py -3 .aide/scripts/aide_lite.py adapter render` | PASS | Generated 7 preview outputs, manifest, and drift report; no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py adapter preview` | PASS | Reported planned generated outputs; wrote nothing. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | Required files/templates/output guidance checks passed after template fixes. |
| `py -3 .aide/scripts/aide_lite.py adapter drift` | PASS | Codex managed section current; other tool outputs preview-only. |
| `py -3 .aide/scripts/aide_lite.py adapter generate` | PASS | Wrote or refreshed only safe `AGENTS.md` managed section. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | `unchanged`; deterministic shortcut over safe AGENTS managed section. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | Second run also `unchanged`, proving determinism. |
| `py -3 -m unittest .aide.scripts.tests.test_adapter_compiler` | FAIL_EXPECTED_INVALID_COMMAND | Hidden `.aide` path is not a package import path; this repeats the QFIX-02 discovery lesson. The supported command below was used. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_adapter_compiler.py` | PASS | 10 adapter compiler tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 112 full AIDE Lite tests after Q24. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | FAIL_THEN_FIXED | First post-Q24 run failed `test_adapt_replaces_managed_drift`; AGENTS template no longer contained the legacy context-packet phrase the test mutates. Q24 restored that compact context-packet rule and reran the suite successfully. |
| `py -3 .aide/scripts/aide_lite.py pack-status --pack .aide/export/aide-lite-pack-v0` | FAIL_INVALID_SYNTAX | `pack-status` has no `--pack` option in Q21/Q24. The correct command below passed. |

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | WARN | Expected dirty state before final commit: Q24 docs/evidence/status, generated adapter outputs, portable pack refresh, and latest task packet. |
| `git diff --check` | PASS | No whitespace errors; Git reported Windows CRLF normalization warnings only. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings. Known warnings are older review gates and stale `.aide/generated/manifest.yaml` source fingerprint. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same warnings; diagnostic text still recommends QFIX-02 review because Harness follow-up text was not in Q24 scope. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only, no mutation, no external calls. Queue health includes Q24 `needs_review`; proposed followups still mention QFIX-02/Q21 and are recorded as residual guidance drift. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q24 adapter status current. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Three token-ledger near-budget warnings inherited from older reports; no hard failures. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Internal estimate, ignore, snapshot, index, context, pack, adapt, drift, verifier, review-pack, ledger, eval, outcome, route, cache, gateway, provider, adapter, and validate checks passed. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Same internal check set passed. |
| `py -3 .aide/scripts/aide_lite.py adapter list` | PASS | Output shape correct; no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py adapter render` | PASS | 7 outputs; unchanged after final template regeneration. |
| `py -3 .aide/scripts/aide_lite.py adapter preview` | PASS | Preview only; no writes. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | Q24 adapter checks passed. |
| `py -3 .aide/scripts/aide_lite.py adapter drift` | PASS | Codex current; Claude/Aider/Cline/Continue/Cursor/Windsurf preview-only. |
| `py -3 .aide/scripts/aide_lite.py adapter generate` | PASS | Only safe AGENTS managed section considered; preview-only targets not written. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | `unchanged`, current. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | `unchanged`, current. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 122 included files, 126 checksums, boundary PASS; no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Run post-adapter-compiler checkpoint audit"` | PASS | `.aide/context/latest-task-packet.md`, 3716 chars, 929 approximate tokens, budget PASS. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 3716 chars, 113 lines, 929 approximate tokens, within budget. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests after Q24 template compatibility fix. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_adapter_compiler.py` | PASS | 10 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 112 tests. |
| Broad targeted `rg` secret scan | PASS_AFTER_INSPECTION | Matches were policy/test/template/path terms such as `TOKEN`, `SECRET_PATTERNS`, `api_key`, and `latest-task-packet`; no actual provider key, credential, `.env` content, `.aide.local` state, raw prompt log, or raw response log was found. |
| Strict key-shaped `rg` scan | PASS | No long `sk-*`, `sk-ant-*`, provider env assignment, or private-key matches found. |

## Known Warnings

- Harness still reports older Q00-Q03/Q05/Q06 review-gate nuance and stale
  `.aide/generated/manifest.yaml` source fingerprint.
- Harness `doctor` / `self-check` follow-up text still recommends QFIX-02
  review even though Q24 has now reached review. Q24 did not change Harness
  follow-up logic because `core/harness/**` was outside the allowed Q24 path
  list.
- AIDE Lite validation still reports three inherited token-ledger near-budget
  warnings for older reports.

## Safety Result

No validation command made provider calls, model calls, outbound network calls,
Gateway forwarding calls, tool runtime calls, or external repo mutations.
