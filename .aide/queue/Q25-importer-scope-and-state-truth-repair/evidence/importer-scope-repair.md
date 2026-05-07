# Importer Scope Repair

## Old Behavior

`import-pack` planned every file under pack `files/`. Because the pack includes
optional fixture-oriented `core/**` and `docs/**` roots, direct import was too
broad for real target-pilot work. Eureka and Dominium therefore used Q21
dry-run plus manual scoped import to avoid out-of-scope target writes.

## New Scoped Behavior

- `import-pack` now has `--mode safe|full`.
- Default mode is `safe`.
- Safe mode imports portable `.aide/**`, `.aide.local.example/**`, target
  templates, `AGENTS.md.template` as managed `AGENTS.md` guidance, and
  `.gitignore` local-state rules.
- Safe mode skips broad roots:
  - `core/**`
  - `docs/**`
- `--mode full` keeps the previous broad behavior available only when a
  reviewed local fixture explicitly selects it.
- Dry-run now reports:
  - exact planned writes;
  - conflicts;
  - skipped paths and skip reasons;
  - provider/model/network call status.
- Existing manual `AGENTS.md` content is preserved outside the managed portable
  section.
- Existing conflicting target files are reported and not overwritten.

## Fixture Result

Temporary fixture:

- dry-run: PASS, safe mode, 105 planned writes, 22 skipped optional paths,
  0 conflicts, 0 writes.
- import: PASS, safe mode, 105 writes, 22 skipped optional paths, 0 conflicts.
- imported fixture `doctor`: PASS.
- imported fixture `snapshot`: PASS.
- imported fixture `index`: PASS.
- imported fixture `pack --task "Fixture Q25 smoke task"`: PASS.
- `core/` copied: false.
- `docs/` copied: false.
- existing `AGENTS.md` manual text remained before the managed
  `AIDE-PORTABLE` section.

## Intentionally Excluded By Default

- source queue/history;
- source profile identity and memory;
- generated source context/reports;
- cache/latest route/controller/Gateway/provider status;
- `.aide.local/`;
- `.env`;
- optional broad `core/**` and `docs/**`;
- secrets, raw prompts, and raw responses.

## Remaining Limitations

Fixture import proves the safer write scope and imported smoke commands, not
that broad target handoff is complete. Q26 must review the Eureka pilot and
handover process before broader use.
