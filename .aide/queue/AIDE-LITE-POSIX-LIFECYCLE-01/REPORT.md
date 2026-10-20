### Shared lifecycle: local continuation passed; hosted qualification pending

**Source:** `809456fa43c543970c45760d5c32db8734c443dc`, Windows 10 `19045`/x64, CPython `3.14.8`. [Exact result](evidence/local-result.json), [retirement and retained digests](evidence/local-qualified.json), [input identities](evidence/package-inputs.json).

| Observation | Result |
| --- | --- |
| Fresh and brownfield development adoption, preservation and detach | Both passed |
| Actual published 1.1 upgrade, interruption and exact recovery | Fresh and customized brownfield passed |
| Real upstream conflict, explicit resolution and changed-resolution refusal | Passed; direct edits and disabled examples preserved |
| Installed owned-file repair interruption/recovery | Passed |
| Actual predecessor path-change rollback | Safely refused; detach/reinstall passed; same-path rollback is a separate unchanged oracle |
| Affected removal/recovery checks and export boundary | Four passed |
| Original Windows callback regression | Passed after conditional optional-argument forwarding correction |
| Original attempt | Timeout/incomplete with one callback error; preserved, not relabelled |
| Linux/macOS native execution | Pending; 15 Windows-host POSIX skips are not qualification |

**Work conserved:** original source `ba5c318e` retains 117 fixture passes/nine skips, eight shared lifecycle passes/two POSIX skips, eleven Windows regression passes and two published-package adoption/detach passes. [Independent dependency review](evidence/continuation-plan-review.json) and [exact dependency proof](evidence/reuse-dependency-proof.json) scope reuse; the original failed test and unfinished cases were rerun under new attempt identities.

**Execution and collection:** job `eba95a543dc440258bb26da090db3e86` exited zero, quiesced and retired. Scratch is absent and reservations released. Peaks: 359,510,016 bytes worker memory and 26,298,797 bytes scratch. Lossless transport verified 109 files/5,139,565 raw bytes. The development export has 878 files, matches the tested manifest and excludes the source-only lifecycle fixture. Eight frozen stable assets remain unchanged. Controller/review model usage remains unknown.

**Repository checks:** `doctor`, `validate` and `commit check --latest` passed after export refresh. `validate` reported 60,925 passes, one existing missing `.aide/prompts/evidence-review.md` reference warning and no failures. Original pre-refresh failures remain in their own records.

**Limits:** development-package evidence does not qualify versioned Lite 1.2 archives or expand the published 1.1 support profile. POSIX ownership is cooperative; arbitrary outer-client writers are not contained. Termination in a rename gap preserves the original backup and requires explicit reconciliation. No additional local retry, hosted run, Git integration, tag or release has occurred. Next: review one exact source checkpoint and one standard three-profile hosted run, retaining failures and original observations.
