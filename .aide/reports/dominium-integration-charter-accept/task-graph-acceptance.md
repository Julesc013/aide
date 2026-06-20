# Task Graph Acceptance

The planning graph remains acyclic and dependency ordered:

- BUILD before CHECK;
- CHECK before ACCEPT;
- trust and preview before mutation;
- rollback after apply;
- scene apply after scene preview;
- RepoGraph as read-only parallel lane.

Downstream task directories remain unmaterialized.
