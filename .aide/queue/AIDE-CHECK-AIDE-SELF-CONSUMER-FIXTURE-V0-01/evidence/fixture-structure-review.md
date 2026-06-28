# Fixture Structure Review

Verified fixture root:

- `.aide/fixtures/aide-self-consumer-fixture-v0/fixture.json`
- `.aide/fixtures/aide-self-consumer-fixture-v0/states/source-pack-v0.json`
- `.aide/fixtures/aide-self-consumer-fixture-v0/states/installed-target-before-v0.json`
- `.aide/fixtures/aide-self-consumer-fixture-v0/states/installed-target-after-v1.json`
- `.aide/fixtures/aide-self-consumer-fixture-v0/manifests/ownership-map.json`
- `.aide/fixtures/aide-self-consumer-fixture-v0/manifests/lifecycle-matrix.json`
- nine scenario files under `.aide/fixtures/aide-self-consumer-fixture-v0/scenarios/`

Scenario ids:

- `fresh-install`
- `profile-generation`
- `upgrade-from-previous-version`
- `same-version-idempotence`
- `target-owned-state-preservation`
- `rollback-after-upgrade`
- `uninstall-preserves-target-state`
- `offline-operation`
- `source-repo-confusion-refusal`

All scenario records declare fixture-only, temp-workspace-only, no source repo apply, no real target modification, no network calls, no provider/model calls, and no release publication.
