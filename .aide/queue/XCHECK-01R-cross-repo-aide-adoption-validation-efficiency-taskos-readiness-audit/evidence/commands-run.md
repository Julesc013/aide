# Commands Run

## AIDE

- `git status --short --branch`: PASS, clean at start.
- `py -3 .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with review-packet token warning.
- `py -3 .aide/scripts/aide_lite.py git plan`: PASS, dry-run status artifacts refreshed.
- `git remote -v; git rev-parse --show-toplevel; git branch --show-current; git branch --all; git rev-parse HEAD; git tag --list; git diff --check`: PASS.
- `git log --oneline --decorate -120`: PASS.
- Queue/status/report file inspections with `Get-Content`, `Get-ChildItem`, and `rg`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status; release status; release draft-status`: PASS.
- `git diff --check`: PASS after writing audit artifacts.
- `git check-ignore .aide.local/`: PASS.
- `py -3 scripts/aide validate`: PASS.
- `py -3 scripts/aide doctor`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with pre-existing review-packet token warning.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py install validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py repair validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py rollback validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS for the pre-existing latest commit.
- `py -3 .aide/scripts/aide_lite.py pack --task "X-TEST-00 AIDE Cross-Repo Validation Tier Model"`: PASS.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS.
- Targeted `rg` secret/raw-prompt scan over XCHECK-01R queue packet and compact reports: PASS, no matches.

## Dominium Read-Only

- `git -C C:\Projects\Dominium\dominium status --short`: PASS, clean.
- `git -C C:\Projects\Dominium\dominium branch --show-current`: PASS, `main`.
- `git -C C:\Projects\Dominium\dominium branch --all`: PASS.
- `git -C C:\Projects\Dominium\dominium remote -v`: PASS.
- `git -C C:\Projects\Dominium\dominium rev-parse HEAD`: PASS, `311c86158587f3fc906b823bc3326259c1859dfc`.
- `git -C C:\Projects\Dominium\dominium log --oneline --decorate -100`: PASS.
- `git -C C:\Projects\Dominium\dominium tag --list`: PASS.
- `git -C C:\Projects\Dominium\dominium diff --check`: PASS.
- `git -C C:\Projects\Dominium\dominium check-ignore .aide.local/`: PASS.
- Target file/report inspections: PASS, read-only.

## Eureka Read-Only

- `git -C C:\Projects\Eureka\eureka status --short`: PASS, clean.
- `git -C C:\Projects\Eureka\eureka branch --show-current`: PASS, `main`.
- `git -C C:\Projects\Eureka\eureka branch --all`: PASS.
- `git -C C:\Projects\Eureka\eureka remote -v`: PASS.
- `git -C C:\Projects\Eureka\eureka rev-parse HEAD`: PASS, `e582028b1db977e28ba6ddc0ed284ca6ccf48234`.
- `git -C C:\Projects\Eureka\eureka log --oneline --decorate -120`: PASS.
- `git -C C:\Projects\Eureka\eureka tag --list`: PASS.
- `git -C C:\Projects\Eureka\eureka diff --check`: PASS.
- `git -C C:\Projects\Eureka\eureka check-ignore .aide.local/`: PASS.
- `git -C C:\Projects\Eureka\eureka rev-list --left-right --count main...dev`: PASS, `0 6`.
- Target file/report inspections: PASS, read-only.

## Notes

Two broad target `rg` inspections produced very large output; they were read-only
and no target files were changed.
