# Validation

## Baseline Before Q34 Edits

- `git status --short`: PASS, clean before validation commands.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`, remote `origin/main`.
- `git remote -v`: PASS, `origin` read/write URLs recorded; no remote mutation performed.
- `git rev-parse HEAD`: PASS, `ca2cc5a1b5599eabd0a02f202dabea75d905844b`.
- `git tag --list`: PASS, no tags.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; known queue review-gate warnings and stale generated manifest warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 27/27 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~10..HEAD`: PASS, 10/10 commits.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS, early Q27 preview generated from `HEAD~20..HEAD`.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS, report-only; generated local reports.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS with warnings for dirty tree after generated baseline files and missing `dev`.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS with same report-only state.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, blocked plan due dirty generated baseline files; no mutation.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid, dirty source recorded.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS.

Generated baseline commands refreshed changelog, golden-run, and Git report files. These are Q34-allowed generated artifacts and will be regenerated again after implementation.

## Final Validation

- `git status --short`: PASS; expected Q34 generated/evidence/export files were dirty before final commit.
- `git diff --check`: PASS.
- `git branch --show-current`: PASS, `main`.
- `git tag --list`: PASS, no tags created.
- `git check-ignore .aide.local/`: PASS, `.aide.local/` ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; known queue review-gate warnings and stale generated manifest warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same known warning class.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 30/30 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~10..HEAD`: PASS, 10/10 commits.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN, preview generated for latest 50 commits with 77 categorized entries and 13 malformed/legacy commits reported.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog status`: PASS, 50 commits, 77 entries, 13 malformed/legacy commits, 8 populated categories.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS, report-only; detected `trunk_without_dev`, current branch `main`, current role `canonical`, no mutation.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS command exit with blocked plan; blockers were dirty-tree classification and missing `dev`; no mutation.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS, 206 files, 209 checksums, boundary result PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary result PASS.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q35 GitHub Protection and CI Advisory v0"`: PASS, `.aide/context/latest-task-packet.md`, 3,692 chars, 923 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, 923 approximate tokens, within 3,200-token budget.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- Targeted broad `rg` secret scan: PASS_AFTER_INSPECTION. Matches were policy, generated-reference, path, and test-fixture terms such as `TOKEN`, `api_key`, `SECRET_PATTERNS`, and regex text; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt, or raw response was found.
- Targeted strict key-shaped scan: PASS_AFTER_INSPECTION. Matches were negative assertions and fake verifier fixtures only; no real provider key or private key was found.

Generated `.aide/evals/runs/**` and `.aide/git/**` side effects from validation were restored before commit because they are outside the Q34 allowed commit scope.
