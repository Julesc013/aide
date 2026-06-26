# Conflict And Refusal Model

Accepted fail-closed coverage includes:

- class conflict and unknown record classes;
- duplicate record and duplicate target path;
- path collision and case-fold collision;
- managed-section overlap;
- file/section ownership conflict;
- nested ownership ambiguity;
- source component mismatch;
- source distribution mismatch;
- unknown owner or missing owner;
- missing evidence refs where required;
- unresolved symlink and reparse uncertainty;
- source-state contamination;
- absolute paths;
- traversal paths;
- unknown required features;
- unknown required extensions;
- digest mismatch and observed digest mismatch;
- unknown and never-touch records allowing apply.

The accepted model is metadata validation and refusal evidence only. It does not
perform apply, repair, delete, rollback, uninstall, or target scanning.
