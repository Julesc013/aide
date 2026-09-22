# Registered bridge evidence

The eight-file source manifest and current validation receipt identify the
reviewed local bridge. The current 43-test run and independent 11-test replay
passed; the earlier first run retains its separate source binding.

`bridge-evidence.zip` preserves every listed raw receipt, patch and log, including
the original independent review and the prior checkpoint/push receipts. Resolve
raw filenames in those records as exact ZIP member names. `bridge-custody.json`
provides SHA-256 and byte length for each member plus the SHA-256 of readable
Git LF projections. Raw generated logs remain outside the committed file list.

The broker task remains active. Local child-process fixtures prove no provider
authentication, credential/filesystem isolation or server atomicity.
