# Q30 Validation

## Baseline Before Q30 Edits

- `git status --short`: PASS, clean before baseline report generation.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `31bd0b29115c9686c4dbdf35577c6d22770ca346`.
- `git log --oneline --decorate -20`: PASS; Q27-Q29 commit sequences present.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate warnings and generated-manifest fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning classes.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; report-only.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 20/20 golden tasks before Q30.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS with dirty-tree and missing-`dev` warnings after baseline generation.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS_BLOCKED; dirty tree and missing `dev`.
- `py -3 .aide/scripts/aide_lite.py git sync --dry-run`: PASS_BLOCKED; dry-run only.
- `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev`: PASS_BLOCKED; source `main` protected and `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main`: PASS_BLOCKED; `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git prune --dry-run`: PASS; no eligible branches.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN before Q30; three malformed pre-Q27 commits.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | Shows Q30 generated artifacts, export pack, and evidence pending commit. |
| `git diff --check` | PASS | Exit 0; CRLF conversion warnings only. |
| `git branch --show-current` | PASS | `main`. |
| `git branch --all` | PASS | Local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`; no `dev`. |
| `git remote -v` | PASS | origin fetch/push URL present; no remote mutation run. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/`. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | Historical review-gate warnings and generated manifest fingerprint drift. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same warning classes; no hard errors. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Report-only; Q30 is now `needs_review`; next recommendation remains Q25 review because earlier review-gated queue items are still pending. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Includes Q30 policy/plan checks; token-ledger near-budget warnings remain classified. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Internal AIDE Lite selftest passes after Q30 fixture fix. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Same internal checks as `test`. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 22/22 golden tasks pass. |
| `py -3 .aide/scripts/aide_lite.py git detect` | PASS | `trunk_without_dev`, current branch `main`, role `canonical`, non-mutating. |
| `py -3 .aide/scripts/aide_lite.py git doctor` | PASS | Warns dirty tree and missing `dev`; policy present. |
| `py -3 .aide/scripts/aide_lite.py git status` | PASS | Reports `main` canonical and `dev` integration target. |
| `py -3 .aide/scripts/aide_lite.py git policy` | PASS | Q28/Q29/Q30 policy anchors pass. |
| `py -3 .aide/scripts/aide_lite.py git plan` | PASS_BLOCKED | Blocks on dirty tree classification and missing `dev`; no mutation. |
| `py -3 .aide/scripts/aide_lite.py git sync --dry-run` | PASS_BLOCKED | Dry-run only; dirty tree blocks apply. |
| `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev` | PASS_BLOCKED | Blocks protected source `main`, dirty tree, missing `dev`. |
| `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main` | PASS_BLOCKED | Blocks missing source `dev` and dirty tree. |
| `py -3 .aide/scripts/aide_lite.py git prune --dry-run` | PASS | Current/protected `main` not eligible. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS | Latest Q30 commit follows Q27 discipline. |
| `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~7..HEAD` | PASS | Q29 final commit plus Q30 commits passed; final evidence commit checked after commit. |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | PASS | 20 commits, 8 categories, 0 malformed commits in latest range. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 183 files, boundary PASS, no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary PASS. |
| `rg -n "aide_dev_main_policy_golden|aide_branch_plan_golden|test_q30_aide_dev_main_policy|aide-dev-main|aide-branch-policy" .aide/export/aide-lite-pack-v0/manifest.yaml .aide/export/aide-lite-pack-v0/files/.aide/evals/golden-tasks/catalog.yaml` | PASS | Exit 1 was treated as expected no-match; Q30 AIDE-local policy artifacts, tests, docs, and golden tasks are excluded from portable pack truth. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q31 Export Pack Sync for Git Commit Workflow"` | PASS | Latest task packet 3,700 chars / 925 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 925 approximate tokens, within budget. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_q30_aide_dev_main_policy.py` | PASS | 10 tests. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 165 tests after export-boundary test addition. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| Targeted `rg` secret scan | PASS_AFTER_INSPECTION | Matches are policy/test/path terms and regex definitions such as `api_key`, `SECRET`, `TOKEN`, `sk-ant`, and `latest-task-packet`; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt, or raw response was found. |

## Blockers Resolved During Final Validation

- `py -3 .aide/scripts/aide_lite.py test` and `selftest` initially failed after Q30 because the temporary selftest repo copied Q29 artifacts but not Q30 branch-policy artifacts. Fixed by copying `Q30_REQUIRED_FILES` into the selftest fixture. Both commands now PASS.

## Classified Remaining Warnings

- Missing local/remote `dev`: expected Q30 output; future explicit operator action required.
- Dirty tree during helper dry-runs: expected while generated artifacts and evidence were pending commit.
- Historical Harness review-gate and generated-manifest warnings: pre-existing, not Q30 failures.
- Token-ledger near-budget warnings: pre-existing classified budget warnings, not Q30 failures.
