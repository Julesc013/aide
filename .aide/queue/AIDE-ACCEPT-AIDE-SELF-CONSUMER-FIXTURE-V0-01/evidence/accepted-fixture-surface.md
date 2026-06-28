# Accepted Fixture Surface

Accepted fixture root:

- `.aide/fixtures/aide-self-consumer-fixture-v0/`

Accepted records:

- `fixture.json`
- `states/source-pack-v0.json`
- `states/installed-target-before-v0.json`
- `states/installed-target-after-v1.json`
- `manifests/ownership-map.json`
- `manifests/lifecycle-matrix.json`
- nine scenario records under `scenarios/`

Accepted characteristics:

- fixture-only;
- temp-workspace-only;
- offline required;
- source repository is not the installed target;
- source-generated state is not target truth;
- no real target repository is modified;
- no external repository is touched.
