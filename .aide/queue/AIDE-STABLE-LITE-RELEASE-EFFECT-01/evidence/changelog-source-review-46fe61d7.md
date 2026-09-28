# Changelog source selection rereview: 46fe61d7

- Reviewed commit: `46fe61d743f077b4ff28bc58721d4fa1d85ddcc4`
- Reviewed tree: `c4d2989fa42eaa6d89913acd98af78ee222fc938`
- Parent: `87635e1815b7f24b18fef43b56f2a186aeb24103`
- Reviewer: `/root/stable_builder_repair_review` (independent read-only agent)
- Verdict: `ACCEPT` for the source and regression repair.
- Finding closed: `--range` now controls both selected commits and `source_head` when `--to` is also present; `A..` resolves its open end to HEAD. The new fixture covers these cases.
- Reviewer checks: read-only source, test and evidence inspection plus `git diff --check`; no tests or generators run by reviewer.
- Limitation: advanced Git revision-set syntax outside documented simple ranges may fail binding. Pack, assets, consumers and release effects require separate qualification and review.
