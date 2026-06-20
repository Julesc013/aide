# Cursor Type Recheck

Recursive fixture inspection found no present `cursor` or `nextCursor` value
that was not a string.

Temporary validator probes also confirmed:

- valid opaque string cursor values pass;
- valid opaque string nextCursor values pass;
- null, numeric, boolean, object, and array cursor values fail;
- null, numeric, boolean, object, and array nextCursor values fail.

Cursor strings remain opaque; no semantic parsing, numeric ordering, encoding
requirement, trimming, or rewrite was introduced.
