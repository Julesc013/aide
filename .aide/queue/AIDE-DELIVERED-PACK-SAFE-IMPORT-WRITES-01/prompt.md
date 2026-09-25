# Bounded task: safe importer writes

The stable portable importer must not publish managed files outside its
observed target if a writable parent changes after path validation. Exercise
the actual write boundary in a disposable Windows fixture, preserve existing
receipt and recovery behavior, and repair the write mechanism using reviewed
platform primitives. Do not use a skipped junction test as acceptance.
