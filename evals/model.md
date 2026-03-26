# Evaluation Model

## Purpose

This document defines the stable model for AIDE evaluation and verification work. It describes how evals are identified, how verification routines are classified, how results are recorded, and how blocked or deferred work is represented without overstating implementation maturity.

## Core Concepts

- An `eval` is a defined verification or assessment effort with a stable id, scope, and expected evidence.
- A `verification routine` is a repeatable check category or procedure used by one or more evals.
- A `grader` is the routine, reviewer, or future automated process that interprets evidence and assigns a result state.
- An `eval run` is one execution or review event against a specific scope at a specific time.
- An `eval report` is a synthesized summary derived from one or more runs.

## Evaluation Categories

The base vocabulary for this phase is:

- `existence`: confirms required files, manifests, directories, or records exist
- `schema`: confirms machine-readable files follow their intended structural shape
- `docs-consistency`: confirms documentation, matrices, manifests, and control-plane records do not contradict one another
- `load-smoke`: reserved for future host or adapter load-level checks
- `editor-smoke`: reserved for future editor or file-interaction checks
- `workspace-smoke`: reserved for future project or workspace interaction checks
- `packaging-check`: reserved for future artifact-shape or manifest verification
- `release-shape`: reserved for future release-record and release-audit verification
- `archival-record`: verifies preservation-oriented evidence, provenance, or extraction records for archival lanes

## Result States

Result states must distinguish between absence of implementation and failure of implementation.

- `planned`: the eval shape exists, but no run has been scheduled yet
- `pending`: a run is expected, but no result has been recorded yet
- `passed`: the eval ran and its acceptance criteria were met
- `failed`: the eval ran and the acceptance criteria were not met
- `blocked`: the eval could not be completed because a concrete blocker prevented meaningful execution
- `deferred`: the eval is intentionally postponed to a later phase
- `not-applicable`: the eval category does not meaningfully apply to the scoped lane
- `unverifiable`: the desired claim cannot currently be verified with available evidence or tooling

## Evidence Expectations

Every eval definition or run should identify the expected evidence shape. Examples include:

- command output
- schema review notes
- manifest or matrix snapshots
- screenshots or logs from later smoke work
- archival provenance records

Evidence must be concrete enough to support the recorded result state. Missing evidence should not be rewritten as a passing result.

## Blocked And Deferred Semantics

- Use `blocked` when the work should proceed now but cannot because of a real blocker such as missing media, missing environment access, or missing implementation.
- Use `deferred` when the work is intentionally postponed because the current phase does not require it yet.
- Use `unverifiable` when the desired question is meaningful but the available evidence or tooling cannot answer it honestly.

## Capability Levels And Eval Depth

Capability levels do not redefine eval categories, but they affect expected depth:

- `L0` lanes usually justify existence, schema, docs-consistency, and limited load-smoke planning.
- `L1` lanes add command or entry-point oriented smoke expectations.
- `L2` lanes justify editor-smoke planning.
- `L3` lanes justify workspace-smoke planning.
- `L4` lanes may require richer behavioral, packaging, and release-shape evaluation later.

Host ceilings differ. A lower-capability lane can still be well-verified within its honest scope.
