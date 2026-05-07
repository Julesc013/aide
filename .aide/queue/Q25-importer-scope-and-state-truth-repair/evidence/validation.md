# Validation

Interpreter: Windows `py -3` using Python 3.11.

## Baseline Before Edits

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git rev-parse HEAD`: PASS,
  `8b19dad7f7666167f1f732b025ea36af1a2c3970`.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; stale QFIX-02/Q21
  followups remained.
- `py -3 .aide/scripts/aide_lite.py validate`: FAIL; export-pack checksum
  mismatch on `manifest.yaml`.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: FAIL; one checksum problem.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS; regenerated pack.
- `py -3 .aide/scripts/aide_lite.py pack-status` after export: PASS.
- `py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <temp> --dry-run`:
  PASS; 127 operations, 0 conflicts, but scope too broad for target pilots.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 112 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Targeted Repair Validation

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_export_import.py`:
  PASS, 12 tests.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS, 122 included files, 125 checksums.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS,
  `checksums_valid: true`, `boundary_result: PASS`,
  `checksum_problems: 0`.
- Safe import dry-run into a temp fixture: PASS, 105 planned writes,
  22 skipped optional broad roots, 0 conflicts.
- Safe import write into a temp fixture: PASS, 105 writes, 22 skipped optional
  broad roots, 0 conflicts.
- Imported fixture `doctor`: PASS.
- Imported fixture `snapshot`: PASS.
- Imported fixture `index`: PASS.
- Imported fixture `pack --task "Fixture Q25 smoke task"`: PASS.
- Fixture `core/` copied: false.
- Fixture `docs/` copied: false.
- Fixture `AGENTS.md` manual content preserved before the managed portable
  section.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; next step is Q25
  review, and stale QFIX-02/Q21 followups are absent.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q26 Eureka Pilot Review And Handover"`:
  PASS, `.aide/context/latest-task-packet.md`, 3,684 chars,
  921 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`:
  PASS, 3,684 chars, 921 approximate tokens, within budget.

## Final Validation Sweep

- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; 148 info, 7 warning,
  0 error. Warnings are existing review gates and generated manifest drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; next step is Q25 review.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS; export pack checksums
  and boundary pass. Existing token-ledger near-budget warnings remain.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 116 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `git check-ignore .aide.local/`: PASS.
- `git diff --check`: PASS; only line-ending warnings from Git on Windows.
- Targeted broad secret scan with `rg`: PASS_AFTER_INSPECTION. Matches were
  policy/example/test/path terms such as `TOKEN`, `SECRET_PATTERNS`,
  `api_key`, and `latest-task-packet`; no actual provider key, credential,
  `.env` content, `.aide.local` state, raw prompt log, or raw response log was
  found.
- Stricter key-shaped scan with `rg`: PASS_AFTER_INSPECTION. Matches were
  false positives from names like `compact-task-packet-required-sections`; no
  private key, provider env assignment, or credential value was found.

## Known Warnings

- Harness generated manifest source fingerprint drift remains an existing
  warning and is outside Q25 scope.
- Early queue review gates remain visible by design.
- AIDE Lite token ledger still reports existing near-budget warnings unrelated
  to Q25.
