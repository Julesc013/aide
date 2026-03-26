# Boot Slice Overview

## What The Boot Slice Is

The first boot slice is a cross-host "identify, invoke, report, and mark" proof.

It contains two tightly bounded behaviors:

- `boot.slice.invoke`: a universal entry-point proof that identifies the host lane, returns a deterministic boot-slice report, and reports capability or explicit unavailability honestly
- `boot.slice.editor-marker`: a minimal `L2` extension that returns or applies one deterministic text change when the lane can honestly provide active editor text

## Why This Slice Was Chosen

This slice is the smallest first wave that still proves the architecture is real:

- it exercises host identity, request or response flow, diagnostics, and capability reporting
- it proves that every committed lane can expose a user or companion entry point
- it stays deterministic and easy to verify
- it leaves room for lanes with lower or narrower ceilings to participate honestly

## What Problem It Solves

The repository now has governance, research, matrices, architecture contracts, environment control-plane records, eval scaffolding, and packaging posture. What it does not yet have is one explicit first implementation target that every committed lane can aim at.

This boot slice closes that gap. It gives later implementation prompts:

- one shared request and response pattern to implement first
- one minimal cross-host observable result
- one explicit acceptance target for degraded, archival, or companion-first lanes
- one oldest-first rollout rule that can progress without hiding blockers

## Why It Fits Modern And Historical Hosts

The selected slice stays inside `L0` through `L2`:

- `L0`: identify host, lane, and version where available
- `L1`: expose one command or companion entry point
- `L2`: perform one deterministic text operation when the lane can honestly provide active editor text

That fits the committed host families more cleanly than a project-aware or deep-UI slice would.

- XcodeKit is explicitly editor-centric and can justify a narrow `L2` proof.
- Visual Studio native lanes can prove a stable entry point and later grow into richer editor or workspace behavior.
- Visual Studio for Mac and CodeWarrior can participate without pretending that archival or environment-heavy lanes are already modern reference implementations.
- Companion lanes can still prove the shared contract through report-first or report-only behavior.

## What It Intentionally Does Not Attempt

The boot slice does not attempt:

- project or workspace awareness
- deep IDE UI integration
- semantic or model-aware transformations
- build, debug, or package orchestration
- release automation
- identical cross-host UX

Those are later phases. The first slice exists to prove contract fidelity, lane honesty, and deterministic behavior.
