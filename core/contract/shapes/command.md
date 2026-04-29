# Command Declaration Shape

## Purpose

Command declarations distinguish implemented queue helper scripts from planned Harness commands.

## Required Fields

- `id`
- `display_name`
- `invocation`
- `command_kind`
- `status`
- `owner_component`
- `mutates_repo`

## Expected Status Values

- `implemented`
- `implemented-skeleton`
- `planned`

## Boundary

Q03 declares future commands only. It does not create `aide` CLI commands or Harness behavior.
