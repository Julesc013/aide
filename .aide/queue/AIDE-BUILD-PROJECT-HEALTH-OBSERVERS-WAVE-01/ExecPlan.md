# AIDE-BUILD-PROJECT-HEALTH-OBSERVERS-WAVE-01

## Objective

Build no-apply health observers for queue, evidence, schema, code structure,
doc structure, reference usage, naming/placement, complexity, and performance.

## Plan

1. Define report-only observer outputs.
2. Bind findings to evidence and candidate ProjectGraph facts.
3. Preserve warnings as advisory until a reviewed task accepts stronger truth.
4. Validate and stop at `needs_review`.
