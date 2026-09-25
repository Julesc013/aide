# Changed files, 2026-09-25

- `.aide/scripts/aide_lite.py`: replace three obsolete Q48 draft claims with
  an accurate boundary between Q43-Q46 report-only planners and separate
  bounded Windows exact-plan apply candidates. Keep local draft, no-tag,
  no-upload and no-publish behavior unchanged.
- `.aide/scripts/tests/test_q48_github_release_draft.py`: reject the old
  planning-only phrases and assert the preview/qualification boundary.
- `docs/reference/aide-lite-release-bundle.md`: align the install notes
  explanation with current source and the eventual release-manifest gate.
- This WorkUnit, queue index, `PLANS.md` and `IMPLEMENT.md`: bind admission,
  test evidence, review and later artifact projection.

No `.aide/export/**` or `.aide/release/**` generated output was edited in
this source task; the next current-generator projection owns those bytes.
