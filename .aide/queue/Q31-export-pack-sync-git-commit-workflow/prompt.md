# Q31 Prompt Summary

Implement Q31 in the AIDE repository as an export-pack synchronization phase.

The phase must make `aide-lite-pack-v0` carry portable Q27-Q30 governance:

- Q27 commit discipline, commit checker, changelog preview, task resumption,
  WorkUnit idempotency, and recovery policy.
- Q28 generic Git workflow policy, branch roles, promotion/sync/prune policy,
  and report-only detection.
- Q29 dry-run Git helper policy and commands.
- Q30's generic lessons while excluding AIDE-specific live branch state.

The pack must not export AIDE source queue history, AIDE-specific branch
detection outputs, latest helper plans, generated context/reports/status,
`.aide.local/`, secrets, raw prompts, raw responses, or target-specific state.

Q31 must validate safe fixture import, prove imported governance commands work,
update documentation and evidence, regenerate the pack and Q32 task packet, and
stop at `needs_review`.

No Eureka/Dominium mutation, branch mutation, provider/model calls, network
calls, GitHub mutation, CI activation, or release publishing is authorized.
