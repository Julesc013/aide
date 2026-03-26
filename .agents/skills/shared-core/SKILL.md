---
name: aide-shared-core
description: Use when defining shared engine boundaries, contracts, protocols, or reusable logic that must stay free of host-specific leakage.
---

## Scope

- `shared/**`
- shared contracts, protocols, and engine boundaries
- cross-host logic that can be defended as genuinely reusable

## Trigger

- when a prompt is about shared-core structure, interfaces, or cross-host abstractions
- when host-specific details must be separated from shared behavior

## Do Not Use

- Do not use this skill when editing `hosts/**` implementation lanes directly.
- Do not use this skill when the work is only packaging, lab setup, or evaluation bookkeeping.
