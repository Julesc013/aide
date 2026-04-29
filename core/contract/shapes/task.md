# Task Catalog Shape

## Purpose

The task catalog describes queue item intent and task types without replacing live queue status.

## Required Fields

- `schema_version`
- `profile_contract_version`
- `catalog_status`
- `source_of_truth_note`
- `task_types`
- `queue_items`

Each queue item should include:

- `id`
- `type`
- `intent`
- `expected_packet`

## Boundary

The canonical task execution state remains `.aide/queue/index.yaml` and each task `status.yaml`.
