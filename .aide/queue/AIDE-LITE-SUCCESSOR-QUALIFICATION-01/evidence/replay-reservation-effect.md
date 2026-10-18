# Replay reservation correction and important task checkpoint

Actual predecessor upgrade25 and recovery26 passed at source23c0739e; preserve
all prior assertions/results. Replay27 job5767c515 failed before archive generation:
existing stable-validate requires a .aide/release canonical reservation. Doctor
and full validate passed (one advisory missing legacy review reference retained).
The refused result, logs, operation records and safe retirement remain in
predecessor-qualified-replay-refused.json. No product defect is established.

Keep run_replay.py byte-identical. Add only the existing .aide/release reservation
at8388608bytes and its already configured volume to the new exact job template.
All53 canonical release members and863 pack members remain pinned immutable inputs;
the unchanged wrapper verifies complete before/after release equality and pack
hashes. This reservation satisfies the existing guard, not authority to rebuild
or write canonical files. Exact archive generation remains in owned scratch.
Default config61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
roots,180seconds,32MiBscratch,8MiBretained,1GiBmemory and every reserve stay unchanged.
Independent recipe review confirmed this minimal remedy and no other concrete
replay-path issue; exact source/effect acceptance is still required.

After exact independent ACCEPT and one managed checkpoint from
23c0739ed11bd602b2a2f68c4f99a22331272b2d, run allocation28 using
replay-reserved-job-template.json. Only committed source/tree placeholders may
change. Maximum29 includes all27 consumed allocations; fixed preview29 remains
separately gated and is not run by this effect. Fresh exact clean source/tree,
sole checkout, executable/config/input identities, pause, ownership and capacity
admission are required. Persist a new replay-reserved-job-result.log before
assertions; retain original replay-job-result.log unchanged. Verify all collected
hashes, quiescence, scratch absence and reservation release. Stop on failure;
no automatic retry or source edits during execution.

The exact reviewed checkpoint may be synced to existing remote
refs/heads/task/aide-lite-successor-qualification-01 for important continuity.
Before that effect require helper plan, clean exact source/tree, sole checkout,
shared admission/dispatch locks, running dispatch and no active job. The remote
task ref must be a4b5d25f64b9e0ae3029302511956f5d33652f60 (or already exact newHEAD),
an ancestor of the reviewed candidate. Local/remote dev/main must remain
4f2c39606378492622fa8580152373fffc074d7c. Push exact commit:exact task ref without
force, then verify all three remote refs. Latest structured commit must PASS;
range must retain exactly known failures4bb6a4f,651464a,ae26a1c, no additional
failure. This shares an explicitly incomplete qualification checkpoint and does
not waive pending owner dispositions or final release gates. No dev/main mutation,
branch deletion, tag, publication, protection change, provider or target-repo effect.
