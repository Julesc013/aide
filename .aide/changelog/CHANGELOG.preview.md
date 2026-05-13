# AIDE Changelog Preview

source_range: HEAD~5..HEAD
commit_count: 5
release_publishing: false

## Added

- canonical AIDE commit discipline and WorkUnit recovery policy. (86974c90938c policy(aide): define structured commits and WorkUnit recovery)
- AIDE Lite commit, changelog, and task recovery command surfaces. (2146efa0db8f feat(aide-lite): add commit and task recovery commands)

## Docs

- documented Q27 commit, changelog, and WorkUnit recovery workflows. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)

## Tests

- deterministic Q27 coverage for commit lint, changelog preview, and WorkUnit no-op recovery. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)

## Internal

- reopened Q27 governance packet for implementation from the repaired baseline. (57b73ba81a94 chore(aide): add Q27 commit and recovery governance packet)
- optional local commit-msg hook template and commit template. (86974c90938c policy(aide): define structured commits and WorkUnit recovery)
- Q27 validation anchors and golden-task runners. (2146efa0db8f feat(aide-lite): add commit and task recovery commands)
- golden-task reports now include Q27 quality gates. (f97d7736d0c0 test(aide): cover commit lint and WorkUnit recovery)
- command catalog now lists Q27 AIDE Lite command families. (0de5071ded87 docs(aide): document commit discipline and recovery workflows)

## Malformed Commits

- None.
