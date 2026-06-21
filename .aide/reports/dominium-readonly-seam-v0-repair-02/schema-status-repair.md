# Schema And Status Repair

The public seam schema now maps each record container to kind-specific record definitions and kind-specific spec requirements. `FalseStatus` constrains non-capability status facts to `false`, including Workbench, runtime, network, provider/model, worker, mutation, GitHub, branch/worktree, and release/promotion status fields.
