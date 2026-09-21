# ExecPlan: Codex Neutrality Dev Integration

## Objective

Produce and integrate a narrow `dev` candidate containing the exact reviewed
repository Codex neutrality state and its provenance, independent of mixed
broker and host implementation history.

## Scope

- Reproduce the eight `.codex` path outcomes from `0e76df9e` exactly.
- Carry the completed original checkpoint packet from `91efe815`.
- Record candidate validation and the superseding main-promotion identity.
- Integrate only this bounded candidate into `dev`.

## Non-Goals

- No user, profile, managed, system, or active-session setting changes.
- No broader permission, sandbox, approval, search, or network policy changes.
- No broker, host, provider, target, release, or specification work.
- No `main` promotion, tag, or release.

## Progress

- [x] Refresh published refs and inspect configuration on relevant branches.
- [x] Locate the reviewed source and closeout commits.
- [x] Create a clean task branch from exact `dev@be3a854a`.
- [x] Reproduce the exact reviewed `.codex` state and checkpoint evidence.
- [x] Validate active pins, TOML, repository structure, and candidate scope.
- [ ] Commit and publish the task branch.
- [ ] Fast-forward `dev` through the authorized integration workflow.
- [ ] Record the superseding exact main-promotion candidate and gate.

## Validation

Compare Git blob identities with `0e76df9e`, require `.codex/config.toml` to be
absent, scan active TOML assignments, parse every remaining role file, run
`codex --strict-config --version`, queue validation, full repository validation,
commit checks, and exact `main..dev` closure after integration.

## Recovery

Before publication, discard only this clean worktree if validation fails. After
publication, fix forward on this task branch. Never restore the old pins or use
the mixed broker branch as the integration vehicle.

## Discoveries And Decisions

- `dev@be3a854a` retained `.codex/config.toml` and execution pins in every role
  file even though the completed campaign state referred to the neutrality task.
- The seven retained `.codex` files now match the reviewed source blobs exactly;
  `.codex/config.toml` is absent.
- The candidate carries the original completed checkpoint packet plus this
  branch-specific integration packet. It contains no runtime or machine state.
