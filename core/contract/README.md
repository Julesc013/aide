# Core Contract

## Purpose

Contract holds declarative AIDE Core records. In Q03, the first contract is the AIDE self-hosting Profile/Contract v0 under `.aide/`.

The Profile says what the repository declares, requires, allows, owns, exposes, and defers. It does not execute work.

## Profile Versus Harness

- Profile: declarative repo contract. It records identity, lifecycle status, source-of-truth rules, components, commands, policies, task types, eval declarations, adapter metadata, and compatibility posture.
- Harness: future executable machinery. It will import, compile, validate, doctor, migrate, bakeoff, and drift-check the Profile after Q04 implements it.

Q03 defines Profile/Contract v0 only. It does not implement Harness commands.

## Contract Files Now

Canonical contract records:

- `.aide/profile.yaml`
- `.aide/toolchain.lock`
- `.aide/components/catalog.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/policies/ownership.yaml`
- `.aide/policies/generated-artifacts.yaml`
- `.aide/policies/compatibility.yaml`
- `.aide/policies/validation-severity.yaml`
- `.aide/tasks/catalog.yaml`
- `.aide/evals/catalog.yaml`
- `.aide/adapters/catalog.yaml`
- `.aide/compat/schema-version.yaml`
- `.aide/compat/migration-baseline.yaml`

Human references:

- `docs/reference/profile-contract-v0.md`
- `docs/reference/source-of-truth.md`

Documented v0 shapes:

- `shapes/profile.md`
- `shapes/component.md`
- `shapes/command.md`
- `shapes/policy.md`
- `shapes/task.md`
- `shapes/eval.md`
- `shapes/adapter.md`
- `shapes/toolchain-lock.md`

## Shape Strategy

Q03 uses small YAML records and Markdown shape documents. The records stay close to a JSON-compatible YAML subset: maps, lists, booleans, strings, and simple scalars. Python's standard library does not include a YAML or JSON Schema parser, so Q04 Harness validation must either use conservative line/shape checks, a reviewed dependency decision, or a future conversion strategy.

## Still Planned

- Q04: executable Harness v0.
- Q05: generated downstream artifact boundaries and drift checks.
- Q06: compatibility baseline and migration hardening.
- Q07: Dominium Bridge baseline.

Runtime, Hosts, Commander, Mobile, IDE extension implementations, provider integrations, app surfaces, packaging automation, and autonomous service logic remain outside Q03.
