# Bounded Windows repair staging hardening

Close the independently reproduced second-writer race in the current dev
`atomic_create_bytes_no_clobber` helper for both repair intent and managed
payload publication. Preserve the accepted pinned-parent/no-clobber design
and fix forward with exact tests, review, combined artifacts, and consumer
qualification. Do not claim full importer or lifecycle safety.
