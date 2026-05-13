# Risks

- Q35 missing state was resolved by `.aide/queue/Q35-github-protection-ci-advisory-v0`.
- Local `main` is 39 commits ahead of `origin/main`; no push/fetch/sync was
  performed because branch/remote mutation and outbound network actions are out
  of scope.
- No AIDE `dev` branch exists. Q30 policy says `dev` is intended integration,
  but creation remains future explicit operator work.
- Export pack is valid, but pack provenance records `DIRTY_SOURCE_RECORDED`
  because export occurred during report generation.
- Automatic installer/upgrade/repair/rollback/uninstall flows do not exist yet.
- Eureka Q32 and Dominium Q33 remain target-side `needs_review`.
- Dominium Q33 evidence includes warning-bearing validation for optional
  generated status/report surfaces.
- Historical malformed commits remain reported for release review; history was
  not rewritten.
- AIDE has governance readiness, not product/runtime readiness.
- Target tool absorption is planned, not implemented.
- Exact tokenizer and provider billing evidence remain absent.
- No GitHub branch protection, CI workflow, release, or tag was applied.
