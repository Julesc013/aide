# Commands Run

All commands ran from `c:\Inbox\Git Repos\aide` unless another cwd is listed.

## Git and Local State

| Command | Exit | Result |
|---|---:|---|
| `git status --short` | 0 | clean before QCHECK; dirty after audit artifacts/status outputs |
| `git branch --show-current` | 0 | `main` |
| `git branch --all` | 0 | local `main`, `remotes/origin/main` |
| `git remote -v` | 0 | origin `https://github.com/Julesc013/aide.git` |
| `git rev-parse HEAD` | 0 | `abebc24278c5de304a02a680f93ec30bc1429e04` |
| `git rev-parse --show-toplevel` | 0 | `C:/Inbox/Git Repos/aide` |
| `git log --oneline --decorate -80` | 0 | inspected Q36-Q48 history |
| `git tag --list` | 0 | no tags |
| `git check-ignore .aide.local/` | 0 | `.aide.local/` ignored |
| `git diff --check` | 0 | PASS |

## Harness and Core AIDE Lite

| Command | Exit | Result |
|---|---:|---|
| `py -3 scripts/aide validate` | 0 | PASS_WITH_WARNINGS; generated manifest freshness warning |
| `py -3 scripts/aide doctor` | 0 | PASS_WITH_WARNINGS; generated manifest freshness warning |
| `py -3 scripts/aide self-check` | 0 | PASS_WITH_WARNINGS; review-gate/generated warning |
| `py -3 .aide/scripts/aide_lite.py doctor` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py selftest` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py eval run` | 0 | PASS, 132/132 golden tasks |
| `py -3 .aide/scripts/aide_lite.py verify` | 0 | WARN during dirty audit worktree; review packet later regenerated under budget |
| `py -3 .aide/scripts/aide_lite.py review-pack` | 0 | PASS, review packet 1636 tokens |
| `py -3 .aide/scripts/aide_lite.py ledger scan` | 0 | PASS, budget warnings for large eval reports only |
| `py -3 .aide/scripts/aide_lite.py ledger report` | 0 | PASS |

## Intent, Repo, Quality

| Command | Exit | Result |
|---|---:|---|
| `py -3 .aide/scripts/aide_lite.py intent compile --prompt "Plan Q49 Dominium Fresh Install Preflight from QCHECK-04 audit evidence"` | 0 | PASS; safe_to_execute false, split required |
| `py -3 .aide/scripts/aide_lite.py intent validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py intent status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repo inventory` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repo validate` | 0 | WARN; unknown classifications advisory |
| `py -3 .aide/scripts/aide_lite.py repo status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py quality ledger` | 0 | PASS; advisory warnings |
| `py -3 .aide/scripts/aide_lite.py quality validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py quality status` | 0 | PASS |

## Refactor, Roots, Tools, Maps

| Command | Exit | Result |
|---|---:|---|
| `py -3 .aide/scripts/aide_lite.py refactor status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py refactor validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py refactor dry-run` | 0 | PASS, no apply |
| `py -3 .aide/scripts/aide_lite.py roots inventory` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py roots validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py roots status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py tools inventory` | 0 | PASS, execution disabled |
| `py -3 .aide/scripts/aide_lite.py tools validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py tools status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py refactor map-status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py refactor validate-map` | 0 | PASS |

## Install Lifecycle

| Command | Exit | Result |
|---|---:|---|
| `py -3 .aide/scripts/aide_lite.py install observe` | 0 | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py install plan` | 0 | PASS, no_apply true |
| `py -3 .aide/scripts/aide_lite.py install dry-run` | 0 | PASS, target_mutation false |
| `py -3 .aide/scripts/aide_lite.py install validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py install status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repair observe` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repair diagnose` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repair plan` | 0 | PASS, no apply |
| `py -3 .aide/scripts/aide_lite.py repair dry-run` | 0 | PASS, target_mutation false |
| `py -3 .aide/scripts/aide_lite.py repair validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py repair status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade observe-current` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade observe-source` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade compare` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade plan` | 0 | PASS, no apply |
| `py -3 .aide/scripts/aide_lite.py upgrade dry-run` | 0 | PASS, target_mutation false |
| `py -3 .aide/scripts/aide_lite.py upgrade validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py upgrade status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py rollback observe` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py rollback plan` | 0 | PASS, no apply |
| `py -3 .aide/scripts/aide_lite.py rollback dry-run` | 0 | PASS, target_mutation false |
| `py -3 .aide/scripts/aide_lite.py rollback validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py rollback status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py uninstall observe` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py uninstall plan` | 0 | PASS, no blanket delete |
| `py -3 .aide/scripts/aide_lite.py uninstall dry-run` | 0 | PASS, target_mutation false |
| `py -3 .aide/scripts/aide_lite.py uninstall validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py uninstall status` | 0 | PASS |

