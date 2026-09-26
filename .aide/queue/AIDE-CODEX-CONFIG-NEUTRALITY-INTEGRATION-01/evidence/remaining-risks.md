# Remaining Risks And Gates

- Invocation, user, profile, managed, system, or built-in configuration may
  still affect an individual Codex session.
- Removing repository pins preserves operator choice; it does not widen or
  guarantee permissions exposed by a particular client or managed policy.
- The previous `main -> be3a854a` review subject is superseded after this
  integration and cannot authorize a later `dev` commit.
- `main` promotion remains an explicit human review gate.
- The exact `main..dev` commit check fails on historical published commit
  `bfb86c12`; a reviewed disposition is required without rewriting shared
  history before the candidate can become promotion-ready.
- The branch-only decision-packet commit `fbca5038` also failed the current
  message-format checker. It is not part of `dev` or the main candidate and is
  retained with a fix-forward disposition rather than rewritten.
