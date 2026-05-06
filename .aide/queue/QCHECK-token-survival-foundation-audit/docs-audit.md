# Documentation Audit

## Accurate Areas

- `README.md` and `ROADMAP.md` correctly describe Q09-Q20 as awaiting review.
- `DOCUMENTATION.md` indexes Q09-Q20 references and artifacts.
- `PLANS.md` contains detailed Q09-Q20 entries.
- `IMPLEMENT.md` records implementation history.
- `AGENTS.md` managed section contains Q20 token/provider guidance.
- `docs/reference/**` contains dedicated docs for Q09-Q20.

## Stale Areas

| File | Issue | Severity |
| --- | --- | --- |
| `.aide/profile.yaml` | `current_focus` still points at Q09 and `implemented_reality` stops at token survival; Gateway/providers still shown only as deferred. | high |
| `scripts/aide self-check` output | next recommended step is Q09 despite Q20 and QCHECK existing. | high |
| `.aide/scripts/aide_lite.py` context packet | `current_queue_ref()` hardcoded through Q17. | medium |
| Q18 `task.yaml` | status `running` contradicts queue index/status. | medium |
| Q01-Q08 task.yaml files | many remain `pending` despite status/evidence indicating implemented or passed. | low/medium |

## Documentation Risk

The human-facing docs are more current than the canonical Profile. That is
backwards: future automation should trust `.aide/profile.yaml`, so profile drift
needs a fix before the next architecture layer.

## Recommended Docs Fix

Create a narrow reconciliation queue item. Do not casually edit all old docs.
The fix should update Profile current focus, self-check next-step logic, and
status mismatches with evidence.
