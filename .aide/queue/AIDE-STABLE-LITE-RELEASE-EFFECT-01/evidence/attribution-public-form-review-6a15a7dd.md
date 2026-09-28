# Attempt-attribution public form review

- Independent reviewer: `/root/stable_effect_review`; fresh read-only review of exact commit `6a15a7dd5e3b0a8b13bf244badaab6c82f6cdf01`, tree `6e8395cff42cb12cc9ac2f2066502c93c33e0324`, parent `25e74785fedd4ddfbd9c1fbdb3310b5040c117e8`.
- Verdict: **ACCEPT** for the candidate release-policy source change. The new `job usage --attempt-set <attempt-roster-json>` form aligns with the delivered CLI and guide, remains mutually exclusive with `--stream`, and explicitly limits accounting to supplied streams. Complete work usage and internal host requests remain unknown. `git diff --check` passed.
- The reviewer did not rerun tests or qualify changed assets. The candidate public list now has 38 forms. Final manifest and exact effect matrix must bind the new form to current bytes, target state, Windows/Python environment, successful attribution and malformed refusal. Previous 37-form effects and assets do not carry over.
