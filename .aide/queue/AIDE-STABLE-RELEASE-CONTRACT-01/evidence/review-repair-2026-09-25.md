# Stable Lite contract review repair, 2026-09-25

## Reviewed subject and retained finding

- Source candidate `aa3bcfec849edf9f6de7b2dd74ce2e7a549698e1`, tree
  `ea39b2a694491c40ef0ba2ef5ebdb7216e5851d3`, received independent
  `REQUEST_CHANGES` from `/root/customization_review`; external report:
  `D:/Projects/AIDE/_review_scratch/stable-release-contract-aa3bcfec-independent-review.md`,
  SHA-256 `45900dbb33e278f3681f72895afbdbbc13dfb038f4913cca3f3966f760b5dec6`.
- The three findings were a false committed-candidate machine-pass claim,
  missing predecessor/conflict CLI forms in the proposed public boundary,
  and ambiguous release verdict strictness. No `aa3bcfec` technical acceptance
  or dev effect is inferred.
- Merge commit `060de47208b3b04f4eddde4cfd6fe13687b45189`, tree
  `ab67fb3040c60b5c8116623581458fc1febc794d`, incorporated accepted
  `dev@a32535a2675f191ae3515f39501658e91ef41103` and its delivered
  `--from-pack`/`--resolve` implementation. `PLANS.md` and `IMPLEMENT.md`
  were the only conflicts and both histories were retained.

## Repair and measured state

- The proposed CLI contract now names required `--pack`, `--target`,
  `--from-pack`, `--resolve`, and `--expect-plan` operands for install, update,
  explicit conflict resolution, rollback, repair and removal forms. Current
  parser help confirms `import-pack --resolve TARGET FILE` and required
  predecessor pack. The final manifest still must qualify each form on
  delivered bytes; parser help is syntax evidence only.
- The first stable release requires an independent technical `ACCEPT` even
  though the general campaign review gate can accept fully disposed
  `ACCEPT_WITH_NOTES` for other exact subjects.
- On merge commit `060de472`, `pack-status`, `validate`, and `doctor` exited 1
  due retained export manifest provenance. Exact logs and hashes are in
  `contract-source-candidate.md`; those failures remain open until a separate
  projection WorkUnit regenerates outputs and checks the committed candidate.
- Focused Q47 tests: 18/18 PASS, exit 0, 36.010 s, external log
  `D:/Projects/AIDE/_review_scratch/stable-contract-superseding-q47.log`,
  SHA-256 `7fa0e5128d0274c1ff1f4362dec56080d84c58038d876f726e1c4625d24d7596`.
- Focused Q48 tests: 11/11 PASS, exit 0, 16.405 s. `git diff --check` and
  task inspect remain required after the source commit. These tests do not
  qualify the final release or clear the export provenance failure.

## Boundary

This source WorkUnit leaves `.aide/export/**` and `.aide/release/**` untouched.
An independently reviewed superseding source candidate must be followed by a
separately scoped projection/integration WorkUnit. No main, tag, upload or
publication action is authorized by this evidence alone.
