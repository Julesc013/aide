# Multi-Commit Policy

Long turns may create multiple commits only when the active WorkUnit or prompt
explicitly allows a multi-step chain and each commit is coherent.

## Commit Boundaries

Use separate commits when changes differ by purpose:

- queue scaffold or status records
- docs and protocol text
- code or behavior
- tests or validation fixtures
- generated artifacts
- evidence and review records

Do not create a mixed commit that hides runtime behavior inside docs or evidence
work.

## Per-Commit Requirements

Before each commit:

- review `git status --short`
- stage only related files
- run proportionate validation for the changed surface
- record validation in task-local evidence
- preserve unrelated user changes

After each commit:

- run `py -3 .aide/scripts/aide_lite.py commit check --latest` when practical
- record any warning or failure
- stop if commit policy fails in a way that is not local to the task

## Branch-Sensitive Work

If branch creation, merge, promotion, push, prune, tag, or publication becomes
necessary, stop and record a review gate unless the current WorkUnit explicitly
authorizes that exact action.
