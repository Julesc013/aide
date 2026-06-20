# Task Dependency Graph

`task-dependency-graph.json` contains the machine-readable graph.

Validation requirements:

- task IDs are unique;
- dependency refs resolve;
- graph is acyclic;
- mutation tasks depend on trust and preview prerequisites;
- read-only parallel tasks are marked read-only;
- no downstream queue directories are materialized by this charter.
