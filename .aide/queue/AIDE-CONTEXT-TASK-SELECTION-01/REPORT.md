# Selected-task context qualification

The existing context compiler now follows the same recorded selection as
`task current`, replacing its historical Q17 fallback. It shows selection source,
recorded status and unresolved/conflicting observations. Completed and blocked tasks
stay selected. Existing packet sections, CLI syntax and token estimates remain.
Selection is not active-worker identity, an atomic snapshot, verified acceptance
or permission to execute. A stale packet can still select old work.

| Allocation | Result | Evidence |
|---|---|---|
| 1, b93da708 | PASS: source 61, no failures/errors/skips | evidence/source-attempt-01.json |
| 2, 425afc83 | FAIL after successful ownership 6/export/doctor/validate/pack status; delivered tests did not start | evidence/pack-attempt-02.json |
| 3, 90ca096b | PASS: delivered 60, then exact three-commit preview | evidence/finish-attempt-03.json |

All three jobs are retired and quiescent. Collected hashes were checked, scratch is
absent, and reservations are released. The original allocation 2 failure is kept:
the wrapper mistakenly expected a source-only document inside the pack. Its
correction reuses the completed export; no export rebuild or extra job occurred.
The guarded commit-message refusal and its corrected draft are also preserved.

Source qualification binds `6a50010b7160ea52206edc84c864c016a7ea74c4`.
Export qualification binds `bf15170f5a0dc41385b732b8d0c0d443dfd55aee` and its
collected 862-member inventory. The CLI and binding-test payloads changed, along
with manifest/checksums. The context reference remains source-only. Delivered
qualification and preview bind `cba99132e729511b497e65ceb4f1c73cc4d6a29a`; the
full pack and source-test subjects remained unchanged. All 17 original binding
methods, 22 current-view methods, 12 resume methods and both source context
consumers were retained; the source-only Harness consumer is not exported.

Capability evidence is CURRENT with unchanged classification. Published Lite
1.0.0 assets, live context outputs and the live outcome ledger are unchanged.
No model calls were requested; controller/review effort and whole-outcome costs
remain unknown. Native downstream adoption, desktop-host binding and broader
programme qualification remain separate obligations.

The final effect in `evidence/integration-effect.json` proposes guarded dev/main
fast-forward synchronization after terminal review and fresh ref checks, followed
by retirement of only this completed local task branch. Actual refs and the local
`evidence/integration-result.log` establish whether those effects completed.
This report qualifies the bounded change; it does not announce a new release.
