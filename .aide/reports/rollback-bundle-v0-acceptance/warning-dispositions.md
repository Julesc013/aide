# Warning Dispositions

Accepted warnings:

- RollbackBundle v0 remained proposed until acceptance.
- Same-session independence is reduced, but no implementation repair was performed.
- Some reverse-operation classes are fixture-covered rather than live-projection-covered because the accepted UpdatePlan has no added managed items.

Disposition:

- The first warning is closed by acceptance.
- The independence warning remains accepted because implementation was unchanged by the check and acceptance.
- The coverage warning remains accepted because live projection coverage reflects the current accepted UpdatePlan, while fixture coverage proves the broader RollbackBundle operation vocabulary.
