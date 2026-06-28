# Next Task Prompt

Create and process `AIDE-ACCEPT-AIDE-SELF-CONSUMER-FIXTURE-V0-01`.

Use live `.aide/queue/index.yaml` as canonical truth.

Accept only `aide_self_consumer_fixture_v0` if the build/check chain remains complete, evidence remains intact, material finding count is `0`, and missing evidence is `0`.

Acceptance boundary:

- fixture corpus;
- self-consumer install/upgrade/rollback/uninstall proof;
- same-version idempotence proof;
- offline fixture operation;
- source-vs-installed-target distinction;
- preservation of target-owned state.

Do not accept real source repo self-update, real target apply, public release, canary profile readiness, network source, GitHub Release source, branch automation, provider/model/network calls, or external repository mutation.
