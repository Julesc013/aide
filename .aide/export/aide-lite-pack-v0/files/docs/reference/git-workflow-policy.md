# Git Workflow Policy

Q28 defines AIDE's local Git workflow policy before any branch mutation helpers
exist.

## Default Model

AIDE uses a trunk-based / GitHub Flow hybrid with an optional permanent `dev`
integration branch:

- `main` is canonical accepted truth.
- `dev` is shareable integration truth and must not be treated as canonical
  release truth.
- `task/*`, `codex/*`, `aide/*`, `fix/*`, and `repair/*` branches are bounded
  work by default.
- `release/*` and `hotfix/*` are explicit maintenance or emergency paths.
- `gh-pages` is a generated deploy branch when a repository actually uses it.

## Commands

```powershell
py -3 .aide/scripts/aide_lite.py git detect
py -3 .aide/scripts/aide_lite.py git doctor
py -3 .aide/scripts/aide_lite.py git status
py -3 .aide/scripts/aide_lite.py git workflow
py -3 .aide/scripts/aide_lite.py git roles
py -3 .aide/scripts/aide_lite.py git policy
```

`git detect` writes `.aide/git/workflow-detection.json` and
`.aide/git/workflow-detection.md`. It reads local branch, remote-branch, tag,
status, and remote-url metadata. It does not fetch, create branches, merge,
delete, prune, push, call GitHub, call providers, or use the network.

## Policies

- `.aide/policies/git-workflow.yaml`
- `.aide/policies/branch-roles.yaml`
- `.aide/policies/promotion-rules.yaml`
- `.aide/policies/sync-policy.yaml`
- `.aide/policies/prune-policy.yaml`
- `.aide/git/project-profiles.yaml`

Project profiles cover AIDE, Eureka, Dominium, website/static-site repositories,
native-client repos, connector-heavy repos, data-snapshot repos, and unknown
repos. Unknown repos stay conservative until inspected.

## Q28 Boundary

Q28 is policy and detection only. Q29 is responsible for safe merge, land,
promote, and prune helper plans and must keep live AIDE branch mutation out of
helper implementation tests.
