# Reviewed ULK PR18 correction integration plan

Current user explicitly authorizes implementation, validation, synchronization, commits and normal merges through full Beta1. This reviewed correction resolves the provider current-truth obligation.

Primary dev is clean at 0e8bcc38f5a55c80974c41da8d2eac10ac703593. The existing task branch is behind its unchanged remote head 484c6832a6c0ac1a4306d85987ee2b5a7c11bd90. The marker-owned review worktree is at that exact head and contains only the seven reviewed truth/checker/test files. Native hygiene passed with one secondary worktree.

Preserve the review worktree and avoid creating another. Temporarily switch the clean primary to its existing task branch, fast-forward it to the exact reviewed remote head, apply the captured checked patch, revalidate, commit and non-force push that task branch. Return the clean primary to dev after the push. No protected source ref, history, worktree ownership record or existing evidence is rewritten.

Independent review: provider_review verified historical and current trees/ancestry, no runtime/header/ABI/package/authority drift, six focused tests and diff-check. Implementation validation: 46 Python tests and all 15 strict checks passed. Patch SHA256: 1478511b1dd9055cff1891d64449b2ec28a654a682137e30bad8ca8789739dd6.

Refresh PR18 with exact new source and let required hosted checks bind that head before normal merge. No tag, publication or consumer adoption is implied.
