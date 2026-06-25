# Material Findings

- workspace.path_probe_matrix: Containment helper rejects traversal, absolute paths, and symlink escape when exercised directly.
- workspace.test_matrix_incomplete: Focused tests do not cover the full required path containment matrix.
- events.duplicate_terminal_reason: A second terminal event must produce the typed duplicate_terminal_event refusal rather than a generic post-terminal refusal.
- events.test_matrix_incomplete: Focused tests do not cover the full required fail-closed event stream matrix.
- artifacts.test_matrix_incomplete: Focused tests do not cover the full required artifact integrity matrix.
- lifecycle.cancelled_terminal_missing: The required compact lifecycle names cancelled as a terminal state, but the repair projection omits it.
- lifecycle.test_matrix_incomplete: Focused tests do not cover every required allowed transition and representative invalid terminal/reconciliation cases.
