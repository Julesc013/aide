# Distribution Object Dependency Graph

```text
Q47 release bundle
Q48 release draft
Q43 install evidence
Q44 repair evidence
Q45 upgrade evidence
Q46 rollback/uninstall evidence
        |
        v
DistributionManifest v1
        |
        +--> ProjectLock v0
        |
        +--> OwnershipLedger v1
                 |
                 v
InstallRecord v0
        |
        +--> MigrationRecord v0
        |
        v
UpdatePlan v1
        |
        +--> RollbackBundle v0
        |
        v
fixture-only DistributionApplyEngine v0
        |
        v
UpdateReceipt v0
        |
        v
AIDE self-consumer fixture
        |
        v
ScreenSave canary -> Eureka canary -> Dominium canary
```

Build order:

1. `AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01`
2. `AIDE-BUILD-PROJECT-LOCK-V0-01`
3. `AIDE-BUILD-OWNERSHIP-LEDGER-V1-01`
4. `AIDE-BUILD-INSTALL-RECORD-V0-01`
5. `AIDE-BUILD-MIGRATION-RECORD-V0-01`
6. `AIDE-BUILD-UPDATE-PLAN-V1-01`
7. `AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`
8. `AIDE-BUILD-UPDATE-RECEIPT-V0-01`
9. `AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01`
10. `AIDE-BUILD-AIDE-SELF-CONSUMER-FIXTURE-V0-01`

Every build needs an independent check and acceptance before downstream objects
depend on it.
