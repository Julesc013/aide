# AIDE Subagent Roles

Subagents should only be spawned when explicitly requested. Read-heavy parallel work is preferred over write-heavy parallel work.

## Researcher

Purpose: read-heavy exploration and synthesis for bounded repository questions.
Use when: a task needs focused inspection, comparison, or summary across existing files.
Do not use when: the main task is immediate implementation or the next blocking step requires tight authorship in the same files.

## Cataloger

Purpose: normalize ids, manifests, enums, inventory rows, and matrix rows.
Use when: work is schema-shaped, repetitive, or inventory-driven.
Do not use when: the task is broad architectural design, prose governance, or host implementation.

## Scaffold

Purpose: generate directories, placeholder files, and repetitive bootstrap structure.
Use when: the task is mostly mechanical scaffold generation with a clear write boundary.
Do not use when: the task needs complex architecture decisions or overlapping write-heavy collaboration.

## Reviewer

Purpose: review correctness, scope discipline, and compliance with repository law.
Use when: a change needs a bounded risk review or policy-alignment check.
Do not use when: the task is simply to generate new scaffold or normalize catalog data.

## Verifier

Purpose: run verification commands and consistency checks on a bounded change set.
Use when: the task needs file existence checks, anchor checks, or structured verification passes.
Do not use when: the task still lacks a stable candidate result to verify.
