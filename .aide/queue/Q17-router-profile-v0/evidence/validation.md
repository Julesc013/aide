# Q17 Validation

## Baseline Validation Before Editing

- `git status --short`: PASS, clean before baseline command refreshes.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info / 7 warnings / 0 errors.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS.
- `py -3 .aide/scripts/aide_lite.py index`: PASS.
- `py -3 .aide/scripts/aide_lite.py context`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: PASS.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL with known hidden `.aide` start-directory importability behavior.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.

## Final Validation

Interpreter used: Windows `py -3` with Python bytecode disabled through
`PYTHONDONTWRITEBYTECODE=1` for Python commands where applicable.

- `git status --short`: PASS before Q17 edits, clean. Final pre-commit status
  showed only Q17-scoped modifications plus generated Q17 route artifacts.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS, 148 info / 7 warnings /
  0 errors. Warnings are the known review-gate nuance for older queue items and
  generated manifest source-fingerprint drift.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS, 148 info / 7 warnings /
  0 errors, same known warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS, report-only, no
  external calls, provider/model calls, network calls, automatic worker
  invocation, or queue auto-merge.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS, 5 tests.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS. Q17 routing artifacts,
  route decision artifacts, token ledger, golden-task report, controller
  report, and compact packets were present.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS. Route decision shape,
  routing artifacts, token-survival files, context artifacts, verifier,
  review, ledger, eval, controller, adapter status, and secret scan all passed.
- `py -3 .aide/scripts/aide_lite.py snapshot`: PASS, wrote
  `.aide/context/repo-snapshot.json`, 719 files, no raw contents.
- `py -3 .aide/scripts/aide_lite.py index`: PASS, wrote repo-map and
  context-index outputs; 719 files and 648 heuristic test mappings.
- `py -3 .aide/scripts/aide_lite.py context`: PASS, wrote
  `.aide/context/latest-context-packet.md`, 1922 chars / 481 approximate
  tokens / within budget.
- `py -3 .aide/scripts/aide_lite.py verify`: PASS, checked 49 files and 41
  changed files, 161 info, 0 warnings, 0 errors.
- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, wrote
  `.aide/context/latest-review-packet.md`, 7093 chars / 1774 approximate
  tokens / budget PASS / verifier PASS after final evidence refresh.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, wrote
  `.aide/reports/token-ledger.jsonl` and `.aide/reports/token-savings-summary.md`,
  65 records, with no regression warnings. The final long validation evidence
  file later produced one near-budget evidence warning, recorded below.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, 65 records. The
  final ledger report has 1 near-budget warning for this validation evidence
  file and 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py eval list`: PASS, 6 golden tasks listed.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 6 pass / 0 warn /
  0 fail, no provider/model/network calls. The rewritten eval run artifacts
  were restored afterward because `.aide/evals/runs/**` is outside Q17's
  committed output scope.
- `py -3 .aide/scripts/aide_lite.py eval report`: PASS, latest golden-task
  report remained PASS.
- `py -3 .aide/scripts/aide_lite.py outcome report`: PASS, 7 outcome records,
  0 warnings, 0 failures, advisory-only.
- `py -3 .aide/scripts/aide_lite.py optimize suggest`: PASS, top
  recommendation `REC-PROCEED-Q18-WITH-GATES`, advisory-only, no provider/model
  or network calls.
- `py -3 .aide/scripts/aide_lite.py route list`: PASS, listed 7 route classes,
  task profiles, and hard floors; no provider/model/network calls.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS, all routing policy,
  model registry, schema, and latest route artifacts were present and shaped
  correctly.
- `py -3 .aide/scripts/aide_lite.py route explain`: PASS, route class
  `frontier`, task class `architecture_decision`, hard floor
  `architecture_decision`, quality gates PASS, advisory-only, no provider/model
  or network calls.
- `py -3 .aide/scripts/aide_lite.py route explain --task-packet .aide/context/latest-task-packet.md`:
  PASS, same Q18 route decision.
- `py -3 .aide/scripts/aide_lite.py pack --task "Implement Q18 Cache and Local State Boundary"`:
  PASS, `.aide/context/latest-task-packet.md`, 3486 chars / 872 approximate
  tokens / budget PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`:
  PASS, 3486 chars, 108 lines, 872 approximate tokens, within budget.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS, internal estimate,
  ignore, snapshot, index, context, pack, adapt, drift, line-ref, verifier,
  review-pack, ledger, eval, outcome, optimize, route, and validate checks.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 66 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`: FAIL with known
  Python unittest importability behavior for hidden `.aide` start directories:
  `ImportError: Start directory is not importable`.
- `git diff --check`: PASS. Git emitted line-ending conversion notices only.
- Targeted `rg` secret scan: PASS after inspection. Matches were policy/test
  terms, section names, fake test fixtures, and path names such as `api_key`,
  `SECRET`, `TOKEN`, `TOKEN_ESTIMATE`, and `sk-ant` regex text; no real
  provider key, credential, `.env` content, `.aide.local` state, raw prompt log,
  or secret value was found.

## Post-Evidence Refresh

After this evidence file was populated, the deterministic generated surfaces
were refreshed again so the committed review packet and token ledger include
the final Q17 evidence:

- `py -3 .aide/scripts/aide_lite.py review-pack`: PASS, latest review packet
  within budget and verifier PASS.
- `py -3 .aide/scripts/aide_lite.py ledger scan`: PASS, 1 near-budget warning
  for `.aide/queue/Q17-router-profile-v0/evidence/validation.md`, 0 regression
  warnings.
- `py -3 .aide/scripts/aide_lite.py ledger report`: PASS, same near-budget
  validation-evidence warning, 0 regression warnings.
- `py -3 .aide/scripts/aide_lite.py route explain --task-packet .aide/context/latest-task-packet.md`:
  PASS, unchanged Q18 route decision.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 66 tests.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py route validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-review-packet.md`:
  PASS, review packet within budget.

## Known Warnings

- Harness v0 still reports generated manifest source-fingerprint drift.
- Harness v0 still reports older raw queue review-gate nuance for Q00-Q03,
  Q05, and Q06.
- AIDE Lite final validation reports one near-budget token ledger warning for
  this deliberately detailed validation evidence file. Q17 prompt packets,
  context packets, review packets, route artifacts, and generated reports remain
  within budget.
- The hidden-directory unittest command with `-t .` remains a known Python
  discovery limitation; direct discovery without `-t .` passes.
