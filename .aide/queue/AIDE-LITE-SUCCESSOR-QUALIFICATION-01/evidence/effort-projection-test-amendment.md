# Preserve the affected extracted-CLI identity oracle

Independent source review found that test_export_import.py:154 expects an exact
source CLI byte copy. Export now deliberately changes one module binding. The
substantive oracle must remain: every other delivered CLI byte is the expected
source text, with exactly one recognized binding projected to the private path.
The rest of that method's actual extracted wait/run/usage/context/refusal and
retirement assertions stay unchanged. This is a contract adaptation, not removing
a failing test or accepting arbitrary delivered code.

Add .aide/scripts/tests/test_export_import.py to the child implementation
allowlist, limited to this identity assertion. Run the complete affected method
test_extracted_export_pack_waits_and_runs_job_without_source_checkout in allocation11,
in addition to the nineteen already proposed methods. Also add the exact
.aide/scripts/tests/test_aide_lite.py path, limited to copying the supplied canonical
normalizer into test_portable_apply_descriptions_match_shipped_modules' minimal
export fixture. Run that entire method with its semantic assertions unchanged
(twenty-one total). Do not change the general minimal-repo factory or import
dummy normalization code. Its existing
native child and local fixture configuration stay inside owned parent scratch;
the outer shared job still enforces the reviewed consumer resource envelope. No
new root, provider grant, resource relaxation, original archive-canary edit or
additional parent allocation. Allocation11 has not launched.

The binding projection must also accept one already-private binding for idempotent
re-export from a delivered CLI. Both accepted inputs always produce the same
private binding. Missing, duplicated or arbitrary bindings still refuse before
reset, and runtime never probes target core. Extend the new drift regression to
cover that legitimate input and arbitrary-path refusal.

This exact additional admission requires independent ACCEPT before editing the
two existing test files. Revised source/effect review follows; the previous proposed
source tree d2c393ae is superseded and must not execute.
