# Remaining risks, 2026-09-25

- Canonical validate/doctor fail because reviewed source changes are not yet
  reflected in the old committed export/release preview. This is an expected
  but real gate; source-only acceptance cannot be reused as artifact acceptance.
- `task next-plan` still includes static historical AIDE source readiness
  fields in its report body. The selected next work is target-owned, but the
  broader report presentation is outside the first stable public CLI list
  unless separately admitted and qualified.
- The exact source candidate needs independent review. A later projection
  must test delivered zero- and one-item target queues and qualify replay.
- No final stable release, main promotion, tag, publication or downloaded
  consumer acceptance is established by this WorkUnit.
