# Install AIDE Lite Pack v0

## Command Import

From the source AIDE repository:

```text
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --dry-run
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo>
```

## Manual Import

Copy files from `files/` into the target repository, then fill the target
templates under `.aide/` with target-specific facts.

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
