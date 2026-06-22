# Guard Report Review

The guard report was checked for runtime-derived behavior.

- nonce `phaseb-report-a` appeared in report A evidence.
- nonce `phaseb-report-b` appeared in report B evidence.
- report digests recomputed independently.
- report digests changed when the nonce changed.
- a copied report A could not satisfy the report B nonce request.
- report counts reconciled with the probe list.

This closes the non-static guard-report finding.
