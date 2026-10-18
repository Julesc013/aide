**Scope:** extend existing portable task handoff with exact selected inputs and returned candidate results.

- .aide/scripts/task_handoff.py: bounded v2 requests and result codec; default v1 remains.
- .aide/scripts/aide_lite.py: explicit input capture and read-only result export/inspection.
- Existing handoff tests: 18 new methods; all 79 original tests preserved.
- Task-OS reference and four corresponding development-pack payloads; existing export metadata.
- Task/evidence records, queue index, root documentation and the existing campaign current view.
- Six existing changelog preview outputs, fixed through a1a45098.

[Source map](source-map.json), [pack map](pack-source.json), [preview map](preview-source.json)
and [closure map](closure-source.json) identify exact subjects. No new runtime owner,
live target, endpoint, release artifact, permission or spending route changes.
