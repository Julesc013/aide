# Q03 Profile Shape Evidence

## Profile Identity

`.aide/profile.yaml` declares:

- `schema_version: aide.profile.v0`
- `profile_contract_version: aide.profile-contract.v0`
- `profile_id: aide-self-hosting`
- `profile_mode: self-hosting`
- repository id `julesc013/aide`
- repository role `AIDE self-hosting repo`
- lifecycle status `reboot/pre-product`

## Architecture Shape

The Profile declares the public model:

- AIDE Core
- AIDE Hosts
- AIDE Bridges

The Profile declares the internal Core split:

- Contract
- Harness
- Runtime
- Compatibility
- Control
- SDK

The Profile records the first shipped stack direction:

- Contract
- Harness
- Compatibility
- Dominium Bridge

## Implemented Reality Versus Future Intent

Implemented or partial reality:

- queue is implemented
- queue helper scripts are implemented read-only scripts
- shared boot slice and host proofs remain bootstrap-era implemented evidence
- Profile/Contract v0 is partial
- Dominium Bridge is skeleton only

Future or deferred intent:

- Harness v0 is Q04
- generated artifacts are Q05
- compatibility baseline is Q06
- Dominium Bridge baseline is Q07
- Runtime, SDK, product Hosts, Commander, Mobile, and IDE Hosts remain deferred

## Contract Declaration Shape

Q03 uses compact YAML catalogs:

- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/tasks/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/adapters/catalog.yaml`

Q03 uses Markdown documented shapes under `core/contract/shapes/**` instead of executable JSON Schema.

## Boundary

The Profile is declarative. Q03 did not add Harness commands, generated downstream artifacts, Runtime behavior, Host behavior, provider adapters, app surfaces, or autonomous service logic.
