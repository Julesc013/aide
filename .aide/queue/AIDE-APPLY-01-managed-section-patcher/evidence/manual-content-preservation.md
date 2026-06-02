# Manual Content Preservation

## Mechanism

- `core/apply/managed_sections.py` computes manual prefix and suffix hashes around the managed section.
- `verify_manual_content_preserved()` checks that text outside the managed markers is byte-for-byte preserved after replacement.
- Planned operations carry `manual_prefix_hash`, `manual_suffix_hash`, `existing_section_hash`, and `new_section_hash`.

## Evidence

- `py -3 -m unittest discover -s core/apply/tests -t .`: PASS, including manual prefix/suffix preservation.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS.
- `managed_section_manual_content_preservation_golden`: PASS.

## Boundary

Only fixture and in-memory patching is implemented. The active repository is not patched by the new command surface.
