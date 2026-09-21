# Candidate Scope

## Base And Source

- Integration base: `be3a854abde73dd1d3498a20c240bd0c0a58c28b`.
- Reviewed neutrality source: `0e76df9e10c0fa6d80b363c0990224ef45853062`.
- Reviewed checkpoint closeout: `91efe8156c4132cc8178e330b43d01db1a678d8c`.

## Included

- Exact deletion of `.codex/config.toml`.
- Exact reviewed content for `.codex/README.md`, `.codex/agents/README.md`, and
  five description-only role TOMLs.
- Original completed neutrality WorkUnit and evidence.
- This integration WorkUnit and one queue-index entry for each task.

## Excluded

- Broker, isolated-host, provider, target, workflow, specification, or product
  source from the mixed task branch.
- Machine/user configuration, `.aide.local/`, credentials, caches, recovery
  archives, generated bulk outputs, and private handoff material.
- `main` mutation, tag, release, and publication effects.

The old `main -> be3a854a` review subject remains historical. After successful
`dev` integration, a new exact commit/tree and complete `main..dev` closure must
be recorded before any promotion decision.
