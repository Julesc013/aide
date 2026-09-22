# Baseline Defect Evidence

- source branch: `dev`
- source commit: `d37219026462d5670f7a724980faf07e30abb85f`
- source artifact: `.aide/release/dist/aide-lite-pack-v0.zip`
- execution: extracted script invoked with isolated Python outside the checkout
- target: fresh disposable directory outside the checkout
- observed result: failure before planning or writing target files
- exact diagnostic: `invalid pack checksums: missing checksum file: files/.aide.local.example/secrets/README.md`

The archive correctly omitted the forbidden path, but its copied
`checksums.json` still described the pre-filter source pack. Existing Q47 tests
used a non-executable placeholder script and therefore could not detect this
consumer-visible failure.
