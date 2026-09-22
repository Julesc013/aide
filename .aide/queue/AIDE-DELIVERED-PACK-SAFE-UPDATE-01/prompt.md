# AIDE-DELIVERED-PACK-SAFE-UPDATE-01

Implement the first ownership-aware AIDE Lite delivered-pack update path.

Reuse `import-pack`, pack checksums, target templates, and existing lifecycle
ownership concepts. Record an exact target-local installed baseline. Permit a
later update only when the current managed bytes still equal that baseline, or
when a separately validated predecessor pack proves the baseline. Detect all
conflicts before payload writes, bind apply to the exact preview identity, and
retain per-step recovery evidence if execution stops partway through.

Exercise only disposable consumer repositories and extracted release bytes.
Do not mutate the source checkout, infer ownership from path alone, overwrite
local edits, broaden safe-mode payload, publish, tag, or claim repair/rollback/
uninstall/full stable-release qualification.
