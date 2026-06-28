# UpdateReceipt Downstream Use

DistributionApplyEngine fixture-only work may use UpdateReceipt v0 to shape receipt outputs for disposable fixture copies only after a separate build/check/accept chain authorizes it.

Allowed:

- cite accepted receipt fields;
- generate receipt-shaped fixture outputs;
- validate preimage/postimage and operation receipt consistency;
- preserve no-apply boundaries in reports.

Not allowed:

- infer real target apply authority;
- infer source repo self-update authority;
- mutate ScreenSave, Eureka, Dominium, or any external repository;
- publish release archives, tags, uploads, or GitHub Releases;
- call provider/model/network services;
- treat source latest output as target truth;
- overwrite project-owned, local-only, never-touch, unknown, or external project state.
