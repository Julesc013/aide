# DAG And Dependency Review

The charter/check task graph is accepted as planning-only:

- task IDs are unique in the source graph;
- dependency refs resolve in the accepted reports;
- DAG is acyclic;
- BUILD precedes CHECK;
- CHECK precedes ACCEPT;
- trust and preview precede mutation;
- rollback follows apply;
- scene apply follows scene preview;
- RepoGraph remains a read-only parallel lane.

No downstream task directories were materialized by this acceptance.
