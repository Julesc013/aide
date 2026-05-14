# Generated Artifact Refresh

## Dry-Run

`py -3 scripts/aide compile --dry-run` reported:

- `validation_status: PASS_WITH_WARNINGS`
- `mode: dry-run`
- generated artifacts are not canonical
- `AGENTS.md`: would keep
- `.agents/skills/aide-queue/SKILL.md`: would keep
- `.agents/skills/aide-execplan/SKILL.md`: would keep
- `.agents/skills/aide-review/SKILL.md`: would keep
- `.aide/generated/preview/CLAUDE.md`: would keep
- `.aide/generated/manifest.yaml`: would replace

## Result

- `py -3 scripts/aide compile --write`: `PASS_WITH_WARNINGS` because the
  compiler wrote generated artifacts while keeping generated outputs
  non-canonical.
- Write result: only `.aide/generated/manifest.yaml` changed.
- `AGENTS.md`, `.agents/skills/aide-queue/SKILL.md`,
  `.agents/skills/aide-execplan/SKILL.md`,
  `.agents/skills/aide-review/SKILL.md`, and
  `.aide/generated/preview/CLAUDE.md` were unchanged.
- Follow-up `py -3 scripts/aide compile --dry-run`: `PASS`; manifest would keep.
- Follow-up `py -3 scripts/aide validate`: `PASS`; generated manifest source
  fingerprint is current.
