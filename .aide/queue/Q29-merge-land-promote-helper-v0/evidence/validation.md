# Q29 Validation

## Baseline Before Q29 Edits

- `git status --short`: PASS, clean.
- `git branch --show-current`: PASS, `main`.
- `git branch --all`: PASS, local `main`; remotes `origin/HEAD -> origin/main`, `origin/main`.
- `git remote -v`: PASS, origin `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS, `0fb6bb2872d718a3ad9f402c2cf026e2b583ebc4`.
- `git log --oneline --decorate -30`: PASS; Q28 commit sequence was present.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`; shell also emitted a local oh-my-posh init warning unrelated to Git ignore behavior.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing review-gate and generated-manifest fingerprint warnings.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same warning classes.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q29 was still listed as superseded before this reopen.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 15/15 golden tasks before Q29.
- `py -3 .aide/scripts/aide_lite.py git detect`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git doctor`: PASS; current branch `main`, role `canonical`, `dev` missing.
- `py -3 .aide/scripts/aide_lite.py git status`: PASS; report-only.
- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: WARN; pre-Q27 malformed commits are reported, no release publishing.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, provenance `DIRTY_SOURCE_RECORDED`, boundary PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: baseline timed out at two minutes before Q29 changes; rerun with longer timeout in final validation.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS, 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS, 8 tests.

## Final Validation

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | Shows Q29 generated docs, reports, queue status, export-pack, changelog, and context changes pending commit. |
| `git diff --check` | PASS | Exit 0; Git reported CRLF normalization warnings only. |
| `git branch --show-current` | PASS | `main`. |
| `git branch --all` | PASS | Local `main`; remote `origin/main`; no `dev` branch exists locally. |
| `git remote -v` | PASS | Origin fetch/push URLs present; no remote mutation performed. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` is ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | Existing review-gate warnings and stale generated-manifest source fingerprint; no Q29 hard failures. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Same existing warning classes; next recommended step still points at older review flow. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Reports Q29 at `needs_review`; older Q25/Q26 review recommendations remain inherited queue-state guidance. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Q29 helper policy, command docs, latest plan, and export-pack anchors pass. Token-ledger near-budget warnings are pre-existing. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Internal AIDE Lite checks pass. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Compatibility alias passes. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 20/20 golden tasks pass, including all five Q29 helper goldens. |
| `py -3 .aide/scripts/aide_lite.py git detect` | PASS | Current live repo: `trunk_without_dev`, branch `main`, role `canonical`, dirty tree true, `dev` missing. |
| `py -3 .aide/scripts/aide_lite.py git doctor` | PASS | Non-mutating; reports `main` canonical, dirty tree true, safe_for_normal_task false. |
| `py -3 .aide/scripts/aide_lite.py git status` | PASS | Non-mutating; next safe action is to classify dirty tree. |
| `py -3 .aide/scripts/aide_lite.py git policy` | PASS | Q28 and Q29 policy anchors pass; no mutation command default is exposed. |
| `py -3 .aide/scripts/aide_lite.py git plan` | PASS_BLOCKED | Writes latest helper plan; blocked by dirty tree and missing `dev`, as expected for live `main`. |
| `py -3 .aide/scripts/aide_lite.py git sync --dry-run` | PASS_BLOCKED | Dry-run only; planned `git status --short` and `git pull --ff-only`; blocked for apply by dirty tree. |
| `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev` | PASS_BLOCKED | Dry-run only; blocked because source role is canonical/protected, tree is dirty, and `dev` is missing. |
| `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main` | PASS_BLOCKED | Dry-run only; blocked because `dev` is missing and tree is dirty. |
| `py -3 .aide/scripts/aide_lite.py git prune --dry-run` | PASS | Dry-run only; current/protected `main` is not eligible. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_q29_git_helper.py` | PASS | 14 fixture helper tests passed in temporary repos. |
| `py -3 -m unittest discover -s .aide/scripts/tests -p test_q28_git_workflow.py` | PASS | 8 workflow tests passed after Q29 command-surface update. |
| `py -3 -m unittest discover -s .aide/scripts/tests` | PASS | 155 tests passed with a 10-minute timeout. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | PASS | Latest completed Q29 doc commit passes structured commit policy. |
| `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~4..HEAD` | PASS | Four completed Q29 commits pass; final export/evidence commit checked after creation. |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | WARN | 20 commits parsed; 3 malformed pre-Q27 commits reported; preview generated; no publishing. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 183 included files; 186 checksums; boundary PASS; no provider/model/network calls. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid; provenance `DIRTY_SOURCE_RECORDED`; boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q30 AIDE Dev Main Policy Sync"` | PASS | Latest task packet generated, 3,670 chars, 918 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 918 approximate tokens, within 3,200-token task-packet budget. |
| Targeted `rg` secret scan | PASS_AFTER_INSPECTION | Matches were policy/test/template/path terms such as `TOKEN`, `api_key`, `SECRET_PATTERNS`, `sk-ant` regex text, and `latest-task-packet`; no actual provider key, `.env`, private key, `.aide.local` state, raw prompt, or raw response was found. |

## Live Branch Mutation Check

- No live `--apply` helper command was run in the AIDE repository.
- No live branch was created, merged, deleted, pushed, pruned, tagged, or fetched.
- All mutating helper paths were exercised only inside temporary fixture Git repositories created by unit tests.
