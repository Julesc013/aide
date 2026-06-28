# Next Task Prompt

Create and process `AIDE-BUILD-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`.

Repo truth outranks this prompt.

Goal:

Repair stale operator-facing routing/status text in `distribution-apply status`, `distribution-apply plan`, and `distribution-apply verify` after `aide_self_consumer_fixture_v0` acceptance.

Scope:

- text/report/routing repair only;
- no behavior broadening;
- no new distribution capability;
- no real apply;
- no canary;
- no release;
- no network/model/provider calls;
- no branch/worktree automation;
- no push.

Required behavior:

- `distribution-apply status/plan/verify` must not route to stale build-era self-consumer fixture text after the self-consumer build/check/accept chain is complete.
- Boundary flags must remain accurate.
- Real target apply and public release remain non-capabilities.

Expected result: `PASS_WITH_WARNINGS` or `PASS`.

Recommended next task: `AIDE-CHECK-DISTRIBUTION-APPLY-ROUTING-TEXT-REPAIR-01`.
