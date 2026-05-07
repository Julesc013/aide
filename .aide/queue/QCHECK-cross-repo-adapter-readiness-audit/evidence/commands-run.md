# Commands Run

Interpreter: `py -3` resolved to Python 3.11 on Windows. Cwd is
`D:/Projects/AIDE/aide` unless noted.

## Git / Queue / State

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --short` | PASS | 0 | Clean at audit start. |
| `git branch --show-current` | PASS | 0 | `main`. |
| `git rev-parse HEAD` | PASS | 0 | `36dcb5cc9907f0e69d615d99ab2b0a1dcb17a2d0`. |
| `git log --oneline -30` | PASS | 0 | Shows QFIX-01, QFIX-02, Q21, Q24, QCHECK, and Q22/Q23-related Q24 refresh history. |
| `Get-Content .aide/queue/index.yaml` | PASS | 0 | QFIX-01, QFIX-02, Q21, Q24, QCHECK present; Q22/Q23 absent from AIDE source index. |
| `Get-Content .aide/profile.yaml` | PASS | 0 | Found stale QFIX-01/QFIX-02/Q21 current focus. |
| `Get-Content .aide/commands/catalog.yaml` | PASS | 0 | Command catalog includes Q24 adapter commands; import note retains Q22/Q23 future wording. |
| `git check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |

## Harness / AIDE Lite

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | 148 info, 7 warnings, 0 errors. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | 0 | Same warnings as validate. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | 0 | Report-only, no mutation, no external calls; stale QFIX-02/Q21 followups remain. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | 0 | Q09-Q20 passed; Q24 adapter status current. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | 0 | 3 token-ledger near-budget warnings, 0 errors. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | 0 | Internal AIDE Lite checks pass. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | 0 | Canonical QFIX-02 test command passes. |

## AIDE Lite Command Sweep

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 .aide/scripts/aide_lite.py snapshot` | PASS | 0 | Wrote non-canonical snapshot during audit: 1,035 files, about 910,297 aggregate approx tokens. |
| `py -3 .aide/scripts/aide_lite.py index` | PASS | 0 | Wrote repo map, test map, context index. |
| `py -3 .aide/scripts/aide_lite.py context` | PASS | 0 | Wrote context packet: 1,943 chars / 486 approx tokens. |
| `py -3 .aide/scripts/aide_lite.py verify` | PASS | 0 | 89 checked files, 6 changed files during audit, 195 info, 0 warnings/errors. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS | 0 | Wrote review packet: 6,639 chars / 1,660 approx tokens. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | PASS_WITH_WARNINGS | 0 | 83 records, 3 budget warnings, no raw prompt/response storage. |
| `py -3 .aide/scripts/aide_lite.py ledger report` | PASS_WITH_WARNINGS | 0 | 3 budget warnings, no regression warnings. |
| `py -3 .aide/scripts/aide_lite.py eval list` | PASS | 0 | 6 active golden tasks. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 0 | 6/6 golden tasks pass, no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py eval report` | PASS | 0 | Latest golden task report PASS. |
| `py -3 .aide/scripts/aide_lite.py outcome report` | WARN | 0 | Advisory warning: `packet_too_large`. |
| `py -3 .aide/scripts/aide_lite.py optimize suggest` | WARN | 0 | Advisory recommendation `REC-PACKET-BUDGET`. |
| `py -3 .aide/scripts/aide_lite.py route list` | PASS | 0 | No provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py route validate` | PASS | 0 | Route artifacts and decision shape valid. |
| `py -3 .aide/scripts/aide_lite.py route explain` | PASS_WITH_WARNING | 0 | Advisory route to frontier for unknown task; outcome recommendation WARN. |
| `py -3 .aide/scripts/aide_lite.py cache status` | PASS | 0 | `.aide.local/` ignored, no tracked local state. |
| `py -3 .aide/scripts/aide_lite.py cache report` | PASS | 0 | Wrote metadata-only cache report; raw prompt/response storage false. |
| `py -3 .aide/scripts/aide_lite.py gateway status` | PASS | 0 | Local skeleton report-only; no calls. |
| `py -3 .aide/scripts/aide_lite.py gateway endpoints` | PASS | 0 | Lists only health/status/route/summaries/version; forwarding forbidden. |
| `py -3 .aide/scripts/aide_lite.py gateway smoke` | PASS | 0 | Local endpoint smoke PASS, no calls. |
| `py -3 .aide/scripts/aide_lite.py provider list` | PASS | 0 | 13 provider families, live calls not allowed. |
| `py -3 .aide/scripts/aide_lite.py provider status` | PASS | 0 | Credentials not configured; live calls false. |
| `py -3 .aide/scripts/aide_lite.py provider validate` | PASS | 0 | Metadata validates; no obvious secrets. |
| `py -3 .aide/scripts/aide_lite.py provider probe --offline` | PASS | 0 | Offline probe only, no credentials/calls. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 0 | 122 included files, 126 checksums, boundary PASS. Generated changes restored after evidence capture. |
| `py -3 .aide/scripts/aide_lite.py pack-status` during dirty command sweep | PASS | 0 | Checksums valid immediately after export-pack refreshed working-tree pack artifacts. |
| `py -3 .aide/scripts/aide_lite.py adapter list` | PASS | 0 | 7 enabled rendered targets plus disabled VS Code optional target. |
| `py -3 .aide/scripts/aide_lite.py adapter render` | PASS | 0 | Outputs unchanged; drift report unchanged. |
| `py -3 .aide/scripts/aide_lite.py adapter preview` | PASS | 0 | Writes none; preview-only targets respected. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | 0 | Adapter required files/templates/generated outputs pass. |
| `py -3 .aide/scripts/aide_lite.py adapter drift` | PASS | 0 | AGENTS current; non-AGENTS targets preview-only. |
| `py -3 .aide/scripts/aide_lite.py adapt` | PASS | 0 | `AGENTS.md` unchanged/current. |
| `py -3 .aide/scripts/aide_lite.py adapt` second run | PASS | 0 | Deterministic; unchanged/current. |

## Tests

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 0 | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 0 | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 0 | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 0 | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 0 | 112 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests -t .` | FAIL_EXPECTED | 1 | Non-canonical hidden-path discovery form fails with start directory not importable. |

