# UpdateReceipt v0 No-Apply Boundary

UpdateReceipt v0 records execution receipts only.

It does not:

- authorize execution;
- perform update apply;
- perform install, migration, rollback, repair, or uninstall apply;
- mutate target repositories;
- create release archives, tags, uploads, or GitHub Releases;
- start DistributionApplyEngine, self-consumer fixtures, or canaries;
- call provider, model, or network services.
