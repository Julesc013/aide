# Install AIDE Lite Pack v0

## Command Import

From the source AIDE repository:

```text
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --dry-run
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --mode safe
```

`--mode safe` is the default. It skips optional broad roots such as `core/` and
`docs/` and prints the exact planned writes plus skipped paths during dry-run.
Use `--mode full` only in reviewed local fixtures where copying optional roots
has been explicitly accepted.

## Manual Import

Copy only the safe portable subset from `files/` into the target repository:
`.aide/`, `.aide.local.example/`, `AGENTS.md.template`, and target templates.
Do not manually copy optional `core/` or `docs/` roots into a product repo unless
that target task explicitly authorizes them. Then fill the target templates
under `.aide/` with target-specific facts.

After import, run in the target repository:

```text
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py pack --task "<target next task>"
py -3 .aide/scripts/aide_lite.py adapter render
py -3 .aide/scripts/aide_lite.py adapter validate
```

Do not copy source `.aide/queue/`, generated context, reports, `.aide.local/`,
provider credentials, raw prompts, or raw responses. Generate adapter outputs
locally in the target repo after target-specific memory and context exist.
