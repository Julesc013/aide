# AIDE Lite Pack v0

Pack id: `aide-lite-pack-v0`

This is a portable metadata and tooling pack for target repositories. It is
generated from AIDE's repo-local no-call token-survival foundation. Q24 adds
portable adapter templates so target repositories can generate local guidance
previews for existing tools after import.

The pack intentionally excludes AIDE's source profile, queue history, project
memory, generated context, reports, route/cache/controller/latest status,
provider/Gateway status reports, eval runs, `.aide.local/`, raw prompts, raw
responses, and secrets.

Q25 makes command import default to `--mode safe`, which plans and writes only
portable `.aide/`, `.aide.local.example/`, target templates, `AGENTS.md`, and
`.gitignore` local-state rules. Optional broad roots such as `core/` and
`docs/` remain in the pack for reviewed fixtures but are skipped unless
`--mode full` is selected explicitly.

Use `install.md` for manual and command-based import steps.
