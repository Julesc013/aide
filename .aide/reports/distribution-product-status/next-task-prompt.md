# Next Task Prompt

Create and process `AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`.

Repo truth outranks this prompt. Independently verify the distribution product-status projection built by `AIDE-BUILD-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`.

Scope:

- check-only;
- no implementation repair unless a separate repair task is created;
- no real target apply;
- no source repo self-apply;
- no canary inventory;
- no release generation or publication;
- no package source implementation;
- no provider/model/network calls;
- no branch/worktree automation;
- no push;
- no external repo mutation.

Verify:

- `.aide/reports/distribution-product-status/current.json` parses and includes required keys;
- `.aide/reports/distribution-product-status/current.md` exists and includes required headings;
- accepted `distribution_apply_engine_v0` and `aide_self_consumer_fixture_v0` are represented;
- accepted boundary `distribution_apply_routing_text_repair_v0` is represented;
- next task routes to `AIDE-CHECK-DISTRIBUTION-PRODUCT-STATUS-PROJECTION-01`;
- real target apply, canary readiness, public release readiness, package source readiness, provider/model/network readiness, runtime readiness, and branch/worktree apply readiness remain false;
- explicit non-capabilities are preserved;
- validation and evidence are complete.

Expected result: `PASS_WITH_WARNINGS` or `PASS`.
