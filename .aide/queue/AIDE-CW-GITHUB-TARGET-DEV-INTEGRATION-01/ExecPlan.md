# ExecPlan: GitHub target source dev integration

## Objective and scope

Merge the fresh-reviewed target source into accepted release-integrity `dev`
while preserving both histories. This WorkUnit covers source, tests, and
coordination records. A separate artifact refresh must clear the expected
post-integration pack provenance before final canonical acceptance.

## Dependencies and exact identities

- Current `dev`: `f77ecba287415ebefb24db97b8543d6256963e45`.
- Target source reviewed: `e378d38e0c51b964ff0886823b5ad6ba62c82f14`,
  tree `c871264626f29b6de593b8d700df5005f44a6148`.
- Target evidence descendant: `d81d953a767492c4f71bfe9a2334944d51cf5201`.
- Merge base: `c6fdc754844cf7d42302218ce08307a7e05dcb61`.
- Fresh review: `ACCEPT_WITH_NOTES` for local source integration only.
- The release repair has already fast-forwarded to remote `dev` with canonical
  validate, doctor, release validate, and draft validate passing.

## Progress

- [x] Resolve the suspected backend and ensure no competing AIDE writer.
- [x] Preserve and publish both fresh-review evidence commits.
- [x] Integrate accepted release source into `dev` first.
- [x] Compile the current intent; the generic classifier marked Git/release
  wording blocked, so this exact owner direction and bounded WorkUnit define
  the authorized local source slice.
- [x] Merge the target evidence descendant into this isolated branch.
- [x] Reconcile `IMPLEMENT.md`, queue index, and planning history without
  downgrading the repaired release generator or artifacts.
- [x] Run 199 combined source cases: 198 passed, one Windows privilege skip.
- [x] Run post-commit canonical checks; record the inherited pack-source
  mismatch as the only validation failure in the child refresh baseline.
- [ ] Commit with a prevalidated message and publish the exact candidate.
- [ ] Land the qualified source on `dev`; then refresh derived artifacts through
  a separate bounded WorkUnit.

## Conflict and recovery policy

The merge preflight found one textual conflict in `IMPLEMENT.md`; the queue
index and `PLANS.md` auto-merge. Preserve both parents' factual log entries.
Keep the current dev release generator and derived artifacts. Until the merge
commit exists, `git merge --abort` returns this task branch to its admission
checkpoint without changing either parent.

## Verification intent and blockers

Run the five target suites and the release/export suites on the combined tree,
then canonical validation. Preserve the Windows privilege skip as a skip.
The target review identified stale export-pack source provenance inherited from
its older base; record that failure precisely and clear it in the bounded
post-integration artifact refresh. Hosted configuration and race testing remain
outside this source integration.
