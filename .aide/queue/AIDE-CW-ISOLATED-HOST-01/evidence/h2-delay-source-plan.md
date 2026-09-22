# Optional delay metadata source slice

Continue on 830bf30d under the accepted same-task source-only scope. Change only
windows_pe.py and its existing direct tests, with owned plan/status/evidence/docs.
No native image, DLL mapping/loading, actual tool copies, grants or profiles.

The actual source-bound Windows observations show RVA attributes1, timestamp0
and a nonzero optional bound-IAT pointer. Installed Microsoft delayimp.h and
its delay helper establish that timestamp0 is unbound and that the optional
bound table is used only when pointer and timestamp are both nonzero. Support
this exact unbound layout; refuse actual nonzero bound timestamps and old VA
attributes. Preserve the initial source/95-test checkpoint and raw refusals.

Preserve existing PE/image bounds and the PeInfo API. Add a distinct validated
mapped virtual extent for writable IAT storage; dependency names and lookup
entries must remain file-backed. Derive finite table spans from the terminated
64-bit lookup table, with at most16,384 total delayed symbol slots per PE, using
the existing export-slot ceiling as the same numeric bound. Do not interpret
bound function addresses. Check optional bound/unload spans and terminators;
where an unload table exists, compare its bytes with the original IAT as the
format requires. Validate optional module-handle storage within the mapped image.
No normal-import policy or system-name exemption is broadened.

Add synthetic optional-table/timestamp0 and virtual-tail IAT successes, plus
nonzero timestamp, absent/truncated lookup/optional tables, missing terminators,
invalid ordinal/name RVAs, table budget and unload mismatch refusals. Preserve
all existing tests. Read-only reinspection of the previously hashed eight public
Windows byte streams may report compatibility; it does not establish native
object/API-set ownership, closure or loader qualification. Freeze source for
independent review before any further effect proposal.
