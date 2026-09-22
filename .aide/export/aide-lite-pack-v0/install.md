# Install AIDE Lite Pack v0

## Command Import

From the root of an extracted release archive, without the source checkout:

```text
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> import-pack --pack . --target <target-repo> --dry-run --mode safe
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> import-pack --pack . --target <target-repo> --mode safe --expect-plan <preview-plan-digest>
```

From the source AIDE repository during development:

```text
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --dry-run
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <target-repo> --mode safe --expect-plan <preview-plan-digest>
```

`--mode safe` is the default. It skips optional broad roots such as `core/` and
non-reference `docs/` content and prints the exact planned writes plus skipped
paths during dry-run. Portable `docs/reference/` governance docs are safe-mode
files. Use `--mode full` only in reviewed local fixtures where copying optional
roots has been explicitly accepted.

Successful import records exact managed-file and portable managed-section
baselines under `.aide/install/`. A later pack updates only unchanged recorded
bytes. Use `--from-pack <validated-predecessor-pack>` to prove the baseline of
an older installation that predates receipts. Local edits, unknown ownership,
changed preview state, invalid packs, and partial prior effects refuse closed.

## Read-Only Removal Planning

After a receipt-backed import, inspect the exact future removal boundary without
changing target bytes:

```text
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> plan-removal --target <target-repo>
py -3 -I -B files/.aide/scripts/aide_lite.py --repo-root <target-repo> plan-removal --target <target-repo> --json
```

Only unchanged bytes recorded as AIDE-managed are future removal candidates.
Local edits, missing state, target-owned files, unknown ownership, and authored
`AGENTS.md` content are preserved. This command is planning-only: it never
deletes files, removes a managed section, or writes lifecycle state.

## Manual Import

Copy only the safe portable subset from `files/` into the target repository:
`.aide/`, `.aide.local.example/`, `docs/reference/` governance docs,
`AGENTS.md.template`, and target templates. Do not manually copy optional
`core/` or broad non-reference `docs/` roots into a product repo unless that
target task explicitly authorizes them. Then fill the target templates under
`.aide/` with target-specific facts.

After import, run in the target repository:

```text
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py repo inventory
py -3 .aide/scripts/aide_lite.py repo validate
py -3 .aide/scripts/aide_lite.py repo status
py -3 .aide/scripts/aide_lite.py quality ledger
py -3 .aide/scripts/aide_lite.py quality validate
py -3 .aide/scripts/aide_lite.py refactor status
py -3 .aide/scripts/aide_lite.py refactor plan
py -3 .aide/scripts/aide_lite.py refactor validate
py -3 .aide/scripts/aide_lite.py pack --task "<target next task>"
py -3 .aide/scripts/aide_lite.py adapter render
py -3 .aide/scripts/aide_lite.py adapter validate
py -3 .aide/scripts/aide_lite.py commit template
py -3 .aide/scripts/aide_lite.py git policy
py -3 .aide/scripts/aide_lite.py git plan
py -3 .aide/scripts/aide_lite.py github validate
```

Do not copy source `.aide/queue/`, generated context, reports, `.aide.local/`,
provider credentials, raw prompts, or raw responses. Generate adapter outputs
locally in the target repo after target-specific memory and context exist.
Commit hooks are copied as `.aide/hooks/commit-msg` but are not installed into
`.git/hooks`; hook installation remains an explicit target action.
