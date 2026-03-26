# AIDE Agent Operating Guide

## Product Identity

- Product name: AIDE
- Expansion: Automated Integrated Development Environment
- Pronunciation: "aid"
- Canonical short namespace: `aide`

## Repository Reality

- This repository is currently in an early bootstrap state.
- The only pre-existing tracked product file at bootstrap was `README.md`.
- `AGENTS.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` are the root control-plane and must remain current.

## Start-of-Run Order

1. Read `AGENTS.md`.
2. Read `PLANS.md`.
3. Read `IMPLEMENT.md`.
4. Read `DOCUMENTATION.md`.
5. Inspect current repository state before editing.

## Execution Doctrine

- Treat queued prompts as an ordered program of work.
- Complete one prompt coherently before advancing to the next.
- Prefer small finished increments over broad partial scaffolding.
- Record blockers, deferrals, and verification truthfully.
- If a queue is not present in the repository or current thread, do not invent feature work. Bootstrap control-plane state, record the blocker, and stop only when no further meaningful progress is possible.

## Editing Doctrine

- Keep changes conservative and auditable.
- Prefer additive structure over rewrites.
- Avoid cross-cutting edits unless they are required to keep the repository coherent.
- Preserve user changes and fix forward.

## Verification Doctrine

- No prompt is complete until its own verification has been performed.
- If runtime verification is unavailable, perform the strongest honest structural verification possible and record the gap.

## Commit Doctrine

- Create at least one commit per completed queued prompt when Git is available.
- Use detailed commit messages with prompt id, scope, key changes, verification, and blocked or deferred notes.
- In this environment, Git may not be on `PATH`; use `C:\Program Files\Git\cmd\git.exe` if needed.
