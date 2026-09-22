# Validation

- Local and remote source and target refs match the exact requested commits.
- Ancestry checks confirm neither parent contains the other.
- Source unique runtime history and net path groups were inventoried.
- `git merge-tree --write-tree dev 75da3310...` identified fourteen conflicts
  and no conflict under `core/runtime/**` or broker-focused test paths.
- Product and runtime tests have not yet been run against the combined tree.

