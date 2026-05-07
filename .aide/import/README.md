# AIDE Lite Import Templates

This directory contains target-neutral templates used by Q21 export/import
tooling. They are not AIDE's own project memory or queue history.

Use these templates when importing the portable AIDE Lite Pack into another
repository. Target repositories must generate their own snapshot, context map,
task packet, evidence packet, token reports, and project memory after import.

Q25 makes `import-pack` default to safe scope. Dry-run prints exact planned
writes and skipped paths. Safe mode imports portable `.aide/` files, target
templates, `.aide.local.example/`, managed `AGENTS.md` guidance, and
`.gitignore` local-state rules. It skips optional broad roots such as `core/`
and `docs/` unless `--mode full` is explicitly chosen for a reviewed local
fixture.

Do not copy source `.aide/queue/`, generated context, reports, `.aide.local/`,
raw prompts, raw responses, or provider credentials into target repos.
