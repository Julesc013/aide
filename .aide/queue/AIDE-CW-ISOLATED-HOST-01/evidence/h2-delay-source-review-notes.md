# Optional delay metadata source review

The exact two-file manifest h2-delay-source-manifest.json binds source at
830bf30d; the full 101-test receipt covers 13 PE, 7 library, 11 contract, 33 image,
27 security and 10 actual Job tests. All source/dependent bytes stayed unchanged.
The two pre-fix compatibility regressions failed before implementation and remain
retained in h2-delay-before-tests.json and its raw log.

Support is limited to RVA attributes1 and timestamp0. Installed Microsoft SDK
source establishes that timestamp0 is unbound even with an optional bound-IAT
pointer. The reader validates terminated file-backed lookup symbols, finite
IAT/bound/unload spans and terminators, and exact original-IAT/unload bytes.
Only IAT/handle metadata can use a bounded zero-filled mapped tail; descriptors,
lookup names and optional bound/unload tables remain file-backed. Raw optional
function addresses are never followed or executed. Nonzero bound timestamps,
old VA attributes and malformed/ambiguous layouts still refuse. At most16,384
delayed symbol slots are examined per PE, using the existing numeric slot bound;
no image, file, module, API-set or worker capacity was raised. PeInfo API unchanged.
Normal import policy is unchanged, and this remains a dependency-metadata reader
rather than a complete Windows loader validator.

The final exact-source read-only reinspection uses the same eight public Windows
DLL hashes as the earlier refused inventory. All eight now parse. The earlier
first inspection remains immutable; its only subsequent source change was an
explicit pair of parentheses around the ordinal mask, and this final observation
rebinds actual execution to the frozen bytes. No inspected DLL was mapped, loaded,
executed, copied or granted; no native object/API host contract is inferred.

The eight modules' import/delay/all-export-forwarder union contains195 names,
including180 API-set names and15 physical names. The SystemContract's128 API-row
limit therefore cannot admit this complete observed superset. That concrete
next decision is open: separately review an exact bounded admission based on
actual host mappings or a justified symbol-relevant closure refinement. Do not
raise the cap silently, exempt Windows names or claim bootstrap/runtime readiness.
Private Python image grants/launch, actual module origins and protected denials
still require their own exact reviewed effect packet. The task remains PENDING.
