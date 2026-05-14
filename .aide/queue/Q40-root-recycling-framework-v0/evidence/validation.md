# Validation

## Baseline And Final Checks

| Command | Result | Notes |
| --- | --- | --- |
| `git status --short` | PASS | Inspected before and after validation; final dirty set limited to Q40 roots, export pack, Q41 task packet, AIDE Lite boundary fix, and Q40 evidence before final commit. |
| `git branch --show-current` | PASS | `main`. |
| `git diff --check` | PASS_WITH_WARNINGS | No whitespace errors; Git reported line-ending normalization warnings in exported pack copies. |
| `git check-ignore .aide.local/` | PASS | `.aide.local/` ignored. |
| `py -3 scripts/aide validate` | PASS_WITH_WARNINGS | Existing generated manifest source fingerprint warning remains. |
| `py -3 scripts/aide doctor` | PASS_WITH_WARNINGS | Existing generated manifest source fingerprint warning remains. |
| `py -3 scripts/aide self-check` | PASS_WITH_WARNINGS | Q36-Q40 are implemented and review-gated; Q40 remains `needs_review`. |
| `py -3 .aide/scripts/aide_lite.py doctor` | PASS | Required AIDE Lite surfaces present. |
| `py -3 .aide/scripts/aide_lite.py validate` | PASS | Q40 root policy/schema/output checks included. |
| `py -3 .aide/scripts/aide_lite.py test` | PASS | Initially exposed a Q40 integration bug where Q39 validation required Q40 root outputs in fixtures; fixed by keeping Q39 generated outputs scoped to Q39. |
| `py -3 .aide/scripts/aide_lite.py selftest` | PASS | Same internal coverage as `test`. |
| `py -3 .aide/scripts/aide_lite.py eval run` | PASS | 71/71 golden tasks passed. Generated eval run reports restored after validation. |
| `py -3 .aide/scripts/aide_lite.py repo inventory` | PASS | 1,751 tracked records, 150 unknown classifications, 491 orphan candidates. Generated Q37 outputs restored after validation. |
| `py -3 .aide/scripts/aide_lite.py repo validate` | WARN | Structural pass with warning for 150 unknown file classifications. |
| `py -3 .aide/scripts/aide_lite.py quality ledger` | PASS | 1,751 ledger records; 0 fail, 51 pass, 355 exempt, 1,345 warn. Generated Q38 reports restored after validation. |
| `py -3 .aide/scripts/aide_lite.py quality validate` | PASS | Existing Q38 policy/schema/ledger shape valid. |
| `py -3 .aide/scripts/aide_lite.py refactor validate` | PASS | Existing Q39 no-apply refactor validation passes; Q39 no longer depends on Q40 root outputs. |
| `py -3 .aide/scripts/aide_lite.py roots inventory` | PASS | 22 roots, 1,781 files, no-apply true after final rebase refresh. |
| `py -3 .aide/scripts/aide_lite.py roots classify` | PASS | 22 roots, 1,781 files, 1,725 review-required file classifications, no-apply true after final rebase refresh. |
| `py -3 .aide/scripts/aide_lite.py roots plan` | PASS | Wrote no-apply root recycling plan for Q41 follow-up. |
| `py -3 .aide/scripts/aide_lite.py roots validate` | PASS | Policies, schemas, generated outputs, no-apply, no-delete, and exception checks pass. |
| `py -3 .aide/scripts/aide_lite.py roots status` | PASS | 22 roots, 3 mixed roots, 22 unknown-owner root candidates, 15 high-risk roots, fate counts `keep=1401`, `unknown=380`. |
| `py -3 .aide/scripts/aide_lite.py roots explain-root .aide` | PASS | `.aide` root reported mixed/high risk with no-apply true. |
| `py -3 .aide/scripts/aide_lite.py roots explain-file .aide/scripts/aide_lite.py` | PASS | File fate `keep`, semantic risk high, review required, `apply_allowed=false`. |
| `py -3 .aide/scripts/aide_lite.py intent validate` | PASS | Existing Q36 no-call intent compiler validation passes. |
| `py -3 .aide/scripts/aide_lite.py changelog preview` | PASS_WITH_REVIEW_NOTES | Preview generated; 3 malformed historical commits reported for review. Preview outputs restored after validation. |
| `py -3 .aide/scripts/aide_lite.py git policy` | PASS | Dry-run/report-only Git policy checks pass. |
| `py -3 .aide/scripts/aide_lite.py github validate` | PASS | Advisory-only GitHub/CI checks pass; no GitHub mutation. |
| `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` | PASS | 365 included files, 368 checksums, boundary pass after rebase onto `origin/main`. |
| `py -3 .aide/scripts/aide_lite.py pack-status` | PASS | Checksums valid, boundary pass, provenance `DIRTY_SOURCE_RECORDED` during in-progress commit. |
| `py -3 .aide/scripts/aide_lite.py pack --task "Q41 Existing Tool Absorption v0"` | PASS | `.aide/context/latest-task-packet.md`, 4,104 chars, 1,026 approx tokens, budget pass. |
| `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md` | PASS | 1,026 approx tokens, within budget. |
| `py -3 -m py_compile .aide/scripts/aide_lite.py` | PASS | AIDE Lite compiles. |
| `py -3 -m unittest discover -s core/harness/tests -t .` | PASS | 27 tests. |
| `py -3 -m unittest discover -s core/compat/tests -t .` | PASS | 5 tests. |
| `py -3 -m unittest discover -s core/providers/tests -t .` | PASS | 8 tests. |
| `py -3 -m unittest discover -s core/gateway/tests -t .` | PASS_AFTER_RERUN | First parallel run timed out after 424 seconds; rerun alone passed 9 tests in about 530 seconds. |
| Targeted `rg` secret scan | PASS_AFTER_INSPECTION | Matches were policy names, test fixtures, regex definitions, placeholder terms, path names, and generated references. No actual provider key, credential, `.env` content, `.aide.local` state, raw prompt log, or raw response log was found. |

## Scope Notes

- No provider, model, network, GitHub API, branch mutation, target repo
  mutation, file move, file delete, reference rewrite, or refactor apply command
  was introduced or run.
- Validation-generated `.aide/repo/**`, Q38 report, changelog preview, and eval
  run churn was restored because those outputs are outside Q40 write scope.
