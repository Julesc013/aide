# Packaging Naming Policy

## Purpose

This document defines naming rules for AIDE artifacts and release records. It complements the repository naming doctrine without changing it.

## Rules

- Source directory names must remain based on compatibility technology or host contract.
- Artifact and release names may include exact host versions when the artifact actually targets those versions.
- Host family, adapter technology, release channel, and package version may appear in artifact or release names when they improve traceability.
- Artifact naming should remain stable and parseable over time.
- Naming should prefer lowercase tokens separated by hyphens unless a packaging format imposes a different convention.

## Good Patterns

- `aide-visual-studio-vsix-v2-vssdk-dev`
- `aide-xcode-xcodekit-beta`
- `aide-codewarrior-companion-archival`
- `aide-vs2022-vsix-v2-vssdk-stable`

## Bad Patterns

- `modern-plugin`
- `legacy-build`
- `vs2022-2026` as a source directory name
- `xcode8plus` as a source directory name
- `final-real-release`

## Boundary Rule

Exact host versions may appear in artifact or release names only when they describe produced artifacts or concrete release records. They must not reshape source layout or adapter-lane naming.
