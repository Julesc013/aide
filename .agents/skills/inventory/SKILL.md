---
name: aide-inventory
description: Use when maintaining inventory ids, enums, manifests, or exact-version records without inventing facts.
---

## Scope

- `inventory/**`
- inventory-backed manifest normalization
- matrix rows that must align with canonical inventory ids

## Trigger

- when adding or normalizing ids, enums, or record shapes
- when exact-version records need `null`, `deferred`, `unverified`, or `placeholder` handling

## Do Not Use

- Do not use this skill when writing governance policy or broad architectural vision.
- Do not use this skill when implementing host adapters or shared-core behavior.
