# Warning Disposition

Warnings accepted:

- The slice is fixture-backed and local only.
- The local Service state used by the fixture is temporary by default.
- No persistent daemon or `.aide.local` state is accepted.
- The LocalProcessExecutionHost fixture remains the only launch path.
- General worker runtime, preview/apply, repository mutation, and release
  behavior remain outside this acceptance.
