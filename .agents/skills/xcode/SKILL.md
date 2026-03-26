---
name: aide-xcode
description: Use when work is centered on `hosts/apple/xcode/**` or the inventory and matrix records that directly govern Xcode lanes.
---

## Scope

- `hosts/apple/xcode/**`
- Xcode lane manifests
- directly related inventory and matrix rows for `xcodekit` or companion posture

## Trigger

- when a prompt targets Xcode host lanes, manifests, or Xcode-specific evaluation posture
- when Xcode-native and companion boundaries need to remain explicit

## Do Not Use

- Do not use this skill for general Apple platform notes outside Xcode lanes.
- Do not use this skill when the task is actually shared-core or packaging work.
