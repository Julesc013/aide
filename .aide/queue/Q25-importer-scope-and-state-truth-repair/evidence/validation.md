# Validation

## Baseline Before Edits

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git rev-parse HEAD`: PASS,
  `8b19dad7f7666167f1f732b025ea36af1a2c3970`.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; stale QFIX-02/Q21
  followups remain.
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

Final validation will be appended before review.
