# Q30 Prompt

Implement AIDE Dev/Main Policy Sync as a bounded governance phase in
`julesc013/aide`.

Required result:

- `main` is documented and validated as AIDE canonical truth.
- `dev` is documented and validated as AIDE integration truth, not canonical
  truth.
- Missing local/remote `dev` produces a future explicit creation/push plan only.
- Q29 helpers remain dry-run/report-only in the live AIDE repository.
- AIDE-specific branch policy and dev/main plan artifacts exist.
- Golden tasks, tests, docs, export pack, and evidence are updated.
- Q30 status ends at `needs_review`.

Forbidden:

- Do not create, push, merge, promote, prune, delete, or fetch live branches.
- Do not call GitHub APIs.
- Do not run provider/model/network calls.
- Do not mutate Eureka, Dominium, or external repositories.
