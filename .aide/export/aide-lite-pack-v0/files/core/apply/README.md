# AIDE Apply Core

This package contains standard-library helpers for AIDE apply planning records.

AIDE-APPLY-01 adds `managed_sections.py`, a fixture-safe parser and patch
planner for explicit generated-section markers. It preserves manual text outside
markers and blocks missing, duplicate, nested, malformed, binary, or ambiguous
marker cases. It does not expose real repository apply behavior.
