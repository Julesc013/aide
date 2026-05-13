# Q26 Validation

Validation will be updated after final commands are run.

## Baseline Before Q26 Edits

- `scripts/aide validate`: PASS_WITH_WARNINGS; only review-gate warnings and
  generated manifest drift.
- `scripts/aide compile --write`: PASS; refreshed `.aide/generated/manifest.yaml`.
- `scripts/aide validate`: PASS_WITH_WARNINGS; generated manifest drift removed.
- `scripts/aide doctor`: PASS_WITH_WARNINGS; generated manifest drift removed.
- `scripts/aide self-check`: PASS_WITH_WARNINGS; generated manifest current.

## Read-Only Eureka Checks

- Eureka `git status --short`: PASS, clean.
- Eureka branch: `dev`.
- Eureka head: `ab2603c021aec6541ba10e5544fdc8cfef1010e8`.
- Eureka `.aide.local/` ignore check: PASS.
- Eureka AIDE Lite `doctor`: PASS.
- Eureka AIDE Lite `validate`: PASS with target review-packet warnings.
- Eureka task-packet estimate: PASS, 1,027 approximate tokens.
- Eureka `git diff --check`: PASS.
- Eureka architecture boundary check: PASS.
- Eureka strict secret scan: PASS, no matches.

## Final Q26 Validation

Final command results used
`C:\Program Files\Hybrid\64bit\Vapoursynth\python.exe` (Python 3.12.9)
unless noted.

- `git status --short`: PASS_WITH_CHANGES; changes are Q26 packet/evidence,
  state-truth docs, Q27-Q29 supersession records, generated packet/review/eval
  artifacts, generated manifest, and Harness guidance.
- `git diff --check`: PASS; Git reported line-ending normalization warnings
  only.
- `git check-ignore .aide.local/`: PASS, `.aide.local/`.
- `scripts/aide compile --write`: PASS; generated manifest refreshed and
  managed sections remained current.
- `scripts/aide validate`: PASS_WITH_WARNINGS; 149 info, 6 warning, 0 error.
  The warnings are existing review gates for Q00-Q03, Q05, and Q06.
- `scripts/aide doctor`: PASS_WITH_WARNINGS; same warning class; generated
  manifest source fingerprint is current.
- `scripts/aide self-check`: PASS_WITH_WARNINGS; same review-gate warnings;
  queue health reports Q25 and Q26 at `needs_review` and Q27-Q29 as
  `superseded`.
- `.aide/scripts/aide_lite.py validate`: PASS with non-failing historical
  token-ledger near-budget warnings for existing Q17/Q18/cache records.
- `.aide/scripts/aide_lite.py test`: PASS.
- `.aide/scripts/aide_lite.py selftest`: PASS.
- `.aide/scripts/aide_lite.py eval run`: PASS, 6/6 golden tasks.
- `.aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary
  PASS, zero checksum problems, zero boundary violations.
- `.aide/scripts/aide_lite.py pack --task "Q27 Commit Discipline WorkUnit
  Recovery v0"`: PASS; latest task packet written, 3,696 chars, 924
  approximate tokens, budget PASS.
- `.aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`:
  PASS; 924 approximate tokens, within budget.
- `.aide/scripts/aide_lite.py review-pack --task-packet
  .aide/context/latest-task-packet.md --evidence-dir
  .aide/queue/Q26-eureka-pilot-review-and-handover/evidence`: PASS; latest
  review packet written, 8,261 chars, 2,066 approximate tokens, budget PASS.
- `.aide/scripts/aide_lite.py verify --task-packet
  .aide/context/latest-task-packet.md`: WARN, 0 errors. The warnings are
  expected diff-scope warnings because the latest task packet now targets the
  next Q27 redo while the current diff is the completed Q26 handover.
- `.aide/scripts/tests` unittest discovery: PASS, 117 tests.
- `core/harness/tests` unittest discovery: PASS, 27 tests.
- `core/compat/tests` unittest discovery: PASS, 5 tests.
- `core/gateway/tests` unittest discovery: PASS, 9 tests.
- `core/providers/tests` unittest discovery: PASS, 8 tests.
- Targeted secret scan with `rg`: PASS_AFTER_INSPECTION. Matches were policy,
  test, template, and path terms such as `TOKEN`, `api_key`, and
  `latest-task-packet`; no real credential, `.env` content, `.aide.local`
  state, raw prompt log, or raw response log was found.