## Generated Output Handling

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --short` after command sweep | WARN | 0 | Generated latest artifacts were dirty from report commands. |
| `git diff --name-only` | WARN | 0 | 17 generated files modified. |
| `git diff --stat` | WARN | 0 | About 931 insertions / 319 deletions in generated latest artifacts. |
| `git restore -- <generated validation artifacts>` | PASS | 0 | Restored audit-run generated changes before writing reports. |
| `git status --short` after restore | PASS | 0 | Clean before report edits. |

## Read-Only Target Repo Inspection

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| Initial PowerShell target-inspection script | FAIL_SCRIPT | 1 | Parser error from `$name:` interpolation; no repo mutation. Corrected and reran. |
| `git -C D:/Projects/Eureka/eureka status --short` | PASS | 0 | Clean. |
| `git -C D:/Projects/Eureka/eureka branch --show-current` | PASS | 0 | `main`. |
| `git -C D:/Projects/Eureka/eureka rev-parse HEAD` | PASS | 0 | `dccfc9c5c97408c4c5fabd877b4caa7d92616813`. |
| `git -C D:/Projects/Eureka/eureka log --oneline -5` | PASS | 0 | Shows four AIDE import pilot commits. |
| `git -C D:/Projects/Eureka/eureka check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |
| Read Eureka `.aide/queue/EUREKA-AIDE-PILOT-01/**` | PASS | 0 | Import, token, validation, and quality evidence present. |
| Strict Eureka credential-shaped scan | PASS | 0 | No matches in inspected `.aide`, guidance, docs, and `.gitignore`. |
| `git -C D:/Projects/Dominium/dominium status --short` | PASS_WITH_WARNINGS | 0 | Two unrelated dirty FAST audit files. |
| `git -C D:/Projects/Dominium/dominium branch --show-current` | PASS | 0 | `main`. |
| `git -C D:/Projects/Dominium/dominium rev-parse HEAD` | PASS | 0 | `768140b807097456bc351a27fb56d4c4a239ee9a`. |
| `git -C D:/Projects/Dominium/dominium log --oneline -7` | PASS | 0 | Shows five AIDE import pilot commits. |
| `git -C D:/Projects/Dominium/dominium check-ignore .aide.local/` | PASS | 0 | `.aide.local/` ignored. |
| Read Dominium `.aide/queue/DOMINIUM-AIDE-PILOT-01/**` | PASS | 0 | Import, token, doctrine, validation, and quality evidence present. |
| Strict Dominium credential-shaped scan | PASS | 0 | No matches in inspected `.aide`, guidance, docs, and `.gitignore`. |

## Security / Local State

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --ignored --short .aide.local .aide.local/` | PASS | 0 | No tracked or ignored local-state files listed. |
| Broad AIDE `rg` secret scan | PASS_AFTER_INSPECTION | 0 | Matches were policy/example/test/path/regex terms; no actual secret found. Missing optional root tool files were reported by `rg`. |
| Strict AIDE credential-shaped scan | PASS | 0 | No matches. |

## Final Validation

| Command | Result | Exit | Summary |
| --- | --- | ---: | --- |
| `git status --short` | PASS | 0 | Only QCHECK audit files modified. |
| `git diff --check` | PASS_WITH_LINE_ENDING_WARNINGS | 0 | No whitespace errors; CRLF conversion warnings only. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 0 | 148 info, 7 warnings, 0 errors. |
| `py -3 .aide/scripts/aide_lite.py validate` | FAIL | 1 | Export pack checksum mismatch: `manifest.yaml`; other surfaces pass with known token warnings. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | 0 | Canonical test runner passes. |
| `py -3 .aide/scripts/aide_lite.py adapter validate` | PASS | 0 | Adapter compiler validation passes. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | FAIL | 1 | Checksums invalid, one problem, boundary PASS, zero boundary violations. |
| strict credential-shaped `rg` scan | PASS | 0 | No matches after report writes. |
