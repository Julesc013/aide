# Remaining implementation and qualification

1. Replace full-tree content handoff with a bounded change-set over trusted base objects; the actual AIDE repository exceeds MAX_FILES.
2. Recover or explicitly repair reserved-before-prepared materialization using object-bound ownership and process-death tests. Current refusal retains the writer.
3. Wire coordinator v1 and exact new request/receipt protocol under this same task with fresh assurance.
4. Implement and qualify actual PR/check/actor enforcement and remote reconciliation transport; production CLI currently refuses apply.
5. Qualify isolated worker/validation/assurance versus trusted broker identities, filesystem/network boundaries and storage quotas. Same-user Job Objects do not supply these boundaries.
6. Run the real two-task demonstration. The broker transport tests are fixtures; a symlink fixture was skipped because the host token could not create it.
