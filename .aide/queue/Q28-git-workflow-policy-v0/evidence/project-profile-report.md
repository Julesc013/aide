# Project Profile Report

Status: superseded pre-repair blocker record.

Q28 was expected to add `.aide/git/project-profiles.yaml` with profiles for:

- AIDE;
- Eureka;
- Dominium;
- website/static-site repos;
- native client repos;
- connector-heavy repos;
- data snapshot repos;
- unknown repos.

No project profiles were implemented because Q27 is materially incomplete.

## Read-Only Eureka Reference

A sibling Eureka repo was inspected read-only. It contains target-local commit
and task-resumption policies plus AGENTS guidance referencing structured commit
checks. No Eureka files were modified.

## Future Profile Notes

When Q28 is reopened:

- AIDE should default to strict trunk plus optional `dev` integration.
- Eureka should use `main` as canonical and `dev` as integration/quarantine for
  reviewed waves.
- Dominium may justify release branches for shipped builds/content/save
  compatibility.
- Website repos should usually use simple GitHub Flow, with `gh-pages` only
  when deployment mode requires it.
