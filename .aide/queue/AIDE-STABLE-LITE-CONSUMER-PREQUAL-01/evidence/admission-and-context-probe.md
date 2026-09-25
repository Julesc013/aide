# Windows Lite consumer prequalification admission, 2026-09-25

## Authority and source

The owner delegated bounded campaign child WorkUnits and disposable
qualification on 2026-09-25. This evaluation branch starts at observed
`dev@b3a001befaac2d2d9a596c1d7dc738dd1733bec6`, tree
`dfc557ae1acddd347f0ca866500865ad603d1b8a`. Current exact local
preview ZIP SHA-256 is
`8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`;
tar.gz SHA-256 is
`11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c`.
The archives remain local `preview_only`/`no_publish` outputs. No final stable
release, tag, main effect or downloaded-byte evidence follows from this task.

## Clean installed local loop

External new target:
`D:/Projects/AIDE/_review_scratch/stable-lite-context-probe/run-clean-20260925-2154/fresh-target`.
The CLI was invoked from the **extracted ZIP**, outside any AIDE development
checkout. A fresh safe import preview exited 0 and reported 816 operations,
zero conflicts, plan digest
`2a7b50b9c99678371e439d3f5553b90bf210cee93ff16698639d4d3db350648f`.
Exact-plan apply exited 0, reported `APPLIED`, wrote 816 owned paths, and
retained the authored README. The required installed
`.aide/prompts/compact-task.md` existed afterward.

From the installed target, `context` exited 0 and wrote a 447-token local
context packet; `pack --task 'Disposable installed AIDE context evidence smoke
task'` exited 0 and wrote a 1,095-token task packet; `verify` exited 0 with
`WARN`, zero errors and 15 warnings. The warnings include optional missing
generated reports and `git status unavailable` because this disposable fresh
target was not a Git repository. No OS-level network trace was run, so this
does not alone qualify an offline guarantee.

External log SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `import-preview.json` | `1558e34044df6f2af39fc2e5e87b2ca4574bc1a065389a5f1a01baa6ccc0dfba` |
| `import-apply.txt` | `a9079192e90d712abc523a9c8c1b1747f3945b2145707c8a1bdf53c4ef349901` |
| `context.log` | `93f5b1825d0c83cd5c3a65f1649269392d294e76e7013f81b874227ae98db487` |
| `pack.log` | `4cc77a1aebf8af28a2cafff1e47380958b05d444a20f0961028798ef4c738318` |
| `verify.log` | `58ee08c93b4f78f7e94198cdf74c4e90a95479f2c9dda864b66209b572b48d0f` |

An earlier probe cloned the prior 25-command canary's **post-tamper** target,
where `.aide/prompts/compact-task.md` had intentionally been removed. Its
`verify` exit 1 is retained under
`stable-lite-context-probe/run-20260925-2148/` and is **not** a fresh-install
failure. A first attempt in the clean run also tried to parse human-readable
preview text as JSON; it refused before apply, then the exact printed digest
was parsed and used successfully. These attempts are not counted as product
failures or hidden from the run history.

## Next gate

The separately implemented lifecycle/restart canary is running in disposable
scratch. Its exact script, failed attempt, passing run or defect, target bytes
and independent review will determine the next source action. Final
downloaded-byte qualification remains open.
