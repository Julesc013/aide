# Import Fixture Report

## Fixture Target

Q21 fixture validation used a temporary local repository target:

```text
C:/Users/Jules/AppData/Local/Temp/aide-q21-fixture-final
```

The fixture was initialized with:

- `README.md`
- an existing `AGENTS.md` containing manual target guidance
- a minimal `.gitignore`

No real Eureka or Dominium repository was touched.

## Dry Run

Command:

```text
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture> --dry-run
```

Result:

- PASS
- operation_count: 116
- conflicts: 0
- written: 0
- provider/model calls: none
- network calls: none

## Import

Command:

```text
py -3 .aide/scripts/aide_lite.py import-pack --pack .aide/export/aide-lite-pack-v0 --target <fixture>
```

Result:

- PASS
- operation_count: 116
- conflicts: 0
- written: 116
- provider/model calls: none
- network calls: none

## Target Smoke

The imported target ran these commands successfully:

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py snapshot`
- `py -3 .aide/scripts/aide_lite.py index`
- `py -3 .aide/scripts/aide_lite.py pack --task "Fixture target smoke task"`
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`

Target task packet result:

- chars: 3789
- approx tokens: 948
- budget status: PASS

## Boundary Checks

- Existing manual `AGENTS.md` content was preserved.
- A managed portable `AGENTS.md` section was added.
- Target `.aide/profile.yaml` and memory files were created from target
  templates, not copied from AIDE's source repo identity.
- Source `.aide/queue/index.yaml` and queue history were not copied.
- Generated source context and reports were not copied.
- Actual `.aide.local/` was not created.
- Target `.gitignore` includes `.aide.local/` protection.

## Warnings

The target `doctor` reports missing Q09-Q20 queue status files because the pack
does not copy AIDE self-hosting queue history. That is expected and correct for
portable target repos.
