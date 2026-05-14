# Q37 Validation

## Baseline Before Editing

- `git status --short`: PASS, clean at start.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`, remote `origin/main`.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, baseline `4cfe6bb4b777346a83eb39598ed463111cdcb631`.
- `git tag --list`: PASS, no tags.
- `git check-ignore .aide.local/`: PASS, ignored.
- `git diff --check`: PASS.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, pre-existing generated manifest fingerprint warning.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, same generated manifest warning.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, Q36 was `needs_review` and Q37 not yet implemented.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, baseline golden tasks passed.
- `py -3 .aide/scripts/aide_lite.py intent compile --prompt "Plan Q37 Repo Intelligence Index v0 from the current AIDE repository state"`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py intent status`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.
- Baseline generated preview/report churn outside Q37 scope was restored before editing.

## Implementation Validation

- `py -3 -m py_compile .aide/scripts/aide_lite.py`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q37_repo_intelligence.py`: PASS, 7 tests.
- Q37 golden tasks: PASS individually.
- `py -3 .aide/scripts/aide_lite.py repo inventory`: PASS, wrote `.aide/repo/*`.
- `py -3 .aide/scripts/aide_lite.py repo classify`: PASS, same pipeline.
- `py -3 .aide/scripts/aide_lite.py repo validate`: WARN, all required files/schemas passed and 146 unknown classifications were reported.
- `py -3 .aide/scripts/aide_lite.py repo status`: PASS, 1,514 files, 146 unknown, 451 orphan candidates.
- `py -3 .aide/scripts/aide_lite.py repo explain-file .aide/scripts/aide_lite.py`: PASS.
- `py -3 .aide/scripts/aide_lite.py repo docs`: PASS, doc-link map generated.
- `py -3 .aide/scripts/aide_lite.py repo tests`: PASS, 35 test records.
- `py -3 .aide/scripts/aide_lite.py repo deps`: PASS, 1,514 dependency records.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS, 274 files included, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS, checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q38 File Quality Ledger v0"`: PASS, `.aide/context/latest-task-packet.md`, 967 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS, within 3,200-token budget.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS after amending the docs commit metadata to include all Q27 trailers.
- `py -3 .aide/scripts/aide_lite.py commit check --range 4cfe6bb..HEAD`: PASS for the five Q37 commits before the final pack/evidence commit.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS; generated preview outputs were restored because they are outside Q37 scope.
- `py -3 .aide/scripts/aide_lite.py changelog validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS, report-only.
- `py -3 .aide/scripts/aide_lite.py github validate`: PASS, report-only.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests`: TIMEOUT after 904 seconds. The canonical QFIX-02 runner is `py -3 .aide/scripts/aide_lite.py test`, which passed.
- Targeted `rg` secret scan: PASS_AFTER_INSPECTION. Matches were policy, path, generated-reference, regex, and fake-test terms such as `api_key`, `SECRET`, `TOKEN`, `PASSWORD`, and `sk-ant`; no actual provider key, credential, private key, `.env` content, `.aide.local` state, raw prompt log, or raw response log was found.

## Known Warnings

- Harness `validate`, `doctor`, and `self-check` still report the pre-existing generated manifest fingerprint warning.
- Harness `doctor` and `self-check` still print Q36 as the next recommended step from core Harness code outside Q37 allowed paths.
- `repo validate` intentionally returns WARN for unknown deterministic classifications; this is evidence for Q38/Q39, not deletion advice.
