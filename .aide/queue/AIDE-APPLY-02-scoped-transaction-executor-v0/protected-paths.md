# AIDE-APPLY-02 Protected Paths

Protected paths for this task and future `AIDE-APPLY-02` implementation:

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`
- `.env.*`
- `secrets/**`
- `credentials/**`
- target repositories
- release publication files
- `.aide/release/dist/**`
- `.aide/release/github-release-*`
- `.aide/release/latest-github-release-draft.*`
- unrelated `docs/canon/**`
- unrelated `contracts/**`
- unrelated `schema/**`
- unrelated implementation roots
- generated authority documents not owned by this task
- raw corpus/archive files
- provider/model/Gateway integration files unless explicitly authorized
- branch/worktree automation files unless explicitly authorized

Any attempted mutation of a protected path must block implementation and be recorded as a review-gated issue.
