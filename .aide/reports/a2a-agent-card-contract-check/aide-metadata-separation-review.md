# AIDE Metadata Separation Review

The outer AIDE envelope may contain governance metadata. The embedded Agent Card projection does not keep that metadata separate: `canonical_truth`, `endpoint_implemented`, `explicit_non_capabilities`, `schema_version`, and AIDE-only skill fields are inside the projected card. This supports the standards-cleanliness failure.
