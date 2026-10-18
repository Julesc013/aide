### Research and adopted direction ? 18 October 2026

**Finding.** No source establishes a universally optimal length or seven-section
format. Use stable meaning, concise rationale and proportionate detail.

- [Git commit](https://git-scm.com/docs/git-commit): short first line, blank
  separator, fuller explanation. The 50-character suggestion is guidance.
- [Git contribution guidance](https://git-scm.com/docs/SubmittingPatches):
  focused changes and motivation; enough explanation to understand later.
  Its rewrite-heavy mailing-list workflow is not adopted over AIDE history policy.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):
  type/description, optional scope, free-form body, footers and breaking markers.
  It mandates no Markdown sections; semantic release remains a separate decision.
- [Google descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html):
  what and why, useful context, stand-alone first line; links supplement rationale.
- [GitHub review guidance](https://docs.github.com/en/pull-requests/concepts/helping-others-review-your-changes):
  focused PRs, explain problem/approach/result and reviewer focus.
- [Google review comments](https://google.github.io/eng-practices/review/reviewer/comments.html):
  explain reasoning and distinguish required changes from optional suggestions.
- [GitHub Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax):
  bold, italics, inline code and lists; underline uses ins HTML. Keep plain-text
  Git readable and avoid reliance on HTML outside known rendering surfaces.
- [Git trailers](https://git-scm.com/docs/git-interpret-trailers):
  machine fields at the end, separately from prose.
- [GitHub squash configuration](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-squashing-for-pull-requests):
  default squash text depends on configuration and commit count. Review the final
  message rather than concatenate noisy interim history.

**AIDE choices, not external mandates.** Lead with outcome/reason; scale detail to
risk. Plain text for commits, bold labels/bullets for PRs/comments; H3/H4 only
when navigation helps. Target roughly 50-72 subject characters, 72-100 body
columns where practical, never wrap identifiers/URLs. No word quota or maximum
that hides material facts. Common small commits need one paragraph and validation;
larger changes add rationale, compatibility/migration and recovery where material.
Retain exact refs and linked evidence; avoid dumping logs, path inventories,
chat chronology and repeated None fields. Project templates remain overridable.
