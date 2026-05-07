# Commands Run

All commands were run from `D:\Projects\AIDE\aide` unless a read-only target
repo path is explicitly listed. Python interpreter used: `py -3`.

## Git / Queue State

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --short` | WARN | 0 | Initial checkpoint was clean per early run; after the required command sweep, generated/report artifacts were modified. |
| `git branch --show-current` | PASS | 0 | `main`. |
| `git rev-parse HEAD` | PASS | 0 | `e2088aed6dd32674c00b8d4701ce8c8be784fdde`. |
| `git log --oneline -30` | PASS | 0 | Q24, Q21, QFIX-02, QFIX-01, QCHECK, Q20 history present. |
| `Get-Content .aide/queue/index.yaml` | PASS | 0 | QFIX-01, QFIX-02, Q21, Q24 present; Q22/Q23 absent. |
| `Test-Path .aide/queue/Q22-eureka-import-pilot` | PASS | 0 | Missing. |
| `Test-Path .aide/queue/Q23-dominium-import-pilot` | PASS | 0 | Missing. |

## Harness Commands

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | Harness validation passed with known warning posture. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | 0 | No hard failures; next-step guidance has residual drift. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | 0 | Report-first; no stale Q09 recommendation, but QFIX-02/Q21 followups remain. |

## AIDE Lite Sweep

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | 0 | No hard failures. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | 0 | Token near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | 0 | Internal checks passed. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | 0 | Canonical test command passed. |
| `py -3 .aide/scripts/aide_lite.py snapshot` | PASS | 0 | Snapshot regenerated; 1,017 files. |
| `py -3 .aide/scripts/aide_lite.py index` | PASS | 0 | Repo/test/context indexes regenerated. |
| `py -3 .aide/scripts/aide_lite.py context` | PASS | 0 | Context packet 1,943 chars / 486 approx tokens. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 0 | 0 warnings/errors. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS | 0 | Review packet 6,658 chars / 1,665 approx tokens. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | PASS | 0 | Ledger regenerated; 3 near-budget warnings. |
| `py -3 .aide/scripts/aide_lite.py ledger report` | PASS | 0 | Summary regenerated; 83 records. |
| `py -3 .aide/scripts/aide_lite.py eval list` | PASS | 0 | 6 tasks. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 0 | 6/6 passed. |
| `py -3 .aide/scripts/aide_lite.py eval report` | PASS | 0 | Latest golden task report available. |
| `py -3 .aide/scripts/aide_lite.py outcome report` | WARN | 0 | Advisory packet-too-large warning. |
| `py -3 .aide/scripts/aide_lite.py optimize suggest` | PASS | 0 | Advisory recommendation produced. |
| `py -3 .aide/scripts/aide_lite.py route list` | PASS | 0 | No-call route metadata. |
| `py -3 .aide/scripts/aide_lite.py route validate` | PASS | 0 | Valid. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS | 0 | Advisory route decision refreshed. |
| `py -3 .aide/scripts/aide_lite.py cache status` | PASS | 0 | Local-state boundary protected. |
| `py -3 .aide/scripts/aide_lite.py cache report` | PASS | 0 | Metadata-only cache reports refreshed. |
| `py -3 .aide/scripts/aide_lite.py gateway status` | PASS | 0 | No-call status refreshed. |
| `py -3 .aide/scripts/aide_lite.py gateway endpoints` | PASS | 0 | Forwarding endpoints forbidden. |
| `py -3 .aide/scripts/aide_lite.py gateway smoke` | PASS | 0 | No-call smoke passed. |
| `py -3 .aide/scripts/aide_lite.py provider list` | PASS | 0 | 13 provider families listed. |
| `py -3 .aide/scripts/aide_lite.py provider status` | PASS | 0 | Live calls false, credentials false. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | 0 | Offline metadata valid. |
| `py -3 .aide/scripts/aide_lite.py provider probe --offline` | PASS | 0 | No-call offline readiness. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 0 | 122 files, 126 checksums, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py adapter list` | PASS | 0 | Targets listed. |
| `py -3 .aide/scripts/aide_lite.py adapter render` | PASS | 0 | Generated adapter manifest/drift refreshed. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | 0 | Adapter outputs valid. |
| `py -3 .aide/scripts/aide_lite.py adapter drift` | PASS | 0 | Codex current, preview-only targets absent. |

## Unit Tests

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 0 | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 0 | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 0 | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 0 | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 0 | 112 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | EXPECTED_FAIL | 1 | Non-canonical hidden-path command fails before test import. |

## Read-Only Target Repo Checks

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git -C D:\Projects\Eureka\eureka status --short` | PASS | 0 | Clean. |
| `git -C D:\Projects\Eureka\eureka branch --show-current` | PASS | 0 | `main`. |
| `git -C D:\Projects\Eureka\eureka rev-parse HEAD` | PASS | 0 | `4c726f849c39763476fa24b81529c7d0d282c844`. |
| `Test-Path D:\Projects\Eureka\eureka\.aide\context\latest-task-packet.md` | PASS | 0 | Missing; Q22 not imported. |
| `Test-Path D:\Projects\Eureka\eureka\.aide\memory\project-state.md` | PASS | 0 | Missing. |
| `git -C D:\Projects\Eureka\eureka check-ignore .aide.local/` | WARN | 1 | `.aide.local/` is not ignored in inspected Eureka repo. |
| `git -C D:\Projects\Dominium\dominium status --short` | WARN | 0 | Existing dirty files unrelated to this audit. |
| `git -C D:\Projects\Dominium\dominium branch --show-current` | PASS | 0 | `main`. |
| `git -C D:\Projects\Dominium\dominium rev-parse HEAD` | PASS | 0 | `5a3f5d84a5e3cdeda52cd4fcc4c682e120dbd9d0`. |
| `Test-Path D:\Projects\Dominium\dominium\.aide` | PASS | 0 | Missing; Q23 not imported. |
| `git -C D:\Projects\Dominium\dominium check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |

## Secret / Local State

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |
| `git status --ignored --short .aide.local .aide.local/` | PASS | 0 | No local-state path shown. |
| Broad `rg` secret scan | PASS_AFTER_INSPECTION | 0 | Policy/test/path matches only; no real secret. |
| Strict key-shaped `rg` scan | PASS | 1 | No key-shaped credential matches. |

## Notes

Outputs are summarized rather than pasted in full to avoid turning the audit
into another prompt-bloat source. No provider, model, network, Eureka mutation,
or Dominium mutation command was run.

## Final Structural Validation

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git diff --check` | PASS | 0 | No whitespace errors; Git emitted expected CRLF normalization warnings for generated/report files. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | 148 info, 7 warnings, 0 errors; existing review-gate and generated-manifest freshness warnings only. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | 0 | Same three token near-budget warnings; export pack checksums and adapter artifacts valid. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | 0 | Canonical AIDE Lite test command still passes. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | 0 | Adapter generated outputs validate; no provider/model/network calls. |
| Final broad `rg` secret scan | PASS_AFTER_INSPECTION | 0 | Policy/test/path matches only; no real credentials found. |
| Final strict key-shaped `rg` scan | PASS | 1 | No long provider key, provider env assignment, or private-key matches. |
| Final `git status --short` | WARN | 0 | Shows audit artifacts plus generated/report artifacts refreshed by the audit sweep. |
