# Path Safety Review

Path safety is implemented in `core/protocol/workunit_cli.py`.

Checks added or preserved:

- task ids must match the safe queue id pattern.
- create specs must be repo-local files.
- evidence paths must resolve under the repository root.
- evidence paths reject `.git`, `.aide-local`, `.aide.local`, `.env*`, `secret`, `secrets`, and `credentials` path markers.
- `safe_new_task_dir` rejects duplicate tasks and unsafe ids before apply.
- apply writes are scoped to `.aide/queue/<task-id>/` and optional `.aide/queue/index.yaml`.

Focused tests cover duplicate/unsafe ids, external evidence paths, secret-like evidence paths, dry-run no-mutation behavior, and temp-root apply behavior.
