# Current Truth Evidence

## Command Evidence

- `repo inventory`: PASS; file_count=5136, unknown_count=0,
  orphan_candidate_count=608.
- `repo status`: PASS; generated_count=943, evidence_count=2687,
  orphan_candidate_count=608.
- `repo validate`: PASS.
- `roots inventory`: PASS; root_count=22, file_count=5136, no_apply=true.
- `roots classify`: PASS; review_required_file_count=5047,
  drop_candidate_is_deletion_approval=false.
- `roots plan`: PASS; no_apply=true, file_moves=false, file_deletes=false,
  reference_rewrites=false.
- `roots status`: PASS; mixed_root_count=3, unknown_root_count=19,
  high_risk_root_count=15.
- `roots validate`: PASS.
- `refactor status`: PASS; no_apply=true, apply_available_in_q39=false.
- `refactor map-status`: PASS; move_entries=0, salvage_entries=20, aliases=0,
  rewrite_entries=40.
- `refactor validate-map`: PASS; no_apply=true, file_moves=false,
  file_deletes=false, reference_rewrites=false.
- `reconciler report`: PASS_WITH_WARNINGS; findings_count=4,
  repair_implemented=false, mutation_performed=false.
- `reconciler validate`: PASS_WITH_WARNINGS.
- `task status`: report-only; task_count=141, latest_task_id is this audit.

## Conclusion

The live repo has enough deterministic no-apply evidence to plan structure work
by authority, but not enough authority to move, delete, rewrite, archive, or
create roots in this task.
