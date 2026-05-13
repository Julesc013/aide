# Q36 ExecPlan

## Objective

Define the first AIDE intent compiler so raw user requests are normalized into
bounded, safe, repo-grounded WorkUnits before execution.

## Required Outputs

- intent compiler policy;
- report-first normalization command;
- deterministic risk/task classification;
- branch and dependency preflight;
- generated WorkUnit summary;
- tests, golden tasks, docs, evidence, and export-pack sync.

## Boundary

Q36 must not execute raw intent, mutate branches, call providers/models, or
perform product work.
