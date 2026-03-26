# System Overview

## Core shape

AIDE is one project with one shared core and many host adapters.

The shared core is the product heart. It is where reusable feature logic, protocol definitions, transforms, diagnostics behavior, configuration normalization, and capability-aware orchestration belong.

Host adapters exist because the repository's researched host families do not expose one uniform extension surface. Some hosts provide a deep native contract, some expose only narrow editor or command surfaces, and some require companion behavior outside the IDE process. AIDE therefore keeps host adapters as thin translation layers around host-specific APIs and execution constraints.

## Why the shared core exists

The research corpus and matrices already show repeated cross-host patterns:

- every lane needs host identity and capability context
- every lane needs feature selection and request or response handling
- every lane needs settings, diagnostics, and explicit unavailable reasons
- every lane must remain honest about current capability versus target capability

Without a shared core, each host lane would re-implement those rules inconsistently. The shared core exists to keep reusable behavior, stable data contracts, and transport-agnostic feature semantics in one place.

## Why host adapters still exist

The same research corpus also shows why AIDE cannot collapse everything into one generic extension runtime:

- Windows Visual Studio spans legacy native, VSIX, and newer out-of-process extensibility contracts
- Visual Studio for Mac is archival and MonoDevelop-derived
- Xcode exposes a narrow public source-editor surface and uses a containing-app model
- CodeWarrior spans classic native SDK and automation surfaces plus later Eclipse-based lines

Because of that variation, host adapters remain necessary. They translate host APIs, packaging rules, lifecycle constraints, and UI behaviors into the stable shared-core contract.

## System layers

At a durable level, the repository is organized into these engineering layers:

1. Governance, research, inventory, and matrices define what is known, supported, and credible.
2. `specs/architecture/` defines the durable contracts that implementation must follow.
3. `shared/` will hold reusable execution logic, schemas, transforms, diagnostics, and transport surfaces.
4. `hosts/` will hold thin host-specific adapters that bind real IDE contracts to the shared-core protocol.

## Runtime shape

A future runtime path is expected to look like this:

1. The host adapter identifies its host family, technology lane, execution mode, and available local context.
2. The host adapter produces a stable request envelope for a requested feature.
3. The shared core evaluates settings, feature requirements, capability availability, and transform rules.
4. The shared core returns a stable response containing diagnostics plus any edits, actions, artifacts, or follow-up requirements.
5. The host adapter applies or presents the result through host-specific UI and runtime glue.

## Role of research, inventory, and matrices

The architecture is constrained by repository evidence, not by generic plugin-system assumptions.

- `research/` explains the real extension surfaces and limits for each host family.
- `inventory/` provides the canonical ids for families, technologies, OS families, and exact versions.
- `matrices/` record support posture, capability ceilings, platform reach, packaging posture, and feature applicability.

The shared-core contract system must therefore consume canonical ids and capability models without redefining them.

## Support tiers and capability levels

Support tiers and capability levels remain governance objects, not architecture-owned enums.

- support tier affects commitment, maintenance expectations, and release posture
- capability level affects how much context and workflow depth the shared core can honestly expect from a given lane

Architecture uses these concepts to negotiate feature eligibility and response shape. It does not redefine them.
