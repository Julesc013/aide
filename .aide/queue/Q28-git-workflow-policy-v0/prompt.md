# Q28 Prompt Summary

Implement AIDE Git Workflow Policy v0:

- branch roles for `main`, `dev`, `task/*`, `release/*`, `hotfix/*`,
  deployment, review, quarantine, and unknown branches;
- report-only workflow detection from local Git state;
- sync, promotion, and pruning policies;
- project workflow profiles for AIDE, Eureka, Dominium, websites, native
  clients, connector-heavy repositories, data snapshots, and unknown repos;
- AIDE Lite `git` command family;
- deterministic golden tasks and tests;
- export-pack integration and documentation.

The prompt also required a prerequisite check: if Q27 outputs are missing or
materially incomplete, Q28 must write blocker evidence and stop rather than
silently implementing Q27 inside Q28.

Q28 stopped on that prerequisite rule because Q27 was blocked and its required
commit discipline, WorkUnit recovery, command, test, documentation, changelog,
and export-pack outputs are absent.
