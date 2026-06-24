# AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01

Create and process `AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01`.

Repo truth outranks this prompt. Inspect the source build task, independent
check task, implementation, focused tests, queue policy, queue index, `PLANS.md`,
and `IMPLEMENT.md`.

This is a bounded repair task. Do not accept the provider. Do not add Omnigent,
ExecutionHost contracts, new adapters, live MCP/A2A/ACP behavior, worker runtime,
Gateway forwarding, provider/model/network calls, preview/apply/rollback, branch
or worktree creation, GitHub mutation, release behavior, target-repository
mutation, or live Dominium command reruns.

Repair only the five material findings:

1. Mismatched capability/provider bindings must fail closed before launch.
2. Receipt launcher accounting and launch metadata must be per invocation.
3. Decoder exceptions must not report complete validation or evidence axes.
4. State-probe failures must fail closed and must not preserve complete typed
   domain results.
5. Cancellation must either be implemented coherently or explicitly declared as
   a v0 non-capability.

Preserve Dominium parity and boundaries:

- exact argv
- shell=False
- at most one launcher call for a valid invocation
- typed refusal semantics
- command-boundary-only capability meaning
- declared state-probe coverage
- no aggregate-validation success claim
- no service-adapter-entry claim
- no capability widening

Required result:

```text
PASS or PASS_WITH_WARNINGS at needs_review
```

Recommended next task only:

```text
AIDE-CHECK-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-REPAIR-01
```
