# Q30 Remaining Risks

- Local and remote `dev` are absent. Q30 records a future explicit operator plan
  but does not create or push the branch.
- `main` is ahead of `origin/main`; Q30 does not push.
- Branch protection is not applied. GitHub protection and CI advisory/application
  remain future phases.
- Q30 does not perform live `dev -> main` promotion.
- Q30 helper dry-runs block while generated artifacts are dirty; this is expected
  during implementation and should be clean/classified before future branch
  mutation.
- Harness validate/doctor/self-check still report historical review-gate warnings
  and generated manifest source-fingerprint drift. These are pre-existing review
  and generated-artifact issues, not Q30 branch-policy blockers.
- AIDE Lite validate reports near-budget warnings for older ledger/cache evidence
  surfaces. These are classified token-budget warnings, not Q30 failures.
- Export pack provenance records `DIRTY_SOURCE_RECORDED` because Q30 exported
  while generated artifacts were pending commit. Checksums and boundary checks
  pass.
- Q31 is needed to sync portable Git/commit workflow support without exporting
  AIDE-specific live branch detection state.
- No provider/model/network calls, GitHub mutation, branch creation, branch
  deletion, branch merge, branch push, tag creation, or release publishing was
  introduced.
