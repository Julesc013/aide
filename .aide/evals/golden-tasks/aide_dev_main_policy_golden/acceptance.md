# AIDE Dev Main Policy Golden Acceptance

This deterministic no-call task passes when:

- `.aide/git/aide-branch-policy.yaml` exists.
- `main` is canonical.
- `dev` is integration.
- `dev` is explicitly not canonical truth.
- Q30 no-live-mutation policy is present.
- Promotion gates include validate, eval, commit range, pack-status, secret scan, and review packet checks.
