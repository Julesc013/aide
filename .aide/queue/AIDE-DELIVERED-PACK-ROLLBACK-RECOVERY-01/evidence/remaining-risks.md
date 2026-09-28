# Remaining risks

- This is source qualification; the frozen stable Lite ZIP and tar do not
  contain the new command. Current-source packaging, delivered-byte canaries
  and exact release delta acceptance are separate gates.
- Partial rollback recovery requires Windows anchored effects and the exact
  saved import-intent digest, pack pair and unchanged project bytes. Completed,
  no-effect and unknown states retain their prior importer reconciliation or
  safe-refusal paths; no hostile concurrent-writer guarantee is claimed.
- Independent technical review of the exact commit is pending.
