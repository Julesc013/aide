# Commands Run

All commands were run from `C:/Inbox/Git Repos/aide` unless another cwd is
listed. Large outputs are summarized.

| Command | Cwd | Exit | Result | Summary |
|---|---|---:|---|---|
| `git status --short` | AIDE | 0 | PASS | Initial worktree clean. Later generated reports became dirty as allowed audit outputs. |
| `git branch --show-current` | AIDE | 0 | PASS | `main`. |
| `git branch --all` | AIDE | 0 | PASS | `main`, `origin/main`; no `dev`. |
| `git remote -v` | AIDE | 0 | PASS | `origin` configured; no network call made. |
| `git rev-parse HEAD` | AIDE | 0 | PASS | `6246811cf02ece09bd25b53ce0625919db658f51`. |
| `git log --oneline --decorate -50` | AIDE | 0 | PASS | Shows Q27-Q34/QFIX-03 commit sequence. |
| `git tag --list` | AIDE | 0 | PASS | No tags. |
| `git check-ignore .aide.local/` | AIDE | 0 | PASS | `.aide.local/` ignored. |
| `git diff --check` | AIDE | 0 | PASS | No whitespace errors. |
| `py -3 scripts/aide validate` | AIDE | 0 | PASS | 149 info, 0 warnings, 0 errors. |
| `py -3 scripts/aide doctor` | AIDE | 0 | PASS | 149 info, 0 warnings, 0 errors; next step Q36. |
| `py -3 scripts/aide self-check` | AIDE | 0 | PASS | Queue health passed; Q36 next; no network/model calls. |
| `py -3 .aide/scripts/aide_lite.py doctor` | AIDE | 0 | PASS | Required AIDE Lite artifacts present. |
| `py -3 .aide/scripts/aide_lite.py validate` | AIDE | 0 | PASS | No FAIL/WARN checks in summarized output. |
| `py -3 .aide/scripts/aide_lite.py test` | AIDE | 0 | PASS | Internal AIDE Lite command checks passed. |
| `py -3 .aide/scripts/aide_lite.py selftest` | AIDE | 0 | PASS | Internal selftest passed. |
| `py -3 .aide/scripts/aide_lite.py eval run` | AIDE | 0 | PASS | 34/34 golden tasks, warn_count 0, fail_count 0. |
| `py -3 .aide/scripts/aide_lite.py verify` | AIDE | 0 | PASS | 89 files, 0 changed files at that moment, 0 warnings, 0 errors. |
| `py -3 .aide/scripts/aide_lite.py review-pack` | AIDE | 0 | PASS | Wrote latest review packet; 1,539 approximate tokens; verifier PASS. |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | AIDE | 0 | PASS | 83 records, budget_warnings 0, budget_watchlist 3. |
| `py -3 .aide/scripts/aide_lite.py ledger report` | AIDE | 0 | PASS | 83 records; budget_warnings 0; regression_warnings 0. |
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | AIDE | 0 | PASS | Latest commit follows Q27 discipline. |
| `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~10..HEAD` | AIDE | 0 | PASS | 10/10 recent commits pass. |
| `py -3 .aide/scripts/aide_lite.py commit template` | AIDE | 0 | PASS | Template printed. |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | AIDE | 0 | PASS | 50 commits, 7 malformed legacy commits reported for review. |
| `py -3 .aide/scripts/aide_lite.py changelog validate` | AIDE | 0 | PASS | Preview outputs and JSON shape valid. |
| `py -3 .aide/scripts/aide_lite.py changelog status` | AIDE | 0 | PASS | Preview-only; release_publishing false. |
| `py -3 .aide/scripts/aide_lite.py task inspect` | AIDE | 0 | PASS | Default task is now Q36; classification `planned`; mutation none. |
| `py -3 .aide/scripts/aide_lite.py task status` | AIDE | 0 | PASS | 39 tasks; Q35 passed and Q36 planned. |
| `py -3 .aide/scripts/aide_lite.py task noop-check` | AIDE | 0 | PASS | Q36 returns `inspect_before_editing`; mutation none. |
| `py -3 .aide/scripts/aide_lite.py git detect` | AIDE | 0 | PASS | trunk_without_dev; current branch `main`; non-mutating. |
| `py -3 .aide/scripts/aide_lite.py git doctor` | AIDE | 0 | PASS_WITH_EXPECTED_WARNING | Dirty tree warning because audit generated reports were present. |
| `py -3 .aide/scripts/aide_lite.py git status` | AIDE | 0 | PASS_WITH_EXPECTED_WARNING | Canonical branch, dirty tree due audit artifacts. |
| `py -3 .aide/scripts/aide_lite.py git policy` | AIDE | 0 | PASS | Git workflow/helper/AIDE branch policies valid. |
| `py -3 .aide/scripts/aide_lite.py git plan` | AIDE | 0 | EXPECTED_BLOCK | Blocked by dirty tree; non-mutating; wrote helper plan. |
| `py -3 .aide/scripts/aide_lite.py git sync --dry-run` | AIDE | 0 | EXPECTED_BLOCK | Dirty tree blocks apply; planned command only. |
| `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev` | AIDE | 0 | EXPECTED_BLOCK | Canonical source role, dirty tree, and missing `dev` block landing. |
| `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main` | AIDE | 0 | EXPECTED_BLOCK | Missing `dev` and dirty tree block promotion. |
| `py -3 .aide/scripts/aide_lite.py git prune --dry-run` | AIDE | 0 | PASS_WITH_EXPECTED_WARNING | Dry-run only; protected/current branch not eligible. |
| `py -3 .aide/scripts/aide_lite.py github advisory` | AIDE | 0 | PASS | Report-only advisory generated; no GitHub API mutation, workflow writes, branch mutation, network, provider, or model calls. |
| `py -3 .aide/scripts/aide_lite.py github status` | AIDE | 0 | PASS | Report-only status; no mutation or network calls. |
| `py -3 .aide/scripts/aide_lite.py github protection` | AIDE | 0 | PASS | Branch-protection plan generated; advisory only. |
| `py -3 .aide/scripts/aide_lite.py github ci` | AIDE | 0 | PASS | CI advisory generated; no `.github/workflows` writes. |
| `py -3 .aide/scripts/aide_lite.py github validate` | AIDE | 0 | PASS | Q35 policies and generated advisory reports validate. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | AIDE | 0 | PASS | 220 files, 223 checksums, boundary PASS, no network/model calls. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | AIDE | 0 | PASS | Checksums valid, provenance DIRTY_SOURCE_RECORDED, boundary PASS. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q36 Intent Compiler and Prompt Normalization v0"` | AIDE | 0 | PASS | Wrote Q36 task packet, 927 approximate tokens. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | AIDE | 0 | PASS | 3,706 chars / 927 approximate tokens / within budget. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | AIDE | 0 | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | AIDE | 0 | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | AIDE | 0 | PASS | 9 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | AIDE | 0 | PASS | 8 tests. |
| Broad targeted `rg` secret scan | AIDE | 0 | PASS_AFTER_INSPECTION | Matches are policy/test/path terms; no actual secret found. |
| Strict key-shaped `rg` secret scan | AIDE | 0 | PASS_AFTER_INSPECTION | Matches are test assertions and prior evidence text forbidding secrets; no actual secret value found. |
| `py -3 scripts/aide validate` after QCHECK reports | AIDE | 0 | PASS_WITH_WARNINGS_THEN_FIXED | Initially reported one generated-manifest stale warning caused by the new queue index entry. |
| `py -3 scripts/aide compile --write` | AIDE | 0 | PASS | Refreshed `.aide/generated/manifest.yaml`; managed sections and preview outputs were unchanged. |
| `py -3 scripts/aide validate` after compile | AIDE | 0 | PASS | 149 info, 0 warnings, 0 errors. |
| `git status --short; git branch --show-current; git rev-parse HEAD` | Eureka | 0 | READ_ONLY | Clean output; branch `dev`; HEAD `4207f7863562c73f21c0a1414e4632237beaa167`. |
| Target file/queue inspection | Eureka | 0 | READ_ONLY | `.aide` present; `EUREKA-AIDE-SYNC-01` present. |
| `git status --short; git branch --show-current; git rev-parse HEAD` | Dominium | 0 | READ_ONLY | Clean output; branch `main`; HEAD `752918d4f281aad12cdb6e892d39460172155e34`. |
| Target file/tool inspection | Dominium | 0 | READ_ONLY | `.aide` present; `DOMINIUM-AIDE-SYNC-01` present; XStack/AuditX/RepoX/TestX-style systems discovered. |

Notes:

- Q35 is implemented. The `github` command family is report-only and passes.
- Git helper dirty-tree warnings are expected before this reconciliation commit
  because allowed report-generation commands modified AIDE-local generated
  reports; final post-commit Git helper checks should be clean except for
  missing `dev`, which remains a documented future operator action.
- No command was run with branch helper `--apply` or `--push`.
- Generated-manifest staleness after queue index registration was fixed with
  `scripts/aide compile --write`.
