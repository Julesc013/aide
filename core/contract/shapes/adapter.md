# Adapter Declaration Shape

## Purpose

Adapter declarations identify target agent workflow families without binding AIDE to a provider implementation.

## Required Fields

- `id`
- `display_name`
- `status`
- `adapter_kind`
- `generated_artifacts`
- `implementation`

## Boundary

Adapters do not own durable AIDE semantics. Generated downstream artifacts remain planned for Q05 and are not produced by Q03.
