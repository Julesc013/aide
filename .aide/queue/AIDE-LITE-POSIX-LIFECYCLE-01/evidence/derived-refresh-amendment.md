### Bounded derived-report refresh

**Reason:** preparation's actual `validate` reported four expected missing development-export entries and one stale capability evidence binding after the CLI changed. `doctor` consequently failed its validation prerequisite. Original output and exact hashes remain in `source-prechecks.json`; neither result is a pass.

**Requested scope amendment:** add only `.aide/reports/capability-ledger.json`, `.aide/reports/capability-ledger.md`, `.aide/reports/capability-evidence-bindings.json` and `.aide/reports/capability-command-status.md` to this WorkUnit. The existing `capability ledger` owner already generates these four source-derived reports. This creates no new capability, authority, support profile or report framework.

**Exact effect after independent ACCEPT:** verify the frozen source/preimage map and current task branch/base, unchanged shared configuration, running dispatch and absent active job under existing control locks; amend only this task's allowed paths; run `py -3 -B .aide/scripts/aide_lite.py capability ledger` once; retain stdout/stderr and all before/after hashes in task evidence. Review generated source/claim changes with the complete source candidate before any commit or allocation. No test, export refresh, new allocation, Git mutation, push or release follows from this amendment.

The separately reviewed local job will refresh the existing generated development export with its ownership inventory. Missing export entries are not repaired by copying files manually, and no original validation failure is erased.
