# Artifact Refresh Baseline

- Published dev: `cc85be9c472a16f39aae98ba00fd5de145098862`.
- Integration commit: `bb689227c6a65292f4728d7ae0f8759c22e77bd3`.
- Reviewed portability candidate: `6cb0a9ac8856a4e733b1d48ef2a86d50badb5d22`.
- Refresh branch: `task/aide-distribution-portability-pack-refresh-01`.
- Initial worktree state: clean.
- Canonical validation before refresh: expected failure limited to the tracked
  export manifest naming source `b3e5c7aa2a1732faee4a9021e64bdba65c6db1cb`
  instead of current dev.

This checkpoint authorizes local deterministic export, bundle, and preview
draft regeneration only. It does not authorize a tag, upload, GitHub Release,
main promotion, hosted effect, or non-disposable target mutation.
