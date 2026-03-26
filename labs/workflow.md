# Lab Workflow

## Purpose

This document defines how environment and bring-up experiments move through the lab area before they become stable repository knowledge.

## Core progression

Lab work typically moves through these states:

- `planned`
- `acquired`
- `installing`
- `boots`
- `usable`
- `blocked`
- `archival-record`

These labels are used to keep partial progress explicit rather than overstating success.

## Prototype path

1. Create a prototype record with scope, intended environment refs, and next step.
2. Reference environment-catalog records where an environment family or instance already exists.
3. Update the prototype as media is acquired, installation begins, and first boot or validation occurs.
4. Promote successful repeatable findings into `environments/` or other authoritative docs when the work stops being experimental.

## Blocked path

When work cannot progress, create or update a blocked record that captures:

- the blocked area
- the relevant environment refs
- the blocker type
- what would unblock the work

Blocked work should remain explicit instead of disappearing into notes or commit messages.

## Archival path

Move work toward archival records when:

- the experiment is no longer active
- only historical evidence remains
- the findings may still be useful later even if no runnable result exists now

## Promotion rule

Successful lab findings should be promoted into stable catalogs, playbooks, architecture docs, or implementation prompts once they become repeatable and trustworthy.

Labs are not the final home for durable operational truth.
