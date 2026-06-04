# Hash Strategy

Algorithm: SHA-256.

Rationale: the lifecycle schema layer does not define a lifecycle-specific hash algorithm. SHA-256 matches the existing repository convention used in apply evidence examples and provides deterministic fixture preimage/postimage references.

Recorded hashes:

- install managed-section preimage: `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60`
- install managed-section postimage: `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b`
- upgrade generated preimage: `sha256:711f55672a8cdd9f0cf57adfd99d120c3b9c5e14857530515efe39cb0ef478fb`
- upgrade generated postimage: `sha256:51ceec95b85bbe69ba69ec9b3b868a6f6aa59b47fd513efc118030fc9f6897f1`
- upgrade manual-preserved preimage: `sha256:62b94003123cba1f0717d5d0c5a1a69743a2be5322ea747108c10712ffc2f0a3`
- upgrade manual-preserved postimage: `sha256:5fe72b63591fbefd6873a1069482a6058ab5c23103e85329d8bbca452479b6fa`
- drifted managed-section preimage: `sha256:4023aef20224dc6dc4d495ebacc5c9f98635344b00ea845c616584fd2c257286`
- missing marker preimage: `sha256:cdbda48c7ab0f5eea8690ce5e58a2c006197bb343f6599b82b1a73bb1953fca0`
- malformed marker preimage: `sha256:c27b23ce54154d00ecddacb4bd10fc66fd1a52cf4c129749ecbc52d11a5f56b5`
- uninstall generated preimage: `sha256:14e1072025df1ed6b349c06098a115eb95bcc9e063f43027b7abe1d9912dad06`
- uninstall manual-preserved postimage: `sha256:5d4af5da11363ed70007175dda00aac5160e17cc9ce724e9ae9d9a7ccffab0a7`

No stale placeholder hashes are used in fixture index, expected reports, or rollback-compatible records created by this task.
