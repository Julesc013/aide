# Q29 Prompt Summary

Implement AIDE Merge / Land / Promote Helper v0:

- dry-run Git sync planning;
- task-branch landing into integration, usually `task/* -> dev`;
- integration promotion to canonical, usually `dev -> main`;
- prune guards based on ancestor containment;
- mutating behavior tested only in temporary Git fixture repos;
- no live AIDE branch creation, merge, push, prune, or deletion.

The prompt also required a prerequisite check: if Q27 or Q28 outputs are
missing or materially incomplete, Q29 must write blocker evidence and stop
rather than silently implementing prerequisite phases inside Q29.

Q29 stopped on that prerequisite rule because Q27 and Q28 were both blocked and
their required policy, command, test, documentation, detection, and export-pack
outputs are absent.
