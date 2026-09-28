# Stable archive safety repair, superseding source candidate

The independent review of `24bd7d0d88c6d3cd9f6924f9b78f35557787c3f1`
returned REQUEST_CHANGES. This repair rejects NTFS alternate stream names,
Windows reserved/ambiguous path components, case aliases and nonregular archive
members before extraction. Tar member inspection now streams under finite
compressed, entry and declared uncompressed size bounds. It does not turn the
rejected review into an acceptance; the repaired commit needs a new exact review.

Code SHA-256: `97ffa409e79095c13ed42573c47e1f48b7e26d02527ad9925712d6cf7cc8f8d4`.
Q47 test SHA-256: `21c9d9de87d6450e720c1bed1bd20f3d9d34a95b208829a8182c5663fc9cef50`.

Configured D: managed runner evidence:

- Job `eb4684e14855411fa31edeaf034dae09`: three focused adversarial tests
  passed, including crafted valid-shape ZIP/tar archives carrying ADS, case and
  trailing-dot aliases, and a small tar member bound. Receipt SHA-256
  `c93d0346e517b437762459d488acb8eefe469822b47295a7b9856b8848369f9f`.
- First full Q47/Q48 run `86590f0264c3406f8961c52ee2db1ded` failed:
  new path validator did not accept an existing `WindowsPath` call site. The
  signature was repaired without normalizing raw untrusted member strings.
- Final full Q47/Q48 job `60347f4ee00d41e7af38c371f3da5fb0`: 35 tests
  passed in 62.792 seconds, exit 0. Peak memory 271,638,528 bytes; peak scratch
  8,236,961 bytes. Scratch was retired and the reservation released. Receipt
  SHA-256 `60991d801b649d058b99703566e97eb155aee7886dc8cc19416bf6cb4b5258db`.

Final manifest is retained at
`D:\Projects\AIDE\.aide.local\execution\control\manifests\stable-builder-q47-q48-archive-repair.json`,
SHA-256 `413d7d2f36b569a53edd06c7a70538e285a153bdc997e2e5651d65594b468639`.
The source was the dirty repair atop reviewed commit `24bd7d0d`; this evidence
binds the exact code/test hashes. The next commit freezes the repaired tree for
independent rereview. These tests do not qualify final stable assets, consumers
or publication.
