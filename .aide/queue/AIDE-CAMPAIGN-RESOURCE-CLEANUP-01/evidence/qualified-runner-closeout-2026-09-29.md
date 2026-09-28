# Bounded resource owner closeout

Scope: AIDE-CAMPAIGN-RESOURCE-CLEANUP-01 only. This closes the owned cleanup
and bounded local execution slice; the parent delivery and release remain
active.

## Source and placement

- Reviewed selected-root setup source
  `5152798b934a498d9ec6e20986263412a0d7c068` is an ancestor of local
  `dev@0cacf2040ce84ddca8722986e24e7d52d5b9020d`. Its independent
  verdict was ACCEPT_WITH_NOTES; the recorded 35-case D-managed suite passed.
- Both existing checkouts use byte-identical ignored
  `.aide.local/execution.json`, SHA-256
  `019669f8faab4ea4e410079ea96966b16742f0e7c6d2e062246a092f1b862834`.
  The approved shared scratch, retained and control roots are beneath
  `D:\Projects\AIDE\.aide.local\execution`. The config reserves 10 GiB free
  disk, 4 GiB physical and commit headroom; each job has finite scratch,
  retained, canonical, memory, log, runtime, process and entry limits.
- Git lists two worktrees: the primary checkout and the retained partial
  import recovery checkout. The prior 34 owned worktree retirements and
  preserved refs are bound in `resource-checkpoint.md` and its receipts.

## Actual AIDE jobs

The current-source D-managed export `b4c1fc11fffc47ec95094db57ae2e303`
passed, receipt SHA-256
`b8afc15316b593f46829a22ea69e2715e530610558268790760004e1b0f01317`.
Observed peak job memory was 200,409,088 bytes and scratch 432 bytes. The
stable-build job `f430fd62b4694bc48c9e3f8921d046db` passed, receipt
SHA-256 `f7d579240a1e51999eb7ceab6dd5bc7fa8448a9aa5e826b54385dc6344300728`;
peak memory was 201,199,616 bytes and scratch 263 bytes. The current release
test job `c367d2f802474fbc913f584c4ed685c7` passed 36 cases, receipt
SHA-256 `3828fb837f5be6b8fcdcf91e32573cb0a627823547e5a2afd6f4330f8719c57d`;
peak memory was 274,059,264 bytes and scratch 6,310,054 bytes. Each receipt
records quiescent exit 0, phase `retired`, scratch absent and reservation
released. Pack and stable generation also passed current-source validation
and zero-change postcommit replay in the release WorkUnit.

## Verification and limits

This closeout used read-only `git merge-base --is-ancestor`, two config
SHA-256 reads, three exact retained receipt reads, `git worktree list`,
free-space and memory observations, and an approved-scratch enumeration.
No new test or model request ran for this evidence edit. D: free space was
70,140,592,128 bytes at observation; scratch had zero children. The old
pre-cleanup D observation was 21,531,815,936 bytes. Concurrent disk activity
prevents attributing the net difference to AIDE cleanup. Application
reservations and monitored thresholds are not filesystem quotas; future
large jobs still require their own admission and retirement checks. Required
failure evidence and the second useful checkout remain preserved.
