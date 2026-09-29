# Bounded source changelog generation

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.
Base `dev`: `6f8dee6f12d4683b91640c24bf342022a00f1d8c`.
Branch: `task/aide-lite-changelog-admission-01` in the existing checkout.

## Change and observed failure

The previous stable build could not run `changelog preview` under the D
managed owner: `.aide/changelog` was an unknown canonical output root. The
default source-checkout CLI could also write those tracked previews outside
job custody. Add that exact canonical root with a finite reservation and
require admitted custody before default source preview generation. Explicit
alternate source-checkout output directories now refuse; extracted Lite and
fixture repositories retain their explicit output-directory behavior.

The new regression failed before the source fix in D job
`9b1982cf7abf4ce9bc12489bb6af3f40` with the expected
`unknown canonical output destination`. Its receipt SHA-256 is
`26fe8ee964d4aa3e7887c7d22b17a497294511be18a7f02c705ce1ea2cee8084`.
After the fix, the same regression passed in D job
`eb686965d52443a6ad36196025d5e07d`, receipt SHA-256
`52acd457ff56e57a3b48c636383018a6745a0e526d061ccf4c1a32c87a42636a`.

The affected managed-workspace suite passed **52/52** in D job
`f100fd0f5ef545c78372ee57067dad5b`, receipt SHA-256
`3135bb5f4e6944d131ad35e7eb4b862e39a43afe18d32d7dd447d1651e01aaed`.
The real source `changelog preview --to 3cc6bf13` passed under the D owner
in job `74978c74a9994d4ba556fe14cb480d7a`, receipt SHA-256
`827ee6b0b350a55a84d646d76e0f8d6481eccbb0613c416a822c010390b5d793`.
It declared the actual D volume and a 32 MiB canonical reservation; 191,602
bytes were observed under `.aide/changelog`. The source head was exactly
`3cc6bf1362aca510aced28ddbab485d4e39317d7`, 50 commits, zero malformed;
Git showed zero changelog file changes. A direct unadmitted source CLI attempt
returned `REFUSED` before writing.

An initial Q34 test pass exposed a separate test-side effect: its
current-repository validation test regenerated six tracked previews for
`HEAD~1..HEAD`. Those six paths were clean before that test. The test now
generates into `AIDE_JOB_TMP`, then validates those isolated outputs. The six
test-generated changes were restored by exact path. The Q34 suite passed
**12/12** after repair in D job `6c07efdc2b24427bb923dbbd41116d22`,
receipt SHA-256 `0e0550434e54d9e3a99f75a64d1c48d50d9afc339e8be7480ad30b018975ba1d`,
with zero tracked changelog drift. All named jobs retired scratch and released
reservations; none initiated a model request.

## Scope and remaining gate

Changed paths: this WorkUnit's task/status/ExecPlan/evidence, the existing
managed owner, Lite CLI, two focused test files, runner guide, and root
planning/implementation records. No archive, stable asset, release effect,
main ref, tag or external target changed. Seek independent exact source review
before `dev`; source acceptance would not requalify the frozen 1.0.0 assets.
