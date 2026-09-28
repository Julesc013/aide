# Exact first-stable source review — REQUEST_CHANGES

Independent `/root/stable_builder_review`, on Windows as
`BLACKGLASS-WIN1\Jules`, reviewed commit
`24bd7d0d88c6d3cd9f6924f9b78f35557787c3f1`, tree
`fd3bbf6ff693c0b823ccb188aa4845fc45003ee5`, against base dev
`f3f59303e5d09683a6345be8cbada06496ec4ff9`. Result:
**REQUEST_CHANGES** for dev source integration. External controller
transcription is retained at
`D:\Projects\AIDE\.aide.local\execution\control\reviews\stable-builder-24bd7d0d-review.md`,
SHA-256 `c9b1b5e775895a2cda2101bea361765a19e235d30e936d459f9a3e3e6934dfb1`.

Blocking: regular ZIP/tar members with NTFS ADS names could be extracted while
the subsequent visible-file walk missed the stream. Raw case-sensitive member
deduplication also missed Windows case and trailing-dot aliases. Both require
refusal before extraction with adversarial fixtures. Secondary: tar
`getmembers()` parsed unbounded metadata before the entry/size checks.

The reviewer used read-only Git/status/diff/hash/code/policy/evidence checks,
including `git diff --check`; they did not rerun the recorded 33 tests or edit
the checkout. The frozen candidate is rejected for integration; repair on a
new commit and seek a superseding exact review. No stable assets or external
effects were accepted.
