# Validation

Interpreter used: `py -3` (Python 3.11 on Windows).

## Baseline Before Edits

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | clean |
| `git branch --show-current` | PASS | `main` |
| `git rev-parse HEAD` | PASS | `997cfe5c52e0bc5e9075ab3bca417bd7ba231867` |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` is ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors; inherited review-gate and generated-manifest warnings. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | No hard structural errors; QFIX-02 still at review gate. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only; Q09-Q20 accepted with notes; QFIX-02 at review gate. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q09-Q20 artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Token ledger near-budget warnings only. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Internal AIDE Lite checks pass. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | QFIX-02 canonical AIDE Lite validation command. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 94 tests before Q21 tests. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |

## Implementation Validation

| Command | Result | Notes |
| --- | --- | --- |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | Generated pack with 111 included files, 115 checksums, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid; boundary PASS; no violations. |
| `py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture> --dry-run` | PASS | operation_count 116, conflicts 0, written 0. |
| `py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture>` | PASS | operation_count 116, conflicts 0, written 116. |
| `<fixture> py -3 .aide/scripts/aide_lite.py doctor` | PASS | Expected warnings for missing source queue status/history in portable target. |
| `<fixture> py -3 .aide/scripts/aide_lite.py snapshot` | PASS | Wrote target-local snapshot. |
| `<fixture> py -3 .aide/scripts/aide_lite.py index` | PASS | Wrote target-local repo map, test map, and context index. |
| `<fixture> py -3 .aide/scripts/aide_lite.py pack --task "Fixture target smoke task"` | PASS | chars 3789, approx tokens 948, budget PASS. |
| `<fixture> py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | approx tokens 948. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py` | PASS | 8 Q21 export/import tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 102 AIDE Lite tests after Q21 tests. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q22 Eureka Import Pilot"` | PASS | Generated Q22 task packet. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | chars 3668, approx tokens 917, budget PASS. |

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | Dirty only with Q21 scoped changes before final commit. |
| `git diff --check` | PASS | No whitespace errors. Git emitted standard Windows LF-to-CRLF working-copy warnings. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` remains ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | 148 info, 7 warnings, 0 errors. Warnings are inherited review-gate/generated-manifest warnings. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same inherited warning set. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only; still recommends QFIX-02 review because QFIX-02 remains at review gate. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Q21 artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Export/import artifacts, checksums, and boundary checks pass; token ledger near-budget warnings remain nonfatal. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Internal checks pass. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Canonical AIDE Lite validation command passes. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 111 included files, 115 checksums, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary PASS, zero checksum problems, zero boundary violations. |
| `py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture> --dry-run` | PASS | operation_count 116, conflicts 0, written 0. |
| `py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture>` | PASS | operation_count 116, conflicts 0, written 116. |
| `<fixture> py -3 .aide/scripts/aide_lite.py doctor` | PASS | Expected missing-Q09-Q20 queue status warnings in portable target. |
| `<fixture> py -3 .aide/scripts/aide_lite.py snapshot` | PASS | Wrote target-local snapshot. |
| `<fixture> py -3 .aide/scripts/aide_lite.py index` | PASS | Wrote target-local repo map, test map, and context index. |
| `<fixture> py -3 .aide/scripts/aide_lite.py pack --task "Fixture target smoke task"` | PASS | chars 3789, approx tokens 948, budget PASS. |
| `<fixture> py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | approx tokens 948, within budget. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q22 Eureka Import Pilot"` | PASS | Q22 task packet unchanged after final generation. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | chars 3668, approx tokens 917, budget PASS. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | PASS | latest review packet chars 8981, approx tokens 2246, budget PASS, verifier PASS. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 102 tests. |
| targeted `rg` secret scan | PASS_AFTER_INSPECTION | Matches were policy/test/template terms, generated path names, regex definitions, placeholder wording, and fake test fixtures such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, and `sk-ant` regex text. No actual provider key, credential, `.env` content, `.aide.local` state, raw prompt log, or raw response log was found. |

## Known Nonfatal Warnings

- Harness still reports inherited Q00-Q03/Q05/Q06 review-gate warnings.
- Harness still reports `.aide/generated/manifest.yaml` source fingerprint drift.
- Harness self-check still recommends QFIX-02 review because QFIX-02 has not
  been reviewed yet.
- AIDE Lite validate reports inherited token-ledger near-budget warnings.
- Imported fixture `doctor` reports missing Q09-Q20 queue status files because
  the portable pack intentionally excludes AIDE self-hosting queue history.
