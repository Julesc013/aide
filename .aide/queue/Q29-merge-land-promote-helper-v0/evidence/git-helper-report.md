# Git Helper Report

Status: blocked before implementation.

Q29 was expected to add:

- `.aide/git/helper-policy.yaml`;
- `.aide/git/helper-commands.md`;
- `.aide/git/latest-helper-plan.json`;
- `.aide/git/latest-helper-plan.md`;
- AIDE Lite `git sync`, `git plan`, `git land`, `git promote`, and
  `git prune` commands.

No helper policy or command surfaces were implemented because Q27 and Q28 are
materially incomplete.

## Required Future Behavior

When Q29 is reopened, helpers must:

- default to dry-run/report-only on the live AIDE repo;
- require explicit `--apply` for local mutation;
- require explicit future `--push` intent for remote mutation;
- block dirty, unknown, protected, or unvalidated states;
- prove ancestor containment before pruning;
- test mutating paths only in temporary fixture repositories.
