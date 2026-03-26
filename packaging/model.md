# Packaging Model

## Purpose

This document defines the stable packaging and release model for AIDE. It describes how artifact classes, package families, manifest placeholders, signing posture, release channels, and release records should be represented without implying that packaging automation or shipped artifacts already exist.

## Core Concepts

- An `artifact class` describes the high-level shape of what may be produced, such as a native extension package, a companion package, or an archival package.
- A `package family` describes the packaging contract or manifest family associated with a host lane, for example VSIX-oriented manifests, Xcode-oriented manifests, companion-oriented manifests, or archival placeholders.
- A `manifest placeholder` is a future-facing record or template that defines expected package metadata without implying a working build pipeline.
- A `release record` is the machine-readable or documentary record of an actual release event when one exists.
- `signing or notarization posture` records whether a lane is expected to require signing, notarization, or equivalent trust posture review.
- A `release channel` records the intended distribution maturity such as `dev`, `alpha`, `beta`, `rc`, `stable`, or `hotfix`.

## Source Layout Versus Artifact Naming

Source layout and artifact naming serve different purposes:

- source directories remain technology-based and stable across time
- artifact names may later include exact host versions, channels, and package versions when concrete packaging work exists

This separation keeps repository structure durable while still allowing precise release records later.

## Packaging Posture

Packaging posture varies by host family and adapter technology:

- modern native-extension lanes may eventually map to more formal manifest families and signing requirements
- companion lanes may use different release shapes than native-extension lanes
- archival lanes may rely on source-only, archival-package, or documentation-heavy release records rather than modern installers

Current posture must stay conservative until real manifests, pipelines, or artifacts exist.