## Governance, Git, Changelog, GitHub Advisory

| Command | Exit | Result |
|---|---:|---|
| `py -3 .aide/scripts/aide_lite.py commit check --latest` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~20..HEAD` | 1 | FAIL on two older malformed commits; latest passes |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | 0 | PASS; malformed historical commits recorded |
| `py -3 .aide/scripts/aide_lite.py changelog validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py changelog status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py task inspect` | 1 | Expected missing active Q49 task before generation |
| `py -3 .aide/scripts/aide_lite.py task status` | 0 | PASS; Q36-Q48 needs_review |
| `py -3 .aide/scripts/aide_lite.py task noop-check` | 1 | Expected missing Q49 task surfaces |
| `py -3 .aide/scripts/aide_lite.py git detect` | 0 | PASS; trunk_without_dev |
| `py -3 .aide/scripts/aide_lite.py git doctor` | 0 | PASS with dirty-audit warning |
| `py -3 .aide/scripts/aide_lite.py git status` | 0 | PASS with dirty-audit warning |
| `py -3 .aide/scripts/aide_lite.py git policy` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py git plan` | 0 | PASS/no mutation |
| `py -3 .aide/scripts/aide_lite.py git sync --dry-run` | 0 | PASS/no mutation |
| `py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev` | 0 | PASS/no mutation; dev absent remains advisory |
| `py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main` | 0 | PASS/no mutation |
| `py -3 .aide/scripts/aide_lite.py github validate` | 0 | PASS/report-only |
| `py -3 .aide/scripts/aide_lite.py github advisory` | 0 | PASS/report-only |
| `py -3 .aide/scripts/aide_lite.py github status` | 0 | PASS/report-only |
| `py -3 .aide/scripts/aide_lite.py github protection` | 0 | PASS/report-only; no settings mutation |
| `py -3 .aide/scripts/aide_lite.py github ci` | 0 | PASS/report-only; no workflow install |

## Export, Release, Draft

| Command | Exit | Result |
|---|---:|---|
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | 0 | PASS; 629 included files |
| `py -3 .aide/scripts/aide_lite.py pack-status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release assets` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release manifest` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release checksums` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release provenance` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release clean --dry-run` | 0 | PASS; deleted 0 |
| `py -3 .aide/scripts/aide_lite.py release draft-validate` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release draft-status` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release upload-plan` | 0 | PASS/no upload |
| `py -3 .aide/scripts/aide_lite.py release checklist` | 0 | PASS |
| `py -3 .aide/scripts/aide_lite.py release publication-boundary` | 0 | PASS/no publish |

## Tests

| Command | Exit | Result |
|---|---:|---|
| canonical `.aide/scripts/tests` command: `py -3 .aide/scripts/aide_lite.py test` | 0 | PASS |
| `py -3 -m unittest discover -s .aide/scripts/tests` | timeout | Timed out after 604s; canonical test runner passes |
| `py -3 -m unittest discover -s core/harness/tests -t .` | 0 | PASS, 27 tests |
| `py -3 -m unittest discover -s core/compat/tests -t .` | 0 | PASS, 5 tests |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | 0 | PASS, 9 tests |
| `py -3 -m unittest discover -s core/providers/tests -t .` | 0 | PASS, 8 tests |

## Optional Target Repo Read-Only Inspection

| Target | Path | Result |
|---|---|---|
| Dominium | `C:\Inbox\Git Repos\dominium` | found; branch `main`; `.aide` and AIDE Lite present; `.aide.local/` ignored; no Q49 queue yet |
| Eureka | `C:\Inbox\Git Repos\eureka` | found; branch `dev`; `.aide` and AIDE Lite present; `.aide.local/` ignored; no Q54 queue yet |

No target repo mutation occurred.
