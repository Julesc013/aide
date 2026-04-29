# Core Control

## Purpose

Control is the future Core home for operating records that govern evidence, cost, verification, packaging posture, and queue discipline.

## Control Inputs

- eval inventories
- environment records
- matrices
- packaging metadata
- benchmarks
- cost/latency envelopes

## Current Physical Locations

- `evals/**` remains the evaluation and run-record surface.
- `environments/**` remains the environment control-plane surface.
- `matrices/**` remains the support, capability, feature, test, and packaging posture surface.
- `inventory/**` remains the canonical id and version-record surface.
- `packaging/**` remains the release-shape and artifact-control surface.

## Boundary

Q02 maps these areas conceptually without moving them. Control policy changes, generated artifact source-of-truth changes, and release actions remain review-gated.
