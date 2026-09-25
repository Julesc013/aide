# Observed one-writer dev effect, 2026-09-25

- Fresh preflight under `BLACKGLASS-WIN1\Jules` and authenticated GitHub
  account `Julesc013` confirmed local/tracking/ls-remote/API
  `dev@d292253b09944f28f0fc794fe3a9679966fe56a0`, candidate
  `6e8af2bd8d16d8952ce627182339904eac4972fc`, tree
  `a964b2e245c935a8127bc7325879f2c9db160dc8`, ancestry, one `dev`
  worktree, clean primary/candidate, absent checked index/ref locks and Git
  operation markers, and exact archive digests. External
  `dev-effect-preflight.txt` SHA-256
  `2dcb6248e110efdcdac039191896918a815163b3e059062d791c09500305e820`.
- Controller `git merge --ff-only 6e8af2bd...` exited 0 and local `dev`
  read back exact candidate/tree. Controller normal `git push origin dev`
  exited 0. No force push, main, tag, publication, hosted or native effect.
- Subsequent local `dev`, `origin/dev`, `git ls-remote`, and GitHub ref API
  all read back full `6e8af2bd8d16d8952ce627182339904eac4972fc`, tree
  `a964b2e245c935a8127bc7325879f2c9db160dc8`; primary and candidate
  worktrees were clean. Reflogs showed local fast-forward and tracking-ref
  update by push. External `observed-dev-effect.txt` SHA-256
  `46eb2d61f53832621273278318131efa454802a8041df3f2f4fa0ad4532400ca`.
- This task evidence closeout is a later branch commit and has not itself
  changed the reviewed source/archive bytes. Any later dev effect requires
  a fresh exact candidate, range and review.
