# Changelog source selection review: 7a521066

- Reviewed commit: `7a521066fdd4bf1346434d60c84090b0a63f77b2`
- Reviewed tree: `1288ad1bded2581e2f11ce21d2d153a16ca96987`
- Reviewer: `/root/stable_builder_repair_review` (independent read-only agent)
- Verdict: `REQUEST_CHANGES`
- Scope: `source_head` selection and the new Git-fixture regression. No pack or release asset acceptance.
- Finding: `--range A..B --to C` reads `A..B` but records `C`; `--range A..` records an empty source head. Both can invalidate or falsely bind release provenance.
- Reviewer validation: source and test diff inspected; `git diff --check` passed. No files edited by reviewer.
- Disposition: repair selector precedence and open-end handling, test both cases, request narrow rereview of superseding source.
