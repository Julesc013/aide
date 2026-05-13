# Remaining Risks

- Q32 and Q33 are target-repository sync prompts and were not run from the AIDE
  repository during QFIX-03; they require starting in the Eureka and Dominium
  repositories.
- Q35 GitHub Protection and CI Advisory is the next AIDE-local advisory
  phase; QFIX-03 did not implement GitHub branch protection, CI workflows, tags,
  release publishing, or GitHub Releases.
- Historical malformed or legacy commits are still reported for release review in
  `.aide/changelog/malformed-commits.md`; this is no longer a command warning and
  QFIX-03 does not rewrite Git history.
- Local `dev` branch creation remains a separately gated operator action; QFIX-03
  does not create, push, merge, prune, or delete branches.
- Passing review-gated queue items with notes does not imply product readiness,
  live provider/model calls, target-repo mutation, or release readiness.
