# AIDE CLI Host

## Purpose

The CLI is the first low-friction AIDE Host for Harness commands and future Runtime commands.

## Boundary

Q02 creates this skeleton only. Existing queue helpers under `scripts/**` and the bootstrap-era shared CLI bridge under `shared/cli/**` remain in their current locations until a later reviewed migration exists.

The CLI host must stay a thin shell over AIDE Core and must not own durable workflow semantics.
