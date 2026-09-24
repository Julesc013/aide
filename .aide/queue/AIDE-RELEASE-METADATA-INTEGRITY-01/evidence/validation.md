# Release integrity integration validation

- Fresh exact source review of `853d1c7a`/tree `b5f69ce1` returned ACCEPT for
  dev integration only; 60 adjacent cases passed without skip or failure.
- The reviewed source was retained as an ancestor of release evidence commit
  `f77ecba287415ebefb24db97b8543d6256963e45`.
- Remote `dev` first observed `f77ecba2`, then combined target and artifact
  candidate `9cc4bb06883754de24096547c6b356524bd71b93`, tree
  `8afadda53f79e7e7094460ff472862b68bac214c`.
- At the first dev landing, canonical validate, doctor, release validate, and
  draft-validate passed. At the combined dev landing, 199 adjacent cases had
  198 passes and one Windows symlink privilege skip. The current generator
  replay changed zero of 44 release files, and pack-status, canonical
  validate, doctor, and exact asset hashes passed.
- This is local metadata/source acceptance, not whole-product or public-release
  acceptance. Detailed combined evidence is in the target integration and
  artifact refresh tasks.
