# Apple Host Families

This subtree holds Apple host-family scaffolds and their compatibility-technology lanes. Product directories remain version-neutral by design, while exact Apple-family coverage is recorded in `inventory/` and `matrices/`.

For Xcode, the current AIDE distinction is between the documented `xcodekit` source-editor lane and a broader `companion` fallback abstraction.

P12 introduces the first Apple boot-slice artifacts. The `companion` lane now carries a runnable thin `cli-bridge` proof, while the `xcodekit` lane carries an explicit blocked structural record for its required native editor proof.
