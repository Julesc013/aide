# Remaining Risks

- UpdatePlan v1 is proposed until independent check and acceptance.
- The build uses fixture/source projections only; it does not prove real target repository scanning or mutation.
- RollbackBundle remains a future object and must be accepted before any fixture apply engine work.
- The live projection reports conflicts/manual review for unknown and never-touch ownership, which is intentional fail-closed behavior.
