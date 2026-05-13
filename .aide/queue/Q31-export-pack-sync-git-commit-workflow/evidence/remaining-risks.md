# Q31 Remaining Risks

## Remaining Risks

- Eureka and Dominium still need explicit Q32/Q33 target sync; Q31 only
  updates the source pack.
- Target-specific branch detection, helper plans, context packets, review
  packets, and evidence are not refreshed until target phases run.
- The commit hook template remains opt-in and is not installed automatically.
- Branch protection and CI enforcement are not applied.
- Changelog preview is not release publishing and does not create tags or
  GitHub Releases.
- Exact tokenizer and provider billing integration remain absent; token counts
  are still chars/4 estimates.
- Gateway/provider runtime forwarding and live provider/model calls remain
  deferred.
- AIDE-specific `dev` branch creation and dev-to-main promotion remain future
  explicit operator actions.
- Q31 status is `needs_review`; acceptance still requires human/GPT review of
  evidence and the generated pack.
