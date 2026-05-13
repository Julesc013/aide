# Promotion Policy

Q28 records promotion policy so Q29 can implement safe helper plans without
inventing branch semantics.

## Task To Dev

`task/*` branches land to `dev` only after:

- the worktree is clean or explicitly understood;
- task evidence exists;
- local validation passes or warnings are classified;
- structured commit checks pass;
- the target integration branch is synchronized before merge.

Q28 does not run the merge. Q29 must make this a dry-run-first helper and must
test mutation only in temporary fixture repositories.

## Dev To Main

`dev` promotes to `main` only after:

- a dev review packet exists;
- full validation passes or warnings are classified;
- changelog preview is generated;
- generated artifacts are reviewed;
- required queue blockers are resolved or classified;
- explicit promotion evidence exists.

`main` remains canonical. `dev` is integration truth and cannot become a second
release source of truth.

## Sync And Prune

Sync policy favors explicit fetch/fast-forward decisions and forbids implicit
merge or rebase of shared branches. Q28 detection itself does not fetch.

Pruning requires ancestor containment proof before any deletion:

```text
git merge-base --is-ancestor <branch> <target>
```

Protected roles such as canonical, integration, release, and deploy are never
eligible for routine prune. Q28 contains no branch-deletion command.

## Future Work

Q29 adds safe branch helper plans. GitHub branch protection and CI enforcement
are later advisory/application phases, not Q28 behavior.
