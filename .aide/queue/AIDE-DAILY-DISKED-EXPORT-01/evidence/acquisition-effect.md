# Held exact wheel acquisition

Run acquire_wheels.py once through unchanged managed_workspace/WindowsJobHost.
It reads only seven exact reviewed HTTPS artifact URLs from files.pythonhosted.org,
rejects redirects, limits every response to pinned size plus one byte, and checks
all actual SHA256/size/native package name/version before considering it reusable.
Inspect zip headers/metadata only; execute or install no downloaded code. Outputs
are exclusive files in owned job output; full streams/results are collected and
scratch retired through the existing runner. No target or canonical output.

Seven wheel inputs total631366bytes. Existing limits/config/reserves unchanged;
one of maximum three child jobs. Per-request timeout20sec, job180sec. On failure,
retain the one terminal result and any partial bytes; no endless retries or global
installation. Retained wheel bytes can serve the separate reviewed offline test
effect only after full actual acquisition/collection digests are verified.

acquisition-job-template.json pins wrapper, wheel inputs, existing runner/host
owners and Python binary. Only source_commit/source_tree can be replaced with the
subsequent exact accepted clean source checkpoint in an ignored effective manifest.
All other bytes/effects remain unchanged. Admission still rechecks exact inputs,
source/ref, pause, prior-attempt reconciliation and reservations under shared lock.
No source/native target qualification, baseline acceptance or release claim.
