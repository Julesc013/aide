# Source checkpoint and single source qualification job

After exact source/effect review, commit only the reviewed candidate through the
managed commit dry-run/apply path using exact message/parent/ref/staged-tree pins.
The source commit is a candidate, not acceptance. Its existing capability binding
is expected stale until the later reviewed refresh; do not hide or waive that fact.

Substitute only resulting source_commit/source_tree in checks-job-template.json.
Recheck every pinned input, existing config digest61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
clean source, running dispatch, reservations and current admission. One job only,
unchanged180-second/1GiB/32MiB/8MiB limits and4GiB reserves. The runner loads the
exact original Git object into owned scratch for a missing-base comparison, then
runs all13 methods (six original unchanged and seven new), including an actual
fresh-process CLI. Fixtures and Git effects stay in owned TEMP. No canonical
outputs, exports, ref effects, provider calls or source mutation from this job.
Collect every result including failure; verify hashes, quiescence, scratch absence
and released reservations. No automatic retry; later export/preview allocations
need distinct exact review. Do not change finite limits to obtain a green result.
