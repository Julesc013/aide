# Observed evidence-only dev effect, 2026-09-25

## Frozen subject and review

- Target before effect: `dev@b3a001befaac2d2d9a596c1d7dc738dd1733bec6`,
  tree `dfc557ae1acddd347f0ca866500865ad603d1b8a`.
- Frozen candidate: `a7254d7d4c9cdaeb9c71b7f2974e0d382ea9b27a`, tree
  `f5d019ed9ca74d0b2f8597499b970044d8b18dd0`.
- External exact effect manifest SHA-256
  `85ebcb0b78d1664b579ed4abc714e896641171af0e451ed7a2d7d23f5f9d2c38`.
- Independent Codex reviewer `/root/historical_date_review` issued
  `ACCEPT_WITH_NOTES`, conditional GO only for local fast-forward and normal
  `dev` push. External report SHA-256
  `91090b281872bc0669f0f515c1defa09ac8cbf483a08fcd949f14297944db7c2`.
  No main/tag/publication GO was given.

## Fresh preflight and actual effect

Fresh preflight JSON outside the repository SHA-256
`be4a3f84b199b87f2374bbdcf9fda90ae80b77d2ac1ed21a50608379a10862c6`
has parsed `preflight_pass: true`. It observed
`BLACKGLASS-WIN1\Jules`, `Julesc013`, clean primary/candidate worktrees,
exact candidate/tree/ancestry/review/manifest/ZIP/tar identities, no checked
Git lock or pending operation, and equal local/tracking/remote/API `dev` refs
at the exact base. No competing AIDE integration writer was observed.

`git merge --ff-only a7254d7d4c9cdaeb9c71b7f2974e0d382ea9b27a` in
the primary `dev` checkout exited 0. Merge log SHA-256
`df2550507a10ee120d5fe84b89e578a7dea7b02aeaceb3590f68bfc819ebd58d`.
Normal `git push origin dev` exited 0; push log SHA-256
`07d29fee24406e4cc0524a151088682ce0befe9df9314f99bd17ea192d9afd13`.
No force, protection bypass, reset or branch deletion was used.

Post-effect JSON outside the repository SHA-256
`97251820bb2309f1543694d5b035c498be8aacb280f6c51969b04d7908173425`
has `effect_pass: true`. It observed local `dev`, `origin/dev`,
`git ls-remote origin refs/heads/dev`, and the GitHub ref API all at the full
candidate `a7254d7d4c9cdaeb9c71b7f2974e0d382ea9b27a`; the tree was
`f5d019ed9ca74d0b2f8597499b970044d8b18dd0`. Primary and integration
worktrees were clean. Preview ZIP and tar hashes remained respectively
`8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`
and `11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c`.

## Retained obligations

This integrated the evidence record only. The installed target Task OS
empty-queue report-truth defect is not repaired. The local preview, synthetic
rollback successor, first harness timeout, OS-level offline trace, real
published version pairs, final qualification, main/tag/publication and
downloaded-byte consumer checks remain separate. This closeout evidence
itself needs independent review before a later `dev` update.
