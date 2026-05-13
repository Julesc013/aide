# Validation

## Q35 Command Surface

- `py -3 .aide/scripts/aide_lite.py github advisory`: PASS.
- `py -3 .aide/scripts/aide_lite.py github status`: PASS.
- `py -3 .aide/scripts/aide_lite.py github protection`: PASS.
- `py -3 .aide/scripts/aide_lite.py github ci`: PASS.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS.

## AIDE Lite And Golden Tasks

- `py -3 .aide/scripts/tests/test_q35_github_advisory.py`: PASS, 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -v`: PASS, 189 tests.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 34/34 golden tasks,
  warn_count 0, fail_count 0.

## Harness And Core Tests

- `py -3 scripts/aide validate`: PASS, 149 info, 0 warnings, 0 errors.
- `py -3 scripts/aide doctor`: PASS, 149 info, 0 warnings, 0 errors.
- `py -3 scripts/aide self-check`: PASS, warning count 0.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Export And Generated Evidence

- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`:
  PASS, 220 files, 223 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid,
  boundary PASS, provenance recorded dirty source truthfully before commit.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.

## Safety Confirmation

- No `.github/workflows` files were created.
- No GitHub API mutation was performed.
- No branch creation, merge, push, prune, tag, or release publication occurred.
- No provider/model/network calls were introduced.
