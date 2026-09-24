# Exact GitHub target source review — 2026-09-24

Decision: **ACCEPT_WITH_NOTES for source integration only**.

Subject: `e378d38e0c51b964ff0886823b5ad6ba62c82f14`, tree `c871264626f29b6de593b8d700df5005f44a6148`, historical merge base `c6fdc754844cf7d42302218ce08307a7e05dcb61`, current `dev` `cc85be9c472a16f39aae98ba00fd5de145098862`. This review was run from disposable checkout `D:\Projects\AIDE\_review_scratch\target-e378d38e-newthread`. The candidate branch was not edited.

## Prior findings

- Endpoint shape and applicability: closed for the local comparator. `github_target_policy.py` now expects individual rules carrying type, source type, source and ruleset ID, derives expected rules only from observed rulesets applicable to `refs/heads/dev`, and excludes the non-dev confinement ruleset. The shape matches GitHub's documented Get rules for a branch response: https://docs.github.com/en/rest/repos/rules.
- Malformed, duplicate, missing, extra, wrong-source, wrong-ruleset, excluded-ruleset, and parameter drift inputs refuse or block before operations in the focused tests. The documented `path@ref` workflow repair source was unchanged by this final commit and its affected suites passed.
- Test accounting corrected: five suites executed 139 cases, 138 passed, one Windows privilege-dependent symlink case skipped, zero failed.

## Verification

- GitHub observation/policy 50, PR observation 21, GitHub HTTP 19, provider bridge 12, integration broker 37: all suites exit 0. Logs `review-target-*.log` are in the disposable checkout.
- `commit check --latest` and `git diff --check c6fdc754..HEAD`: passed. All 29 changed paths fit the task allowlist; the checkout stayed clean.
- The stored live review plan is blocked by unresolved broker-principal and workflow/check identities, has zero operations, and marks `apply_authorized: false`.
- `doctor` and `validate` exit 1 solely for the two reported export-pack provenance checks: tracked pack source `b3e5c7aa` differs from this unintegrated branch head. The combined source requires a fresh, separately validated pack before delivered-byte claims.

## Limits

No target settings or workflow installation, restricted credential qualification, hosted race, native protected-host effect, main promotion, or publication was performed. The old Sagan terminal output was not present in repository evidence and was not read from private Codex session storage. Acceptance permits a current-base source integration candidate, not activation of hosted behavior.
