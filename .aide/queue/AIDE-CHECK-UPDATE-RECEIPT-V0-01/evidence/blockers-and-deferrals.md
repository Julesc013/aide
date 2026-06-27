# Blockers And Deferrals

Blockers:

- None.

Deferrals:

- UpdateReceipt acceptance remains a separate queue task.
- DistributionApplyEngine remains not started and requires accepted UpdateReceipt plus explicit queue routing.
- Self-consumer fixture and canaries remain future tasks.

Warnings:

- Positive fixture granularity does not individually exercise every operation receipt class or skipped-operation reason, though schema/helper validation covers the full enum surfaces.
