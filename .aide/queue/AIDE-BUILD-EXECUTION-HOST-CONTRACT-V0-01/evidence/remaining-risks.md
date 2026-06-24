# Remaining Risks

Remaining risks are deliberately deferred and non-blocking for this build:

- no live ExecutionHost runtime exists;
- no LocalProcessExecutionHost exists;
- no worker process can be started through this contract;
- no scheduler, leases, or supervisor exist;
- no durable Service integration exists;
- no provider/model/network invocation is authorized;
- no preview/apply/rollback path exists.

These risks are bounded by explicit non-capabilities and by routing the next
task to an independent check before acceptance.
