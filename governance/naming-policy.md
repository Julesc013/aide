# AIDE Naming Policy

## Purpose

This document defines stable naming rules for source directories, files, adapters, manifests, and artifacts.

## Core Naming Rules

- Names must be precise, durable, and stable across time.
- Source directories are named for compatibility technology or host contract.
- Source directories must not be named for exact host versions, version ranges, or vague eras.
- Once a stable contract name is chosen, do not recase or rename it merely because supported versions changed.

## Directory Naming

- Use lowercase ASCII names by default.
- Use hyphen separators when a multi-word directory name is needed.
- Name directories for the contract surface they represent, not for marketing labels.
- Good examples: `extensibility`, `xcodekit`, `vsix-v1`, `vsix-v2-vssdk`, `companion`, `ide-sdk`
- Bad examples: `vs2022-2026`, `xcode8plus`, `modern`, `legacy`

## File Naming

- Policy, architecture, and inventory files should use descriptive lowercase names, typically in kebab-case.
- File names should describe content or contract, not aspirational outcomes.
- If an ecosystem requires a specific casing or file name, follow the external contract only at that boundary.

## Adapter Naming

- Adapter identifiers should make the host family and contract surface obvious.
- Prefer names that can survive future host-version expansion without renaming.
- Adapter names should align with the directory name of the compatibility technology they implement.

## Manifest Naming

- Manifest names should describe what they declare, such as support, capabilities, packaging, or inventory.
- Exact support coverage belongs in metadata/manifests and later matrix data rather than in source directory names.
- Manifest schemas may include exact host versions where the schema requires them.

## Artifact Naming

- Release and packaging artifact names may include exact host versions, release channels, or target identifiers.
- Artifact names are allowed to be more specific than source directory names because they describe produced deliverables rather than long-lived source structure.
- Example artifact specificity is acceptable even when the corresponding source directory remains contract-based.

## Stability Rule

- Naming must remain stable across time so automation, inventory, and documentation do not churn unnecessarily.
- Do not rename a source lane simply because a host moved from current to historical status.
- Do not introduce directory names that collapse multiple unrelated technologies into a vague label.
