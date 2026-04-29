# Core Contract

## Purpose

Contract holds repo-facing declarations for AIDE Core. These records define what other parts of AIDE may rely on before runtime or host implementation consumes them.

## Declaration Families

- profiles
- schemas
- commands
- policies
- tasks
- eval declarations
- component maps
- environment declarations

## Boundary

Q02 creates the Contract skeleton only. The actual profile and contract v0 is Q03. Bootstrap-era `specs/**` and `shared/schemas/**` remain where they are and are treated as evidence until a later reviewed migration exists.
