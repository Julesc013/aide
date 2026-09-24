# Target-Policy Source Publication

- Branch: `task/aide-cw-github-target-qualification-01`
- Commit: `bb433bb74f645e0904ca34bf3af38516ae05a7ad`
- Tree: `a871c65880161f147f35cf8df7269bba9af3a867`
- Remote: `origin`
- Remote observation: `git ls-remote --heads origin
  task/aide-cw-github-target-qualification-01` returned the exact commit.
- Commit-message check: PASS.
- Source result: PASS_WITH_WARNINGS; 96 affected tests passed.
- Post-commit canonical validation: WARN; only the existing export-pack source
  provenance remains at `b3e5c7aa2a1732faee4a9021e64bdba65c6db1cb`.

Publication preserves the review subject. It does not authorize or perform a
workflow installation, ruleset/settings mutation, credential change, hosted
race, branch promotion, tag, or release. The restricted broker principal and
workflow/check identities remain unresolved, so the live operation list remains
empty and blocked.

The task branch is not a delivered pack. Rebuilding and qualifying portable
artifacts belongs after reviewed integration, so this receipt records the
provenance drift instead of mutating unrelated export/release paths.
