# Q31 Fixture Import Report

## Test Command

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q31_export_pack_governance.py`: PASS, 6 tests.

## Fixture Coverage

The Q31 fixture tests create temporary local target repositories and use the
committed pack in safe mode. They do not push, fetch, call GitHub, call
providers/models, or mutate any real target repo.

Covered behavior:

- Safe fixture import receives commit-message policy, hook template, commit
  template, task recovery policies, and generic Git workflow policies.
- Hook template is imported under `.aide/hooks/commit-msg`.
- `.git/hooks/commit-msg` is not installed automatically.
- AIDE-specific generated branch detection files, latest helper plans, AIDE
  branch policy, AIDE dev/main plans, generated context, queue history,
  reports, `.aide.local/`, and `.env` are not imported as target truth.
- Imported fixture can run:
  - `commit template`
  - `commit check --message-file COMMIT_MSG` with a valid structured message
  - `commit check --message-file BAD_COMMIT_MSG` and receive the expected failure
  - `task inspect --task-id FIXTURE-TASK`
  - `git policy`
  - `git detect`
  - `git plan`

## Result

Fixture import behavior is suitable for Q32/Q33 target sync preparation. It is
not proof that Eureka or Dominium have already been refreshed; those repos must
be synced and validated in their own phases.
