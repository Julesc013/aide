# Next Task Scope

## AIDE Next Task

Recommended next AIDE task:

`Q27 - Commit Discipline And WorkUnit Recovery v0`

Reason:

Q25 repaired the pack/import baseline, and Q26 records the Eureka pilot review
handover. The stale Q27-Q29 blocked attempts are superseded, so the next useful
AIDE governance phase is the Q27 redo for structured commits, replay-safe
WorkUnits, task resumption, no-op detection, and changelog-ready commit bodies.

## Eureka Target Note

The current sibling Eureka latest task packet points at a separate target-repo
task. Q26 does not authorize starting that work from AIDE. Any Eureka work must
be done in the Eureka repo from its current queue and prompt.

## Golden Task Candidates For Later

Q27 or later phases should consider golden tasks for:

- safe import excludes source queue, source generated context, reports, cache,
  local state, and secrets;
- compact task packets stay within budget and include exact repo references;
- target pilots preserve manual `AGENTS.md` content;
- repeated prompts no-op or resume from repo-local evidence;
- malformed commit messages are reported rather than hidden.
